from flask import Flask, render_template, request, redirect, url_for, make_response
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create uploads folder if not exists

# ─── Person 1: Routes + URL Building ────────────────────────────

@app.route('/')
def home():
    return render_template('index.html',
        name="Your Name",
        bio="3rd year IT Engineering student who is learning Flask.",
        skills=["Python", "Flask", "SQL", "HTML/CSS"]
    )

@app.route('/projects')
def projects():
    project_list = [
        {"title": "PROJECT 1", "desc": "Describe your project."},
        {"title": "PROJECT 2", "desc": "Describe your project."},
        {"title": "PROJECT 3", "desc": "Describe your project."},
    ]
    return render_template('projects.html', projects=project_list)

# URL Building example — dynamic route
@app.route('/user/<username>')
def user_profile(username):
    return f"<h2>Profile page of: {username}</h2>"


# ─── Person 2: HTTP Methods + Request Object ────────────────────

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        print(f"Message from {name}: {message}")
        return redirect(url_for('home'))
    return render_template('contact.html')


# ─── Person 3: Cookies ──────────────────────────────────────────

@app.route('/setcookie')
def setcookie():
    resp = make_response(render_template('cookie.html', msg="Cookie has been set!"))
    resp.set_cookie('username', 'Rahul')  # sets cookie in browser
    return resp

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('username')  # reads cookie from browser
    if name:
        return render_template('cookie.html', msg=f"Welcome back, {name}! 🎉")
    return render_template('cookie.html', msg="No cookie found. Go to /setcookie first.")

@app.route('/deletecookie')
def deletecookie():
    resp = make_response(render_template('cookie.html', msg="Cookie deleted!"))
    resp.delete_cookie('username')
    return resp


# ─── Person 3: File Uploading ───────────────────────────────────

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return render_template('upload.html', msg="No file selected!")
        filepath = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(filepath)
        return render_template('upload.html', msg=f"✅ File '{f.filename}' uploaded successfully!")
    return render_template('upload.html', msg=None)


if __name__ == '__main__':
    app.run(debug=True)
