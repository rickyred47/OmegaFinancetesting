from flask import Flask

app = Flask(__name__)

from routes import loginaccess

loginaccess.setup_page_routing(app)

if __name__ == '__main__':
    app.run()
