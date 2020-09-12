from pymongo import MongoClient



class clsmongo():
	def __init__(self):
		self.cluster = MongoClient("mongodb://127.0.0.1:27017/")
		self.db=self.cluster["mdbkaja"] # connection to the database
		self.tbl = '' # selecting a collection

	def checkuserrequeststatus(self,username):
		self.tbl = self.db['mtblpika']
		post = {"_id":username}
		data =  self.tbl.find(post)
		for value in data:
			requeststatus = value["requeststatus"]
			spongename = value["spongename"]
		if requeststatus == "sent":
			return requeststatus, spongename
		else:
			return requeststatus,spongename

	def uploadaudio(self,username,audiotitle,filename):
		self.tbl = self.db['mtblaudio']
		post = {"username":username,"audiotitle":audiotitle,"filename":filename}
		self.tbl.insert(post)

	def retrieveaudio(self):
		self.tbl = self.db['mtblaudio']
		return self.tbl.find()

	def getspecificaudio(self,uname,fname):
		self.tbl = self.db['mtblaudio']
		post = {"username":uname,"filename":fname}
		print(post)
		return self.tbl.find(post)


	def activateuser(self,uname,logintime,token):
		self.tbl = self.db['mtblpika']
		fil = { "_id": uname}
		upd =  {"$set": {"online": True,"logintime":logintime,"logofftime":"","token":token}}
		self.tbl.update_one(fil,upd)

	def logoffuser(self,uname,logofftime):
		self.tbl = self.db['mtblpika']
		fil = { "_id": uname}
		upd =  {"$set": {"online": False,"logofftime":logofftime,"token":"","requeststatus":"expired"}}
		self.tbl.update_one(fil,upd)

	def getsponges(self):
		self.tbl = self.db['mtblsponges']
		post = {"active":True}
		result = self.tbl.find(post)
		return result

	def getspecificsponges(self,spongename):
		self.tbl = self.db['mtblsponges']
		post = { "_id": spongename}
		result = self.tbl.find(post)
		return result

	def upspongeprofile(self,spongeuname,aboutsponge,audioname,activate):
		self.tbl = self.db['mtblsponges']
		fil = { "_id": spongeuname}
		post = {"$set": {"aboutsponge": aboutsponge, "audioname": audioname, "active":activate}}
		self.tbl.update(fil,post)

	def spongetalkrequests(self,spongename,username,requesttime):
		self.tbl = self.db['mtblrequests']
		key = spongename + "_______" + requesttime
		post = {"_id":key,"requestactive": True,"username":username}
		self.tbl.insert(post)

	def updatetalkrequests(self,username,result):
		self.tbl = self.db['mtblrequests']
		fil = { "username": username,"requestactive" : True}
		upd = {"$set" : {"requestactive": False, "outcome" : result}}
		self.tbl.update(fil,upd)

	def userrequests(self,spongename,username,requesttime):
		self.tbl = self.db['mtblpika']
		fil = { "_id": username.lower()}
		upd =  {"$set": {"spongename": spongename,"requeststatus":"sent","requesttime":requesttime}}
		self.tbl.update(fil,upd)

	def retrieverequestsforsponge(self,spongename):
		self.tbl = self.db['mtblrequests']
		post = {"requestactive" : True}
		results =  self.tbl.find(post)
		uname = 'zzzzzzz'
		for x in results:
			uname =  x['username']
		return uname


	def updateuserrequest(self,username,reqstatus):
		self.tbl = self.db['mtblpika']
		fil = { "_id": username.lower()}
		upd =  {"$set": {"requeststatus":reqstatus}}
		self.tbl.update(fil,upd)

	def retrieverequestssentbysuer(self,username):
		self.tbl = self.db[username]
		post = {"requestactive" : True}
		return self.tbl.find(post)
