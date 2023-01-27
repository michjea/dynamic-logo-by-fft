"""
"""

__author__ = "Jeanne Michel"
__contact__ = "jeanne.michel@he-arc.ch"
__copyright__ = "© 2023 HE-Arc"
__date__ = "25/01/2023"

import sys
from lib.Gif import Gif

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Error: missing arguments")
        exit(1)

    image_path = sys.argv[1]
    json_path = sys.argv[2]

    gif = Gif(image_file_name=image_path, parameters_file_name=json_path)
    gif.start()
    gif.generate()
