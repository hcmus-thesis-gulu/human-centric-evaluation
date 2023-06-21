import os

distance = "euclidean"
# embedding_dim = 2

groundtruth_folder = "classic/data"
summary_folder = "ablation/dino/summaries/{distance}/pca-only/embedding-{embedding_dim}"
result_folder = "ablation/dino/results/{distance}/pca-only/embedding-{embedding_dim}"

for i in range(2, 9):
    embedding_dim = 1 << i
    tmp_summary_folder = summary_folder.format(distance=distance, embedding_dim=embedding_dim)
    tmp_result_folder = result_folder.format(distance=distance, embedding_dim=embedding_dim)
    os.mkdir(tmp_result_folder)
    
    os.system("python classic/evaluation.py --groundtruth-folder {groundtruth_folder} --summary-folder {summary_folder} --result-folder {result_folder} --mode shot --coef 0 --expand 0.20 --fill-mode linear".format(
        groundtruth_folder=groundtruth_folder,
        summary_folder=tmp_summary_folder,
        result_folder=tmp_result_folder,
        
    ))
    
#     os.system("python scripts/summarization.py --embedding-folder {embedding_folder} --context-folder {context_folder} --summary-folder {summary_folder} --scoring-mode uniform --kf-mode middle-ends --reduced-emb --bias -1 --max-len 0".format(
#         embedding_folder=embedding_folder,
#         context_folder=tmp_context_folder,
#         summary_folder=tmp_summary_folder
#     ))