
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty


class StatusBar(BoxLayout):
    connection_update = StringProperty('Never')
    speed_update = StringProperty('Never')

    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.speed_label = Label(text=f'Speed: {self.speed_update}')
        self.connection_label = Label(text=f'Connection: {self.connection_update}')
        self.add_widget(self.connection_label)
        self.add_widget(self.speed_label)

    def on_connection_update(self, instance, last_update):
        self.connection_label.text = f'Connection: {last_update}'

    def on_speed_update(self, instance, last_update):
        self.speed_label.text = f'Speed: {last_update}'
