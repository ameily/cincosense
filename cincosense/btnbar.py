
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher

from .icon_button import IconButton


class ButtonBar(BoxLayout, EventDispatcher):

    def __init__(self, width: int = 64, **kwargs):
        BoxLayout.__init__(self, orientation='vertical', width=width, size_hint=(None, 1),
                           **kwargs)
        EventDispatcher.__init__(self)

        self.register_event_type('on_reload')
        self.reload = IconButton(size=(width, width), source='reload-sm.png')
        self.add_widget(self.reload)

        self.reload.bind(on_press=lambda btn: self.dispatch('on_reload'))

    def on_reload(self):
        pass

