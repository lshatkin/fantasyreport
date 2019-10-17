from flask_script import Manager
from fantasyApp.services.historical import getInfo
from fantasyApp import app

manager = Manager(app)

@manager.command
def historical():
    getInfo()

if __name__ == "__main__":
    manager.run()