QUESTION_PROMPT = """
You are an experienced technical interviewer.

Candidate Details

Job Role:
{role}

Experience:
{experience}

Resume:
{resume}

Generate exactly 5 UNIQUE interview questions.

Rules:
- Base questions on the candidate's resume if available.
- If no resume is uploaded, generate questions based on the job role.
- Mix beginner, intermediate, and advanced questions.
- Include one scenario-based question.
- Include one problem-solving question.
- Return ONLY a numbered list.
"""

EVALUATION_PROMPT = """
You are an experienced technical interviewer.

Job Role:
{role}

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return exactly in this format:

Score: X/10

Feedback:
(Explain why you gave this score.)

Strengths:
- Point 1
- Point 2

Weaknesses:
- Point 1
- Point 2

Suggested Answer:
(Provide a better answer.)
"""