import json
import os
import cv2
from pywebio import input, output, start_server
import pywebio_battery
import json
import random
from uuid import uuid4

common_json = "human-centric/common-questions.json"
comparison_json = "human-centric/comparison-questions.json"
questions_json = "human-centric/questions.json"
survey_info_json = "human-centric/survey-information.json"
original_path = "videos/original/{name}.webm"
user_path = "videos/user-summaries/{name}_{user_idx}.webm"
our_path = "videos/user-summaries/{name}_1.webm"
answers_path = "human-centric/answers/{uuid}.json"

def short_answer_question(question):
    answer = input.input(question)
    return answer

def paragraph_question(question):
    answer = input.textarea(question)
    return answer

def multiple_choice_question(question, options):
    answer = input.radio(question, options)
    return answer

def checkbox_question(question, options):
    answers = input.checkbox(question, options)
    return answers

def linear_scale_question(question, lower_bound=0, upper_bound=10):
    answer = input.slider(question, value=lower_bound, min_value=lower_bound, max_value=upper_bound)
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
        
def broadcast_video(video_path):
    frame_width = "640"
    frame_height = "360"
    
    video_path = os.path.join("static", video_path)
    pywebio_battery.put_video(video_path, width=frame_width, height=frame_height)

def present_comparison(video_infor, comparison_questions):
    output.put_markdown("### Original Video")
    broadcast_video(original_path.format(name=video_infor['name']))
    output.put_markdown("### Summary Video")    
    user_idx = random.randint(0, 15)
    if user_idx:
        broadcast_video(user_path.format(name=video_infor['name'], user_idx=user_idx))
    else:
        broadcast_video(our_path.format(name=video_infor['name']))
        
    results = []
    for question in comparison_questions:
        answer = ask_question(question)
        result_obj = {
            "question": question,
            "user_index": user_idx,
            "answer": answer
        }
        results.append(result_obj)
    return results
    
def present_normal(video_infor, common_questions):
    user_idx = random.randint(-1, 15)
    match user_idx:
        case -1:
            broadcast_video(original_path.format(name=video_infor['name']))
        case 0:
            broadcast_video(our_path.format(name=video_infor['name']))
        case _:
            broadcast_video(user_path.format(name=video_infor['name'], user_idx=user_idx))
            
    results = []
    for question in common_questions:
        answer = ask_question(question)
        result_obj = {
            "question": question,
            "answer": answer
        }
        results.append(result_obj)
    for question in video_infor['questions']:
        answer = ask_question(question)
        result_obj = {
            "question": question,
            "answer": answer
        }
        results.append(result_obj)
        
    return results

def survey():
    with open(common_json, "r") as f:
        common_questions = json.load(f)
    with open(comparison_json, "r") as f:
        comparison_questions = json.load(f)
    with open(questions_json, "r") as f:
        video_infos = json.load(f)
    with open(survey_info_json, "r") as f:
        survey_infor = json.load(f)
    survey_uuid = uuid4().hex
    survey_results = []
    
    output.put_markdown("# {title}".format(title=survey_infor["title"]))
    output.put_text(survey_infor["description"])
    number_of_videos = linear_scale_question(survey_infor["number_of_videos"], 0, 25)
    
    if number_of_videos:
        videos_to_ask = random.sample(video_infos, number_of_videos)
        for idx, video_infor in enumerate(videos_to_ask, start=1):
            output.put_markdown("## Video #{idx}".format(idx=idx))
            compare_or_normal = random.randint(0, 1)
            if compare_or_normal:
                results = present_comparison(video_infor, comparison_questions)
            else:
                results = present_normal(video_infor, common_questions)
                
            result_obj = {
                "name": video_infor["name"],
                "survey_results": results
            }
            survey_results.append(result_obj)

    result_path = answers_path.format(uuid=survey_uuid)
    with open(result_path, "w") as f:
        json.dump(survey_results, f, indent=4)
        
        
if __name__ == '__main__':
    start_server(survey, static_dir="./", port=8080)