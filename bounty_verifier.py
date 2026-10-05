# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class BountyVerifier(gl.Contract):
    last_submission: str
    last_score: u32
    last_approved: bool
    last_explanation: str

    def __init__(self):
        self.last_submission = ""
        self.last_score = u32(0)
        self.last_approved = False
        self.last_explanation = ""

    @gl.public.write
    def verify_submission(self, submission: str):
        def evaluate():
            prompt = f"""
Evaluate this bounty submission:

{submission}

Return JSON with exactly these fields:
{{
  "score": 0,
  "approved": false,
  "explanation": "short explanation"
}}

Rules:
- score must be an integer from 0 to 100
- approved must be true only when score is at least 70
- the submission must contain meaningful executable implementation
- documentation or dependency declarations alone are not sufficient
"""
            return gl.nondet.exec_prompt(prompt, response_format="json")

        result = gl.eq_principle.prompt_comparative(
            evaluate,
            principle="""
The validators should agree on the meaning of the evaluation.
The score must be between 0 and 100.
Approval is appropriate only for a meaningful implementation.
"""
        )

        self.last_submission = submission
        self.last_score = u32(result["score"])
        self.last_approved = result["approved"]
        self.last_explanation = result["explanation"]

    @gl.public.view
    def get_result(self) -> dict:
        return {
            "submission": self.last_submission,
            "score": self.last_score,
            "approved": self.last_approved,
            "explanation": self.last_explanation,
        }
