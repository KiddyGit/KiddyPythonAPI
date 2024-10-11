from flask import Flask
from image_routes import image_bp
app = Flask(__name__)


app.register_blueprint(image_bp)


@app.route('/')
def hello():
    return "<center><h1>Hello, World!</h1></center>"

# Register the Blueprints




if __name__ == '__main__':
    app.run()
