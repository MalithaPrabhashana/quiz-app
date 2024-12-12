import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # Replace with your FastAPI server URL if different


def teacher_view():
    st.title("Teacher's Panel")

    # Get input for question text and type
    question_text = st.text_input("Enter the Question Text:")
    question_type = st.selectbox(
        "Select Question Type",
        ["Single Answer", "True False", "Multiple Choice"]
    )

    # Initialize variables for options and correct answer
    options = []
    correct_answer = None

    # Handle inputs based on question type
    if question_type == "Multiple Choice":
        option_1 = st.text_input("Option 1:")
        option_2 = st.text_input("Option 2:")
        option_3 = st.text_input("Option 3:")
        option_4 = st.text_input("Option 4:")

        options = [option_1, option_2, option_3, option_4]
        correct_answer = st.selectbox(
            "Select Correct Answer", [1, 2, 3, 4]
        )  # Correct answer is 1-based index

    elif question_type == "True False":
        options = ["True", "False"]
        correct_answer = st.selectbox(
            "Select Correct Answer", ["True", "False"]
        )  # Correct answer is the actual string

    else:  # Write Answer (single_answer)
        correct_answer = st.text_input("Enter the Correct Answer:")

    # Add question button
    if st.button("Add Question"):
        # Format the request data
        question_data = {
            "question_type": question_type.lower().replace(" ", "_"),  # Convert to snake_case
            "question_data": {
                "text": question_text,
                "options": options if question_type == "Multiple Choice" else [],
                "correct_answer": correct_answer if question_type != "Multiple Choice" else int(correct_answer),
            },
        }

        # Send the POST request to the backend
        response = requests.post(f"{BASE_URL}/teacher/add-question", json=question_data)

        # Handle the response
        if response.status_code == 200:
            st.success("Question added successfully!")
        else:
            st.error("Failed to add question. Try again.")
            

def student_view():
    st.title("Student's Panel")

    if "total_score" not in st.session_state:
        st.session_state.total_score = 0
        st.session_state.answered_questions = set()

    st.markdown(f"""
        <style>
        .total-score {{
            position: fixed;
            top: 70px;
            right: 10px;
            font-size: 24px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 10px;
            border-radius: 5px;
        }}
        </style>
        <div class="total-score">
            Total Score: {st.session_state.total_score}
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Available Questions")
    response = requests.get(f"{BASE_URL}/student/all-questions")

    if response.status_code == 200:
        questions = response.json()

        for question in questions["questions"]:
            if question["id"] in st.session_state.answered_questions:
                continue

            st.write(f"Q{question['id']}: {question['question']}")

            if question["options"]:
                selected_option = st.radio(
                    f"Options for Q{question['id']}", question["options"], key=f"q_{question['id']}"
                )

                if st.button(f"Submit Answer for Q{question['id']}", key=f"submit_{question['id']}"):
                    selected_answer_id = question["options"].index(selected_option) + 1

                    if selected_answer_id == question.get("correct_answer_id", 1):
                        st.session_state.total_score += 1
                        st.success(f"Correct answer for Q{question['id']}!")
                    else:
                        st.error(f"Incorrect answer for Q{question['id']}.")

                    st.session_state.answered_questions.add(question["id"])
            else:
                student_answer = st.text_input(
                    f"Your Answer for Q{question['id']}:", key=f"answer_{question['id']}"
                )
                if st.button(f"Submit Answer for Q{question['id']}", key=f"submit_{question['id']}"):
                    correct_answer = question.get("correct_answer", "").strip().lower()

                    if student_answer.strip().lower() == correct_answer:
                        st.session_state.total_score += 1
                        st.success(f"Correct answer for Q{question['id']}!")
                    else:
                        st.error(f"Incorrect answer for Q{question['id']}.")

                    st.session_state.answered_questions.add(question["id"])
    else:
        st.error("Failed to load questions. Try again.") 

# Main app
st.sidebar.title("Quiz App")
user_type = st.sidebar.radio("Who are you?", ["Teacher", "Student"])

if user_type == "Teacher":
    teacher_view()
else:
    student_view()
