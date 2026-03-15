from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skillswap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class SkillCategory(Enum):
    TECHNICAL = "Technical"
    CREATIVE = "Creative"
    ACADEMIC = "Academic"


user_skills = db.Table(
    "user_skills",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    faculty = db.Column(db.String(120))
    bio = db.Column(db.Text)
    skills = db.relationship(
        "Skill",
        secondary=user_skills,
        backref=db.backref("users", lazy="dynamic"),
        lazy="dynamic",
    )


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False, default=SkillCategory.TECHNICAL.value)


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    users = User.query.all()
    return render_template("dashboard.html", users=users)


@app.route("/profile/<int:user_id>/edit", methods=["GET", "POST"])
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.name = request.form.get("name", "")
        user.faculty = request.form.get("faculty", "")
        user.bio = request.form.get("bio", "")

        # clear existing skills first
        for skill in user.skills.all():
            user.skills.remove(skill)

        skill_names = [s.strip() for s in request.form.get("skills", "").split(",") if s.strip()]
        for skill_name in skill_names:
            skill = Skill.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name, category="Technical")
                db.session.add(skill)
                db.session.flush()
            user.skills.append(skill)

        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("profile_edit.html", user=user)

@app.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    if keyword:
        users = User.query.join(User.skills).filter(
            Skill.name.ilike(f"%{keyword}%") |
            User.name.ilike(f"%{keyword}%") |
            User.faculty.ilike(f"%{keyword}%") |
            User.bio.ilike(f"%{keyword}%")
        ).distinct().all()
    else:
        users = User.query.all()
    return render_template("dashboard.html", users=users, keyword=keyword)

@app.route("/skill/add", methods=["GET", "POST"])
def add_skill():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        skill_name = request.form.get("skill_name", "").strip()
        category = request.form.get("category", SkillCategory.TECHNICAL.value)

        if skill_name and user_id:
            user = User.query.get_or_404(user_id)
            skill = Skill.query.filter_by(name=skill_name).first()
            if not skill:
                skill = Skill(name=skill_name, category=category)
                db.session.add(skill)
                db.session.flush()
            if skill not in user.skills.all():
                user.skills.append(skill)
            db.session.commit()

        return redirect(url_for("dashboard"))

    users = User.query.all()
    return render_template("add_skill.html", users=users, categories=SkillCategory)

if __name__ == "__main__":
    app.run(debug=True)
