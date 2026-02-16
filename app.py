from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skillswap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# MODELS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    faculty = db.Column(db.String(120))
    bio = db.Column(db.Text)
    skills = db.relationship("Skill", backref="user", lazy=True)

class Skill(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# ROUTE

@app.route("/profile/<int:user_id>/edit", methods=["GET", "POST"])
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.faculty = request.form["faculty"]
        user.bio = request.form["bio"]

        skills_text = request.form["skills"]
        names = [s.strip() for s in skills_text.split(",") if s.strip()]

        Skill.query.filter_by(user_id=user.id).delete()

        for name in names:
            db.session.add(Skill(name=name, user=user))

        db.session.commit()
        return redirect(url_for("edit_profile", user_id=user.id))

    return render_template("profile_edit.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
