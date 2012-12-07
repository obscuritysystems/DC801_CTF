from bot import Bot
import smtplib
import re


class FlagBotAI(Bot):

	def __init__(self):

		self.host=''
		self.channel = ''
		self.nicks = 'FlagBot'
		self.password = ''
		self.host_name = 'Obscurity Systems'
		self.dsn = "host=localhost dbname=ircbot user=ircman password="
		self.sheep = True;
		self.debug = True;
		self.database_enabled = True;
		self.smtp_server = ''
	
	def custom_ai(self,text,timestamp):
