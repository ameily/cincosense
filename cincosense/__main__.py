#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
import logging
import sys
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock

from .connection_panel import ConnectionPanel
from .speed_panel import SpeedPanel
from .icon_button import IconButton
from .btnbar import ButtonBar
from .statusbar import StatusBar
from . import style
from .config import config

# logging.basicConfig(stream=sys.stderr, level=logging.INFO)
Window.size = (800, 400)

class MyApp(App):

    def build(self):
        Logger.info('MyApp2: thing 1')
        hbox = BoxLayout(orientation='horizontal', spacing=5)
        vbox = BoxLayout(orientation='vertical', spacing=5)

        # hbox_top = BoxLayout(orientation='horizontal', padding=[10, 10], spacing=10)
        self.connection_panel = ConnectionPanel(padding=[0, 0], spacing=5)
        self.speed_panel = SpeedPanel(padding=[0, 0], spacing=5)
        vbox.add_widget(self.connection_panel)
        vbox.add_widget(self.speed_panel)
        hbox.add_widget(vbox)

        self.btn_bar = ButtonBar(width=64)
        hbox.add_widget(self.btn_bar)

        self.btn_bar.bind(on_reload=lambda target: self.run_sensors(reset=True))
        self.connection_panel.bind(on_sensor_done=self.on_connection_sensor_done)
        self.speed_panel.bind(on_sensor_done=self.on_speed_sensor_done)

        self.running_sensors = 0
        self.last_connection_update = None
        self.last_speed_update = None

        self.update_interval = Clock.schedule_interval(self.schedule_update, 5)

        self.status_bar = StatusBar(size_hint=(1, None), height=16)
        vbox.add_widget(self.status_bar)

        self.run_sensors()

        return hbox

    def run_sensors(self, connection: bool = True, speed: bool = True, reset: bool = False):
        self.btn_bar.reload.disabled = True
        if connection:
            self.status_bar.connection_update = 'Running'
            self.connection_panel.run_sensors(reset=reset)
            self.running_sensors += 1

        if speed:
            self.status_bar.speed_update = 'Running'
            self.speed_panel.run_sensors(reset=reset)
            self.running_sensors += 1

    def on_sensor_done(self):
        self.running_sensors -= 1
        if self.running_sensors == 0:
            self.btn_bar.reload.disabled = False

    def on_connection_sensor_done(self, target):
        self.on_sensor_done()
        self.last_connection_update = datetime.now()
        self.status_bar.connection_update = self.last_connection_update.strftime('%I:%M:%S %p')

    def on_speed_sensor_done(self, target):
        self.on_sensor_done()
        self.last_speed_update = datetime.now()
        self.status_bar.speed_update = self.last_speed_update.strftime('%I:%M:%S %p')

    def schedule_update(self, dt):
        if self.running_sensors:
            return

        delta = (datetime.now() - self.last_speed_update).total_seconds()
        # or not self.speed_panel.is_good()
        speed = (delta < 0 or delta >= config.speed_update_interval or
                 self.speed_panel.state != 'good')

        delta = (datetime.now() - self.last_connection_update).total_seconds()
        connection = (delta < 0 or delta >= config.connection_update_interval
                      or self.speed_panel.state != 'good' or speed)

        if not connection and not speed:
            return

        self.run_sensors(connection=connection, speed=speed)


if __name__ == '__main__':
    MyApp().run()
