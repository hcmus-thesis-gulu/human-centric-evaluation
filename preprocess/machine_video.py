import os
import argparse
import numpy as np

from preprocess.utils import broadcast_video


def materialize_video(video_folder, summary_folder, demo_folder, video_name,
                      max_length, sum_rate, fps=None):
    keyframe_file = os.path.join(summary_folder, f'{video_name}_keyframes.npy')
    keyframes = np.load(keyframe_file)
    
    keyframe_video_path = os.path.join(demo_folder, f'{video_name}_keyframes.avi')
    raw_video_path = os.path.join(video_folder, f'{video_name}.mp4')
    
    broadcast_video(input_video_path=raw_video_path,
                    frame_indices=keyframes,
                    output_video_path=keyframe_video_path,
                    max_length=max_length,
                    sum_rate=sum_rate,
                    fps=fps
                    )
        

def materialize_videos(video_folder, summary_folder, demo_folder, max_length,
                       sum_rate, fps=None):
    video_files = os.listdir(video_folder)
    
    for video_file in video_files:
        video_name = video_file.split('.')[0]
        print(f'Processing {video_name}')
        
        materialize_video(video_folder=video_folder,
                          summary_folder=summary_folder,
                          demo_folder=demo_folder,
                          video_name=video_name,
                          max_length=max_length,
                          sum_rate=sum_rate,
                          fps=fps)


def main():
    parser = argparse.ArgumentParser(description='Visualize result')
    parser.add_argument('--video-folder', type=str, required=True,
                        help='Path to folder containing videos')
    parser.add_argument('--summary-folder', type=str, required=True,
                        help='path to output folder for clustering')
    parser.add_argument('--demo-folder', type=str, required=True,
                        help='path to folder saving demo videos')
    
    parser.add_argument('--output-fps', type=int, help='video fps')
    parser.add_argument('--max-length', type=int, default=30,
                        help='maximum length of output video (in seconds)')
    parser.add_argument('--sum-rate', type=float, default=0.15,
                        help='rate of summary video (0 < rate < 1)')

    args = parser.parse_args()
    
    materialize_videos(video_folder=args.video_folder,
                       summary_folder=args.context_folder,
                       demo_folder=args.demo_folder,
                       max_length=args.max_length,
                       sum_rate=args.sum_rate,
                       fps=args.output_fps)


if __name__ == '__main__':
    main()
