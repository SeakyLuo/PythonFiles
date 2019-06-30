#%%
from pytesseract import image_to_string
from PIL import Image
import cv2
import numpy as np
from scipy.misc import imsave
import matplotlib.pyplot as plt

#%%
path = f'intermediates/83.png'
img = cv2.imread(path)
kernel = np.ones((5, 5), np.uint8)
img = cv2.dilate(img, kernel, iterations = 1)
cv2.imwrite('after1.jpg', img)
string = image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
print('String: ', string)