#%%
from pytesseract import image_to_string
from PIL import Image
import cv2
import numpy as np
from scipy.misc import imsave
import matplotlib.pyplot as plt
import os
from skimage import morphology,draw
from skimage import io, data, color
from skimage import measure

#%%
path = f'intermediates/71.png'
img = cv2.imread(path)

#%%
row,col = img.shape[:2]
mmap = np.zeros([row,col])
#因为图像是三维的所以在这块取第一维
for i in range(row):
    for j in range(col):
        mmap[i,j] = img[i,j,0]
mmap = (mmap < 0.5) * 1  #图像二值化
img2 = morphology.skeletonize(mmap) #图像的二值化骨架提取
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
ax1.imshow(img, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('img', fontsize=20)
ax2.imshow(img2, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('img2', fontsize=20)
fig.tight_layout()
plt.show()

#%%
