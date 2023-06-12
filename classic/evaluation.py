import os
import argparse
import time
import numpy as np
import json
from scipy.io import loadmat
from evaluator import evaluateSummary


def evaluateSummaries(groundtruth_folder, summary_folder, result_folder,
                      coef, mode):
    f_measures = {}
    
    for groundtruth_name in os.listdir(groundtruth_folder):
        if groundtruth_name.endswith('.mat'):
            filename = os.path.splitext(groundtruth_name)[0]
            groundtruth_path = os.path.join(groundtruth_folder,
                                            groundtruth_name)
            groundtruth = loadmat(groundtruth_path)
            
            user_summary = groundtruth['user_score']
            scores_path = os.path.join(summary_folder,
                                       filename + '_scores.npy')
            keyframes_path = os.path.join(summary_folder,
                                          filename + '_keyframes.npy')
            
            if os.path.exists(scores_path):
                scores = np.load(scores_path)
                keyframe_indices = np.load(keyframes_path)
                
                # file_end = '_reduced.npy' if reduced_emb else '_embeddings.npy'
                # embedding_file = filename + file_end
                # embedding_path = os.path.join(embedding_folder, embedding_file)
                # embeddings = np.load(embedding_path)
                
                # eval_results = evaluateSummary(machine_embeddings=embeddings,
                #                                machine_parts=scores,
                #                                user_summary=user_summary,
                #                                method=method,
                #                                mode=mode
                #                                )
                
                eval_results = evaluateSummary(scores=scores,
                                               user_summary=user_summary,
                                               keyframe_indices=keyframe_indices,
                                               coef=coef,
                                               mode=mode
                                               )
                
                f_score, f_scores, summary_lengths, summary_length = eval_results
                
                f_measures[filename] = {
                    'f_score': f_score,
                    'f_scores': f_scores,
                    'summary_lengths': summary_lengths,
                    'summary_length': summary_length,
                    'video_length': len(user_summary),
                    'summarized_rate': summary_length / len(user_summary)
                }
                
                print(f'F-measure of {filename} is {f_score}')
    
    if f_measures:
        f_measure = np.mean([f_measures[key]['f_score']
                             for key in f_measures])
        
        mean_sum_rate = np.mean([f_measures[key]['summarized_rate']
                                 for key in f_measures])
        var_sum_rate = np.var([f_measures[key]['summarized_rate']
                               for key in f_measures])
        
        results = {
            'f_measures': f_measures,
            'average_f_measure': f_measure,
            'dist_summarized_rate': {
                'mean': mean_sum_rate,
                'var': var_sum_rate,
            }
        }
        
        print(f'Average F-measure: {f_measure:.4f}')
        
    json_file = os.path.join(result_folder, 'results.json')
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(results, file)


def evaluate():
    parser = argparse.ArgumentParser(description='Evaluate machine learning algorithm summaries.')
    parser.add_argument('--groundtruth-folder', type=str, required=True,
                        help='Path to the folder containing groundtruth .mat files')
    # parser.add_argument('--embedding-folder', type=str, required=True,
    #                     help='Path to the folder containing output .npy files')
    parser.add_argument('--summary-folder', type=str, required=True,
                        help='Path to the folder containing output .npy files')
    parser.add_argument('--result-folder', type=str, default='result',
                        help='Path to the folder containing the result of evaluation')
    
    # parser.add_argument('--reduced-emb', action='store_true',
    #                     help='Whether to use reduced embeddings')
    parser.add_argument('--mode', type=str, default='frame',
                        help='Evaluation mode: "frame" or "fragment"')
    parser.add_argument('--coef', type=float, default=2.0,
                        help='Coefficient for taking more frames')
    # parser.add_argument('--method', type=str, default='middle',
    #                     help='Method to evaluate: "middle" or "mean"')
    
    args = parser.parse_args()
    evaluateSummaries(groundtruth_folder=args.groundtruth_folder,
                      summary_folder=args.summary_folder,
                      result_folder=args.result_folder,
                      coef=args.coef,
                      mode=args.mode
                      )


if __name__ == '__main__':
    start_time = time.time()
    evaluate()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')
