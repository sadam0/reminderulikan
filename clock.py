# -*- coding: utf-8 -*-

import os
import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from pymongo import MongoClient

from linebot import LineBotApi
from linebot.models import TextMessage

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token)

mongodb_id = os.getenv('MONGODB_ID')
mongodb_pw = os.getenv('MONGODB_PW')

client = MongoClient("mongodb://cluster1-shard-00-00-imdfs.mongodb.net:27017,cluster1-shard-00-01-imdfs.mongodb.net:27017,cluster1-shard-00-02-imdfs.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster1-shard-0&authSource=admin")
client.admin.authenticate(mongodb_id, mongodb_pw, mechanism='SCRAM-SHA-1')
db = client.user_data

logging.basicConfig()

def sendTextMessage(user_id, text):
	message = TextMessage("1", text)
	line_bot_api.push_message(user_id, message)

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def scheduled_job():
    print('This job is run every five seconds.')
    query = db["users"].find()
    print("DB count: %d" % query.count())
    # sendTextMessage("U171903a51154a9693c8c49fbce6af0d1", "time is up!")
    print('This job is finished.')

sched.start()
