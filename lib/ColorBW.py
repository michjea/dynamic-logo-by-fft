__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.Color import *
from lib.Tools import *
import matplotlib.pyplot as plt
import cv2
import numpy as np


class ColorBW(Color):
    """The ColorBW class is a child class of the Color class that is used to apply a mask to a black and white image using the Discrete Fourier Transform (DFT) shift.

    Attributes:
        dft_shift (numpy ndarray): DFT shift of the image.
        last_fshift (numpy ndarray): Last DFT shift of the image with mask applied.

    Methods:
        get_magnitude(): This method returns the magnitude of the image of the last applied mask.
        apply_mask(mask, keep_last=False): This method takes a mask and applies it to the image using the DFT shift.
    """

    dft_shift = None
    last_fshift = None

    def __init__(self, img_bw):
        self.dft_shift = Tools.dft_shift(img_bw)

    def get_magnitude(self):
        magnitude = Tools.get_magnitude(self.last_fshift)
        return magnitude

    def apply_mask(self, mask, keep_last=False):
        """This method takes a mask and applies it to the image using the DFT shift.

        Args:
            mask (numpy ndarray): Mask to apply to the image.
            keep_last (bool, optional): Default to false.

        Returns:
            numpy ndarray: Image with the mask applied.
        """

        mask2 = np.zeros((mask.shape[0], mask.shape[1], 2), np.float32)
        mask2[:, :, 0] = mask
        mask2[:, :, 1] = mask

        fshift = self.dft_shift * mask2

        img_back = Tools.get_img_back(fshift)
        self.last_fshift = fshift

        return img_back
