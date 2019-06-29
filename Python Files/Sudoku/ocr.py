# Credits to https://github.com/apollojain/sudoku_solver

from pytesseract import image_to_string
import cv2
import numpy as np
from scipy.misc import imsave

def rectify(h):
    '''
    DESCRIPTION
    -----------
    This function basically takes your numpy array and
    finds your corners for the actual sudoku puzzle.
    INPUT PARAMETERS
    ----------------
    h: np.array
        This is the original numpy array that you are finding
        the corner coordinates to.
    OUTPUT PARAMETERS
    -----------------
    hnew: np.array
        This contains the four corners of np.array
    '''
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

def pre_processing(image):
    '''
    DESCRIPTION
    -----------
    This function basically preprocesses the image so that
    a gray threshold is applied to it to make all of the borders
    and numbers are significantly clearer
    INPUT PARAMETERS
    ----------------
    image: PIL.image
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    return gray, thresh

def find_puzzle(image):
    '''
    DESCRIPTION
    -----------
    This function finds the general area where your sudoku puzzle
    is located and then returns a new images that eliminates
    all of the noise in your old image and only has the portion that
    you want.
    INPUT PARAMETERS
    ----------------
    image: PIL.image

    OUTPUT PARAMETERS
    -----------------
    warp: np.array
        This contains the numpy array that represents your return
        image, which is only the section of the original image that
        contains your sudoku puzzle.
    '''
    gray, thresh = pre_processing(image)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    biggest = None
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 100:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            if area > max_area and len(approx == 4):
                biggest = approx
                max_area = area

    if biggest is not None:
        biggest = rectify(biggest)
        h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)
        retval = cv2.getPerspectiveTransform(biggest, h)
        warp = cv2.warpPerspective(gray, retval, (450, 450))
        return warp
    return None

def split_sudoku_cells(image) -> dict:
    '''
    DESCRIPTION
    -----------
    This function takes in an image, finds your puzzle, and then
    splits the image into 81 numpy arrays, each if which represents
    cell (i, j) of your sudoku puzzle.
    INPUT PARAMETERS
    ----------------
    image: PIL.image

    OUTPUT PARAMETERS
    -----------------
    dictionary: dictionary
        Each entry (i, j) includes a numpy array that represents the image
        that corresponds to sudoku cell (i, j)
    '''
    dictionary = {}
    warp = find_puzzle(image)
    if warp is not None:
        array = np.split(warp, 9)
        dictionary = {
            (i + 1, j + 1) : np.array([np.split(arr, 9)[j] for arr in array[i]])
            for i in range(9) for j in range(9)
        }
    return dictionary

def image_to_matrix(image, intermediatesPath) -> dict:
    '''
    DESCRIPTION
    -----------
    This takes in your image name and then processes it
    using the ocr_image function. Subsequently, it places
    it in a 2d array to be returned.
    INPUT PARAMETERS
    ----------------
    image: string
        The path + name of your image, including extensions

    OUTPUT PARAMETERS
    -----------------
    matrix: dict
        The sudoku puzzle in a dict form with a tuple as key, an int as value
        key:   a tuple (i, j) with i, j ranging from 1 to 9
        value: if empty then 0 otherwise the number
    '''
    d = split_sudoku_cells(cv2.imread(image))
    matrix = {}
    for i, j in d:
        path = f'{intermediatesPath}/{i}{j}.png'
        imsave(path, d[i, j])
        img = cv2.imread(path)
        p_img = pre_processing(img)[1]
        imsave(path, p_img)
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = (255 - img)
        string = image_to_string(img)
        # print(i, j, string)
        matrix[i, j] = int(string) if string.isnumeric() else 0
    return matrix