# GenLayer Bounty Verifier

A GenLayer Intelligent Contract that uses consensus-based AI evaluation to verify bounty submissions against defined requirements.

## Overview

Bounty programs often require manual verification to determine whether a submitted project satisfies predefined requirements.

GenLayer Bounty Verifier provides a reusable Intelligent Contract that evaluates a submission against natural-language requirements and produces a structured verification result.

## How It Works

1. Define the bounty requirements.
2. Submit the project or work for verification.
3. The Intelligent Contract evaluates the submission.
4. GenLayer consensus is used to evaluate the decision.
5. The contract returns an approval status, score, and explanation.

## Verification Result

The verifier returns:

- `approved` — whether the submission satisfies the requirements
- `score` — a score from 0 to 100
- `reason` — a short explanation of the decision

Example:

```json
{
  "approved": true,
  "score": 85,
  "reason": "The submission satisfies the stated requirements."
}


## Deployed Contract

The Intelligent Contract was deployed and tested successfully using GenLayer Studio.

Contract address:

0x0Cb95111845e73c477B83e89F0FAa11960819880
