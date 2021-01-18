import logging
from config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bot import updater, browser
from telegram.ext import run_async
from telegram import ChatAction
import os
import time
from os import execl
from sys import executable

userId = Config.USERID
usernameStr = Config.USERNAME
passwordStr = Config.PASSWORD
k=0
audio=k
a=k

def joinZoom(context, url_meet, passStr, userId):

    def audioexit(context):
        global k
        global audio
        global a
        if(k>=35):    #meeting exit sequence
            try:
                browser.save_screenshot("ss.png")
                context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
                os.remove('ss.png')
            except:
                pass
            context.bot.send_message(chat_id=userId, text="Exiting Meeting")
            browser.quit()
            execl(executable, executable, "chromium.py")
        if(audio == "Unmute"):
            a+=1
            try:
                browser.find_element_by_xpath('//*[@id="wc-container-left"]/div[4]/div/div/div/div[1]').click()
                number = browser.find_element_by_xpath('//*[@id="wc-footer"]/div/div[2]/button[1]/div/div/span').text
                print(int(number))
                if(int(number) <10 and a>=5):
                    try:
                        browser.save_screenshot("ss.png")
                        context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
                        os.remove('ss.png')
                    except:
                        pass
                    context.bot.send_message(chat_id=userId, text="Your Meeting has ended early after " + str(k) + " minutes." + "\nExiting Meeting!")
                    browser.quit()
                    execl(executable, executable, "chromium.py")
            except:
                pass
        if(audio != "Unmute"):
            try:
                try:
                    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[1]/span').text
                except:
                    browser.refresh()
                    time.sleep(10)
                browser.find_element_by_xpath('//*[@id="voip-tab"]/div/button').click()
                time.sleep(2)
                browser.find_element_by_xpath('//*[@id="wc-footer"]/div/div[2]/button[1]').click()
                time.sleep(3)
                while(audio != "Unmute"):
                    audio = str(browser.find_element_by_xpath('//*[@id="wc-container-right"]/div/div[2]/div/button[2]').text)
                    if(audio == "Mute"):
                        browser.find_element_by_xpath('//*[@id="wc-container-right"]/div/div[2]/div/button[2]').click()
                        time.sleep(5)
                browser.save_screenshot("ss.png")
                context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
                context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), caption="Joinied with Audio", timeout = 120).message_id
                os.remove('ss.png')
                time.sleep(5)
            except:
                if(k>=20):
                    try:
                        browser.save_screenshot("ss.png")
                        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
                        context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
                        os.remove('ss.png')
                    except:
                        pass
                    context.bot.send_message(chat_id=userId, text="Seems Like This Meeting is Not Today.")
                    browser.quit()
                    execl(executable, executable, "chromium.py")
        k+=1
    try:
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.TYPING)
        browser.get('https://zoom.us/facebook_oauth_signin')
        browser.find_element_by_id('email').send_keys(usernameStr)
        browser.find_element_by_id('pass').send_keys(passwordStr)
        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')
        browser.find_element_by_id('loginbutton').click()
        time.sleep(4)
        try:
            browser.find_element_by_xpath('//*[@id="platformDialogForm"]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/button[2]').click()
        except:
            pass
        time.sleep(4)
        context.bot.send_message(chat_id=userId, text="Logged In!")
        browser.get('https://zoom.us/wc/join/'+ url_meet+ '?action=join&pwd='+ passStr)
        time.sleep(5)
        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), timeout = 120).message_id
        os.remove('ss.png')
        browser.find_element_by_xpath('//*[@id="joinBtn"]').click()
        time.sleep(5)
        browser.save_screenshot("ss.png")
        context.bot.send_chat_action(chat_id=userId, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_photo(chat_id=userId, photo=open('ss.png', 'rb'), caption="Attending Your Meeting", timeout = 120).message_id
        os.remove('ss.png')
    except Exception as e:
        context.bot.send_message(chat_id=userId, text="Error Occurred Please Check")
        print(str(e))
        browser.quit()
        execl(executable, executable, "chromium.py")
    logging.info("DONE")
    j = updater.job_queue
    j.run_repeating(audioexit, 60, 0)

@run_async
def zoom(update, context):
    logging.info("DOING")
    url_meet = update.message.text.split()[1]
    passStr = update.message.text.split()[2]
    userId = update.message.chat_id
    joinZoom(context, url_meet, passStr, userId)