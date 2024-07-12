from ext import app, db
from models import User

with app.app_context():

    db.drop_all()
    db.create_all()

    admin_user = User(username="I<3Racha", password="HardPassword2909", role="Admin")
    admin_user.create()