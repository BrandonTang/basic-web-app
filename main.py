import os
import hashlib
import sqlite3 as sql
from flask import Flask, render_template, request, session, url_for, redirect, flash
from models import *

# Initialize the app from Flask
app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Return the home page that displays all uploaded images and their captions.
    """
    logged_in = False
    if session.get('logged_in') is True:
        logged_in = True
    username = session.get('username')
    conn = sql.connect("appsec.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY post_id DESC")
    posts = cursor.fetchall()
    posts = [posts[i:i + 1] for i in range(0, len(posts), 1)]
    conn.commit()
    conn.close()
    posts_index = 0
    return render_template('index.html', posts=posts, posts_index=posts_index, logged_in=logged_in, username=username)


@app.route('/posts<int:posts_index>', methods=['GET', 'POST'])
def index_posts(posts_index):
    """
    Return the home page where the posts_index refers to the index of the set of 10 images showing from recently uploaded.
    """
    logged_in = False
    if session.get('logged_in') is True:
        logged_in = True
    username = session.get('username')
    conn = sql.connect("appsec.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY post_id DESC")
    posts = cursor.fetchall()
    posts = [posts[i:i + 1] for i in range(0, len(posts), 1)]
    conn.commit()
    conn.close()
    posts_index = posts_index
    return render_template('index.html', posts=posts, posts_index=posts_index, logged_in=logged_in, username=username)


@app.route('/delete_post<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    """
    Return the home page after deleting the selected post from the database and deleting it from the uploads folder.
    """
    conn = sql.connect("appsec.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE post_id = ?", (id,))
    post = cursor.fetchone()
    filename = str(id) + post[2]
    os.unlink("./static/uploads/" + filename)
    cursor.execute("DELETE FROM posts WHERE post_id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('.index'))


@app.route('/edit_post<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    """
    Return the home page after deleting the selected post from the database and deleting it from the uploads folder.
    """
    logged_in = False
    if session.get('logged_in') is True:
        logged_in = True
    username = session.get('username')
    conn = sql.connect("appsec.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE post_id = ?", (id,))
    post = cursor.fetchone()
    conn.commit()
    conn.close()
    if request.method == "POST":
        caption = request.form['caption']
        conn = sql.connect("appsec.db", timeout=10)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET caption = ? WHERE post_id = ?", (caption, id))
        conn.commit()
        conn.close()
        flash('Picture caption successfully edited!', category='success')
        return redirect(url_for('.index'))
    return render_template('edit_post.html', post=post, logged_in=logged_in, username=username)


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    """
    Return the page where users can upload images.
    """
    logged_in = False
    if session.get('logged_in') is True:
        logged_in = True
    username = session.get('username')
    if request.method == "POST":
        mimetype_list = ['image/png', 'image/jpeg', 'image/gif']
        image_file = request.files['upload_file']
        mimetype = image_file.mimetype
        if mimetype in mimetype_list:
            caption = request.form['caption']
            insert_post(username, image_file.filename, caption)
            conn = sql.connect("appsec.db", timeout=10)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE username = ? AND image = ? AND caption = ?",
                           (username, image_file.filename, caption))
            post = cursor.fetchone()
            post_id = post[0]
            conn.commit()
            conn.close()
            image_file.save("./static/uploads/" + str(post_id) + image_file.filename)
            flash('Image successfully uploaded!', category='success')
            return render_template('upload_image.html', logged_in=logged_in, username=username)
        else:
            flash('Uploaded file is an invalid type! Please try uploading again.')
            return render_template('upload_image.html', logged_in=logged_in, username=username)
    return render_template('upload_image.html', logged_in=logged_in, username=username)


@app.route('/login')
def login():
    """
    Return the login page that calls login_auth on submit.
    """
    return render_template('login.html')


@app.route('/login_auth', methods=['GET', 'POST'])
def login_auth():
    """
    Authenticates user credentials, creates session for user if valid, else redirects to login with flash message.
    """
    username = request.form['username']
    password = request.form['password']
    md5password = hashlib.md5(password.encode('utf-8')).hexdigest()
    conn = sql.connect("appsec.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, md5password))
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    if user:
        session['username'] = username
        session['logged_in'] = True
        flash('User successfully logged in!', category='success')
        return redirect(url_for('index'))
    else:
        flash('Invalid login or username or password.', category='error')
        return redirect(url_for('login'))


@app.route('/register')
def register():
    """
    Return the register page that calls register_auth on submit.
    """
    return render_template('register.html')


@app.route('/register_auth', methods=['GET', 'POST'])
def register_auth():
    """
    Checks if user already exists, redirects to register page if true, else creates new user.
    """
    username = request.form['username']
    password = request.form['password']
    md5password = hashlib.md5(password.encode('utf-8')).hexdigest()
    conn = sql.connect("appsec.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    if user:
        flash('User already exists.', category='error')
        return redirect(url_for('register'))
    else:
        insert_user(username, md5password)
        flash('User successfully registered! You may login now.', category='success')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """
    Logs out the user and removes information from session, then redirects to index page.
    """
    session.pop('username')
    session.pop('logged_in')
    flash('User successfully logged out.', category='success')
    return redirect('/')


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
