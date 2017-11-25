# manage.py

import unittest

from flask_script import Manager

from project import created_app, db
from project.api.models import User

app = created_app()
manager = Manager(app)


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='mahfuz', email="mahfuz@endecoder.com"))
    db.session.add(User(username='shawon', email="shawon@endecoder.com"))
    db.session.add(User(username='alamin', email="alamin@mah3uz.com"))
    db.session.add(User(username='admin', email="admin@endecoder.com"))
    db.session.commit()

if __name__ == '__main__':
    manager.run()

