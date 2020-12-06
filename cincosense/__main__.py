#
# Copyright (C) 2020 Adam Meily, meily.adam@gmail.com
#
import logging
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger

from .connection_panel import ConnectionPanel
from .speed_panel import SpeedPanel

# logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class MyApp(App):

    def build(self):
        Logger.info('MyApp2: thing 1')
        vbox = BoxLayout(orientation='vertical')

        # hbox_top = BoxLayout(orientation='horizontal', padding=[10, 10], spacing=10)
        connection_panel = ConnectionPanel(padding=[10, 10], spacing=10)
        speed_panel = SpeedPanel(padding=[10, 10], spacing=10)
        vbox.add_widget(connection_panel)
        vbox.add_widget(speed_panel)

        return vbox



if __name__ == '__main__':
    MyApp().run()
