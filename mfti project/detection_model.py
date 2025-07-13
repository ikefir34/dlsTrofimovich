import ultralytics
from ultralytics import YOLO
import cv2
import os

def img_processing(input_path, output = 'output/out_img.jpg', model_path = 'models/model_3.pt'):
    model = YOLO(model_path)

    if os.path.exists(output): os.remove(output)

    result = model(input_path)

    img_result = result[0].plot()
    cv2.imwrite(output, img_result)


def video_processing(input_path, output= 'output/out_vid.mp4', model_path = 'models/model_3.pt'):
    model = YOLO(model_path)

    if os.path.exists(output): os.remove(output)

    vid = cv2.VideoCapture(input_path)
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vid.get(cv2.CAP_PROP_FPS)
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_vid = cv2.VideoWriter(output, fourcc, fps, (width, height))

    while True:
        ret, frame = vid.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        annotated_frame = results[0].plot()
        out_vid.write(annotated_frame)

    vid.release()
    out_vid.release()
    cv2.destroyAllWindows()

