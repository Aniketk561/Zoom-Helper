# Zoom Helper Meeting Bot
A bot written in python that auto attends your classes offline as its hosted on heroku.

## 🚨Bot Commands

    /zoom              - Command to join Zoom Meeting
    /timetable         - Get timetable of scheduler
    /status            - Sends screenshot of the web page
    /restart           - Close all the opened window and restarts the script
    /timetable         - Sends Timetable of the day with schedule file.
    /disable_scheduler - Temporarily Disables Scheduler.
    /enable_scheduler  - Enables scheduler from previous disabled state.
    /help              - Gives List of commands on Telegram.

## Deploy to Heroku
**One Click Deploy**

<a href="https://heroku.com/deploy?template=https://github.com/wrecker3000/Zoom-Helper/">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>


1. First , Create Account On heroku .Also, create an Facebook account and login it on zoom and set it up.

2. Also Get Bot token from telegram thorugh BotFather ..

3. Click on deploy button below .Make sure You have logged in heroku and finished with fb setup.

4. In config env vars , put your bot token and facebook id password in username and password.

5. Deploy the bot and finish it up. Now u can send commands to your telegram bot to join zoom meetings.

6. You can Schedule Joining zoom meetings thorugh bot by using sending scheduled meesages feature of telegram.

## Deploying By CLI

* `git clone https://github.com/wrecker3000/Zoom-Helper/`
 * `cd Zoom-Helper`
 * `pip install -r requirements.txt`
 * `python chromium.py`
 * `heroku login -i`
 * `heroku create appname --buildpack heroku/python`
 * `heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver -a appname`
 *  `heroku buildpacks:add https://github.com/1337w0rm/heroku-buildpack-google-chrome -a appname`
 * `git init`
 * `heroku git:remote -a appname`
 * `git add .`
 * `git commit -am "Your commit message"`
 * `git push heroku master`
 * `heroku ps:scale worker=1`


>Note: Leaving of meeting is defined after 35 mins. If you want any other leaving time, define values on your own.


