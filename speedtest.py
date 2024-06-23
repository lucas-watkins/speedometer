import json
import subprocess
from dataclasses import dataclass
import pickle
import os
from datetime import datetime, timedelta


@dataclass
class Previous:
    tests = []
    
    @staticmethod
    def pickle_tests() -> None:
        pickle.dump(Previous.tests, open('previous_tests.bin', 'wb'))
        

class SpeedTest:

    def __init__(self):
        self._download_speed = None
        self._upload_speed = None
        self.__raw_json = dict()
        self.__timestamp = datetime.now()
        
    @property
    def download_speed(self) -> float:
        """ Download speed in mbps """
        try:
            return round(int(self.__raw_json['download']['bandwidth']) / 125000)
        except KeyError:
            return self._download_speed
            
    @property
    def upload_speed(self) -> int:
        """ Upload speed in mbps """
        try:
            return round(int(self.__raw_json['upload']['bandwidth']) / 125000)
        except KeyError:
            return self._upload_speed
        
    @property
    def latency(self) -> int:
        """ Latency in ms """
        return round(int(self.__raw_json['ping']['latency']))
    
    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, val) -> None:
        self.__timestamp = val

    def run(self) -> None:
        """ Runs speed test on initalization """
        try:
            self.__raw_json = json.loads(subprocess.run(['speedtest', '-f', 'json'], capture_output=True).stdout)

        except subprocess.SubprocessError:
            print('Error Running Speed Test')
        
        self.__timestamp = datetime.now()
        
        Previous.tests.append(self)

    @download_speed.setter
    def download_speed(self, val) -> None:
        self._download_speed = val
        
    @upload_speed.setter
    def upload_speed(self, val) -> None:
        self._upload_speed = val


# setup lists dataclass
if os.path.isfile('previous_tests.bin'):
    Previous.tests = pickle.load(open('previous_tests.bin', 'rb'))
    for test in Previous.tests:
        if datetime.today() - timedelta(days=30) > test.timestamp:
            Previous.tests.remove(test)

   