from flask import Blueprint,render_template

page_bp=Blueprint("page",__name__)

@page_bp.route("/")
def home():
    return render_template("index.html")

@page_bp.route("/loginpage")
def loginpage():
    return render_template("login.html")

@page_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")