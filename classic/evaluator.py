import numpy as np

def computeSummary(scores, length, method='max'):
    if method == 'max':
        return np.argpartition(scores, -length)[-length:]

def evaluateSummary(machine_summary, user_summary, mode='frame'):
    f_measures = []
    for user in range(user_summary.shape[1]):
        if mode == 'frame':
            user_selected = np.where(user_summary[:, user] > 0)[0]
            length = len(user_selected)
            machine_selected = computeSummary(machine_summary, length)
            
            tp = len(np.intersect1d(machine_selected, user_selected))
            fp = len(np.setdiff1d(machine_selected, user_selected))
            fn = len(np.setdiff1d(user_selected, machine_selected))
        elif mode == 'fragment':
            user_fragments = np.unique(user_summary[:, user])
            length = len(user_fragments)
            machine_selected = computeSummary(machine_summary, length)
            
            intersected_indices = np.intersect1d(machine_selected, np.where(user_summary[:, user] > 0)[0])
            tp = len(np.unique(user_summary[intersected_indices, user]))
            
            fp = length - tp
            fn = length - tp
        
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f_measure = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        f_measures.append(f_measure)
    
    avg_f_measure = sum(f_measures) / len(f_measures)
    return avg_f_measure