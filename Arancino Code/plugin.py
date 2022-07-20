from iotronic_lightningrod.modules.plugins import Plugin
from oslo_log import log as logging
LOG = logging.getLogger(__name__)

# User imports
import time
import datetime
import random
import json
from os.path import exists


class Worker(Plugin.Plugin):

    def __init__(self, uuid, name, q_result=None, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)

    def run(self):
        device = {}
        device['board_name'] = self.name
        device['board_id'] = self.uuid
        device['plugin_name'] = self.name
        device['plugin_id'] = self.uuid
        json_string = json.dumps(device)
        device_file = open('device_data.json', 'w')
        device_file.write(json_string)
        device_file.close()
        LOG.info("Plugin " + self.name + " starting...")
        LOG.info(self.params)
        while True:
            if not exists('sensor_data.json'):
                s2 = open('sensor_data.json', 'w')
                s2.write(json.dumps({"time": "sensor_val"}))
                s2.close()
            f = open('sensor_data.json', "r")
            sensor_data = json.loads(f.read())
            sensor_val = str(random.uniform(30, 37))
            sensor_data[str(datetime.datetime.now())] = sensor_val
            sensor_json_string = json.dumps(sensor_data)
            sensor_file = open('sensor_data.json', 'w')
            sensor_file.write(sensor_json_string)
            sensor_file.close()
            time.sleep(60)
            LOG.info("After sleep")
