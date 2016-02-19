import sqlite3

DATABASE='../flaskr.db'

conn = sqlite3.connect(DATABASE)
c = conn.cursor()
l = c.execute('select * from entries')
for item in l:
	i = item[0]
	title = item[1]
	body = item[2]
	time = item[3]
	with open(title, 'w') as f:
		f.write('title: '+title.encode('gb2312'))
		f.write('\n')
		f.write('date: '+time.encode('gb2312'))
		f.write('\n\n')
		f.write(body.encode('gb2312'))
