from license_plate_recognition import DetectPlates
from license_plate_recognition import NumberPlate
from license_plate_recognition import DetectChars
from imutils.video import FPS
import datetime
import draft
import time
import cv2
import os
import numpy as np

MIN_NUMBER_OF_CHARS = 7
path = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(path, '/ToAPI/img_XE/')

def run(imgOriginalScene):
    blnKNNTrainingSuccessful = NumberPlate.loadKNNDataAndTrainKNN()  # attempt KNN training
    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

    count_img = 0
    if len(listOfPossiblePlates) != 0:
        # if we get in here list of possible plates has at leat one plate
        # sort the list of possible plates in DESCENDING order
        # (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key=lambda possiblePlate: 
            len(possiblePlate.strChars), reverse=True)

        # suppose the plate has the most recognized chars 
        # (the first plate in sorted by string length descending order) 
        # is the actual plate up size and show actual plate
        licPlate = listOfPossiblePlates[0]

        # get the finally Chars
        NumberPlate.detectCharsInPlates(licPlate)
        strPlate = licPlate.strChars
        
        # min license plate text
        if len(strPlate) <  MIN_NUMBER_OF_CHARS:
            pass
        else:
            temp = datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S")
            dt = temp.split('-')
            # cv2.putText(licPlate.imgPlate,'license plate number = ' + licPlate.strChars, 
            #                                 bottomLeftCornerOfText, 
            #                                 font, 
            #                                 fontScale,
            #                                 fontColor,
            #                                 lineType)
            print('license plate number = ' + licPlate.strChars)
            cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate

            img_name = "".join(dt) + "_" + str(count_img) +".jpg"
            img_dir1 = "ToAPI/imgXE/" + img_name
            cv2.imwrite(img_dir1, licPlate.imgPlate)
            count_img += 1
            result = draft.uploadCar_VToAPI(img_name,strPlate)