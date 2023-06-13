""" Convert user summaries into .avi videos
"""
import os
import time
import argparse
from tqdm import tqdm
from scipy import io as sio

from preprocess.utils import broadcast_video


def visualize_video(filename, video_path, user_summaries, user_folder,
                    fps=None):
    num_users = user_summaries.shape[1]
    
    for user_idx in tqdm(range(num_users)):
        user_file = filename + f'_user{user_idx + 1}.avi'
        user_path = os.path.join(user_folder, user_file)
        
        broadcast_video(input_video_path=video_path,
                        frame_indices=user_summaries[:, user_idx],
                        output_video_path=user_path,
                        fps=fps
                        )


def visualize_videos(video_folder, groundtruth_folder, user_folder, fps=None):
    for video_file in os.listdir(video_folder):
        if video_file.endswith('.mp4'):
            filename = video_file[:-4]
            print(f'Visualizing user summaries of {filename}')
            video_path = os.path.join(video_folder, video_file)
            
            groundtruth_file = filename + '.mat'
            groundtruth_path = os.path.join(groundtruth_folder,
                                            groundtruth_file)
            groundtruth = sio.loadmat(groundtruth_path)
            
            user_summaries = groundtruth['user_score']
            
            visualize_video(filename=filename,
                            video_path=video_path,
                            user_summaries=user_summaries,
                            user_folder=user_folder,
                            fps=fps
                            )


def main():
    parser = argparse.ArgumentParser(description='Visualize summaries by users')
    parser.add_argument('--video-folder', type=str, required=True,
                        help='Path to folder containing videos')
    parser.add_argument('--groundtruth-folder', type=str, required=True,
                        help='path to folder containing feature files')
    parser.add_argument('--user-folder', type=str, required=True,
                        help='path to folder saving videos from users')
    
    parser.add_argument('--output-fps', type=int, help='video fps')

    args = parser.parse_args()
    
    visualize_videos(video_folder=args.video_folder,
                     groundtruth_folder=args.groundtruth_folder,
                     user_folder=args.user_folder,
                     fps=args.output_fps
                     )


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')
