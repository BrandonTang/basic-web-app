import sqlite3 as sql


def insert_user(username, password):
    con = sql.connect("appsec.db", timeout=10)
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?,?)",
                (username, password))
    con.commit()
    con.close()


def insert_post(username, image, caption):
    con = sql.connect("appsec.db", timeout=10)
    cur = con.cursor()
    cur.execute("INSERT INTO posts (username, image, caption) VALUES (?,?,?)",
                (username, image, caption))
    con.commit()
    con.close()
