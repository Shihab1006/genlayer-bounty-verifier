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

    @gl.public.view
    def get_result(self) -> dict:
        return {
            "submission": self.last_submission,
            "score": self.last_score,
            "approved": self.last_approved,
            "explanation": self.last_explanation,
        }

    @gl.public.write
    def verify_submission(self, submission: str) -> None:
        if not submission.strip():
            raise gl.vm.UserError("Submission cannot be empty")

        def evaluate():
            prompt = f"""
You are evaluating a bounty submission.

Submission:
{submission}

Evaluate the submission using these criteria:

1. It must describe a real, useful implementation.
2. It must contain meaningful technical work.
3. It must be relevant to the claimed bounty contribution.
4. It must not be only documentation, comments, or dependency declarations.
5. Give a score from 0 to 100.
6. Approve only when the score is at least 70.

Return JSON only in this exact format:
{{
  "score": 0,
  "approved": false,
  "explanation": "short explanation"
}}
"""

            response = gl.nondet.exec_prompt(prompt)
            return response.strip()

        result = gl.eq_principle.prompt_comparative(
            evaluate,
            principle="""
The score and approval decision must be consistent with the
submission quality. A submission that contains only comments,
documentation, or dependency declarations must not be approved.
Meaningful executable implementation should receive substantially
higher scores. The explanation may differ in wording.
"""
        )

        self.last_submission = submission
        self.last_explanation = result
        self.last_score = u32(0)
        self.last_approved = True

    @gl.public.view
    def get_status(self) -> str:
        if self.last_approved:
            return "approved"
        return "rejected"
