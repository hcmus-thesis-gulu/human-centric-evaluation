import os
import argparse
import numpy as np

from preprocess.utils import broadcast_video


def visualize_video(video_folder, embedding_folder, context_folder,
                    demo_folder, video_name, max_length, sum_rate,
                    fps=None):
    sample_file = os.path.join(embedding_folder, f'{video_name}_samples.npy')
    keyframe_file = os.path.join(context_folder, f'{video_name}_keyframes.npy')
    
    sample_video_path = os.path.join(demo_folder, f'{video_name}_sample.avi')
    keyframe_video_path = os.path.join(demo_folder, f'{video_name}_keyframes.avi')
    raw_video_path = os.path.join(video_folder, f'{video_name}.mp4')
    
    try:
        samples = np.load(sample_file)
        broadcast_video(input_video_path=raw_video_path,
                        frame_indices=samples,
                        output_video_path=sample_video_path,
                        max_length=max_length,
                        sum_rate=sum_rate,
                        fps=fps
                        )
        
        keyframes = np.load(keyframe_file)
        broadcast_video(input_video_path=raw_video_path,
                        frame_indices=keyframes,
                        output_video_path=keyframe_video_path,
                        max_length=max_length,
                        sum_rate=sum_rate,
                        fps=fps
                        )
    except Exception as error:
        print(error)
        print(f'{video_name} not found')


def main():
    parser = argparse.ArgumentParser(description='Visualize result')
    parser.add_argument('--video-folder', type=str, required=True,
                        help='Path to folder containing videos')
    parser.add_argument('--embedding-folder', type=str, required=True,
                        help='path to folder containing feature files')
    parser.add_argument('--context-folder', type=str, required=True,
                        help='path to output folder for clustering')
    parser.add_argument('--demo-folder', type=str, required=True,
                        help='path to folder saving demo videos')
    parser.add_argument('--video-name', type=str, help='video name')
    
    parser.add_argument('--output-fps', type=int, help='video fps')
    parser.add_argument('--max-length', type=int, default=30,
                        help='maximum length of output video (in seconds)')
    parser.add_argument('--sum-rate', type=float, default=0.15,
                        help='rate of summary video (0 < rate < 1)')

    args = parser.parse_args()
    
    visualize_video(video_folder=args.video_folder,
                    embedding_folder=args.embedding_folder,
                    context_folder=args.context_folder,
                    demo_folder=args.demo_folder,
                    video_name=args.video_name,
                    max_length=args.max_length,
                    sum_rate=args.sum_rate,
                    fps=args.output_fps)


if __name__ == '__main__':
    main()
