import numpy as np
from scipy.io import loadmat
from evaluator import evaluateSummary
import os
import argparse
import time

def evaluateSummaries(groundtruth_folder, output_folder, mode):
    f_measures = []
    for mat_file in os.listdir(groundtruth_folder):
        if mat_file.endswith('.mat'):
            video_name = os.path.splitext(mat_file)[0]
            mat_data = loadmat(os.path.join(groundtruth_folder, mat_file))
            user_summary = mat_data['user_summary']
            
            npy_file = os.path.join(output_folder, video_name + '_segments.npy')
            if os.path.exists(npy_file):
                machine_summary = np.load(npy_file)
                f_measure = evaluateSummary(machine_summary, user_summary, mode)
                f_measures.append(f_measure)
                print(f'{video_name}: {f_measure}')
    
    if f_measures:
        avg_f_measure = sum(f_measures) / len(f_measures)
        print(f'Average F-measure: {avg_f_measure:.4f}')

def evaluate():
    parser = argparse.ArgumentParser(description='Evaluate machine learning algorithm summaries.')
    parser.add_argument('--groundtruth', type=str, required=True,
                        help='Path to the folder containing groundtruth .mat files')
    parser.add_argument('--output', type=str, required=True,
                        help='Path to the folder containing output .npy files')
    parser.add_argument('--mode', type=str, default='frame',
                        help='Evaluation mode: "frame" or "fragment"')
    args = parser.parse_args()
    
    evaluateSummaries(args.groundtruth, args.output, args.mode)

if __name__ == '__main__':
    start_time = time.time()
    evaluate()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')