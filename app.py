from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from database import Users
from databasepay import Payments
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "dddgggeyeueueu"


UPLOAD_FOLDER = 'static/images/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 90 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


@app.route('/', methods=["POST", "GET"])
def register():  # put application's code here
    if request.method == "POST":
        jina = request.form['name']
        arafa = request.form['email']
        siri = request.form['password']
        encrypted_password = generate_password_hash(siri)
        Users.create(name=jina, email=arafa, password=encrypted_password)
        flash('Account created successfully!')
    return render_template("register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = Users.get(Users.email == email)
            encrypted_password = user.password
            if check_password_hash(encrypted_password, password):
                flash("User logged in successfully")
                session["logged_in"] = True
                session["name"] = user.name
                return redirect(url_for("dashboard"))
        except Users.DoesNotExist:
            flash("Wrong username or password")
    # put application's code here
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    users = Users.select()
    return render_template("dashboard.html", users=users)


@app.route('/dashboard_two')
def dashboard_two():
    return render_template("dashboard2.html")


@app.route('/dashsec1')
def dashsec_one():
    users = Payments.select()
    return render_template("dashsec1.html", users=users)


@app.route('/dashsec2')
def dashsec_two():
    return render_template("dashsec2.html")


@app.route('/dashsec3')
def dashsec_three():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    users = Users.select()
    return render_template("dashsec3.html", users=users)


@app.route('/dashsec4')
def dashsec_four():
    users = Payments.select()
    return render_template("dashsec4.html", users=users)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/books')
def books():
    return render_template("books.html")


@app.route('/books', methods=["POST", "GET"])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Book successfully uploaded and displayed below')
        return render_template("books.html", filename=filename)
    else:
        flash("Allowed types are: png, jpg, jpeg, gif")
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/' + filename), code=301)


@app.route('/pay', methods=["POST", "GET"])
def pay():
    if request.method == "POST":
        user_name = request.form['name']
        amount = request.form['amount']
        file = request.form['file']
        Payments.create(name=user_name, amount=amount, file=file)
        flash("Purchase Process is successful.")
    return render_template("pay.html")


@app.route('/borrow_log')
def borrow():
    return render_template("borrowlog.html")


@app.route('/receipt/<int:id>')
def receipt(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = Payments.get(Payments.id == id)

    user_name = user.name
    user_file = user.file
    user_amount = user.amount

    return render_template("receipt.html", user=user, name=user_name, file=user_file, amount=user_amount)


@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    user = Users.get(Users.id == id)
    if request.method == "POST":
        updateName = request.form['name']
        updateEmail = request.form['email']
        updatePassword = request.form['password']
        encrypted_pass = generate_password_hash(updatePassword)

        user.name = updateName
        user.email = updateEmail
        user.password = encrypted_pass
        user.save()
        flash("User updated")
        return redirect(url_for("dashboard"))
    return render_template("update.html", user=user)


@app.route('/logout')
def logout():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    Users.delete().where(Users.id == id).execute()
    flash("User deleted successfully!")
    return redirect(url_for("dashboard"))


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


if __name__ == '__main__':
    app.run()
