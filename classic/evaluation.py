import os
import argparse
import time
import numpy as np
import json
from scipy.io import loadmat
from evaluator import evaluateSummary


# TODO: Storing the video-level result to a json in result folder
def evaluateSummaries(groundtruth_folder, summary_folder,
                      result_folder, mode):
    f_scores = {'scores': {}}
    for groundtruth_name in os.listdir(groundtruth_folder):
        if groundtruth_name.endswith('.mat'):
            grountruth_file = os.path.splitext(groundtruth_name)[0]
            groundtruth_path = os.path.join(groundtruth_folder,
                                            groundtruth_name)
            groundtruth = loadmat(groundtruth_path)
            
            user_summary = groundtruth['user_summary']
            segments = os.path.join(summary_folder,
                                    grountruth_file + '_segments.npy')
            
            if os.path.exists(segments):
                machine_parts = np.load(segments)
                f_score, f_measure = evaluateSummary(machine_parts,
                                                     user_summary,
                                                     mode)
                
                f_scores['scores'][grountruth_file] = f_score
                print(f'F-measure of {grountruth_file} is {f_measure}')
                
                result_file = os.path.join(result_folder,
                                           grountruth_file + '_feval.npy')
                np.save(result_file, f_measure)
    
    if f_scores:
        avg_f_score = sum(f_scores) / len(f_scores)
        f_scores['average'] = avg_f_score
        print(f'Average F-measure: {avg_f_score:.4f}')
        
    json_file = os.path.join(result_folder, 'f_scores.json')
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(f_scores, file)


def evaluate():
    parser = argparse.ArgumentParser(description='Evaluate machine learning algorithm summaries.')
    parser.add_argument('--groundtruth-folder', type=str, required=True,
                        help='Path to the folder containing groundtruth .mat files')
    parser.add_argument('--summary-folder', type=str, required=True,
                        help='Path to the folder containing output .npy files')
    parser.add_argument('--result-folder', type=str, default='result',
                        help='Path to the folder containing the result of evaluation')
    
    parser.add_argument('--mode', type=str, default='frame',
                        help='Evaluation mode: "frame" or "fragment"')
    
    args = parser.parse_args()
    evaluateSummaries(groundtruth_folder=args.groundtruth_folder,
                      summary_folder=args.summary_folder,
                      result_folder=args.result_folder,
                      mode=args.mode)


if __name__ == '__main__':
    start_time = time.time()
    evaluate()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')