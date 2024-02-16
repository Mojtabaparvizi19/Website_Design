from flask import Flask, render_template, request
import requests
from smtplib import *
import os
email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/send_info", methods=["POST"])
def send_info():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    with SMTP(host="smtp.gmail.com", port=587) as my_connection:
        my_connection.starttls()
        my_connection.login(user="ace.amazoon@gmail.com", password=password)
        my_connection.sendmail(from_addr="ace.amazoon@gmail.com",
                               to_addrs="email",
                               msg=f"subject:You have new contact message\n\n"
                                   f"name: {name}\n"
                                   f"email: {email}\n"
                                   f"phone: {phone}\n"
                                   f"message: {message}")

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
