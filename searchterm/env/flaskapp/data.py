import sqlite3
conn = sqlite3.connect('prawsearchterm.db')
c = conn.cursor()

def Articles():
    c.execute('SELECT submURL, submTitle FROM searchTable ORDER BY submURL DESC' )
    entries = [dict(submURL=row[0], submTitle=row[1]) for row in c.fetchall()]
    
    return entries
