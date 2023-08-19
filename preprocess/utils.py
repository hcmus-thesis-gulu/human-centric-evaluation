import cv2 as cv
from tqdm import tqdm
from classic.utils import generate_summary


def count_frames(video_path):
    # Extract features for each frame of the video
    video = cv.VideoCapture(video_path)
    # Get the video's frame rate, total frames
    fps = int(video.get(cv.CAP_PROP_FPS))

    count = 0
    while True:
        ret, _ = video.read()
        if not ret:
            break
        count += 1

    video.release()
    return fps, count


def broadcast_segment(output_video_path, raw_video, segments, scores, summary_length, fps, width, height):
    keyframes = generate_summary(segments=segments,
                                 scores=scores,
                                 fill_mode='linear',
                                 key_length=summary_length
                                 )

    fourcc = cv.VideoWriter_fourcc(*'VP90')
    video = cv.VideoWriter(output_video_path, fourcc,
                           float(fps), (width, height))
    cur_idx = 0
    pbar = tqdm(total=len(keyframes))

    while True:
        ret, frame = raw_video.read()
        if not ret:
            break

        if keyframes[cur_idx] > 0:
            video.write(frame)

        if cur_idx in keyframes:
            pbar.update(1)

        cur_idx += 1

    pbar.close()
    video.release()


def broadcast_fragment(output_video_path, raw_video, frame_indices, summary_length, fps, width, height):
    # Length of the fragment around each keyframe
    fragment_length = summary_length // len(frame_indices)
    print(f'Length of the fragment: {fragment_length}')

    # Fragment width of the computed fragment length
    fragment_width = max(0, (fragment_length - 1) // 2)
    print(f'Width of fragments: {fragment_width}')

    fourcc = cv.VideoWriter_fourcc(*'VP90')
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

    pbar.close()
    video.release()


def broadcast_video(input_video_path, input, output_video_path, segments,
                    max_length, sum_rate, fps=None):
    raw_video = cv.VideoCapture(input_video_path)
    width = int(raw_video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(raw_video.get(cv.CAP_PROP_FRAME_HEIGHT))

    computed_fps, video_length = count_frames(input_video_path)

    if fps is None:
        fps = computed_fps

    print(f'FPS: {fps}')

    # Maximum nunmber of frames in the summary
    frames_length = int(max_length * fps)

    # Estimated number of frames in the summary
    estimated_length = int(video_length * sum_rate)

    # Final number of frames of the summary
    summary_length = max(min(frames_length, estimated_length),
                         len(input))
    print(f'Frames in the summary: {summary_length}')

    if segments is not None:
        broadcast_segment(output_video_path=output_video_path,
                          raw_video=raw_video,
                          segments=segments,
                          scores=input,
                          summary_length=summary_length,
                          fps=fps,
                          width=width,
                          height=height)
    else:
        broadcast_fragment(output_video_path=output_video_path,
                           raw_video=raw_video,
                           frame_indices=input,
                           summary_length=summary_length,
                           fps=fps,
                           width=width,
                           height=height)

    raw_video.release()
