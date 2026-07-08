import json
import streamlit as st

from interview_agent import generate_questions, evaluate_answer
from utils import save_transcript, extract_score
from resume_parser import extract_resume_text

st.set_page_config(page_title="AI Interview Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Interview Agent")

# ---------------- Session State ---------------- #

defaults = {
    "name": "",
    "email": "",
    "role": "",
    "experience": "",
    "resume": "",
    "questions": [],
    "current": 0,
    "answers": [],
    "feedback": [],
    "scores": [],
    "submitted": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- Home Page ---------------- #

if len(st.session_state.questions) == 0:

    st.header("Candidate Details")

    name = st.text_input("Candidate Name")

    email = st.text_input("Email")

    role = st.text_input(
        "Job Role",
        placeholder="Java Developer"
    )

    experience = st.selectbox(
        "Experience",
        [
            "0 Years",
            "1 Year",
            "2 Years",
            "3 Years",
            "4 Years",
            "5+ Years"
        ]
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if st.button("🚀 Start Interview", use_container_width=True):

        if not name or not email or not role:
            st.error("Please fill all details.")

        else:

            resume_text = ""

            if uploaded_resume:
                resume_text = extract_resume_text(uploaded_resume)

            st.session_state.resume = resume_text

            st.session_state.name = name
            st.session_state.email = email
            st.session_state.role = role
            st.session_state.experience = experience

            # Generate questions using resume
            try:
                st.session_state.questions = generate_questions(
                    role,
                    experience,
                    resume_text
                )
            except TypeError:
                # Fallback if generate_questions() only accepts role
                st.session_state.questions = generate_questions(role)

            st.session_state.current = 0
            st.session_state.answers = []
            st.session_state.feedback = []
            st.session_state.scores = []
            st.session_state.submitted = False

            st.rerun()

# ---------------- Interview ---------------- #

else:

    index = st.session_state.current
    total_questions = len(st.session_state.questions)

    if index < total_questions:

        progress = (index + 1) / total_questions

        st.subheader(f"Question {index + 1} of {total_questions}")
        st.progress(progress)

        question = st.session_state.questions[index]

        st.write("### Interview Question")
        st.write(question)

        if not st.session_state.submitted:

            answer = st.text_area(
                "Your Answer",
                height=220,
                key=f"answer_{index}"
            )

            if st.button("Submit Answer", use_container_width=True):

                if answer.strip() == "":
                    st.warning("Please enter your answer.")

                else:

                    result = evaluate_answer(
                        st.session_state.role,
                        question,
                        answer
                    )

                    score = extract_score(result)

                    st.session_state.answers.append(answer)
                    st.session_state.feedback.append(result)
                    st.session_state.scores.append(score)

                    st.session_state.submitted = True
                    st.rerun()

        else:

            st.subheader("Your Answer")
            st.write(st.session_state.answers[index])

            st.subheader("AI Evaluation")
            st.info(st.session_state.feedback[index])

            st.metric(
                "Score",
                f"{st.session_state.scores[index]}/10"
            )

            if st.button("Next Question ➡️", use_container_width=True):

                st.session_state.current += 1
                st.session_state.submitted = False
                st.rerun()

    # ---------------- Final Dashboard ---------------- #

    else:

        st.balloons()

        st.success("🎉 Interview Completed!")

        total = sum(st.session_state.scores)
        average = round(total / len(st.session_state.scores), 2)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Overall Score", f"{total}/{len(st.session_state.scores) * 10}")

        with col2:
            st.metric("Average Score", f"{average}/10")

        # Recommendation

        if average >= 8:
            recommendation = "Strong Hire"
            st.success("✅ Recommendation: Strong Hire")

        elif average >= 6:
            recommendation = "Hire"
            st.success("👍 Recommendation: Hire")

        elif average >= 4:
            recommendation = "Borderline"
            st.warning("🤔 Recommendation: Borderline")

        else:
            recommendation = "Not Recommended"
            st.error("❌ Recommendation: Not Recommended")

        # Strengths & Weaknesses

        strengths = []
        weaknesses = []

        for i, score in enumerate(st.session_state.scores):

            if score >= 8:
                strengths.append(
                    f"Q{i+1}: Strong answer ({score}/10)"
                )

            elif score <= 5:
                weaknesses.append(
                    f"Q{i+1}: Needs improvement ({score}/10)"
                )

        st.write("---")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("💪 Strengths")

            if strengths:
                for item in strengths:
                    st.success(item)
            else:
                st.write("No major strengths identified.")

        with col2:

            st.subheader("📉 Weaknesses")

            if weaknesses:
                for item in weaknesses:
                    st.error(item)
            else:
                st.write("No major weaknesses identified.")

        st.write("---")
        st.header("Interview Report")

        for i in range(total_questions):

            with st.expander(f"Question {i+1}"):

                st.write("### Question")
                st.write(st.session_state.questions[i])

                st.write("### Your Answer")
                st.write(st.session_state.answers[i])

                st.write("### AI Evaluation")
                st.info(st.session_state.feedback[i])

                st.metric(
                    "Score",
                    f"{st.session_state.scores[i]}/10"
                )

        # ---------------- Save Evaluation ---------------- #

        evaluation = {

            "candidate_name": st.session_state.name,
            "email": st.session_state.email,
            "role": st.session_state.role,
            "experience": st.session_state.experience,
            "resume": st.session_state.resume,

            "scores": st.session_state.scores,

            "overall_score": total,
            "average_score": average,

            "recommendation": recommendation,

            "strengths": strengths,
            "weaknesses": weaknesses

        }

        with open("evaluation.json", "w") as f:
            json.dump(evaluation, f, indent=4)

        # ---------------- Save Transcript ---------------- #

        save_transcript({

            "candidate_name": st.session_state.name,
            "email": st.session_state.email,
            "role": st.session_state.role,
            "experience": st.session_state.experience,
            "resume": st.session_state.resume,

            "questions": st.session_state.questions,
            "answers": st.session_state.answers,
            "evaluation": st.session_state.feedback,
            "scores": st.session_state.scores

        })

        st.success("✅ Transcript saved as transcript.json")
        st.success("✅ Evaluation saved as evaluation.json")