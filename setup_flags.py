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
db_password = '8a5kSjQ1kK0JUlmzKiH2S8'
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

def get_teamflags(passphrase):
	
	#select count(flags.id),teams.name from teams join flags on flags.team_owner_id = teams.id;
	with con: 

		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("select * from teams join flags on flags.team_owner_id = teams.id")
		rows = cur.fetchall()	

		teamsandflags = [] 
		for row in rows:
			flag = gpg.decrypt(row['text'],passphrase=passphrase).data
			row['text'] = flag
			teamsandflags.append(row)

		return teamsandflags
		

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
	try:
		flag  = raw_input('Enter Flag Text:')
		team_id = raw_input('Enter Team ID:')
		print "Saving Flag: %s to database." % (flag) 

		with con:    
			cur = con.cursor()
			encrypted_flag = encrypt(flag.strip()) 
			cur.execute("INSERT INTO flags (created,text,points,team_owner_id) values (NOW(),%s,'1000.00',%s)", (encrypted_flag,team_id))
			print "Number of rows effected: %d" % cur.rowcount

	except:
		print "Add failed..."


def setup_gpg(email,passphrase):

	input_data = gpg.gen_key_input(name_email=email,passphrase=passphrase)
	key = gpg.gen_key(input_data)
	print key

def enter_team():
	team_name  = raw_input('Enter Team Name:')
	print "Saving Team: %s to database." % (team_name.strip()) 

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

	flags_and_teams = get_teamflags(entered_passphrase)	
	teams = get_teams()

	timestamp = int(time.time()) 

	for flag in flags_and_teams:

		qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
		qr.add_data(flag['text'].strip())
		qr.make() # Generate the QRCode itself
		# im contains a PIL.Image.Image object
		im = qr.make_image()

		if not os.path.exists(flag_directory +"/"+ flag['name']):
			os.makedirs(flag_directory + "/" + flag['name'])
		# To save it
		salt = os.urandom(team_salt_length).encode('hex')
		filename = "./"+flag_directory +"/"+flag['name']+ "/" +str(flag['id']) +"_"+str(salt)+ str(timestamp) + '.png'
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

def save_team_hash(flag_id,team_id,flag_hash):
	with con:    
		cur = con.cursor()
		cur.execute("insert into flag_hashes(submission_team_id,flag_id,hash) values(%s,%s,%s);", (team_id,flag_id,flag_hash))

def get_teams_capturable_flags(id,passphrase):

	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("select * from flags where team_owner_id != %s",(id))
		rows = cur.fetchall()
		flags = []
		for row in rows:
			flag = gpg.decrypt(row['text'],passphrase=passphrase).data
			row['text'] = flag
			flags.append(row)

		return flags

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
			print teams 
			for team in teams:
				print "--------------------------------"
				print 'Team name: '+ team['name']
				print "--------------------------------"
				print "\n"
				flags = get_teams_capturable_flags(team['id'],entered_passphrase)
				print flags
				for flag in flags:
					
					print  'Flag Name: ' + flag['text']
					teamflag_hash  = hmac.new(team['salt'],flag['text'],sha256).hexdigest()
					stored_team_hash = hmac.new(master_salt,teamflag_hash,sha256).hexdigest()
					print teamflag_hash
					print stored_team_hash
					save_team_hash(flag['id'],team['id'],stored_team_hash)



def manual_check_flags(team_salt):
#select * from flag_hashes where hash =
	with con:
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("select * from flag_hashes where hash = %s",(master_salt))
		rows = cur.fetchall()
		flags = []
		for row in rows:
			flag = gpg.decrypt(row['text'],passphrase=passphrase).data
			row['text'] = flag
			flags.append(row)

		return flags

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
	print "8: Setup GPG KEY"
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
	elif setup_menu == '8':
		os.system('clear')
		email = raw_input("Enter e-mail:")
		passphrase = raw_input("Enter passphrase")
		setup_gpg(email,passphrase)
		raw_input("Press Enter to continue...")
	elif setup_menu == 'q':
		setup_menu_run = False

