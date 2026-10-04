# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import genlayer as gl


class BountyVerifier(gl.Contract):    """
    Consensus-based bounty submission verifier.

    The contract:
    1. Stores bounty requirements.
    2. Accepts a submission URL.
    3. Retrieves the submitted content from the web.
    4. Uses GenLayer validators to evaluate the submission.
    5. Uses the Equivalence Principle to reach consensus.
    6. Stores an approval decision, score, and explanation.
    """

    bounty_requirements: str
    last_submission_url: str
    last_approved: bool
    last_score: int
    last_reason: str

    def __init__(self, bounty_requirements: str) -> None:
        self.bounty_requirements = bounty_requirements
        self.last_submission_url = ""
        self.last_approved = False
        self.last_score = 0
        self.last_reason = ""

    @gl.public.view
    def get_requirements(self) -> str:
        """Return the bounty requirements."""
        return self.bounty_requirements

    @gl.public.view
    def get_last_result(self) -> str:
        """Return the latest verification result as JSON."""
        return json.dumps(
            {
                "approved": self.last_approved,
                "score": self.last_score,
                "reason": self.last_reason,
                "submission_url": self.last_submission_url,
            }
        )

    @gl.public.write
    def verify_submission(self, submission_url: str) -> None:
        """
        Verify a bounty submission using web content and
        consensus-based AI evaluation.
        """

        if not submission_url.startswith(("http://", "https://")):
            raise ValueError("submission_url must start with http:// or https://")

        def evaluate_submission() -> str:
            response = gl.nondet.web.get(submission_url)

            content = response.body.decode("utf-8")

            # Keep the prompt bounded so extremely large pages
            # do not consume unnecessary execution resources.
            content = content[:12000]

            prompt = f"""
You are a decentralized bounty submission evaluator.

Your task is to determine whether a submitted project satisfies
the bounty requirements.

BOUNTY REQUIREMENTS:
{self.bounty_requirements}

SUBMISSION URL:
{submission_url}

SUBMISSION CONTENT:
{content}

Evaluate only the evidence contained in the submission content.

Return ONLY valid JSON in exactly this structure:

{{
  "approved": true,
  "score": 85,
  "reason": "Short explanation of the decision."
}}

Rules:

1. "approved" must be either true or false.
2. "score" must be an integer from 0 to 100.
3. The score must reflect how strongly the submission satisfies
   the stated bounty requirements.
4. Do not invent evidence that is not present in the submission.
5. If important requirements are missing or cannot be verified,
   lower the score and set approved to false when appropriate.
6. Keep "reason" concise and factual.
7. Return JSON only. Do not use Markdown.
"""

            result = gl.nondet.exec_prompt(prompt)

            # Remove accidental Markdown code fences.
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

            # Validate that the validator returned valid JSON.
            parsed = json.loads(result)

            if not isinstance(parsed.get("approved"), bool):
                raise ValueError("approved must be a boolean")

            if not isinstance(parsed.get("score"), int):
                raise ValueError("score must be an integer")

            if parsed["score"] < 0 or parsed["score"] > 100:
                raise ValueError("score must be between 0 and 100")

            if not isinstance(parsed.get("reason"), str):
                raise ValueError("reason must be a string")

            return json.dumps(
                {
                    "approved": parsed["approved"],
                    "score": parsed["score"],
                    "reason": parsed["reason"],
                }
            )

        consensus_result = gl.eq_principle.prompt_comparative(
            evaluate_submission,
            "The approved decision and score should be consistent between validators. "
            "The validators should agree on whether the submission satisfies the "
            "bounty requirements based only on the provided evidence."
        )

        final_result = json.loads(consensus_result)

        self.last_submission_url = submission_url
        self.last_approved = final_result["approved"]
        self.last_score = final_result["score"]
        self.last_reason = final_result["reason"]
