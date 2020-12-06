#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
import threading
import logging
import subprocess
import json
from functools import partial
import socket
from typing import List

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.logger import Logger
from dns.resolver import Resolver

from .bool_sensor import BoolSensor
from .metric_sensor import MetricSensor
from .ping import ping
from .config import config


class SpeedPanel(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        # ping local gateway - bolt
        # ping external gateway - external-link
        # dns query, icanhazip - person
        # icanhazip - get external IP - cloud
        self.external_ip_sensor = BoolSensor(text='Internet', image='cloud.png')
        self.latency = MetricSensor(text='Latency', image='clock.png')
        self.download = MetricSensor(text='Download', image='cloud-download.png')
        self.upload = MetricSensor(text='Upload', image='cloud-upload.png')

        self.add_widget(self.external_ip_sensor)
        self.add_widget(self.latency)
        self.add_widget(self.download)
        self.add_widget(self.upload)

        Clock.schedule_once(lambda dt: self.run_sensors(), 5.0)

    def run_sensors(self):
        thread = threading.Thread(target=self._run_sensors)
        thread.start()

    def _run_sensors(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(('icanhazip.com.', 80))
            sock.sendall(b'GET / HTTP/1.1\r\nHost: icanhazip.com\r\n\r\n')
            data = sock.recv(1024)
            sock.close()
        except OSError:
            Logger.exception('Connection: remote TCP connection failed')
            # self.mark_bad(self.external_ip_sensor)
            return

        Logger.info('Connection: remote TCP connection successful')
        myip = data[data.index(b'\r\n\r\n'):].decode().strip()
        Logger.info('Connection: connectivity is good, my external IP address is: %s', myip)
        self.external_ip_sensor.mark_good()

        Logger.info('Speed: running speed test')
        try:
            content = subprocess.check_output(['speedtest-cli', '--json'])
        except subprocess.CalledProcessError:
            Logger.exception('speedtest-cli failed')
            return

        result = json.loads(content.decode().strip())
        Clock.schedule_once(partial(self.set_result, result))

    def set_result(self, result, dt: int = None) -> None:
        latency = result['ping']
        download = result['download'] / 1024 / 1024
        upload = result['upload'] / 1024 / 1024

        self.latency.set_value(f'{latency:.0f}ms', config.ideal_latency / latency)
        self.download.set_value(f'{download:.1f}mb/s', download / config.download_mbps)
        self.upload.set_value(f'{upload:.1f}mb/s', upload / config.upload_mbps)

        Logger.info('Speed: results: latency=%.0fms, download=%.1fmb/s, upload=%.1fmb/s', latency, download, upload)
