# import os
# import cv2

# src = 'videos/user-summaries'
# dst = 'videos/user-summaries'

# def convert_to_mp4(input_file, output_file):
#     video = cv2.VideoCapture(input_file)
#     if (video.isOpened() == False): 
#         print("Error reading video file")

#     frame_width = int(video.get(3))
#     frame_height = int(video.get(4))
   
#     size = (frame_width, frame_height)
#     fps = video.get(cv2.CAP_PROP_FPS)
   
#     result = cv2.VideoWriter(output_file, 
#                          cv2.VideoWriter_fourcc(*'MP4V'),
#                          fps, size)
    
#     while(True):
#         ret, frame = video.read()
    
#         if ret == True: 
#             result.write(frame)
    
#         else:
#             break
  
#     video.release()
#     result.release()
    
#     cv2.destroyAllWindows()
   
#     print("The video was successfully saved")

# for filename in os.listdir(src):
#     filename = filename.split(".")[0] + ".{ext}"
#     input = os.path.join(src, filename.format(ext='avi'))
#     output = os.path.join(dst, filename.format(ext='mp4'))
#     convert_to_mp4(input, output)
#     print(output)

import json
from pywebio import input
from pywebio import output
import pywebio_battery
import json
import random
from uuid import uuid4

common_json = "human-centric/common-questions.json"
comparison_json = "human-centric/comparison-questions.json"
questions_json = "human-centric/questions.json"
survey_info_json = "human-centric/survey-information.json"
original_path = "videos/original/{name}.mp4"
user_path = "videos/user-summaries/{name}_{user_idx}.mp4"
our_path = "videos/user-summaries/{name}_1.mp4"
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
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    pywebio_battery.put_video(video_path)
    print(video_path)
    
    # url = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    # pywebio_battery.put_video(url)

def present_comparison(video_infor, comparison_questions):
    output.put_markdown("### Original Video")
    print(video_infor)
    broadcast_video(original_path.format(name=video_infor['name']))
    output.put_markdown("### Summary Video")    
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

def survey():
# # original_path = "videos/original/{name}.webm"
# # user_path = "videos/user-summaries/{name}_{user_idx}.avi"
# # our_path = "videos/user-summaries/{name}_1.avi"
# # answers_folder = "human-centric/answers"

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
    
    output.put_markdown("# {title}".format(title=survey_infor["title"]))
    output.put_text(survey_infor["description"])
    number_of_videos = linear_scale_question(survey_infor["number_of_videos"], 0, 25)
    
    if number_of_videos:
        videos_to_ask = random.sample(video_infos, number_of_videos)
        for idx, video_infor in enumerate(videos_to_ask, start=1):
            output.put_markdown("## Video #{idx}".format(idx=idx))
            compare_or_normal = 0
            # random.randint(0, 1)
            if compare_or_normal:
                answers = present_comparison(video_infor, comparison_questions)
            else:
                answers = present_normal(video_infor, common_questions)
            survey_answers.append(answers)
        
if __name__ == '__main__':
    survey()




# def main():



        
    
#     if input.button("Start the Survey"):
#         videos_to_ask = random.sample(video_infos, number_of_videos)
#         for idx, video_infor in enumerate(videos_to_ask, start=1):
#             input.header("Video #{idx}".format(idx=idx))
#             compare_or_normal = 0
#             # random.randint(0, 1)
#             if compare_or_normal:
#                 answers = present_comparison(video_infor, comparison_questions)
#             else:
#                 answers = present_normal(video_infor, common_questions)
#             survey_answers.append(answers)

#     if input.button("Submit Answers"):
#         print(survey_answers)
#         with open(answers_path.format(survey_uuid), "w") as f:
#             json.dump(survey_answers, f)
    
# if __name__ == "__main__":
#     main()
