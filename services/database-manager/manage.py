from flask.cli import FlaskGroup

import sys
sys.path.append('./application/')

from database.server import app, db
from database.db_actuator import seed

cli = FlaskGroup(app)

@cli.command("verify_db")
def verify_db():
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_database():
    seed(app, db)

if __name__ == "__main__":
    cli()