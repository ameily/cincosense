#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
import os

IMAGE_BASE_PATH = os.path.join(os.path.dirname(__file__), 'resources', 'img')

def locate_image(filename: str) -> str:
    return os.path.join(IMAGE_BASE_PATH, filename)


SUCCESS_BG = [0.129, 0.533, 0.219, 1]  # #218838
SUCCESS_FG = [1, 1, 1, 1]


DANGER_BG = [0.784, 0.137, 0.2, 1]  # #c82333
DANGER_FG = [1, 1, 1, 1]
DANGER_IMAGE = locate_image('warning.png')

WARNING_BG = [0.878, 0.659, 0, 1]  # #e0a800
WARNING_FG = [0.129, 0.145, 0.161, 1]  # #212529

UNKNOWN_BG = [0.353, 0.384, 0.408, 1]  # #5a6268
UNKNOWN_FG = [1, 1, 1, 1]
UNKNOWN_IMAGE = locate_image('question-mark.png')
