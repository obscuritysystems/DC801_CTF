import sqlite3 as lite

old_db_con = lite.connect('/opt/db/openwest.db')
old_db_cur = old_db_con.cursor()

old_db_cur.execute("SELECT * from flags")
rows = old_db_cur.fetchall()

new_db_con = lite.connect('/opt/db/dc801.db')
new_db_cur = new_db_con.cursor()
for row in rows:
    new_db_cur.execute('INSERT INTO ctf_flag(flag,notes,game_id) values (?,?,?)',(row[1],row[2],0))
    new_db_con.commit()
    print row

