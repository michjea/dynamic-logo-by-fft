"""_summary_
"""

__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.Gif import Animation
import random
import numpy as np
import cv2


class EllipseAnimation(Animation):
    """The EllipseAnimation class is a child class of the Animation class and is used to create an animation by drawing ellipses on the frames of an image.

    Attributes:
        x_axis_lengtg (tuple): The minimum and maximum length of the x axis of the ellipse, in percent of the width of the image.
        y_axis_length (tuple): The minimum and maximum length of the y axis of the ellipse, in percent of the height of the image.
        stroke_thickness (tuple): The minimum and maximum thickness of the ellipse.
        x_position (tuple): The minimum and maximum x position of the ellipse, in percent of the width of the image.
        y_position (tuple): The minimum and maximum y position of the ellipse, in percent of the height of the image.
        step (float): The step size of the animation.
        iterations (tuple): The minimum and maximum number of iterations of the animation.
        shape_color (int): The color of the ellipse. 0 is white, 1 is black.

    Methods:
        run(): This function creates an animation by drawing ellipses on the frames of an image, with various properties of the ellipses (such as angle, x and y axis length, thickness, and position) changing randomly between iterations. The function uses the OpenCV library to draw the ellipses on the frames and also has functionality for creating a smooth transition between frames. The function also utilizes a "mask" which is an array of zeros the same size as the image, with the ellipse being drawn on it using the given parameters. The function then applies this mask to the image to create the animation.
        set_parameters(parameter_name): This function sets the parameters of the animation based on the parameter name given.
    """

    x_axis_length: tuple = None
    y_axis_length: tuple = None
    stroke_thickness: tuple = None
    x_position: tuple = None
    y_position: tuple = None
    step: float = None
    iterations: tuple = None
    shape_color: int = None

    def __init__(self, color, gif, parameter_name):
        super().__init__(color, gif)
        self.color = color
        self.gif = gif
        self.set_parameters(parameter_name)

    def run(self):
        """This function creates an animation by drawing ellipses on the frames of an image, with various properties of the ellipses (such as angle, x and y axis length, thickness, and position) changing randomly between iterations. The function uses the OpenCV library to draw the ellipses on the frames and also has functionality for creating a smooth transition between frames. The function also utilizes a "mask" which is an array of zeros the same size as the image, with the ellipse being drawn on it using the given parameters. The function then applies this mask to the image to create the animation.
        """
        shape = self.gif.image.shape

        start_angle = random.randint(0, 360)
        start_x_axis = random.randint(
            shape[1]//100*self.x_axis_length[0], shape[1]//100*self.x_axis_length[1])
        start_y_axis = random.randint(
            shape[0]//100*self.y_axis_length[0], shape[0]//100*self.y_axis_length[1])
        start_thick = random.randint(
            self.stroke_thickness[0], self.stroke_thickness[1])
        start_x = shape[1]//2
        start_y = shape[0]//2
        iter = random.randint(self.iterations[0], self.iterations[1])

        is_first = True
        keep_last = False
        pct = 0
        mask = []

        for i in range(iter):
            end_angle = random.randint(0, 360)
            end_x_axis = random.randint(
                shape[1]//100*self.x_axis_length[0], shape[1]//100*self.x_axis_length[1])
            end_y_axis = random.randint(
                shape[0]//100*self.y_axis_length[0], shape[0]//100*self.y_axis_length[1])
            end_thick = random.randint(
                self.stroke_thickness[0], self.stroke_thickness[1])
            end_x = random.randint(
                shape[1]//100*self.x_position[0], shape[1]//100*self.x_position[1])
            end_y = random.randint(
                shape[0]//100*self.y_position[0], shape[0]//100*self.y_position[1])

            distance_x = end_x - start_x
            distance_y = end_y - start_y

            exponent = random.randint(1, 3)

            while pct < 1:
                x = start_x + distance_x * pct
                y = start_y + pow(pct, exponent) * distance_y

                angle = start_angle + (end_angle - start_angle) * pct
                xAxis = start_x_axis + (end_x_axis - start_x_axis) * pct
                yAxis = start_y_axis + (end_y_axis - start_y_axis) * pct
                thickness = start_thick + (end_thick - start_thick) * pct

                mask = np.zeros(
                    (self.gif.image.shape[0], self.gif.image.shape[1]), np.float32)

                if self.shape_color == 0:
                    mask.fill(1)

                cv2.ellipse(mask, (int(x), int(y)), (int(xAxis), int(yAxis)), int(
                    angle), 0, 360, (self.shape_color, self.shape_color, self.shape_color), int(thickness))

                if is_first and self.gif.lask_mask != []:
                    super().morph(self.gif.lask_mask, mask, steps=10)
                    is_first = False

                img_back = self.color.apply_mask(mask, keep_last=keep_last)
                keep_last = True
                self.gif.images.append(img_back)
                self.gif.magnitudes.append(self.color.get_magnitude())
                self.gif.set_last_image(img_back)

                pct += self.step

            start_angle = end_angle
            start_x_axis = end_x_axis
            start_y_axis = end_y_axis
            start_thick = end_thick
            start_x = end_x
            start_y = end_y

        if mask != []:
            self.gif.lask_mask = mask

    def set_parameters(self, parameter_name):
        """Sets the parameters for the animation.

        Args:
            parameter_name (str): The name of the parameter to set.

        Raises:
            TypeError: If x_axis_length is not a tuple of int or float.
            TypeError: If y_axis_length is not a tuple of int or float.
            TypeError: If stroke_thickness is not a tuple of int or float.
            TypeError: If x_position is not a tuple of int or float.
            TypeError: If y_position is not a tuple of int or float.
            TypeError: If step is not a float.
            TypeError: If iterations is not a tuple of int or float.
        """
        params = self.gif.json_parser.get_parameter(parameter_name)

        if not all(isinstance(item, (int, float)) for item in params['x_axis_length']):
            raise TypeError("x_axis_length must be a tuple of int or float")
        self.x_axis_length = tuple(params['x_axis_length'])

        if not all(isinstance(item, (int, float)) for item in params['y_axis_length']):
            raise TypeError("y_axis_length must be a tuple of int or float")
        self.y_axis_length = tuple(params['y_axis_length'])

        if not all(isinstance(item, (int, float)) for item in params['stroke_thickness']):
            raise TypeError("stroke_thickness must be a tuple of int or float")
        self.stroke_thickness = tuple(params['stroke_thickness'])

        if not all(isinstance(item, (int, float)) for item in params['x_position']):
            raise TypeError("x_position must be a tuple of int or float")
        self.x_position = tuple(params['x_position'])

        if not all(isinstance(item, (int, float)) for item in params['y_position']):
            raise TypeError("y_position must be a tuple of int or float")
        self.y_position = tuple(params['y_position'])

        if not isinstance(params['step'], (int, float)):
            raise TypeError("step must be a float")
        self.step = params['step']

        if not all(isinstance(item, (int, float)) for item in params['iterations']):
            raise TypeError("iterations must be a tuple of int or float")
        self.iterations = tuple(params['iterations'])
