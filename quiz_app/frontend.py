import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # Replace with your FastAPI server URL if different


def teacher_view():
    st.title("Teacher's Panel")

    question_text = st.text_input("Enter the Question Text:")
    question_type = st.selectbox(
        "Select Question Type",
        ["Write Answer", "True/False", "Multiple Choice"]
    )

    if question_type == "Multiple Choice":
        option_1 = st.text_input("Option 1:")
        option_2 = st.text_input("Option 2:")
        option_3 = st.text_input("Option 3:")
        option_4 = st.text_input("Option 4:")
        correct_answer = st.selectbox(
            "Select Correct Answer", [option_1, option_2, option_3, option_4]
        )
        options = [option_1, option_2, option_3, option_4]
    elif question_type == "True/False":
        options = ["True", "False"]
        correct_answer = st.selectbox("Select Correct Answer", options)
    else:  # Write Answer
        options = None
        correct_answer = st.text_input("Enter the Correct Answer:")

    if st.button("Add Question"):
        question_data = {
            "text": question_text,
            "options": options,
            "correct_answer": correct_answer,
        }
        response = requests.post(f"{BASE_URL}/teacher/add-question", json=question_data)

        if response.status_code == 200:
            st.success("Question added successfully!")
        else:
            st.error("Failed to add question. Try again.")


def student_view():
    st.title("Student's Panel")

    st.subheader("Available Questions")
    response = requests.get(f"{BASE_URL}/student/get-questions")

    if response.status_code == 200:
        questions = response.json()
        for question in questions:
            st.write(f"Q{question['id']}: {question['text']}")
            
            if question["options"]:
                if question["options"] == ["True", "False"]:  # True/False
                    selected_option = st.radio(
                        f"Options for Q{question['id']}", question["options"], key=question['id']
                    )
                else:  # Multiple Choice
                    selected_option = st.radio(
                        f"Options for Q{question['id']}", question["options"], key=question['id']
                    )
                if st.button(f"Submit Answer for Q{question['id']}", key=f"submit_{question['id']}"):
                    answer_data = {
                        "question_id": question["id"],
                        "answer": selected_option,
                    }
                    answer_response = requests.post(f"{BASE_URL}/student/submit-answer", json=answer_data)
                    if answer_response.status_code == 200:
                        st.success(f"Answer submitted for Q{question['id']}!")
                    else:
                        st.error(f"Failed to submit answer for Q{question['id']}.")
            else:  # Write Answer
                student_answer = st.text_input(
                    f"Your Answer for Q{question['id']}:", key=f"answer_{question['id']}"
                )
                if st.button(f"Submit Answer for Q{question['id']}", key=f"submit_{question['id']}"):
                    answer_data = {
                        "question_id": question["id"],
                        "answer": student_answer,
                    }
                    answer_response = requests.post(f"{BASE_URL}/student/submit-answer", json=answer_data)
                    if answer_response.status_code == 200:
                        st.success(f"Answer submitted for Q{question['id']}!")
                    else:
                        st.error(f"Failed to submit answer for Q{question['id']}.")
    else:
        st.error("Failed to load questions. Try again.")


# Main app
st.sidebar.title("Quiz App")
user_type = st.sidebar.radio("Who are you?", ["Teacher", "Student"])

if user_type == "Teacher":
    teacher_view()
else:
    student_view()
