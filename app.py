from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)
app.config.from_pyfile('config.cfg')



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/logout')
def logout():
    return render_template('projects.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run()