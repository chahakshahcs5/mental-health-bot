# importing from flask module the Flask class, the render_template function, the request function, url_for
# and redirect function to redirect to index home page after updating the app database
from flask import Flask, render_template, request, url_for, redirect, make_response

# Mongoclient is used to create a mongodb client, so we can connect on the localhost
# with the default port
from pymongo import MongoClient

# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId

# Instantiate the Flask class by creating a flask application
app = Flask(__name__)
# Create the mongodb client
client = MongoClient("localhost", 27017)


# Get and Post Route
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return redirect(url_for("index"))
    # Check if User is authenticated by checking for email cookie
    email = request.cookies.get("email")
    if email:
        # User is authenticated, you can retrieve user information using email
        user = User.find_one({"email": email})
        return render_template("index.html")
    return redirect(url_for("login"))


# Get and Post Route
@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.find_one(
            {
                "email": email,
            }
        )
        print(user)
        if user:
            error = "Email already exist. Please use different Email."
            return render_template("register.html", error=error)
        else:
            User.insert_one({"email": email, "password": password})
            return redirect(url_for("login"))
    return render_template("register.html")


# Get and Post Route
@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        # Query the database for the user with the provided username
        user = User.find_one({"email": email})
        # Check if the user exists and the password matches
        if user and user["password"] == password:
            response = make_response(redirect(url_for("index")))
            response.set_cookie("email", user["email"])
            return response
        else:
            # Authentication failed, show an error message
            error = "Invalid email or password. Please try again."
            return render_template("login.html", error=error)
    return render_template("login.html")


db = client.mental_health  # creating your flask database using your mongo client
User = db.users  # creating a collection called "users"
