from license_plate_recognition import PossibleChar
from license_plate_recognition import DetectChars
from license_plate_recognition import Preprocess
from license_plate_recognition import Plate
import numpy as np
import cv2
import os

kNearest = cv2.ml.KNearest_create()

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

def loadKNNDataAndTrainKNN():
    allContoursWithData = []
    validContoursWithData = []
    training_classification = "license_plate_recognition/classifications.txt"
    training_images = "license_plate_recognition/flattened_images.txt"

    try:
        npaClassifications = np.loadtxt(training_classification, np.float32)                  
    except:
        print("[ERROR] Unable to open classifications.txt, exiting program\n")
        os.system("pause")
        return False

    try:
        npaFlattenedImages = np.loadtxt(training_images, np.float32)
    except:
        print("[ERROR] Unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
        return False

    # reshape numpy array to 1d, necessary to pass to call to train
    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
    # set default K to 1
    kNearest.setDefaultK(1)
    # train KNN object
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    # if we got here training was successful so return true
    return True

def detectCharsInPlates(licPlate):
    # preprocess to get grayscale and threshold images
    licPlate.imgGrayscale, licPlate.imgThresh = Preprocess.preprocess(licPlate.imgPlate)     
    licPlate.imgThresh = cv2.resize(licPlate.imgThresh, (0, 0), fx = 1.3, fy = 1.3)
    thresholdValue, licPlate.imgThresh = cv2.threshold(licPlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    listOfPossibleCharsInPlate = findPossibleCharsInPlate(licPlate.imgGrayscale, licPlate.imgThresh)

    listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)
    # within each list of matching chars
    for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
        # sort chars from left to right
        listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)
        # and remove inner overlapping chars
        listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i])
        
        # within each possible plate, suppose the longest list of potential matching chars is the actual list of chars
        intLenOfLongestListOfChars = 10
        intLenOfShortestListOfChars = 4

        if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfShortestListOfChars and intLenOfLongestListOfChars > len(listOfListsOfMatchingCharsInPlate[i]):
            listOfListsOfMatchingCharsInPlate[i] = listOfListsOfMatchingCharsInPlate[i]

        licPlate.strChars = recognizeCharsInPlate(licPlate.imgThresh, listOfListsOfMatchingCharsInPlate[i])
        if len(listOfListsOfMatchingCharsInPlate)>1 :
            licPlate.strChars = recognizeCharsInPlate(licPlate.imgThresh, listOfListsOfMatchingCharsInPlate[1]) +" "+ recognizeCharsInPlate(licPlate.imgThresh, listOfListsOfMatchingCharsInPlate[0])
    return licPlate

def findPossibleCharsInPlate(imgGrayscale, imgThresh):
    listOfPossibleChars = []
    imgThreshCopy = imgThresh.copy()

    # find all contours in plate
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        possibleChar = PossibleChar.PossibleChar(contour)
        # if contour is a possible char, note this does not compare to other chars (yet) . . .
        if DetectChars.checkIfPossibleChar(possibleChar):
            # add to list of possible chars            
            listOfPossibleChars.append(possibleChar)       

    return listOfPossibleChars

def findListOfListsOfMatchingChars(listOfPossibleChars):
    # with this function, we start off with all the possible chars in 
    # one big list the purpose of this function is to re-arrange the one 
    # big list of chars into a list of lists of matching chars, note that 
    # chars that are not found to be in a group of matches do not need to be 
    # considered further
    listOfListsOfMatchingChars = []

    # for each possible char in the one big list of chars
    for possibleChar in listOfPossibleChars:                        
        # find all chars in the big list that match the current char
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        
        # also add the current char to current possible list of matching chars
        listOfMatchingChars.append(possibleChar)                

        # if current possible list of matching chars is not long enough to 
        # constitute a possible plate jump back to the top of the for loop and 
        # try again with next char, note that it's not necessary to save 
        # the list in any way since it did not have enough chars to be 
        # a possible plate if we get here, the current list passed test as a 
        # "group" or "cluster" of matching chars
        if len(listOfMatchingChars) < 4:     
            continue
        # so add to our list of lists of matching chars
        listOfListsOfMatchingChars.append(listOfMatchingChars)

        # remove the current list of matching chars from the big list so 
        # we don't use those same chars twice, make sure to make a 
        # new big list for this since we don't want to change the original big list
        listOfPossibleCharsWithCurrentMatchesRemoved = []
                                                                                        
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))
        # recursive call
        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)

        # for each list of matching chars found by recursive call   
        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:
            # add to our original list of lists of matching chars
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             

        break

    return listOfListsOfMatchingChars

def findListOfMatchingChars(possibleChar, listOfChars):
    # the purpose of this function is, given a possible char and a big 
    # list of possible chars, find all chars in the big list that are a match 
    # for the single possible char, and return those matching chars as a list

    listOfMatchingChars = []
     # for each char in big list
    for possibleMatchingChar in listOfChars:
        # if the char we attempting to find matches for is the exact same char
        # as the char in the big list we are currently checking then we should 
        # not include it in the list of matches b/c that would end up double 
        # including the current char so do not add to list of matches and 
        # jump back to top of for loop          
        if possibleMatchingChar == possibleChar:    
            continue
        
        # compute stuff to see if chars are a match
        fltDistanceBetweenChars = DetectChars.distanceBetweenChars(possibleChar, possibleMatchingChar)
        fltAngleBetweenChars = DetectChars.angleBetweenChars(possibleChar, possibleMatchingChar)
        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)
        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

        # check if chars match
        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):

            # if the chars are a match, add the current char to list of matching chars
            listOfMatchingChars.append(possibleMatchingChar)
    return listOfMatchingChars

# if we have two chars overlapping or to close to each other to possibly be 
# separate chars, remove the inner (smaller) char, this is to prevent including 
# the same char twice if two contours are found for the same char, for example 
# for the letter 'O' both the inner ring and the outer ring may be found as contours, 
# but we should only include the char once
def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)

    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            # if current char and other char are not the same char
            if currentChar != otherChar:
                # if current char and other char have center points at almost the same location . . .
                if DetectChars.distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                    # if we get in here we have found overlapping chars next 
                    # we identify which char is smaller, then if that char was 
                    # not already removed on a previous pass, remove it

                    # if current char is smaller than other char
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:     
                        # if current char was not already removed on a previous pass . . .    
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:              
                            # then remove current char
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)

                    # else if other char is smaller than current char
                    else:
                        # if other char was not already removed on a previous pass . . .
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:
                            # then remove other char
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)

    return listOfMatchingCharsWithInnerCharRemoved

# this is where we apply the actual char recognition
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    # the chars in the lic plate
    strChars = ""
    height, width = imgThresh.shape
    imgThreshColor = np.zeros((height, width, 3), np.uint8)

    # sort chars from left to right
    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)
    # make color version of threshold image so we can draw contours in color on it
    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)

    # for each char in plate
    for currentChar in listOfMatchingChars:
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

        # crop char out of threshold image
        imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight, 
            currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        # resize image, this is necessary for char recognition
        imgROIResized = cv2.resize(imgROI, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))
        # flatten image into 1d numpy array
        npaROIResized = imgROIResized.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))        
        # convert from 1d numpy array of ints to 1d numpy array of floats
        npaROIResized = np.float32(npaROIResized)               
        # finally we can call findNearest !!!
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)       
        # get character from results 
        strCurrentChar = str(chr(int(npaResults[0][0])))            
        # append current char to full string
        strChars = strChars + strCurrentChar
    return strChars