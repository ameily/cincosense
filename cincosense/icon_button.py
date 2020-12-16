#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
from kivy.uix.image import Image
from kivy.uix.button import Button

from . import style


class IconButton(Button):

    def __init__(self, source: str, **kwargs):
        super().__init__(size_hint=(None, None), **kwargs)
        self.img = Image(source=style.locate_image(source), pos_hint=(None, None),
                         allow_stretch=False, size_hint=(None, None))
        self.img.size = self.img.texture_size
        self.img.pos = (self.x, self.y + self.height)
        self.add_widget(self.img)
        self.bind(pos=self._update_pos)

    def _update_pos(self, *args):
        self.img.pos = (self.x + ((self.width - self.img.width) / 2),
                        self.y + ((self.height - self.img.height) / 2))
