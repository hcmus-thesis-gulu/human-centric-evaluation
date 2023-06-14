import streamlit as st
import json
import random
from uuid import uuid4

common_json = "human-centric/common-questions.json"
comparison_json = "human-centric/comparison-questions.json"
questions_json = "human-centric/questions.json"
survey_info_json = "human-centric/survey-information.json"
original_path = "videos/original/{name}.webm"
user_path = "videos/user-summaries/{name}_{user_idx}.avi"
our_path = "videos/user-summaries/{name}_1.avi"
answers_path = "human-centric/answers/{uuid}.json"

universal_index = 0

def short_answer_question(question):
    global universal_index
    answer = st.text_input(question, key=universal_index)
    universal_index += 1
    return answer

def paragraph_question(question):
    global universal_index
    answer = st.text_area(question, key=universal_index)
    universal_index += 1
    return answer

def multiple_choice_question(question, options):
    global universal_index
    answer = st.radio(question, options, key=universal_index)
    universal_index += 1
    return answer

def checkbox_question(question, options):
    global universal_index
    st.write(question)
    answers = []
    for option in options:
        answers.append(st.checkbox(option, key=universal_index))
        universal_index += 1
    return answers

def linear_scale_question(question, lower_bound=0, upper_bound=10):
    global universal_index
    answer = st.slider(question, lower_bound, upper_bound, key=universal_index)
    universal_index += 1
    return answer

def ask_question(question):
    question_type = question['type']
    match question_type:
        case 'short':
            return short_answer_question(question['question'])
        case 'multiple':
            return multiple_choice_question(question['question'], question['options'])
        case 'checkbox':
            return checkbox_question(question['question'], question['options'])
        case 'linear':
            return linear_scale_question(question['question'])

def ask_question(question):
    match question["type"]:
        case "short":
            return short_answer_question(question["question"])
        case "multiple":
            return multiple_choice_question(question["question"], question["options"])
        case "checkbox":
            return checkbox_question(question["question"], question["options"])
        case "linear":
            return linear_scale_question(question["question"])

def broadcast_video(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    st.video(video_bytes)

def present_comparison(video_infor, comparison_questions):
    st.subheader("Original Video")
    print(video_infor)
    broadcast_video(original_path.format(name=video_infor['name']))
    st.subheader("Summary Video")    
    user_idx = random.randint(0, 15)
    if user_idx:
        broadcast_video(user_path.format(name=video_infor['name'], user_idx=user_idx))
    else:
        broadcast_video(our_path.format(name=video_infor['name']))
        
    answers = []
    for question in comparison_questions:
        answers.append(ask_question(question))
    return answers
    
def present_normal(video_infor, common_questions):
    user_idx = random.randint(-1, 15)
    match user_idx:
        case -1:
            broadcast_video(original_path.format(name=video_infor['name']))
        case 0:
            broadcast_video(our_path.format(name=video_infor['name']))
        case _:
            broadcast_video(user_path.format(name=video_infor['name'], user_idx=user_idx))
            
    answers = []
    for question in common_questions:
        answers.append(ask_question(question))
    for question in video_infor['questions']:
        answers.append(ask_question(question))
        
    return answers


def main():
# original_path = "videos/original/{name}.webm"
# user_path = "videos/user-summaries/{name}_{user_idx}.avi"
# our_path = "videos/user-summaries/{name}_1.avi"
# answers_folder = "human-centric/answers"

    with open(common_json, "r") as f:
        common_questions = json.load(f)
    with open(comparison_json, "r") as f:
        comparison_questions = json.load(f)
    with open(questions_json, "r") as f:
        video_infos = json.load(f)
    with open(survey_info_json, "r") as f:
        survey_infor = json.load(f)
    survey_uuid = uuid4().hex
    survey_answers = []
        
    st.title(survey_infor["title"])
    st.write(survey_infor["description"])
    st.divider()
    number_of_videos = linear_scale_question(survey_infor["number_of_videos"], 0, 25)
    
    if st.button("Start the Survey"):
        videos_to_ask = random.sample(video_infos, number_of_videos)
        for idx, video_infor in enumerate(videos_to_ask, start=1):
            st.header("Video #{idx}".format(idx=idx))
            compare_or_normal = 0
            # random.randint(0, 1)
            if compare_or_normal:
                answers = present_comparison(video_infor, comparison_questions)
            else:
                answers = present_normal(video_infor, common_questions)
            survey_answers.append(answers)

    if st.button("Submit Answers"):
        print(survey_answers)
        with open(answers_path.format(survey_uuid), "w") as f:
            json.dump(survey_answers, f)
    
if __name__ == "__main__":
    main()
