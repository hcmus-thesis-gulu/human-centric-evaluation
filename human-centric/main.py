import streamlit as st

def short_answer_question():
    answer = st.text_input("Short answer question")
    return answer

def paragraph_question():
    answer = st.text_area("Paragraph question")
    return answer

def multiple_choice_question():
    options = ["Option 1", "Option 2", "Option 3"]
    answer = st.radio("Multiple choice question", options)
    return answer

def checkbox_question():
    options = ["Option 1", "Option 2", "Option 3"]
    answer = st.checkbox("Checkbox question 1", key="cb1")
    answer2 = st.checkbox("Checkbox question 2", key="cb2")
    answer3 = st.checkbox("Checkbox question 3", key="cb3")
    return [answer, answer2, answer3]

def linear_scale_question():
    answer = st.slider("Linear scale question", 0, 10)
    return answer

def multiple_choice_grid_question():
    options = ["Option 1", "Option 2", "Option 3"]
    answer = ""
    for row in range(3):
        answer += st.radio(f"Row {row+1}", options)
    return answer

def checkbox_grid_question():
    options = ["Option 1", "Option 2", "Option 3"]
    answer = ""
    for row in range(3):
        answer += str(st.checkbox(options[row]))
    return answer

def main():
    st.title("Survey")

    st.header("Short Answer")
    short_answer = short_answer_question()

    st.header("Paragraph")
    paragraph = paragraph_question()

    st.header("Multiple Choice")
    multiple_choice = multiple_choice_question()

    st.header("Checkbox")
    checkbox = checkbox_question()

    st.header("Linear Scale")
    linear_scale = linear_scale_question()

    st.header("Multiple Choice Grid")
    multiple_choice_grid = multiple_choice_grid_question()

    st.header("Checkbox Grid")
    checkbox_grid = checkbox_grid_question()

    # Submit button
    if st.button("Submit"):
        # Do something with the survey responses
        st.write("Short Answer:", short_answer)
        st.write("Paragraph:", paragraph)
        st.write("Multiple Choice:", multiple_choice)
        st.write("Checkbox:", checkbox)
        st.write("Linear Scale:", linear_scale)
        st.write("Multiple Choice Grid:", multiple_choice_grid)
        st.write("Checkbox Grid:", checkbox_grid)

if __name__ == "__main__":
    main()
