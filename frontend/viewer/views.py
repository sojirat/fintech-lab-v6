from django.shortcuts import render
from pymongo import MongoClient

def log_table(request):
    client = MongoClient("mongodb://mongo:27017/")
    db = client.fintech
    logs = list(db.logs.find().sort("timestamp", -1))
    return render(request, 'viewer/log_table.html', {'logs': logs})