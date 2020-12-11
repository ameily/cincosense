#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.logger import Logger

from . import style


class MetricSensor(BoxLayout):

    def __init__(self, text: str = None, image: str = None, metric: str = None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.text = text
        self.image_path = style.locate_image(image)
        self.label = Label(text=f'{text}\n...', color=style.UNKNOWN_FG, halign='center')
        self.image = Image(source=style.UNKNOWN_IMAGE)
        # self.value = Label(text='...', color=style.UNKNOWN_FG)
        self.add_widget(self.image)
        self.add_widget(self.label)
        # self.add_widget(self.value)

        with self.canvas.before:
            self.color = Color(*style.UNKNOWN_BG)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_value(self, value: str, percent: float) -> None:
        # if percent > 1.0:
        #     percent = 1.0
        if percent < 0.0:
            percent = 0.0

        self.label.text = f'{value}\n{percent:.0%}\n{self.text}'
        if percent >= 0.9:
            fg, bg = style.SUCCESS_FG, style.SUCCESS_BG
        elif percent >= 0.70:
            fg, bg = style.WARNING_FG, style.WARNING_BG
        else:
            fg, bg = style.DANGER_FG, style.DANGER_BG

        self.label.color = self.image.color = fg
        self.color.rgba = bg
        self.image.source = self.image_path

    def mark_unknown(self):
        self.label.color = self.image.color = style.UNKNOWN_FG
        self.color.rgba = style.UNKNOWN_BG
        self.image.source = style.UNKNOWN_IMAGE
        self.label.text = f'{self.text}\n...'
