import cv2 as cv
from tqdm import tqdm


def broadcast_video(input_video_path, frame_indices,
                    output_video_path, fps=None):
    raw_video = cv.VideoCapture(input_video_path)
    width = int(raw_video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(raw_video.get(cv.CAP_PROP_FRAME_HEIGHT))
  
    if fps == None:
        fps = int(raw_video.get(cv.CAP_PROP_FPS))
    
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    video = cv.VideoWriter(output_video_path, fourcc,
                           float(fps), (width, height))
    cur_idx = 0
    pbar = tqdm(total=len(frame_indices))
    indices = set(frame_indices.tolist())
    
    while True:
        ret, frame = raw_video.read()
        if not ret:
            break
        
        if cur_idx in indices:
            video.write(frame)
            pbar.update(1)
        
        cur_idx += 1
      
    raw_video.release()
    video.release()
    pbar.close()
