import numpy as np


def mean_embeddings(embeddings):
    return np.mean(embeddings, axis=0)


# Compute the cosine similarity between set of features and its mean
def similarity_score(embeddings, mean=None):
    if mean is None:
        mean = mean_embeddings(embeddings)
    
    return np.dot(embeddings, mean) / (np.linalg.norm(embeddings) *
                                       np.linalg.norm(mean)
                                       )
