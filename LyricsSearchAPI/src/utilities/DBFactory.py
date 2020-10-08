import sys
from os import path

sys.path.append(path.abspath('/Users/WaylonLuo/git/DrugAbusePrevention'))

from dbModels.MongoDbModel import MongoDbModel
from dbModels.MongoDbService import MongoDbService

class DBFactory:
    def insert2MongoDB(self, id, tableName, dBName, data):
          
        mongoDbService = MongoDbService('mongodb://localhost:27017/')
        mongoDbModel = MongoDbModel(mongoDbService.client, dBName, 1)
        mongoDbModel.insert(id, data, tableName)
        mongoDbService.close()