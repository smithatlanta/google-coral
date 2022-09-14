# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from luma.core.render import canvas
from PIL import ImageDraw
from time import sleep
from influxdb import InfluxDBClient
from my_enviro_board import MyEnviroBoard

import argparse
import itertools
import os
import time

DEFAULT_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), 'cloud_config.ini')


def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')


def _none_to_nan(val):
    return float('nan') if val is None else val


def _none_to_zero(val):
    return 0 if val is None else val


def main():
    # client = InfluxDBClient(
    #     '10.0.2.100', 8086, 'coralmonitor', 'coralmonitor', 'coralstats')

    # Pull arguments from command line.
    parser = argparse.ArgumentParser(description='Enviro Kit Demo')
    parser.add_argument('--display_duration',
                        help='Measurement display duration (seconds)', type=int,
                        default=60)
    parser.add_argument('--upload_delay', help='Cloud upload delay (seconds)',
                        type=int, default=300)
    parser.add_argument(
        '--cloud_config', help='Cloud IoT config file', default=DEFAULT_CONFIG_LOCATION)
    args = parser.parse_args()

    # Create instances of EnviroKit and Cloud IoT.
    enviro = MyEnviroBoard()
    # Indefinitely update display and upload to cloud.
    sensors = {}
    read_period = int(args.upload_delay / (2 * args.display_duration))
    for read_count in itertools.count():
        sensors['temperature'] = enviro.temperature * (9.0 / 5.0) + 32
        sensors['humidity'] = enviro.humidity
        sensors['ambient_light'] = enviro.ambient_light
        sensors['pressure'] = enviro.pressure * 10.0
        print(sensors)

        msg = 'Temp: %.2f C\n' % _none_to_nan(sensors['temperature'])
        msg += 'RH: %.2f %%\n' % _none_to_nan(sensors['humidity'])
        msg += 'Light: %.2f lux\n' % _none_to_nan(sensors['ambient_light'])
        msg += 'Pressure: %.2f kPa' % _none_to_nan(sensors['pressure'])
        sensorTime = time.ctime()
        # json_body = [
        #     {
        #         "measurement": "coral",
        #         "time": sensorTime,
        #         "fields": {
        #             "temperature":  _none_to_zero(sensors['temperature']),
        #             "humidity": _none_to_zero(sensors['humidity']),
        #             "ambient_light": _none_to_zero(sensors['ambient_light']),
        #             "pressure": _none_to_zero(sensors['pressure'])
        #         }
        #     }
        # ]
        update_display(enviro.display, msg)
        print(msg)
        # client.write_points(json_body)
        sleep(args.display_duration)


if __name__ == '__main__':
    main()
