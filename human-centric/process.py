import json
import os
import random
import csv

answer_folder = "human-centric/answers-huhu"
fields = ['video name', 'user summary', 'our summary']
scores = {}

with open("human-centric/questions.json", "r") as f:
    data = json.load(f)
    for x in data:
        scores[x['name']] = {
            'original': {},
            'user summary': {},
            'our summary': {}
        }



for filename in os.listdir(answer_folder):
    answer_path = os.path.join(answer_folder, filename)
    with open(answer_path, "r") as f:
        data = json.load(f)
    for video_set in data:
        video_name = video_set['name']
        survey_results = video_set['survey_results']
        user_index = video_set['user_index']
        # random.randint(0, 30)
        for result in survey_results:
            question = result['question']['question']
            question_type = result['question']['type']
            answer = result['answer']
            if question_type != 'multiple':
                continue
            if user_index == 0:
                if question not in scores[video_name]['original'].keys():
                    scores[video_name]['original'][question] = {}
                if answer not in scores[video_name]['original'][question].keys():
                    scores[video_name]['original'][question][answer] = 0
                scores[video_name]['original'][question][answer] += 1
            elif user_index <= 15:
                if question not in scores[video_name]['user summary'].keys():
                    scores[video_name]['user summary'][question] = {}
                if answer not in scores[video_name]['user summary'][question].keys():
                    scores[video_name]['user summary'][question][answer] = 0
                scores[video_name]['user summary'][question][answer] += 1
            else:
                if question not in scores[video_name]['our summary'].keys():
                    scores[video_name]['our summary'][question] = {}
                if answer not in scores[video_name]['our summary'][question].keys():
                    scores[video_name]['our summary'][question][answer] = 0
                scores[video_name]['our summary'][question][answer] += 1

print(scores)
with open("human-centric/multiple.json", "w") as f:
    json.dump(scores, f)
# with open("human-centric/score.csv", "w") as f:
#     csvwriter = csv.writer(f) 
#     csvwriter.writerow(fields) 
#     for video_name in scores.keys():
#         tmp = [video_name]
#         if scores[video_name]['user summary']['count']:
#             tmp.append(scores[video_name]['user summary']['score']/scores[video_name]['user summary']['count'])
#         else:
#             tmp.append('NaN')
#         if scores[video_name]['our summary']['count']:
#             tmp.append(scores[video_name]['our summary']['score']/scores[video_name]['our summary']['count'])
#         else:
#             tmp.append('NaN')
        
#         csvwriter.writerow(tmp)    

    


    