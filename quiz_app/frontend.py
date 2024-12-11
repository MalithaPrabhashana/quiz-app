import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # Replace with your FastAPI server URL if different


def teacher_view():
    st.title("Teacher's Panel")

    # Get input for question
    question_text = st.text_input("Enter the Question Text:")
    question_type = st.selectbox(
        "Select Question Type",
        ["Write Answer", "True/False", "Multiple Choice"]
    )

    # Initialize variables for options and correct answer
    options = []
    correct_answer = None

    # Based on the selected question type, gather the question data
    if question_type == "Multiple Choice":
        option_1 = st.text_input("Option 1:")
        option_2 = st.text_input("Option 2:")
        option_3 = st.text_input("Option 3:")
        option_4 = st.text_input("Option 4:")
        
        options = [option_1, option_2, option_3, option_4]
        
        # Select the correct answer based on the option number (1-4)
        correct_answer = st.selectbox(
            "Select Correct Answer", [1, 2, 3, 4]
        )

    elif question_type == "True/False":
        options = ["True", "False"]
        correct_answer = st.selectbox("Select Correct Answer", [1, 2])  # 1 for True, 2 for False

    else:  # Write Answer
        options = None
        correct_answer = st.text_input("Enter the Correct Answer:")

    # Check if all required inputs are filled
    if st.button("Add Question"):
        # Format the question data as required by the backend
        question_data = {
            "question_type": question_type.lower().replace(" ", "_"),  # Convert to snake_case
            "question_data": {
                "text": question_text,
                "options": options,
                "correct_answer": correct_answer,  # Pass correct_answer as an integer
            },
        }

        # Send the POST request to add the question
        response = requests.post(f"{BASE_URL}/teacher/add-question", json=question_data)

        # Handle response
        if response.status_code == 200:
            st.success("Question added successfully!")
        else:
            st.error("Failed to add question. Try again.")


def student_view():
    st.title("Student's Panel")

    st.subheader("Available Questions")
    response = requests.get(f"{BASE_URL}/student/all-questions")

    if response.status_code == 200:
        questions = response.json()
        for question in questions["questions"]:
            st.write(f"Q{question['id']}: {question['question']}")

            if question["options"]:
                if question["options"] == ["True", "False"]:  # True/False
                    selected_option = st.radio(
                        f"Options for Q{question['id']}", question["options"], key=f"q_{question['id']}"
                    )
                else:  # Multiple Choice
                    selected_option = st.radio(
                        f"Options for Q{question['id']}", question["options"], key=f"q_{question['id']}"
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
            else:  # No options, hence free-text answer
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
