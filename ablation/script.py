import os

distance = "euclidean"
# embedding_dim = 3

groundtruth_folder = "classic/data"
summary_folder = "ablation/dino-brute-force/summaries/{distance}/pca-only/embedding-{embedding_dim}"
# /intermediate-{intermediate_dim}"
result_folder = "ablation/dino-brute-force/{distance}/pca-only/embedding-{embedding_dim}"
# /intermediate-{intermediate_dim}"

for i in range(4, 129):
    # intermediate_dim = 1 << i
    embedding_dim = 1 << i
    tmp_summary_folder = summary_folder.format(distance=distance, embedding_dim=embedding_dim)
                                            #    , intermediate_dim=intermediate_dim)
    tmp_result_folder = result_folder.format(distance=distance, embedding_dim=embedding_dim)
                                            #  , intermediate_dim=intermediate_dim)
    os.mkdir(tmp_result_folder)
    
    os.system("python classic/hypersearch.py --groundtruth-folder {groundtruth_folder} --summary-folder {summary_folder} --result-folder {result_folder} --mode shot --min-coef 0.0 --max-coef 0.1 --iter-coef 0.5  --min-expand 0.15 --max-expand 0.30 --iter-expand 0.05".format(
        groundtruth_folder=groundtruth_folder,
        summary_folder=tmp_summary_folder,
        result_folder=tmp_result_folder,
        
    ))