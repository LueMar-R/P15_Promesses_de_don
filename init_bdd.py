from flask import Flask
from flask_pymongo import pymongo


connection_string = "mongodb+srv://Lud:ludivine@cluster0.zblke.mongodb.net/dons?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)
db = client.get_database('dbdons')
collec = db.dons
