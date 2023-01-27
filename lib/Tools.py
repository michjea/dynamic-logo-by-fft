__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

import cv2
import numpy as np


class Tools:
    """_summary_

    Methods:
    """
    @staticmethod
    def dft_shift(img_grey):
        """_summary_

        Args:
            img_grey (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Fourier transform
        dft = cv2.dft(np.float32(img_grey), flags=cv2.DFT_COMPLEX_OUTPUT)
        # Reorganization of the quadrants
        dft_shift = np.fft.fftshift(dft)
        print("Send dft_shift")
        return dft_shift

    @staticmethod
    def dft_shift_color(img_color):
        """_summary_

        Args:
            img_color (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Split image into three channels
        b, g, r = cv2.split(img_color)
        # Get dft for each channel
        dft_shift_b = Tools.dft_shift(b)
        dft_shift_g = Tools.dft_shift(g)
        dft_shift_r = Tools.dft_shift(r)
        # Return dfts
        return dft_shift_b, dft_shift_g, dft_shift_r

    @staticmethod
    def get_mag_and_phase(img_grey):
        """_summary_

        Args:
            img_grey (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Get dft shift
        dft_shift = dft_shift(img_grey)
        # Extract magnitude and phase
        magnitude, phase = cv2.cartToPolar(
            dft_shift[:, :, 0], dft_shift[:, :, 1])
        # Return magnitude and phase
        return magnitude, phase

    @staticmethod
    def get_mag_and_phase_color(img_color):
        """_summary_

        Args:
            img_color (_type_): _description_

        Returns:
            _type_: _description_
        """
       # separate to three channels
        b, g, r = cv2.split(img_color)

        # Fourier transform of each channel
        dft_b = cv2.dft(np.float32(b), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_g = cv2.dft(np.float32(g), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_r = cv2.dft(np.float32(r), flags=cv2.DFT_COMPLEX_OUTPUT)

        # shift zero-frequency component to center of spectrum
        dft_shift_b = np.fft.fftshift(dft_b)
        dft_shift_g = np.fft.fftshift(dft_g)
        dft_shift_r = np.fft.fftshift(dft_r)

        # extract magnitude and phase
        magnitude_b, phase_b = cv2.cartToPolar(
            dft_shift_b[:, :, 0], dft_shift_b[:, :, 1])
        magnitude_g, phase_g = cv2.cartToPolar(
            dft_shift_g[:, :, 0], dft_shift_g[:, :, 1])
        magnitude_r, phase_r = cv2.cartToPolar(
            dft_shift_r[:, :, 0], dft_shift_r[:, :, 1])

        return magnitude_b, magnitude_g, magnitude_r, phase_b, phase_g, phase_r

    @staticmethod
    def get_img_back(fshift):
        """_summary_

        Args:
            fshift (_type_): _description_

        Returns:
            _type_: _description_
        """
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
        #print("Send img_back")
        return img_back

    @staticmethod
    def get_img_back_phase(phase, magnitude):
        """_summary_

        Args:
            phase (_type_): _description_
            magnitude (_type_): _description_

        Returns:
            _type_: _description_
        """
        real, imaginary = cv2.polarToCart(phase, magnitude)
        fshift = cv2.merge([real, imaginary])
        img_back = Tools.get_img_back(fshift)
        img_back = cv2.normalize(
            img_back, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        return img_back

    @staticmethod
    def get_img_back_phase_bgr(p_b, p_g, p_r, m_b, m_g, m_r):
        """_summary_

        Args:
            p_r (_type_): _description_
            p_g (_type_): _description_
            p_b (_type_): _description_
            m_r (_type_): _description_
            m_g (_type_): _description_
            m_b (_type_): _description_

        Returns:
            _type_: _description_
        """
        # inverse Fourier transform
        real_b, imaginary_b = cv2.polarToCart(m_b, p_b)
        back_b = cv2.merge([real_b, imaginary_b])
        back_dft_b = np.fft.ifftshift(back_b)
        img_back_b = cv2.idft(back_dft_b)
        img_back_b = cv2.magnitude(img_back_b[:, :, 0], img_back_b[:, :, 1])
        img_back_b = cv2.normalize(
            img_back_b, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        real_g, imaginary_g = cv2.polarToCart(m_g, p_g)
        back_g = cv2.merge([real_g, imaginary_g])
        back_dft_g = np.fft.ifftshift(back_g)
        img_back_g = cv2.idft(back_dft_g)
        img_back_g = cv2.magnitude(img_back_g[:, :, 0], img_back_g[:, :, 1])
        img_back_g = cv2.normalize(
            img_back_g, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        real_r, imaginary_r = cv2.polarToCart(m_r, p_r)
        back_r = cv2.merge([real_r, imaginary_r])
        back_dft_r = np.fft.ifftshift(back_r)
        img_back_r = cv2.idft(back_dft_r)
        img_back_r = cv2.magnitude(img_back_r[:, :, 0], img_back_r[:, :, 1])
        img_back_r = cv2.normalize(
            img_back_r, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        # merge three channels
        img_back = cv2.merge((img_back_b, img_back_g, img_back_r))

        return img_back

    @staticmethod
    def get_magnitude(dft_shift):
        """_summary_

        Args:
            dft_shift (_type_): _description_

        Returns:
            _type_: _description_
        """
        magnitude = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
        magnitude_spectrum = np.log(magnitude+1)
        return magnitude_spectrum

    @staticmethod
    def add_noise_to_phase(phase, mu, sigma):
        """_summary_

        Args:
            phase (_type_): _description_
            mu (_type_): _description_
            sigma (_type_): _description_

        Returns:
            _type_: _description_
        """
        noise = np.random.normal(mu, sigma, phase.shape)
        phase_ = phase + noise
        phase_[phase_ > 2*np.pi] = 2*np.pi
        # if values are smaller than 0, set them to 0
        phase_[phase_ < 0] = 0
        # convert to float32
        phase_ = phase_.astype(np.float32)
        return phase_
