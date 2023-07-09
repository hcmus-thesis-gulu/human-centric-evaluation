import csv 
import json


pca_only_result_file = "ablation/dino-brute-force/{distance}/pca-only/embedding-{embedding_dim}/test_shot_results.json"
pca_tsne_result_file = "ablation/dino-brute-force/{distance}/pca-tsne/embedding-{embedding_dim}/intermediate-{intermediate_dim}/test_shot_results.json"

csv_file = "ablation/results-top-5.csv"

fields = ["embedding-dim"]
cosine_pca_only = ["cosine-pca-only"]
cosine_pca_tsne_2 = ["cosine-pca-tsne-2"]
cosine_pca_tsne_3 = ["cosine-pca-tsne-3"]
euclidean_pca_only = ["euclidean-pca-only"]
euclidean_pca_tsne_2 = ["euclidean-pca-tsne-2"]
euclidean_pca_tsne_3 = ["euclidean-pca-tsne-3"]
random_summary = ["random-summary"]

def get_stats(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        
    max_f = 0.0
    avg_f = 0.0
    top_5 = 0.0
    for ele in data:
        max_f = max(max_f, ele['max-f'])
        avg_f = max(avg_f, ele['avg-f'])
        top_5 = max(top_5, ele['top-5'])
    
    return max_f, avg_f, top_5
        

for i in range(4, 129):
    fields.append(i)
    random_summary.append(0.402)
    
    tmp_result_file = pca_only_result_file.format(distance="cosine", embedding_dim=i)
    max_f, avg_f, top_5 = get_stats(tmp_result_file)
    cosine_pca_only.append(top_5)
    
    tmp_result_file = pca_tsne_result_file.format(distance="cosine", embedding_dim=2, intermediate_dim=i)
    max_f, avg_f, top_5 = get_stats(tmp_result_file)
    cosine_pca_tsne_2.append(top_5)
    
    tmp_result_file = pca_tsne_result_file.format(distance="cosine", embedding_dim=3, intermediate_dim=i)
    max_f, avg_f, top_5 = get_stats(tmp_result_file)
    cosine_pca_tsne_3.append(top_5)
    
    tmp_result_file = pca_only_result_file.format(distance="euclidean", embedding_dim=i)
    max_f, avg_f, top_5 = get_stats(tmp_result_file)
    euclidean_pca_only.append(top_5)
    
    tmp_result_file = pca_tsne_result_file.format(distance="euclidean", embedding_dim=2, intermediate_dim=i)
    max_f, avg_f, top_5 = get_stats(tmp_result_file)
    euclidean_pca_tsne_2.append(top_5)
    
    tmp_result_file = pca_tsne_result_file.format(distance="euclidean", embedding_dim=3, intermediate_dim=i)
    max_f, avg_f, top_5 = get_stats(tmp_result_file)
    euclidean_pca_tsne_3.append(top_5)
    

# print(len(fields))
with open(csv_file, 'w') as f: 
    csvwriter = csv.writer(f) 
    csvwriter.writerow(fields) 
    csvwriter.writerow(cosine_pca_only)
    csvwriter.writerow(cosine_pca_tsne_2)
    csvwriter.writerow(cosine_pca_tsne_3)
    csvwriter.writerow(euclidean_pca_only)
    csvwriter.writerow(euclidean_pca_tsne_2)
    csvwriter.writerow(euclidean_pca_tsne_3)
    csvwriter.writerow(random_summary)