import os
import argparse
import numpy as np

from preprocess.utils import broadcast_video


def visualize_video(video_folder, embedding_folder, context_folder,
                    demo_folder, video_name, frag_width, fps=None):
    sample_file = os.path.join(embedding_folder, f'{video_name}_samples.npy')
    keyframe_file = os.path.join(context_folder, f'{video_name}_keyframes.npy')
    
    sample_video_path = os.path.join(demo_folder, f'{video_name}_sample.avi')
    keyframe_video_path = os.path.join(demo_folder, f'{video_name}_keyframes.avi')
    raw_video_path = os.path.join(video_folder, f'{video_name}.mp4')
    
    try:
        samples = np.load(sample_file)
        broadcast_video(input_video_path=raw_video_path, frame_indices=samples,
                        output_video_path=sample_video_path,
                        fragment_width=frag_width, fps=fps
                        )
        
        keyframes = np.load(keyframe_file)
        broadcast_video(input_video_path=raw_video_path,
                        frame_indices=keyframes,
                        output_video_path=keyframe_video_path,
                        fps=fps, fragment_width=frag_width
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
    parser.add_argument('--frag-width', type=int, default=10,
                        help='width of key fragment around the keyframes')

    args = parser.parse_args()
    
    visualize_video(video_folder=args.video_folder,
                    embedding_folder=args.embedding_folder,
                    context_folder=args.context_folder,
                    demo_folder=args.demo_folder,
                    video_name=args.video_name,
                    frag_width=args.frag_width,
                    fps=args.output_fps)


if __name__ == '__main__':
    main()
