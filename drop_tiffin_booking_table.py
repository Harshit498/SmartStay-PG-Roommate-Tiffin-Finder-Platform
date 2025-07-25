import sqlite3

conn = sqlite3.connect('instance/site.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS tiffin_booking')
conn.commit()
conn.close()
print('Dropped tiffin_booking table.') 