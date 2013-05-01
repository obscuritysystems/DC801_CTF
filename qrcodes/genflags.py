import sqlite3 as lite
import os
import sys 
import hmac
import time
from hashlib import sha256
from hashlib import sha1
from base64 import b64encode, b64decode
from qrcode import *


import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

salt = '1asdf2Mna34Ag'
con = lite.connect('/opt/openwest.db')
cur = con.cursor()
cur.execute("create TABLE if not exists flags ( id INTEGER PRIMARY KEY AUTOINCREMENT, flag TEXT, notes TEXT)")
cur.execute("create TABLE if not exists captures ( id INTEGER PRIMARY KEY AUTOINCREMENT,  flag_id INTEGER, captured DATETIME)")
con.commit()
#cur = con.cursor()
#cur.execute('INSERT INTO flag(flag,notes) values (?,?,?)',())
#con.commit()

flag_directory = '/tmp/flags/'

def generate_flags():
    salt = os.urandom(team_salt_length).encode('hex')
    for i in range(1,100):
        flag = hmac.new(salt,randomword(128),sha1).hexdigest()
        print flag
        cur = con.cursor()
        cur.execute('INSERT INTO flags(flag,notes) values (?,?)',(flag,'openwest'))
        con.commit()



def generate_qrcodes():
    
    cur = con.cursor()
    cur.execute("select * from flags")
    rows = cur.fetchall()
    #print rows
    for flag in rows:
        print flag[1]
        qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
        qr.add_data(flag[1])
        qr.make() # Generate the QRCode itself
        im = qr.make_image()

        if not os.path.exists(flag_directory):
            os.makedirs(flag_directory)

        filename = flag_directory + 'openwest_'+str(flag[0])+'.png'
        im.save(filename)
        print filename

'''
    for flag in flags_a:

        qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
        qr.add_data(flag['text'].strip())
        qr.make() # Generate the QRCode itself
        # im contains a PIL.Image.Image object
        im = qr.make_image()

        if not os.path.exists(flag_directory +"/"+ flag['name']):
            os.makedirs(flag_directory + "/" + flag['name'])
        # To save it
        filename = "./"+flag_directory +"/"+flag['name']+ "/" +str(flag['id']) +"_"+str(salt)+ str(timestamp) + '.png'
       
        
        im.save(filename)
        print "\n"
        print flag['text']
        print filename 
'''
generate_qrcodes()
