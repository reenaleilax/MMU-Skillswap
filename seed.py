from app import app, db, User, Skill

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = [
            User(email="s1@stu.mmu.ac.uk", faculty="Science", bio="Loves data."),
            User(email="s2@stu.mmu.ac.uk", faculty="Business", bio="Into startups."),
            User(email="s3@stu.mmu.ac.uk", faculty="Arts", bio="Creative mind."),
            User(email="s4@stu.mmu.ac.uk", faculty="Engineering", bio="Builds stuff."),
            User(email="s5@stu.mmu.ac.uk", faculty="Health", bio="Cares about people."),
            User(email="s6@stu.mmu.ac.uk", faculty="Law", bio="Future lawyer."),
        ]
        db.session.add_all(users)
        db.session.commit()
