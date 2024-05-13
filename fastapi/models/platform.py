'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-16 00:31:58
LastEditors: Ryan Zhang
LastEditTime: 2024-04-18 12:08:25
'''
'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-10 16:14:27
LastEditors: Ryan Zhang
LastEditTime: 2024-04-10 16:44:29
'''

class Platform:
    def __init__(self):
        self._os_info = None
        self._os_name = None
        self._os_version = None
        self._os_release = None
        self._architecture = None
        self._network_name = None
        self._processor = None
        self._windows_root_path = r"C:\Users\horiz\AppData\Local\gowaf"
        self._linux_root_path = r"/usr/local/gowaf"

    # OS Info
    @property
    def os_info(self):
        return self._os_info

    @os_info.setter
    def os_info(self, value):
        self._os_info = value

    # OS Name
    @property
    def os_name(self):
        return self._os_name

    @os_name.setter
    def os_name(self, value):
        self._os_name = value

    # os_version
    @property
    def os_version(self):
        return self._os_version

    @os_version.setter
    def os_version(self, value):
        self._os_version = value

    # os_release
    @property
    def os_release(self):
        return self._os_release

    @os_release.setter
    def os_release(self, value):
        self._os_release = value

    # Architecture
    @property
    def architecture(self):
        return self._architecture

    @architecture.setter
    def architecture(self, value):
        self._architecture = value

    # network_name
    @property
    def network_name(self):
        return self._network_name

    @network_name.setter
    def network_name(self, value):
        self._network_name = value

    # processor
    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, value):
        self._processor = value

