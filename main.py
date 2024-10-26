from skeleton_detection import SkeletonDetector
from sound_trigger import SoundTrigger
from movement_detector import MovementDetector
import cv2

def main():
    cap = cv2.VideoCapture(2) 
    detector = SkeletonDetector()
    sound_trigger = SoundTrigger()
    movement_detector = MovementDetector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

       
        frame = cv2.flip(frame, 1)

        landmarks = detector.detect_skeleton(frame)
        if landmarks:
            movement = movement_detector.detect_movement(landmarks)
            if movement:
                sound_trigger.play_sound(movement)

        cv2.imshow('Air Drum', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
