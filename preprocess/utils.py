import cv2 as cv
from tqdm import tqdm


def broadcast_video(input_video_path, frame_indices,
                    output_video_path, max_length,
                    sum_rate, fps=None):
    raw_video = cv.VideoCapture(input_video_path)
    width = int(raw_video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(raw_video.get(cv.CAP_PROP_FRAME_HEIGHT))
    video_length = int(raw_video.get(cv.CAP_PROP_FRAME_COUNT))
  
    if fps is None:
        fps = int(raw_video.get(cv.CAP_PROP_FPS))
    
    # Maximum nunmber of frames in the summary
    frames_length = int(max_length * fps)
    
    # Estimated number of frames in the summary
    estimated_length = int(video_length * sum_rate)
    
    # Final number of frames of the summary
    summary_length = min(frames_length, estimated_length)
    
    # Length of the fragment around each keyframe
    fragment_length = summary_length // len(frame_indices)
    
    # Fragment width of the computed fragment length
    fragment_width = (fragment_length - 1) // 2
    
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    video = cv.VideoWriter(output_video_path, fourcc,
                           float(fps), (width, height))
    cur_idx = 0
    pbar = tqdm(total=len(frame_indices))
    kf_idx = 0
    
    while True:
        ret, frame = raw_video.read()
        if not ret:
            break
        
        while kf_idx < len(frame_indices) and frame_indices[kf_idx] < cur_idx - fragment_width:
            kf_idx += 1
        if kf_idx < len(frame_indices) and abs(frame_indices[kf_idx] - cur_idx) <= fragment_width:
            video.write(frame)
        
        if cur_idx in frame_indices:
            pbar.update(1)
        
        cur_idx += 1
      
    raw_video.release()
    video.release()
    pbar.close()
