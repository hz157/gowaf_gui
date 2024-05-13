'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-16 00:47:01
LastEditors: Ryan Zhang
LastEditTime: 2024-04-16 00:51:45
'''
from utils.xdbSearcher import XdbSearcher

class IPDatabaseManager:
    _instance = None

    @classmethod
    def GetInstance(cls):
        if cls._instance is None:
            dbPath = "./files/ip2region.xdb"
            cb = XdbSearcher.loadContentFromFile(dbfile=dbPath)
            cls._instance = XdbSearcher(contentBuff=cb)
        return cls._instance

    @classmethod
    def CloseInstance(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None
