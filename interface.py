import streamlit as st
import json
import random

# Set the title of the app
st.title("Video and Multiple Choice Questions")

# Load the videos and questions from a JSON file
with open("videos_and_questions.json", "r") as f:
    videos_and_questions = json.load(f)

# Ask the user how many videos they want to watch
num_videos = st.number_input("How many videos do you want to watch?", min_value=1, max_value=len(videos_and_questions))

# Randomly sample the specified number of videos without replacement
selected_videos_and_questions = random.sample(videos_and_questions, num_videos)

# Initialize an empty list to store all of the user's answers
all_user_answers = []

# Loop through the selected videos and their corresponding questions
for video_and_questions in selected_videos_and_questions:
    # Display the video
    st.video(video_and_questions["video"])

    # Initialize an empty list to store the user's answers for this video
    user_answers = []

    # Loop through the questions and display them with their options
    for question in video_and_questions["questions"]:
        st.write(question["question"])
        answer = st.radio("", question["options"])
        user_answers.append(answer)

    # Add the user's answers for this video to the list of all answers
    all_user_answers.append({
        "video": video_and_questions["video"],
        "answers": user_answers
    })

    # Display the user's answers for this video
    st.write("Your answers for this video:")
    st.write(user_answers)

# Save all of the user's answers to a JSON file
with open("user_answers.json", "w") as f:
    json.dump(all_user_answers, f)

# Add a message at the end
st.write("Thank you for participating! Your answers have been saved.")
