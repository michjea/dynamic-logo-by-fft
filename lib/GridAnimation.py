__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.Gif import Animation
import random
import numpy as np
import cv2


class GridAnimation(Animation):
    """_summary_

    Attributes:

    Methods:

    """
    cell_number: tuple = None
    stroke_thickness: tuple = None
    step: int = None
    iterations: tuple = None
    shape_color: int = None

    def __init__(self, color, gif, parameter_name):
        super().__init__(color, gif)
        self.color = color
        self.gif = gif

        self.set_parameters(parameter_name)

    def run(self):
        """_summary_
        """
        shape = self.gif.image.shape
        distance = 0
        if shape[0] > shape[1]:
            distance = shape[0]
        else:
            distance = shape[1]

        is_first = True
        keep_last = False
        start_thick = random.randint(
            self.stroke_thickness[0], self.stroke_thickness[1])
        iter = random.randint(self.iterations[0], self.iterations[1])
        start_cell_number = random.randint(
            distance//100*self.cell_number[0], distance//100*self.cell_number[1])
        mask = []

        for i in range(iter):
            end_cell_number = random.randint(
                distance//100*self.cell_number[0], distance//100*self.cell_number[1])
            end_thick = random.randint(
                self.stroke_thickness[0], self.stroke_thickness[1])

            for n in np.arange(int(start_cell_number), int(end_cell_number), self.step):
                mask = np.zeros(
                    (shape[0], shape[1]), np.float32)

                if self.shape_color == 0:
                    mask.fill(1)

                thick = start_thick + \
                    (end_thick - start_thick) * (n - start_cell_number) / \
                    (end_cell_number - start_cell_number)

                for j in np.arange(0, distance, n):
                    cv2.line(mask, (int(j), 0),
                             (int(j), shape[0]), self.shape_color, int(thick))
                    cv2.line(mask, (0, int(j)),
                             (shape[1], int(j)), self.shape_color, int(thick))

                if is_first and self.gif.lask_mask != []:
                    super().morph(self.gif.lask_mask, mask, steps=10)
                    is_first = False

                img_back = self.color.apply_mask(mask, keep_last=keep_last)
                keep_last = True
                self.gif.images.append(img_back)
                self.gif.magnitudes.append(self.color.get_magnitude())
                self.gif.set_last_image(img_back)

            start_cell_number = end_cell_number
            start_thick = end_thick
        if mask != []:
            self.gif.lask_mask = mask

    def set_parameters(self, parameter_name):
        """_summary_

        Args:
            parameter_name (_type_): _description_

        Raises:
            TypeError: _description_
            TypeError: _description_
            TypeError: _description_
            TypeError: _description_
        """
        params = self.gif.json_parser.get_parameter(parameter_name)

        if not all(isinstance(item, (int, float)) for item in params['cell_number']):
            raise TypeError("cell_number must be a tuple of int or float")
        self.cell_number = tuple(params['cell_number'])

        if not all(isinstance(item, (int, float)) for item in params['stroke_thickness']):
            raise TypeError("stroke_thickness must be a tuple of int or float")
        self.stroke_thickness = tuple(params['stroke_thickness'])

        if not isinstance(params['step'], (int, float)):
            raise TypeError("step must be a tuple of int or float")
        self.step = params['step']

        if not all(isinstance(item, (int, float)) for item in params['iterations']):
            raise TypeError("iterations must be a tuple of int or float")
        self.iterations = tuple(params['iterations'])
