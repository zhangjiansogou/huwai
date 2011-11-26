from mongokit import *
import datetime
import types 
import pymongo
import uuid

class DBException(Exception):
    def __init__(self, error):
        Exception.__init__(self)
	self.error = error

#Activity data structure
class ActivityData(Document):
	structure = {
		'title':unicode,
		'link':unicode,
		'imageurl':{"originurl":unicode,"localurl":unicode},
		'organizername':unicode,
		'activityclass':unicode,
		'place':unicode,
		'time':unicode,
		'hotnumber':unicode,
		'uuid':str,
		'date_creation':datetime.datetime,
		'rank':int
	}
	required_fields = ['title','link','imageurl.originurl','imageurl.localurl','organizername','activityclass','place','time','hotnumber']
 	default_values = {'uuid':str(uuid.uuid4()),
'rank':0, 'date_creation':datetime.datetime.utcnow}

#Activity Class
class DB:
	def __init__(self):
		self.connection = Connection()
		self.connection.register([ActivityData])
		self.collection = self.connection.test.example
		self.data = self.connection.test.example.ActivityData()

	#filter data type: data{'name', u'hello'}
	def setRank(self, data, rankvalue):
		if type(data) is types.DictType:
			self.collection.update(data, {'$set':rankvalue})

	def save(self, data):
		if type(data) is types.DictType:
			for i in data:
				self.data[i] = data[i]
			self.data["uuid"] = str(uuid.uuid4())
			self.data.save()
		else:
			raise DBException("Wrong Data type, please check.")

	def find(self, page=1, number=8, data=""):
		if type(data) is types.StringType and data == "all":
			return self.collection.find().sort('rank', pymongo.DESCENDING)
		if type(data) is types.StringType and data == "":
			return self.collection.find().sort('rank', pymongo.DESCENDING).skip((page-1)*number).limit(number)
		if type(data) is types.DictType:
			return self.collection.find(data).sort('rank', pymongo.DESCENDING).skip((page-1)*number).limit(number)
		else:
			raise DBException("Wrong Data type, please check.")
	
	def remove(self, data):
		if type(data) is types.DictType:
			self.collection.remove(data)
		else:
			raise DBException("Wrong Data type, please check.")

	#the first parameter is the updated data{'title':u'zhangjian', 'author':u'hello'}, 
	#the second parameter is the criteria{'title':u'zhangjian'}.
	def update(self, data, criteria):
		if type(data) is types.DictType:
			if type(criteria) is types.DictType:
				self.collection.update(criteria, {'$set':data})
			else:
				raise DBException("The second paramter's type is wrong, please check.")
		else:
			raise DBException("The second paramter's type is wrong, please check.")

