import numpy as np


# For each segment, compute the mean features and
# similarity of all features with the mean
def extractSummary(self, embeddings, segments):
    segment_scores = []
    
    for _, start, end in segments:
        # Get the associated features
        segment_features = embeddings[start:end]
        
        # Calculate the similarity with representative
        if self.representative == "mean":
            mean = mean_embeddings(segment_features)
        elif self.representative == "middle":
            mean = segment_features[len(segment_features) // 2]
        
        score = similarity_score(segment_features, mean)
        segment_scores.extend(score.tolist())
    
    return np.asarray(segment_scores)


def computeSummary(segments, length, method='max'):
    if length < len(segments):
        selection_step = len(segments) / length
        selected_parts = segments[::selection_step]
        
        # Select representative of the selected parts
        selection = extractSummary(selected_parts, method)
        return selection
    else:
        # Select representative of all parts
        summary = extractSummary(segments, method)
        unselected
        selection =  np.argpartition(scores, -length)[-length:]
        return selection


def evaluateSummary(machine_parts, user_summary, mode='frame'):
    f_measures = []
    for user in range(user_summary.shape[1]):
        user_selected = np.where(user_summary[:, user] > 0)[0]
        
        if mode == 'frame':
            length = len(user_selected)
            machine_selected = computeSummary(machine_parts, length)
            
            tp = len(np.intersect1d(machine_selected, user_selected))
            fp = len(np.setdiff1d(machine_selected, user_selected))
            fn = len(np.setdiff1d(user_selected, machine_selected))
        elif mode == 'fragment':
            user_fragments = np.unique(user_summary[:, user])
            length = len(user_fragments)
            machine_selected = computeSummary(machine_parts, length)
            
            intersected_indices = np.intersect1d(machine_selected,
                                                 user_selected)
            
            tp = len(np.unique(user_summary[intersected_indices, user]))
            fp = length - tp
            fn = length - tp
        
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f_measure = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        f_measures.append(f_measure)
    
    # Maximum F-measure across all users
    f_score = max(f_measures)
    
    return f_score, f_measures
