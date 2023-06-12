import argparse
import time
import json

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
    
    parser.add_argument('--mode', type=str, default='frame',
                        help='Evaluation mode: "frame" or "fragment"')
    parser.add_argument('--min-coef', type=float, default=1.0)
    parser.add_argument('--min-coef', type=float, default=5.0)
    parser.add_argument('--max-expand', type=int, default=8)
    
    args = parser.parse_args()
    
    search_resuls = []
    
    for coef in range(args.min_coef, args.max_coef + 1, 0.5):
        for expand in range(args.max_expand + 1):
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
                'coef': coef,
                'expand': expand,
                'score': score
            }
            search_resuls.append(search_result)
            
    # Sort by score
    sorted_result = sorted(search_resuls, key=lambda x: x['score'],
                           reverse=True)
    print(sorted_result[:10])
    
    result_path = args.result_folder + '/search_results.json'
    with open(result_path, 'w', encoding='utf-8') as result_file:
        json.dump(search_resuls, result_file)


if __name__ == '__main__':
    start_time = time.time()
    search()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')
