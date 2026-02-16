from app import app, db, User, Skill

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
