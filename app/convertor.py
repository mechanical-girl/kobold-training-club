import sqlite3

conn = sqlite3.connect('data/monsters.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS monsters''')
c.execute('''CREATE TABLE monsters(
                guid test,
                fid text,
                name text,
                cr text,
                size text,
                type text,
                tags text,
                section text,
                alignment text,
                environment text,
                ac int,
                hp int,
                init text,
                lair int,
                legendary int,
                named int,
                source text)''')

conn.commit()


with open('data/kfc master monster list - Monsters.tsv') as f:
    line = f.readline()
    print(line)
    while True:
        line = f.readline()
        if not line:
            break

        values = line.split("\t")
        c.execute('''INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (*values,))

    conn.commit()
