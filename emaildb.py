import sqlite3

conn =  sqlite3.connect(r"C:\Victor\python_sql\sql1.db")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (email TEXT, count INTEGER)')

# fname = input('Enter file name: ')
#
# if (len(fname) < 1): fname = 'mail.txt'

fname = 'mail.txt'

fh = open(fname)

for line in fh:
    cur.execute('Select count From Counts where email = ? ', (line,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts(email, count) VALUES (?,1)',(line,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (line,))
    conn.commit()

sqlstr = "SELECT email, count FROM Counts"

for row in cur.execute(sqlstr):
    print (str(row[0]))

cur.close()