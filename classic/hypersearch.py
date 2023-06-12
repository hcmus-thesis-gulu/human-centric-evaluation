import argparse
import time
import json
import numpy as np

from evaluation import evaluateSummaries, testSummaries


def search():
    parser = argparse.ArgumentParser(description='Evaluate machine learning algorithm summaries.')
    
    parser.add_argument('--original', action='store_true',
                        help='Evaluate the original dataset'
                        )
    # parser.add_argument('--original-folder', type=str,
    #                     help='Path to the folder containing the original dataset'
    #                     )
    
    parser.add_argument('--groundtruth-folder', type=str, required=True,
                        help='Path to the folder containing groundtruth .mat files')
    parser.add_argument('--summary-folder', type=str, required=True,
                        help='Path to the folder containing output .npy files')
    parser.add_argument('--result-folder', type=str, default='result',
                        help='Path to the folder containing the result of evaluation')
    
    parser.add_argument('--mode', type=str, default='frame',
                        help='Evaluation mode: "frame" or "fragment"')
    parser.add_argument('--min-coef', type=float, default=1.0)
    parser.add_argument('--max-coef', type=float, default=5.0)
    parser.add_argument('--max-expand', type=int, default=8)
    
    args = parser.parse_args()
    
    search_resuls = []
    
    for coef in np.arange(args.min_coef, args.max_coef + 1, 0.5):
        for expand in np.arange(args.max_expand + 1):
            if args.original:
                score = evaluateSummaries(groundtruth_folder=args.groundtruth_folder,
                                          summary_folder=args.summary_folder,
                                          result_folder=None,
                                          coef=coef,
                                          mode=args.mode,
                                          expand=expand
                                          )
            else:
                score = testSummaries(groundtruth_folder=args.groundtruth_folder,
                                      summary_folder=args.summary_folder,
                                      result_folder=None,
                                      coef=coef,
                                      expand=expand
                                      )
            
            search_result = {
                'coef': float(coef),
                'expand': int(expand),
                'f-score': float(score[0]),
                'top-5': float(score[1]),
            }
            search_resuls.append(search_result)
            
    # Sort by score
    sorted_result = sorted(search_resuls, key=lambda x: x['top-5'],
                           reverse=True)
    for i, result in enumerate(sorted_result[:10]):
        print(f"{i+1}. Coef: {result['coef']:.2f}, Expand: "
              + f"{result['expand']}, Score: {result['f-score']:.4f}"
              + f", Top-5: {result['top-5']:.4f}"
              )
    
    result_name = 'original' if args.original else 'test'
    result_path = args.result_folder + f'/{result_name}_results.json'
    
    with open(result_path, 'w', encoding='utf-8') as result_file:
        json.dump(search_resuls, result_file)


if __name__ == '__main__':
    start_time = time.time()
    search()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')
