
import h5py
import json
filename = "classic/data/eccv16_dataset_summe_google_pool5.h5"
import numpy as np
import csv


# change_points
# features
# gtscore
# gtsummary
# n_frame_per_seg
# n_frames
# n_steps
# picks
# user_summary
    
fields = ["name", "fps", "#frames", "#segments", "#key frames", "#key segments", "#annotators"]
rows = []

with open("report/tmp.json", "r") as f:
    data = json.load(f)
    
with open("report/fps.json", "r") as f:
    fps = json.load(f)

def get_key_frames(gt_summary, n_frames, picks):
    gt_summary.append(0)
    gt_summary = np.array(gt_summary, dtype=np.int64)
    picks.append(1000000000)
    picks = np.array(picks, dtype=np.int64)
    interpolate_summary = np.zeros((n_frames), dtype=np.int64)
    
    for i in range(n_frames):
        lower_bound = np.where(picks <= i)[0][-1]
        upper_bound = np.where(picks >= i)[0][0]
        if picks[upper_bound] - i <= i - picks[lower_bound]:
            interpolate_summary[i] = gt_summary[upper_bound]
        else:
            interpolate_summary[i] = gt_summary[lower_bound]

    return interpolate_summary

def get_key_segments(key_frames):
    current = [-1, -1]
    key_segments = []
    n_frames = key_frames.shape[0]
    for i in range(n_frames):
        if key_frames[i]:
            if current[0] == -1:
                current[0] = i
            current[1] = i
        else:
            if current[0] != -1:
                key_segments.append((current[0], current[1]))
            current[0] = -1
            current[1] = -1
    return key_segments
    
    
for video_name in data.keys():
    print(video_name)
    # name, fps
    this_row = [video_name, fps[video_name]]
    
    video_data = data[video_name]
    # #frames
    n_frames = video_data["n_frames"]
    this_row.append(n_frames)
    # #segments
    segments = video_data["change_points"]
    this_row.append(len(segments))
    
    gt_summary = video_data["gtsummary"]
    picks = video_data["picks"]
    key_frames = get_key_frames(gt_summary, n_frames, picks)
    
    # #key frames
    this_row.append(key_frames.sum())
    
    key_segments = get_key_segments(key_frames)
    
    # #key segments
    this_row.append(len(key_segments))
    
    # #annotators
    this_row.append(len(video_data["user_summary"]))
        
    rows.append(this_row)
    # break

with open("report/overview.csv", "w") as f:
    csvwriter = csv.writer(f) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(rows)
    
    
print("HEHEHEHEH")