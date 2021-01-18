import logging
from config import Config
from bot import updater, browser
from telegram.ext import run_async
from telegram import ChatAction
import os
import time
import pickle
from os import execl
from sys import executable
import csv
import datetime
from bot.zoom import joinZoom

meeting_list = list()

def convertTime(string_time):
    hour = string_time.split(':')[0]
    minute = string_time.split(':')[1]
    datetime_str = f'{datetime.date.today().strftime("%m/%d/%y")} {hour}:{minute}:00'
    datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    return datetime_object

class Meeting():
    def __init__(self, name, day, time, mid, mpass):
        self.name = name
        self.time = convertTime(time)
        self.mid = mid
        self.mpass = mpass

def getTodayMeetings():
    try:
        with open('bot/zoom.csv') as file:
            read = csv.reader(file, delimiter=',')
            for row in read:
                if row[1] == datetime.datetime.today().strftime('%A'):
                    meeting = Meeting(row[0], row[1], row[2], row[3], row[4])
                    meeting_list.append(meeting)
    except:
        print("Zoom schedule not found. Disabling Scheduler")
        Config.SCHEDULE = 'False'

def zoom(context):
    logging.info("DOING") 
    userId = Config.USERID
    url_meet = context.job.context[0]
    passStr = context.job.context[1]
    context.bot.send_message(chat_id=userId, text="TIME FOR MEETING: " + str(context.job.context[2]))
    joinZoom(context, url_meet, passStr, userId)

def timeTable(update, context):
    if Config.SCHEDULE == 'False':
        context.bot.send_message(chat_id=update.message.chat_id, text="Scheduler is Disabled")
    if Config.SCHEDULE == 'True':
        text = "Today's Meeting: \n \n"
        for row in meeting_list:
            text+=str(row.name) + " at " + str(row.time).split()[1] + "\n"
        context.bot.send_message(chat_id=update.message.chat_id, text=text)
        try:
            context.bot.send_document(chat_id=update.message.chat_id, document=open('bot/zoom.csv', 'rb'), caption="Entire Schedule", timeout = 120)
        except:
            pass

def zJobQueue():
    logging.info("Adding Timetable Data")
    getTodayMeetings()
    j = updater.job_queue    
    for row in meeting_list:
        secs = (row.time - datetime.datetime.now()).total_seconds()
        if(secs > 0):
            print(secs)
            j.run_once(zoom, secs, context=(row.mid, row.mpass, row.name))
