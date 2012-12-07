import os
import gnupg
import MySQLdb as mdb
import hmac
import time
from hashlib import sha256
from base64 import b64encode, b64decode
from qrcode import *
#from time import time
#from operator import xor


gnupg_home = '/home/dc801ctf'
db_user = 'root'
db_ip = 'localhost'
db_password = ''
db_database = 'dc801_ctf'
team_salt_length = 32
flag_directory = 'qr_flags'

setup_menu_run = True;
#gpg setup
gpg = gnupg.GPG(gnupghome = gnupg_home)

#mysql conneciton setup
con = mdb.connect(db_ip, db_user, db_password, db_database)

def encrypt(text):
	encrypted_data = gpg.encrypt(text, 'root@dc801.org')
	return str(encrypted_data)


def print_flags(flags):
	for flag in flags:
		print flag

def get_flags(passphrase):

	with con: 

		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT * FROM flags")
		rows = cur.fetchall()	

		flags = [] 
		for row in rows:
			flag = gpg.decrypt(row['text'],passphrase=passphrase).data
			row['text'] = flag
			flags.append(row)

		return flags



def enter_flag():

	flag  = raw_input('Enter Flag Text:')
	print "Saving Flag: %s to database." % (flag) 

	with con:    
		cur = con.cursor()
		encrypted_flag = encrypt(flag) 
		cur.execute("INSERT INTO flags (created,text,points) values (NOW(),%s,'1000.00')", (encrypted_flag))
		print "Number of rows effected: %d" % cur.rowcount


def enter_team():
	team_name  = raw_input('Enter Team Name:')
	print "Saving Team: %s to database." % (team_name) 

	salt = os.urandom(team_salt_length).encode('hex')
	with con:    
		cur = con.cursor()
		cur.execute("insert into teams (created,name,salt) values (NOW(),%s,%s);", (team_name,salt))
		print "Number of rows effected: %d" % cur.rowcount

def delete_team(id):

	with con: 
		cur = con.cursor()
		cur.execute("delete from teams where id = %s", (id))
		print "Number of rows effected: %d" % cur.rowcount

	

def generate_qrcodes():

	entered_passphrase = raw_input('Enter Passphrase to view flags: ')

	if not os.path.exists(flag_directory):
	    os.makedirs(flag_directory)

	flags = get_flags(entered_passphrase)	
	teams = get_teams()

	timestamp = int(time.time()) 

	for team in teams:
			print "--------------------------------"
			print 'Team name: '+ team['name']
			print "--------------------------------"
			print "\n"

		for flag in flags:
			qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
			qr.add_data(flag)
			qr.make() # Generate the QRCode itself

			# im contains a PIL.Image.Image object
			im = qr.make_image()

			# To save it
		
			salt = os.urandom(team_salt_length).encode('hex')
			filename = "./"+flag_directory +"/"+team['name']+ "/" +str(flag['id']) +"_"+str(salt)+ str(timestamp) + '.png'
			im.save(filename)
			print "\n"
			print flag['text']
			print filename



def get_teams():

	with con: 
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT * FROM teams")
		rows = cur.fetchall()
		return rows

def list_teams():
	teams = get_teams()
	print teams
	
def generate_team_hashes():
	
	not_decrypted = True

	while not_decrypted:

		entered_passphrase = raw_input('Enter Passphrase to decrypt flags: ')

		flags = get_flags(entered_passphrase)
		print_flags(flags)

		proceed = raw_input('Did Flags Look Decrypted? [Y/N]')

		if proceed.lower().find('y') != -1:
			not_decrypted = False
			master_salt = raw_input('Enter Master Salt:')
			teams = get_teams()

			for team in teams:
				print "--------------------------------"
				print 'Team name: '+ team['name']
				print "--------------------------------"
				print "\n"

				for flag in flags:
					
					print  'Flag Name: ' + flag['text']
					teamflag_hash  = hmac.new(team['salt'],flag['text'],sha256).hexdigest()
					stored_team_hash = hmac.new(master_salt,teamflag_hash,sha256).hexdigest()
					print teamflag_hash
					print stored_team_hash

	
		

while setup_menu_run:
	os.system('clear')
	print "DC801 CTF Setup ~ by Nemus"
	print "1: Enter Flags"
	print "2: List Flags"
	print "3: Create Team"
	print "4: List Team"
	print "5: Delete Team"
	print "6: Generate Team Hashes"
	print "7: Genearate Flag QRCodes"
	print "q: Quit"

	setup_menu =raw_input('---> ')

	if setup_menu == '1':
		os.system('clear')
		enter_flag()
		raw_input("Press Enter to continue...")
	elif setup_menu == '2':
		os.system('clear')
		entered_passphrase = raw_input('Enter Passphrase to view flags: ')
		flags = get_flags(entered_passphrase)
		print_flags(flags)
		raw_input("Press Enter to continue...")
	elif setup_menu == '3':
		os.system('clear')
		enter_team()
		raw_input("Press Enter to continue...")
	elif setup_menu == '4':
		os.system('clear')
		list_teams()
		raw_input("Press Enter to continue...")
	elif setup_menu == '5':
		os.system('clear')
		list_teams()
		team_id = raw_input('Enter team ID to delete')
		delete_team(team_id)
		raw_input("Press Enter to continue...")
	elif setup_menu == '6':
		os.system('clear')
		generate_team_hashes()
		raw_input("Press Enter to continue...")
	elif setup_menu == '7':
		os.system('clear')
		generate_qrcodes()
		raw_input("Press Enter to continue...")
	elif setup_menu == 'q':
		setup_menu_run = False

