from manager import app
from views import ifixit
from commands.fixit import GetFixit
from commands.icecat import GetIcecat
app.cli.add_command(GetFixit)
app.cli.add_command(GetIcecat)
app.register_blueprint(ifixit)


if __name__ == '__main__':
    app.run()
