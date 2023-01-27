__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.EllipseAnimation import EllipseAnimation
#import parameters as p


class EllipseAnimationWhite(EllipseAnimation):
    """Classe EllipseAnimationWhite. Child of class EllipseAnimation.
    """

    def __init__(self, color, gif):
        super().__init__(color, gif, "white_ellipse")
        self.color = color
        self.gif = gif

        self.shape_color: int = 1

    def run(self):
        super().run()
