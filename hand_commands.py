import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Para imágenes estáticas:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.flip(cv2.imread(file), 1)
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        print('Handedness:', results.multi_handedness)
        if not results.multi_hand_landmarks:
            continue
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            print('hand_landmarks:', hand_landmarks)
            print(
                f'Index finger tip coordinates: (',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
            )
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        
            # Detectar gestos específicos
            extended_fingers = [l.x > hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x for l in hand_landmarks.landmark]
            if extended_fingers[mp_hands.HandLandmark.INDEX_FINGER_TIP] and extended_fingers[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] and not any(extended_fingers[1:]):
                print("Se detectó el gesto de paz")
                # Realizar acciones correspondientes al gesto de paz

            if extended_fingers[mp_hands.HandLandmark.THUMB_TIP] and not any(extended_fingers[1:]):
                print("Se detectó el gesto de mano")
                # Realizar acciones correspondientes al gesto de mano

            if extended_fingers[mp_hands.HandLandmark.PINKY_TIP] and not any(extended_fingers[:4]):
                print("Se detectó el gesto de losser")
                # Realizar acciones correspondientes al gesto de losser

        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

# Para la entrada de la cámara web:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        
                extended_fingers = [l.x > hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x for l in hand_landmarks.landmark]
                if extended_fingers[mp_hands.HandLandmark.THUMB_TIP] and extended_fingers[mp_hands.HandLandmark.INDEX_FINGER_TIP] and extended_fingers[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] and extended_fingers[mp_hands.HandLandmark.RING_FINGER_TIP] and extended_fingers[mp_hands.HandLandmark.PINKY_TIP]:
                    print("Se detectó el gesto de mano")
                  

                if not extended_fingers[mp_hands.HandLandmark.INDEX_FINGER_TIP] and not extended_fingers[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] and not extended_fingers[mp_hands.HandLandmark.RING_FINGER_TIP] and not extended_fingers[mp_hands.HandLandmark.PINKY_TIP]:
                    print("Se detectó el signo de rock")
                  


                if extended_fingers[mp_hands.HandLandmark.PINKY_TIP] and not any(extended_fingers[:4]):
                    print("Se detectó el gesto de losser")

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()

