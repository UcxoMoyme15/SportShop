from ext import app

if __name__ == "__main__":
    from routes import home, about, contact, login, signup, profile, create_product, delete_product, edit_product
    app.run(debug=True)

