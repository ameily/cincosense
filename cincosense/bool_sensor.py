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
from kivy.graphics import Color, Rectangle

from . import style


class BoolSensor(BoxLayout):

    def __init__(self, text: str, image: str, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.image_path = style.locate_image(image)
        self.label = Label(text=text, color=style.UNKNOWN_FG)
        self.image = Image(source=style.UNKNOWN_IMAGE)
        self.add_widget(self.image)
        self.add_widget(self.label)

        with self.canvas.before:
            self.color = Color(*style.UNKNOWN_BG)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self._update_rect, size=self._update_rect)
        self.state = 'unknown'

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def mark_good(self, immediate: bool = False):
        if immediate:
            self._mark('good')
        else:
            Clock.schedule_once(partial(self._mark, 'good'))

    def mark_bad(self, immediate: bool = False):
        if immediate:
            self._mark('bad')
        else:
            Clock.schedule_once(partial(self._mark, 'bad'))

    def mark_unknown(self, immediate: bool = False) -> None:
        if immediate:
            self._mark('unknown')
        else:
            Clock.schedule_once(partial(self._mark, 'unknown'))

    def _mark(self, state: str, dt: int = None) -> None:
        if self.state == state:
            return

        if state == 'good':
            fg, bg = style.SUCCESS_FG, style.SUCCESS_BG
            image_path = self.image_path
        elif state == 'bad':
            fg, bg = style.DANGER_FG, style.DANGER_BG
            image_path = style.DANGER_IMAGE
        elif state == 'unknown':
            fg, bg = style.UNKNOWN_FG, style.UNKNOWN_BG
            image_path = style.UNKNOWN_IMAGE

        self.color.rgba = bg
        self.label.color = self.image.color = fg
        self.image.source = image_path
        self.state = state
