import cv2
import time

def track_object(cap):
    tracker = cv2.TrackerCSRT_create()
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from source.")
        return

    bbox = cv2.selectROI("Select Object", frame, False)
    tracker.init(frame, bbox)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        else:
            cv2.putText(frame, "Lost", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.imshow("Object Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_tracker_video(video_path):
    cap = cv2.VideoCapture(video_path)
    track_object(cap)

def run_tracker_live():
    cap = cv2.VideoCapture(0)
    track_object(cap)
