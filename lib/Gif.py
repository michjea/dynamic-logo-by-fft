__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

#import parameters as p
import imageio
import matplotlib.pyplot as plt
import io
from lib.Color import *
from lib.ColorBGR import *
from lib.ColorBW import *
import cv2
import random
import numpy as np
import time
from lib.JsonParser import JsonParser
import datetime


class Gif:
    """_summary_

    Attributes:

    Methods:
    """
    frames = []
    magnitudes = []
    images = []
    image = None
    color: Color = None
    lask_mask = []
    last_image = None
    is_infinite = False
    json_parser: JsonParser = None

    def __init__(self, image_file_name=None, parameters_file_name=None, is_infinite=False, image_data=None, json_data=None):
        self.is_infinite = is_infinite
        if json_data is not None:
            self.json_parser = JsonParser()
            self.json_parser.data = json_data
        else:
            self.json_parser = JsonParser(parameters_file_name)

        color_mode = self.json_parser.get_parameter("general")["color_mode"]

        if color_mode == True:
            if image_data is not None:
                self.image = cv2.imdecode(
                    np.frombuffer(image_data, np.uint8), 1)
            else:
                self.image = cv2.imread(image_file_name, 1)
            self.color = ColorBGR(self.image, self.json_parser)
        else:
            if image_data is not None:
                self.image = cv2.imdecode(
                    np.frombuffer(image_data, np.uint8), 0)
            else:
                self.image = cv2.imread(image_file_name, 0)
            self.color = ColorBW(self.image)

    def get_last_image(self):
        return self.last_image

    def set_last_image(self, image):
        if self.is_infinite:
            time.sleep(0.1)

        self.last_image = image

    def start(self):
        """_summary_
        """

        print("Generating frames...")

        fps = self.json_parser.get_parameter("general")["fps"]
        duration = self.json_parser.get_parameter("general")["duration"]

        while (len(self.images) < fps*duration or self.is_infinite):
            animation = random.randint(0, 1)
            c = random.randint(0, 1)
            f = random.randint(0, 1)
            if animation == 0:
                if c == 0:
                    if f == 0:
                        from lib.EllipseAnimationBlack import EllipseAnimationBlack
                        ellipse = EllipseAnimationBlack(
                            self.color, self)
                        ellipse.run()
                    else:
                        from lib.EllipseAnimationBlackFull import EllipseAnimationBlackFull
                        ellipse = EllipseAnimationBlackFull(
                            self.color, self)
                        ellipse.run()
                else:
                    if f == 0:
                        from lib.EllipseAnimationWhite import EllipseAnimationWhite
                        ellipse = EllipseAnimationWhite(
                            self.color, self)
                        ellipse.run()
                    else:
                        from lib.EllipseAnimationWhiteFull import EllipseAnimationWhiteFull
                        ellipse = EllipseAnimationWhiteFull(
                            self.color, self)
                        ellipse.run()
            else:
                if c == 0:
                    from lib.GridAnimationBlack import GridAnimationBlack
                    grid = GridAnimationBlack(
                        self.color, self)
                    grid.run()
                else:
                    from lib.GridAnimationWhite import GridAnimationWhite
                    grid = GridAnimationWhite(
                        self.color, self)
                    grid.run()

    def generate(self, return_bytes=False):
        """_summary_

        Args:
            return_bytes (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """

        print("Generating gif...")

        show_magnitude = self.json_parser.get_parameter("general")[
            "show_magnitude"]
        gif_name = self.json_parser.get_parameter("general")["gif_name"]
        if gif_name == "auto":
            gif_name = datetime.datetime.now().strftime("%d%m%Y-%H%M%S") + ".gif"

        fps = self.json_parser.get_parameter("general")["fps"]

        # if show_magnitude:
        i1 = plt.subplot(211).imshow(
            self.image, cmap='gray')
        plt.xticks([]), plt.yticks([])
        i2 = plt.subplot(212).imshow(
            self.image, cmap='gray')
        plt.xticks([]), plt.yticks([])
        for i in range(len(self.images)):
            i1.set_data(self.images[i])
            i1.autoscale()
            i2.set_data(self.magnitudes[i])
            i2.autoscale()
            buf = io.BytesIO()
            plt.savefig(buf, format='jpg')
            buf.seek(0)
            self.frames.append(imageio.v2.imread(buf))
        # else:
        #    self.frames = self.images

        if return_bytes:
            with io.BytesIO() as output:
                imageio.mimsave(output, self.frames, format='gif', fps=fps)
                return output.getvalue()

        print("Saving gif...")
        imageio.mimsave(gif_name + '.gif', self.frames,
                        fps=fps)
        print("Saving gif...")
        imageio.mimsave(gif_name + '-1.gif', self.images,
                        fps=fps)
        print("Done !")


class Animation:
    """This is the Animation class, which is responsible for creating animations from masks and colors.

    Attributes:
        color (Color): An instance of the Color class, used to apply the mask to images.
        gif (Gif): An instance of the Gif class, used to create and store the animation frames.

    Methods:
        run(): This is an abstract method that should be implemented by a subclass.
        morph(last_mask, next_mask, steps=10): This function morphs the mask from the last frame to the next frame over a specified number of steps.
    """
    color: Color = None
    gif: Gif = None

    def __init__(self, color, gif):
        self.color = color
        self.gif = gif

    @abstractmethod
    def run(self):
        pass

    def morph(self, last_mask, next_mask, steps=10):
        """This function morphs the mask from the last frame to the next frame over a specified number of steps.

        Args:
            last_mask (_type_): The mask from the last frame.
            next_mask (_type_): The mask dor the next frame.
            steps (int, optional): The number of steps to use for the morph. Defaults to 10.
        """
        keep_last = False
        for i in range(steps):
            alpha = i / (steps - 1)
            mask_morph = cv2.addWeighted(
                last_mask, 1 - alpha, next_mask, alpha, 0)

            img_back = self.color.apply_mask(mask_morph, keep_last=keep_last)
            keep_last = True
            self.gif.images.append(img_back)
            self.gif.magnitudes.append(self.color.get_magnitude())
            self.gif.set_last_image(img_back)
        return


if __name__ == "__main__":
    gif = Gif("logo.png", "parameters.json")
    gif.start()
    gif.generate()
