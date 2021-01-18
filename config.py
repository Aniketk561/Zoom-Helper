import os
class Config(object):
	APP_NAME = os.environ.get('APP_NAME')
	BOT_TOKEN = os.environ.get('BOT_TOKEN')
	USERNAME = os.environ.get('FACEBOOK_ID')
	PASSWORD = os.environ.get('PASSWORD')
	SCHEDULE = str(os.environ.get('SCHEDULE'))
	USERID = os.environ.get('USER_ID')
	URL = os.environ.get('URL')