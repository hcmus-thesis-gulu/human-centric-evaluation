import numpy as np
from utils import mean_embeddings, similarity_score


# # For each segment, compute the mean features and
# # similarity of all features with the mean
# def extractSummary(embeddings, segments, method):
#     segment_scores = []
#     keyframe_indices = []
    
#     for _, start, end in segments:
#         # Get the associated features
#         segment_features = embeddings[start:end]
        
#         # Calculate the similarity with representative
#         if method == "mean":
#             mean = mean_embeddings(segment_features)
#         elif method == "middle":
#             mean = segment_features[len(segment_features) // 2]
        
#         score = similarity_score(segment_features, mean)
#         segment_scores.extend(score.tolist())
        
#         # Select the representative with the highest similarity
#         keyframe_index = np.argmax(score) + start
#         keyframe_indices.append(keyframe_index)
    
#     return np.asarray(segment_scores), np.asarray(keyframe_indices).sort()


# def computeSummary(embeddings, segments, length, method):
#     scores, key_indices = extractSummary(embeddings, segments, method)
    
#     if length < len(key_indices):
#         selection_step = len(key_indices) / length
#         selections = key_indices[::selection_step]
#         return selections
#     else:
#         unselected_scores = np.delete(scores, key_indices)
#         selection = np.argpartition(unselected_scores,
#                                     -length)[-length:]
        
#         # Final selections are the keyframes and the selected frames
#         selections = np.concatenate((key_indices, selection))
#         selections.sort()
        
#         return selections


def computeSummary(scores, keyframe_indices, length):
    if length < len(keyframe_indices):
        selection_step = (len(keyframe_indices) // length) + 1
    else:
        selection_step = 1
        
    selection = keyframe_indices[::selection_step]
    remained_length = length - len(selection)
    assert remained_length >= 0
    
    unselected_scores = np.delete(scores, selection)
    
    try:
        other_selection = np.argpartition(unselected_scores,
                                        -remained_length)[-remained_length:]
    except Exception as error:
        print(error)
        print(f"length: {length}")
        print(f"len(keyframe_indices): {len(keyframe_indices)}")
        print(f"len(selection): {len(selection)}")
        print(f"remained_length: {remained_length}")
    
    selections = np.concatenate((selection, other_selection))
    return np.sort(selections)


def evaluateSummary(scores, user_summary, keyframe_indices, mode='frame'):
    f_scores = []
    lengths = []
    
    for user in range(user_summary.shape[1]):
        user_selected = np.where(user_summary[:, user] > 0)[0]
        
        if mode == 'frame':
            length = len(user_selected)
            machine_selected = computeSummary(scores=scores,
                                              keyframe_indices=keyframe_indices,
                                              length=length,
                                              )
            
            tp = len(np.intersect1d(machine_selected, user_selected))
            fp = len(np.setdiff1d(machine_selected, user_selected))
            fn = len(np.setdiff1d(user_selected, machine_selected))
        elif mode == 'fragment':
            user_fragments = np.unique(user_summary[:, user])
            length = len(user_fragments)
            machine_selected = computeSummary(scores=scores,
                                              keyframe_indices=keyframe_indices,
                                              length=length,
                                              )
            
            intersected_indices = np.intersect1d(machine_selected,
                                                 user_selected)
            
            tp = len(np.unique(user_summary[intersected_indices, user]))
            fp = length - tp
            fn = length - tp
        
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f_score = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        f_scores.append(f_score)
        lengths.append(length)
    
    # Maximum F-measure across all users
    f_score = max(f_scores)
    summary_length = lengths[np.argmax(f_scores)]
    
    return f_score, f_scores, lengths, summary_length
