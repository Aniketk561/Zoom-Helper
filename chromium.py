import logging
import os
import time
from telegram.ext import CommandHandler, Job, run_async
from telegram import ChatAction
from config import Config
import requests
from selenium.webdriver.common.keys import Keys
from os import execl
from sys import executable
from bot import updater, dp, browser
from bot.zoom import zoom
from bot.zoom_schedule import timeTable
if Config.SCHEDULE == 'True':
    from bot.zoom_schedule import zJobQueue
    url = Config.URL
    r = requests.get(url, allow_redirects=True)
    try:
        os.remove('bot.zoom.csv')
    finally:
        open('bot/zoom.csv', 'wb').write(r.content)

userId = Config.USERID
usernameStr = Config.USERNAME
passwordStr = Config.PASSWORD
appnameStr = Config.APP_NAME

@run_async
def exit(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    try:
        browser.find_element_by_xpath('//html').click()
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="wc-footer"]/div/div[3]/div/button').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="wc-footer"]/div[2]/div[2]/div[3]/div/div/button').click()
        time.sleep(2)
    except:
        pass
    browser.save_screenshot("ss.png")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'),caption="Exiting..!!", timeout = 120)
    os.remove('ss.png')
    browser.quit()
    execl(executable, executable, "chromium.py")

@run_async
def help(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if not os.access("bot/disabled_zoom", os.F_OK) and not os.access("bot/zoom.csv", os.F_OK):
        context.bot.send_message(chat_id=update.message.chat_id, text="\
            List of notes in Bot: \n-/help \n-/exit \n-/status \n-/zoom <meetingid> <password>")
    if os.access("bot/disabled_zoom", os.F_OK) or os.access("bot/zoom.csv", os.F_OK):
        context.bot.send_message(chat_id=update.message.chat_id, text="\
            List of notes in Bot: \n-/help \n-/exit \n-/status \n-/disable_schedule \n-/enable_schedule \n-/timetable \n-/zoom <meetingid> <password>")

@run_async
def disable_schedule(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if Config.SCHEDULE == 'False':
        context.bot.send_message(chat_id=update.message.chat_id, text="Scheduler is already disabled")
    if Config.SCHEDULE == 'True':
        try:
            browser.get('https://id.heroku.com/login')
            browser.find_element_by_id('email').send_keys(usernameStr)
            browser.find_element_by_id('password').send_keys(passwordStr)
            browser.find_element_by_xpath('//*[@id="login"]/form/button').click()
            time.sleep(7)
            browser.get('https://dashboard.heroku.com/apps/' + appnameStr + '/settings')
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/div[5]/main/div[2]/div[2]/ul/li[2]/div/div[2]/div/button').click()
            time.sleep(3)
            browser.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[5]/main/div[2]/div[2]/ul/li[2]/div/div[2]/div/div/form/table/tbody/tr[5]/td[3]/button[1]').click()
            time.sleep(3)
            schedule = browser.find_element_by_id('config-var-value')
            schedule.clear()
            schedule.send_keys('False')
            browser.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
            context.bot.send_message(chat_id=update.message.chat_id, text="Disabled Schedule!")
            browser.quit()
            execl(executable, executable, "chromium.py")
        except Exception as e:
            print(str(e))
            context.bot.send_message(chat_id=update.message.chat_id, text="Server Down. Check with Admin")

@run_async
def enable_schedule(update, context):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if Config.SCHEDULE == 'True':
        context.bot.send_message(chat_id=update.message.chat_id, text="Scheduler is already Enabled")
    if Config.SCHEDULE == 'False':
        try:
            browser.get('https://id.heroku.com/login')
            browser.find_element_by_id('email').send_keys(usernameStr)
            browser.find_element_by_id('password').send_keys(passwordStr)
            browser.find_element_by_xpath('//*[@id="login"]/form/button').click()
            time.sleep(7)
            browser.get('https://dashboard.heroku.com/apps/' + appnameStr + '/settings')
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/div[5]/main/div[2]/div[2]/ul/li[2]/div/div[2]/div/button').click()
            time.sleep(3)
            browser.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[5]/main/div[2]/div[2]/ul/li[2]/div/div[2]/div/div/form/table/tbody/tr[5]/td[3]/button[1]').click()
            time.sleep(3)
            schedule = browser.find_element_by_id('config-var-value')
            schedule.clear()
            schedule.send_keys('True')
            browser.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
            context.bot.send_message(chat_id=update.message.chat_id, text="Enabled Schedule!")
            browser.quit()
            execl(executable, executable, "chromium.py")
        except Exception as e:
            print(str(e))
            context.bot.send_message(chat_id=update.message.chat_id, text="Server Down. Check with Admin")

@run_async
def status(update, context):
    browser.save_screenshot("ss.png")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), timeout = 120)
    os.remove('ss.png')

def main():
    dp.add_handler(CommandHandler("zoom", zoom))
    dp.add_handler(CommandHandler("help", help))
    if Config.SCHEDULE == 'True':
        zJobQueue()
        dp.add_handler(CommandHandler("timetable", timeTable))
    dp.add_handler(CommandHandler("disable_schedule", disable_schedule))
    dp.add_handler(CommandHandler("enable_schedule", enable_schedule))
    dp.add_handler(CommandHandler("exit", exit))
    dp.add_handler(CommandHandler("status", status))
    logging.info("Bot started")
    updater.start_polling()

if __name__ == '__main__':
    main()
