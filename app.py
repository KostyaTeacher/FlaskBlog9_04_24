from flask import Flask, render_template, abort, url_for, redirect, flash, request
from db import get_db_connection

app = Flask(__name__)
app.config["SECRET_KEY"] = "AprioriKS"

@app.get("/")
def index():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    return render_template("index.html", posts=posts)

@app.get("/<int:post_id>")
def get_post(post_id):
    post = return_post(post_id)
    if post is None:
        abort(404)
    return render_template("post.html", post=post)


def return_post(post_id):
    connection = get_db_connection()
    post = connection.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()
    connection.close()
    return post


@app.get("/create/")
def get_create():
    return render_template("create.html")

@app.post("/create/")
def post_create():
    title = request.form["title"]
    content = request.form["content"]
    if not title or len(title) < 5:
        flash("Title is required!")
        return render_template("create.html")
    else:
        connection = get_db_connection()
        connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        connection.commit()
        connection.close()
        return redirect(url_for("index"))

@app.get("/<int:post_id>/edit")
def get_edit(post_id):
    post = return_post(post_id)
    return render_template("edit.html", post=post)

@app.post("/<int:post_id>/edit")
def post_edit(post_id):
    post = return_post(post_id)
    title = request.form["title"]
    content = request.form["content"]
    if not title or len(title) < 5:
        flash("Title is required!")
        return render_template("edit.html", post=post)
    else:
        connection = get_db_connection()
        connection.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, post_id))
        connection.commit()
        connection.close()
        return redirect(url_for("index"))

@app.post("/<int:post_id>/delete")
def post_delete(post_id):
    post = return_post(post_id)
    connection = get_db_connection()
    connection.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()
    return redirect(url_for("index"))





if __name__ == '__main__':
    app.run(port = 8080, debug=True)