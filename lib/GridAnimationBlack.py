__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

from lib.GridAnimation import *
#import parameters as p


class GridAnimationBlack(GridAnimation):
    """_summary_

    Methods:
    """

    def __init__(self, color, gif):
        super().__init__(color, gif, "black_grid")
        self.color = color
        self.gif = gif

        self.shape_color = 0

    def run(self):
        super().run()
