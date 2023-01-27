__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.Color import *
from lib.Tools import *
import numpy as np
import matplotlib.pyplot as plt
#import parameters as p
import random


class ColorBGR(Color):
    """This is the ColorBGR class. It is a subclass of the class Color.
    This class takes an image and applies a mask to it. It also returns the magnitude of the image of the last applied mask.

    Args:
        json_parser (JsonParser): This is the JsonParser object that contains the parameters for the noise.
        magnitude_b, magnitude_g, magnitude_r, phase_b, phase_g, phase_r (numpy.ndarray): These are the magnitude and phase of the image.
        last_mag (numpy.ndarray): This is the magnitude of the last applied mask.
        last_phase_b, last_phase_g, last_phase_r (numpy.ndarray): These are the phase of the last applied mask.
        last_mask (numpy.ndarray): This is the last applied mask.
        mu_b, mu_g, mu_r (float): These are the mean of the noise.
        sigma_b, sigma_g, sigma_r (float): These are the standard deviation of the noise.

    Methods:
        apply_mask(mask, keep_last=False): This method takes a mask and applies it to the image.
        get_magnitude(): This method returns the magnitude of the image of the last applied mask.
        set_parameters(): This method sets the parameters for the noise.
    """
    json_parser = None

    magnitude_b = None
    magnitude_g = None
    magnitude_r = None

    phase_b = None
    phase_g = None
    phase_r = None

    last_mag = None

    last_phase_b = None
    last_phase_g = None
    last_phase_r = None

    last_mask = None

    mu_b = None
    mu_g = None
    mu_r = None

    sigma_b = None
    sigma_g = None
    sigma_r = None

    def __init__(self, img_color, json_parser):
        self.magnitude_b, self.magnitude_g, self.magnitude_r, self.phase_b, self.phase_g, self.phase_r = Tools.get_mag_and_phase_color(
            img_color)

        self.json_parser = json_parser

        self.last_phase_b = self.phase_b
        self.last_phase_g = self.phase_g
        self.last_phase_r = self.phase_r

        self.set_parameters()

    def get_magnitude(self):
        return self.last_mask

    def apply_mask(self, mask, keep_last=False):
        """Apply a mask to the color instance

        Args:
            mask (numpy array): The mask to apply to the image. Must be a numpy array of the same size as the image.
            keep_last (bool, optional): Whether to keep the last phase or add noise to it. Defaults to False.

        Returns:
            numpy array: The image with the mask applied.
        """

        self.last_mask = mask

        m_b = self.magnitude_b * mask
        m_g = self.magnitude_g * mask
        m_r = self.magnitude_r * mask

        mu_b = np.random.uniform(self.mu_b[0], self.mu_b[1])
        mu_g = np.random.uniform(self.mu_g[0], self.mu_g[1])
        mu_r = np.random.uniform(self.mu_r[0], self.mu_r[1])

        s_b = np.random.uniform(self.sigma_b[0], self.sigma_b[1])
        s_g = np.random.uniform(self.sigma_g[0], self.sigma_g[1])
        s_r = np.random.uniform(self.sigma_r[0], self.sigma_r[1])

        p_b = Tools.add_noise_to_phase(self.phase_b, mu_b, s_b)
        p_g = Tools.add_noise_to_phase(self.phase_g, mu_g, s_g)
        p_r = Tools.add_noise_to_phase(self.phase_r, mu_r, s_r)

        if keep_last:
            p_b = self.last_phase_b
            p_g = self.last_phase_g
            p_r = self.last_phase_r
        else:
            self.last_phase_b = p_b
            self.last_phase_g = p_g
            self.last_phase_r = p_r

        self.last_mag = m_b

        img_back = Tools.get_img_back_phase_bgr(p_b, p_g, p_r, m_b, m_g, m_r)

        return img_back

    def set_parameters(self):
        """This function sets the parameters of the noise filter by retrieving them from the json file using the json_parser.
        It checks if the retreived parameters are tuples of int or float and assigns them to the corresponding attributes of the noise filter object. If the retrieved parameters are not tuples of int or flaot, it raises a TypeError.

        Raises:
            TypeError: mu_b_channel must be a tuple of int or float.
            TypeError: mu_g_channel must be a tuple of int or float.
            TypeError: mu_r_channel must be a tuple of int or float
            TypeError: sigma_b_channel must be a tuple of int or float.
            TypeError: sigma_g_channel must be a tuple of int or float.
            TypeError: sigma_r_channel must be a tuple of int or float.
        """
        params = self.json_parser.get_parameter("noise")

        if not all(isinstance(item, (int, float)) for item in params['mu_b_channel']):
            raise TypeError("mu_b_channel must be a tuple of int or float")
        self.mu_b = tuple(params['mu_b_channel'])

        if not all(isinstance(item, (int, float)) for item in params['mu_g_channel']):
            raise TypeError("mu_g_channel must be a tuple of int or float")
        self.mu_g = tuple(params['mu_g_channel'])

        if not all(isinstance(item, (int, float)) for item in params['mu_r_channel']):
            raise TypeError("mu_r_channel must be a tuple of int or float")
        self.mu_r = tuple(params['mu_r_channel'])

        if not all(isinstance(item, (int, float)) for item in params['sigma_b_channel']):
            raise TypeError("sigma_b_channel must be a tuple of int or float")
        self.sigma_b = tuple(params['sigma_b_channel'])

        if not all(isinstance(item, (int, float)) for item in params['sigma_g_channel']):
            raise TypeError("sigma_g_channel must be a tuple of int or float")
        self.sigma_g = tuple(params['sigma_g_channel'])

        if not all(isinstance(item, (int, float)) for item in params['sigma_r_channel']):
            raise TypeError("sigma_r_channel must be a tuple of int or float")
        self.sigma_r = tuple(params['sigma_r_channel'])
