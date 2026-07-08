import os
from groq import Groq
from dotenv import load_dotenv
from prompts import QUESTION_PROMPT, EVALUATION_PROMPT

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# Common AI Function
# -----------------------------
def ask_ai(prompt):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.9,
        max_tokens=1200
    )

    return response.choices[0].message.content


# -----------------------------
# Generate Interview Questions
# -----------------------------
def generate_questions(role, experience, resume_text=""):

    if not resume_text.strip():
        resume_text = "No Resume Uploaded."

    prompt = QUESTION_PROMPT.format(
        role=role,
        experience=experience,
        resume=resume_text
    )

    response = ask_ai(prompt)

    questions = []

    for line in response.split("\n"):

        line = line.strip()

        if line and line[0].isdigit():

            question = line.split(".", 1)[1].strip()

            questions.append(question)

    return questions


# -----------------------------
# Evaluate Candidate Answer
# -----------------------------
def evaluate_answer(role, question, answer):

    prompt = EVALUATION_PROMPT.format(
        role=role,
        question=question,
        answer=answer
    )

    return ask_ai(prompt)