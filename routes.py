from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, ProductForm
from ext import app
from os import path
from models import Product, User
profiles = []

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", products=products, role="Admin")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data, role="Guest")
        new_user.create()
        return redirect("/login")
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    print("Received profile id", profile_id)
    return render_template("profile.html", user=profiles[profile_id])


@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product_details.html", product=product)


@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.img.data
        directory = path.join(app.root_path, "static", image.filename)
        image.save(directory)

        new_product.img = image.filename

        new_product.create()
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        product.save()
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)

    product.delete()

    return redirect("/")
