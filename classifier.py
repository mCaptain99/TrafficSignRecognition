
import keras
import numpy as np
from utils import *
import cv2


reconstructed_model = keras.models.load_model("road_sign_model")
sizex, sizey = 500, 300


def process_image(image):
    blur_img = cv2.GaussianBlur(image, (3, 3), sigmaX=0, sigmaY=0)
    edges_img = cv2.Canny(image=blur_img, threshold1=250, threshold2=250)

    circles = cv2.HoughCircles(edges_img, cv2.HOUGH_GRADIENT, 1, 500 / 8,
                               param1=200, param2=30,
                               minRadius=10, maxRadius=30)

    predicted_signs = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            w, h = int(2.5 * radius), (2.5 * radius)
            x0, y0 = max(0, min(int(center[0] - w // 2), sizex - 1)), max(0, min(int(center[1] - h // 2), sizey - 1))
            x1, y1 = max(0, min(int(x0 + w), sizex - 1)), max(0, min(int(y0 + h), sizey - 1))
            cropped_image = image[y0:y1, x0:x1]
            img = cv2.resize(cropped_image, (50, 50), interpolation=cv2.INTER_LINEAR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.rectangle(image, (x0, y0), (x1, y1), (0, 0, 0), 2)
            predcition = np.argmax(reconstructed_model.predict(np.array([img]), verbose=False), axis=1)
            #print(f'Predicted sing: {labels[predcition[0]]}')
            predicted_signs.append(labels[predcition[0]])
            cv2.circle(image, center, 1, (255, 100, 100), 3)
            cv2.circle(image, center, radius, (255, 0, 0), 3)
            cv2.putText(image, f'{labels[predcition[0]]}', (x0, y0),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    contours, _ = cv2.findContours(
        edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        if i == 0:
            i = 1
            continue
        approx = cv2.approxPolyDP(
            contour, 0.07 * cv2.arcLength(contour, True), True)

        if len(approx) == 3 and cv2.contourArea(contour) > 100 and check_if_triangle(approx):
            x0, y0, x1, y1 = get_triangle_frame(approx)
            cropped_image = image[y0:y1, x0:x1]
            img = cv2.resize(cropped_image, (50, 50), interpolation=cv2.INTER_LINEAR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            predcition = np.argmax(reconstructed_model.predict(np.array([img]), verbose=False), axis=1)
            #print(f'Predicted sing: {labels[predcition[0]]}')
            predicted_signs.append(labels[predcition[0]])
            cv2.drawContours(image, [contour], 0, (0, 0, 255), 5)
            cv2.putText(image, f'{labels[predcition[0]]}', (x0, y0),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.imshow('img', image)

    return predicted_signs


def read_from_camera(path):
    cap = cv2.VideoCapture(path)
    ret, image = cap.read()
    predicted_signs = {}
    last = ''
    while (True):
        ret, image = cap.read()
        try:
            image = cv2.resize(image, (sizex, sizey))
        except cv2.error:
            return
        predictions = process_image(image)
        keys = []
        for prediction in predictions:
            keys.append(prediction)
            predicted_signs[prediction] = predicted_signs[prediction] + 1 if predicted_signs.get(prediction, None) else 1
        for key in predicted_signs:
            if key not in keys:
                predicted_signs[key] = 0
            elif predicted_signs[key] >= 2:
                if last != key:
                    print(f'Prediction: {key}')
                    last = key
                predicted_signs[key] = 0
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        cv2.imshow('img', image)

    #sleep(1)
    cap.release()
    cv2.destroyAllWindows()

labels = {
     0: '30',
     1: '50',
     2: '70',
     3: 'AccessDenied',
     4: 'Bumper',
     5: 'CloseRoad',
     6: 'LeftSign',
     7: 'OneWayRoad',
     8: 'Parking',
    9: 'PedestrianCrossWalk',
    10: 'RightSign',
    11: 'Roundabout',
    12: 'Stop',
    13: 'Uneven',
    14: 'Yield',
    15: 'other'
}

import sys

read_from_camera(sys.argv[1])
