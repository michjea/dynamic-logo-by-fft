__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.EllipseAnimation import *
#import parameters as p


class EllipseAnimationBlack(EllipseAnimation):
    """Classe EllipseAnimationBlack. Child of class EllipseAnimation.

    Methods:
        run(): Runs the parent method.

    """

    def __init__(self, color, gif):
        super().__init__(color, gif, "black_ellipse")
        self.color = color
        self.gif = gif

        self.shape_color: int = 0

    def run(self):
        super().run()
