#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
import os
from cincoconfig import *

CONFIG_FILENAME = os.path.join(os.path.dirname(__file__), '..', 'cincosense.cfg.yml')


schema = Schema()
schema.local_gateway = IPv4AddressField(required=True)
schema.local_dns = ListField(IPv4AddressField(), required=True)
schema.external_gateway = IPv4AddressField(required=True)
schema.external_dns = ListField(IPv4AddressField(), required=True)
schema.download_mbps = FloatField(required=True)
schema.upload_mbps = FloatField(required=True)
schema.ideal_latency = FloatField(default=100.0)

config = schema()
config.load(CONFIG_FILENAME, format='yaml')
