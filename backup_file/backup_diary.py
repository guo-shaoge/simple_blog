#/usr/bin/python
import sqlite3
import os

DATABASE='../flaskr.db'

def backup(c):
	l = c.execute('select * from entries')
	for item in l:
		i = item[0]
		title = item[1].encode('gb2312')
		body = item[2].encode('gb2312')
		time = item[3].encode('gb2312')
		with open(os.path.join('./backup_file/real_files/', title+'_'+time), 'w') as f:
			f.write('title: '+title)
			f.write('\n')
			f.write('date: '+time)
			f.write('\n\n')
			f.write(body)

if __name__=='__main__':
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	backup(c)
