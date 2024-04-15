from flask.cli import FlaskGroup

import sys
sys.path.append('./application/')

from user.handlers import app

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()