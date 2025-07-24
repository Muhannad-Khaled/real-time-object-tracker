# # import cv2

# # # فتح الفيديو
# # cap = cv2.VideoCapture("video.mp4")

# # # تصفح أول 100 فريم للبحث عن مشهد مناسب
# # frame = None
# # for i in range(100):
# #     ret, frame = cap.read()
# #     if not ret:
# #         print("لم يتم تحميل فريم من الفيديو.")
# #         cap.release()
# #         exit()

# #     # عرض الفريم
# #     cv2.imshow("تصفح الفيديو - اضغط S لاختيار الجسم", frame)
# #     # لو المستخدم ضغط "s" نوقف التصفح ونبدأ اختيار الجسم
# #     key = cv2.waitKey(50) & 0xFF
# #     if key == ord("s"):
# #         break

# # cv2.destroyAllWindows()

# # # تأكد أن في فريم صالح
# # if frame is None:
# #     print("لا يوجد فريم صالح.")
# #     cap.release()
# #     exit()

# # # اختيار الجسم من الفريم الحالي
# # bbox = cv2.selectROI("اختر الجسم المراد تتبعه", frame, fromCenter=False, showCrosshair=True)
# # cv2.destroyWindow("اختر الجسم المراد تتبعه")

# # # إنشاء المتتبع (CSRT = دقة عالية)
# # tracker = cv2.TrackerCSRT_create()

# # # تهيئة المتتبع بالفريم المختار والبـوكس
# # tracker.init(frame, bbox)

# # # تتبع الجسم في باقي الفيديو
# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break

# #     success, bbox = tracker.update(frame)

# #     if success:
# #         x, y, w, h = [int(v) for v in bbox]
# #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
# #         cv2.putText(frame, "Tracking", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
# #     else:
# #         cv2.putText(frame, "Lost", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# #     cv2.imshow("Object Tracker", frame)
# #     key = cv2.waitKey(30) & 0xFF
# #     if key == 27:  # Esc
# #         break

# # cap.release()
# # cv2.destroyAllWindows()


# import cv2

# def run_tracker(video_path):
#     cap = cv2.VideoCapture(video_path)

#     frame = None
#     for _ in range(100):
#         ret, frame = cap.read()
#         if not ret:
#             break
#         cv2.imshow("Preview - Press 's' to select object", frame)
#         if cv2.waitKey(40) & 0xFF == ord('s'):
#             break

#     cv2.destroyAllWindows()

#     if frame is None:
#         return

#     bbox = cv2.selectROI("Select object", frame, fromCenter=False, showCrosshair=True)
#     cv2.destroyWindow("Select object")

#     tracker = cv2.TrackerCSRT_create()
#     tracker.init(frame, bbox)

#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter("output_tracked.mp4", fourcc, fps, (width, height))

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         ok, bbox = tracker.update(frame)

#         if ok:
#             x, y, w, h = [int(v) for v in bbox]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(frame, "Tracking", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame, "Lost", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

#         out.write(frame)
#         cv2.imshow("Tracking", frame)
#         if cv2.waitKey(30) & 0xFF == 27:
#             break

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

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
