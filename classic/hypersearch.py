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
                        chocies=['frame', 'fragment', 'shot'],
                        help='Evaluation mode: "frame", "fragment" or "shot"')
    
    parser.add_argument('--min-coef', type=float, default=1.0)
    parser.add_argument('--max-coef', type=float, default=5.0)
    parser.add_argument('--iter-coef', type=float, default=0.5)
    
    parser.add_argument('--min-expand', type=float,
                        help='Int > 1: Minimum number of frames to expand'
                        + '0 < Float < 1: Minimum percentage of selection')
    parser.add_argument('--max-expand', type=float,
                        help='Int > 1: Maximum number of frames to expand'
                        + '0 < Float < 1: Maximum percentage of selection')
    parser.add_argument('--iter-expand', type=float,
                        help='Iteration between min-expand and max-expand')
    
    args = parser.parse_args()
    
    fill_modes = ['linear', 'nearest', 'nearest-up']
    search_resuls = []
    
    for coef in np.arange(args.min_coef,
                          args.max_coef + args.iter_coef,
                          args.iter_coef):
        for expand in np.arange(args.min_expand,
                                args.max_expand + args.iter_expand,
                                args.iter_expand):
            if args.mode == 'shot':
                for fill_mode in fill_modes:
                    score = testSummaries(groundtruth_folder=args.groundtruth_folder,
                                          summary_folder=args.summary_folder,
                                          result_folder=None,
                                          coef=coef,
                                          mode=args.mode,
                                          fill_mode=fill_mode,
                                          expand=expand
                                          )
                    
                    search_result = {
                        'coef': float(coef),
                        'expand': int(expand),
                        'fill-mode': fill_mode,
                        'max-f': float(score[0]),
                        'avg-f': float(score[1]),
                        'top-5': float(score[2]),
                    }
                    search_resuls.append(search_result)
            else:
                if args.original:
                    score = evaluateSummaries(groundtruth_folder=args.groundtruth_folder,
                                              summary_folder=args.summary_folder,
                                              result_folder=None,
                                              coef=coef,
                                              mode=args.mode,
                                              expand=expand
                                              )
                elif args.mode == 'frame':
                    score = testSummaries(groundtruth_folder=args.groundtruth_folder,
                                          summary_folder=args.summary_folder,
                                          result_folder=None,
                                          coef=coef,
                                          mode=args.mode,
                                          fill_mode=None,
                                          expand=expand
                                          )
            
                search_result = {
                    'coef': float(coef),
                    'expand': int(expand),
                    'max-f': float(score[0]),
                    'avg-f': float(score[1]),
                    'top-5': float(score[2]),
                }
                search_resuls.append(search_result)
            
    # Sort by score
    sorted_result = sorted(search_resuls, key=lambda x: x['top-5'],
                           reverse=True)
    for i, result in enumerate(sorted_result[:10]):
        param = f"coef={result['coef']:.2f}, expand={result['expand']}"
        if args.mode == 'shot':
            param += f", fill-mode={result['fill-mode']}"
            
        result = f"avg-f={result['avg-f']:.4f}, top-5={result['top-5']:.4f}"
        if result['max-f'] is not None:
            result += f", max-f={result['max-f']:.4f}"
        
        display = f"{i+1}. {param}; {result}"
        print(display)
    
    result_name = 'original' if args.original else 'test'
    result_path = args.result_folder + f'/{result_name}_results.json'
    
    with open(result_path, 'w', encoding='utf-8') as result_file:
        json.dump(search_resuls, result_file)


if __name__ == '__main__':
    start_time = time.time()
    search()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time:.2f} seconds')
