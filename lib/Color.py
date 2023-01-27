__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"


from abc import abstractmethod


class Color:
    """This is the Color class, which is an abstract calss that defines the basic functionality for working with colors in an animation.

    Attributes:
        None

    Methods:
        apply_mask(mask, keep_last=False): This is an abstract method that should be implemented by a subclass. The apply_mask method should take a mask and apply it to the image.
        get_magnitude(): This is an abstract method that should be implemented by a subclass. The get_magnitude method should return the magnitude of the image of the last applied mask.
    """

    def __init__(self):
        pass

    @abstractmethod
    def apply_mask(self, mask, keep_last=False):
        pass

    @abstractmethod
    def get_magnitude(self):
        pass
