#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
import threading
import logging
import socket
from typing import List

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.logger import Logger
from dns.resolver import Resolver

from .bool_sensor import BoolSensor
from .ping import ping
from .config import config


class ConnectionPanel(BoxLayout, EventDispatcher):

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, orientation='horizontal', **kwargs)
        EventDispatcher.__init__(self)
        # ping local gateway - bolt
        # ping external gateway - external-link
        # dns query, icanhazip - person
        # icanhazip - get external IP - cloud
        self.local_gateway_sensor = BoolSensor(text='Local Gateway', image='bolt.png')
        self.external_gateway_sensor = BoolSensor(text='External Gateway',
                                                  image='external-link.png')
        self.external_dns_sensor = BoolSensor(text='External DNS', image='person.png')
        self.local_dns_sensor = BoolSensor(text='Local DNS', image='people.png')

        self.add_widget(self.local_gateway_sensor)
        self.add_widget(self.external_gateway_sensor)
        self.add_widget(self.external_dns_sensor)
        self.add_widget(self.local_dns_sensor)

        self.register_event_type('on_sensor_done')

    def run_sensors(self, reset: bool = False):
        if reset:
            self.local_gateway_sensor.mark_unknown(True)
            self.external_gateway_sensor.mark_unknown(True)
            self.external_dns_sensor.mark_unknown(True)
            self.local_dns_sensor.mark_unknown(True)

        thread = threading.Thread(target=self._run_sensors)
        thread.start()

    def _run_sensors(self):
        Logger.info('Connection: running connection sensors')
        if not ping(config.local_gateway):
            Logger.error('Connection: local gateway ping failed')
            self.mark_bad(self.local_gateway_sensor, self.external_gateway_sensor,
                          self.external_dns_sensor, self.local_dns_sensor)
            return

        Logger.info('Connection: local gateway ping successful')
        self.local_gateway_sensor.mark_good()

        if not ping(config.external_gateway):
            Logger.info('Connection: external gateway ping failed')
            self.mark_bad(self.external_gateway_sensor, self.external_dns_sensor,
                          self.local_dns_sensor)
            return

        Logger.info('Connection: external gateway ping successful')
        self.external_gateway_sensor.mark_good()

        resolver = Resolver(configure=False)
        resolver.nameservers = list(config.external_dns)

        try:
            ans = resolver.resolve('google.com.')
            icanhazip = str(ans[0])
        except:
            Logger.exception('Connection: external dns query failed')
            self.mark_bad(self.external_dns_sensor, self.local_dns_sensor)
            return

        Logger.info('Connection: external dns query successful')
        self.external_dns_sensor.mark_good()

        resolver = Resolver(configure=False)
        resolver.nameservers = list(config.local_dns)

        try:
            ans = resolver.resolve('google.com.')
            icanhazip = str(ans[0])
        except:
            Logger.exception('Connection: internal dns query failed')
            self.mark_bad(self.local_dns_sensor)
            return

        Logger.info('Connection: internal dns query successful')
        self.local_dns_sensor.mark_good()
        self.dispatch('on_sensor_done')

    def mark_bad(self, *sensors: List[BoolSensor]) -> None:
        for sensor in sensors:
            sensor.mark_bad()
        self.dispatch('on_sensor_done')

    def on_sensor_done(self):
        pass
