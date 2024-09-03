import cv2
import os

# Create a directory to save video clips
output_dir = 'video_clips'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set up video capture from the default camera
cap = cv2.VideoCapture(0)

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Initialize variables
clip_duration = 10  # 10 seconds per clip
fps = 30  # Frames per second
frame_count = 0
clip_count = 0
buffer_frames = []

# To store the first 2 seconds of the first clip
initial_frames = []
initial_frame_limit = 2 * fps  # First 2 seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    buffer_frames.append(frame)
    frame_count += 1

    # Save the initial 2 seconds of the first clip
    if clip_count == 0 and frame_count <= initial_frame_limit:
        initial_frames.append(frame)

    # Save the clip every 10 seconds
    if frame_count == clip_duration * fps:
        clip_count += 1
        output_file = os.path.join(output_dir, f'clip_{clip_count}.avi')

        out = cv2.VideoWriter(output_file, fourcc, fps, (frame.shape[1], frame.shape[0]))

        # For the first clip, just save normally
        if clip_count == 1:
            for buffered_frame in buffer_frames:
                out.write(buffered_frame)

        # For subsequent clips, prepend the first 2 seconds of the first clip
        else:
            for initial_frame in initial_frames:
                out.write(initial_frame)
            for buffered_frame in buffer_frames:
                out.write(buffered_frame)

        out.release()

        # Reset for the next clip
        buffer_frames = []
        frame_count = 0

    # Display the live feed (optional)
    cv2.imshow('Live Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
