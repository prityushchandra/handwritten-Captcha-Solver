import os
import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt

border_size = 5

class Roi:
    def __init__(self, roi, x, y, w, h):
        self.roi = roi
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def process_image(image):
    th = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 125, 20)
    blurred = cv2.medianBlur(th, 7)
    inverted = cv2.bitwise_not(blurred)
    eroded = cv2.erode(inverted, np.ones((1, 1), np.uint8))
    dilated = cv2.dilate(eroded, np.ones((2, 2), np.uint8))
    # cv2.imwrite('denoised.jpg', dilated)
    # plt.imshow(dilated, 'gray')
    return th


def load_model(model_name):
    return keras.models.load_model('models/' + model_name)


def get_labels(file_name):
    with open('labels/' + file_name, 'r') as mapping:
        lines = mapping.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')

    return lines


def get_model_and_mapping():
    return {

        1: (load_model('mymodel'), get_labels('all_characters.txt'))
    }


def add_border(img):
    h, w = img.shape
    pad_h, pad_w = 0, 0
    if w > h:
        pad_h = int((w - h) / 2)
    else:
        pad_w = int((h - w) / 2)
    padded_img = cv2.copyMakeBorder(img, top=pad_h, bottom=pad_h, left=pad_w, right=pad_w,
                                    borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return padded_img


def predict_character(classifier, labels, image, text, position, choice):
    image = cv2.dilate(image, kernel=np.ones((2, 2), np.uint8), iterations=1)
    text_1 = list()
    X_list = list()
    pred_list = list()
    # cv2.imshow('Predicting Image', image)
    # cv2.waitKey(0)
    X = image.reshape(1, 784)
    X = X / 255
    X = X.reshape(X.shape[0], int(X.shape[1] ** 0.5), int(X.shape[1] ** 0.5))
    X = X[..., np.newaxis]
    pred_list.append(X)
    pred = classifier.predict(X)
    # print(pred.shape)
    largest = pred.argmax()
    nbr = labels[largest]
    nbr_1 = labels[np.delete(pred, largest).argmax()]
    nbr = nbr.split(' ')
    nbr_1 = nbr_1.split(' ')
    if (choice == 3 and position > 0 and chr(int(nbr[1])).isupper()):
        text.append(chr(int(nbr[1]) + 32))
    else:
        text.append(chr(int(nbr[1])))
    text_1.append(chr(int(nbr_1[1])))
    # for i, p in enumerate(pred.reshape(-1, 1)):
        # print("Predicted: %c with %f" % (chr(int(labels[i].split(' ')[1])), p))
    X_list.append(X)
    return text


def segment(image, isPara):
    orig_image = image

    im2, ctrs, hier = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort contours
    if isPara:
        sorted_ctrs = sorted(ctrs, key=lambda ctr: (cv2.boundingRect(ctr)[1], cv2.boundingRect(ctr)[0]))
    else:
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    roi_list = list()

    roi_objects = []

    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = orig_image[y:y + h, x:x + w]
        # show ROI
        roi_list.append(roi)
        roi_objects.append(Roi(roi, x , y, w, h))
        # cv2.imshow('segment no:'+str(i), roi)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.waitKey(0)

    # cv2.imshow('marked areas', image)
    # cv2.waitKey(0)
    # print('Recognized' + text)
    return roi_list, roi_objects


def recognize_image(imagepath, choice=1):
    (classifier, labels) = get_model_and_mapping()[choice]

    image = 255-cv2.imread(imagepath,0)


    segmented_lines, lines_objects = segment(image, False)

    text = list()

    for line in range(len(lines_objects)):

        distances = []

        _, words_obj = segment(lines_objects[line].roi, True)

        for i in range(len(words_obj)-1):
            distances.append(words_obj[i+1].x-(words_obj[i].x+words_obj[i].w))

        minimum = maximum = 0

        try:
            minimum = np.min(distances)
            maximum = np.max(distances)
        except ValueError:
            pass

        for i in range(len(words_obj)):
            padded_img = add_border(words_obj[i].roi)
            # cv2.imshow('Bordered Image', padded_img)
            # cv2.waitKey(0)
            # padded_img = cv2.cvtColor(padded_img, cv2.COLOR_BGR2GRAY)
            padded_img = cv2.resize(padded_img, (28 - (border_size * 2), 28 - (border_size * 2)),
                                    interpolation=cv2.INTER_AREA)
            padded_img = cv2.copyMakeBorder(padded_img, border_size, border_size, border_size, border_size,
                                            cv2.BORDER_CONSTANT, value=[0, 0, 0])
            padded_img[padded_img>50] = 255;
            text = predict_character(classifier, labels, padded_img, text, i, choice)
            # print(text)

            # print(distances)

            if minimum >= maximum/2:
                continue



    return ''.join(text)


def final_pred(imagepath):
    # final_process(image)
    text = recognize_image(imagepath)
    text=text.replace('q','g')
    # text=text.replace('g','9')
    text=text.replace('O','0')


    return text

# for i in os.listdir('image'):
#     if i!='.DS_Store':
#         # img=cv2.imread('image/'+str(i))
#         text = final_pred('image/'+str(i))
#
#         print text
