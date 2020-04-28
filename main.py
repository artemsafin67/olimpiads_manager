from flask import Flask, render_template, request, redirect, make_response, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data.forms.loginForm import LoginForm
from data.forms.registerForm import RegisterForm
from data.forms.taskForm import TaskForm
from data.forms.registerOlimpForm import RegisterOlimpForm

import datetime

from data.database.all_for_session import create_session, global_init

from data.tables.olimpiad import Olimpiad
from data.tables.olimpiadsGroupNews import OlimpiadsGroupNews
from data.tables.olimpiadsGroup import OlimpiadsGroup
from data.tables.olimpiadRegistration import OlimpiadRegistration
from data.tables.user import User

from useful_classes import TimeTable

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfjdkfjdkfjdkfdj'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    db_session = create_session()
    return db_session.query(User).get(user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_session = create_session()
        user = db_session.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')

        return render_template("login.html", message="Неправильный логин или пароль", form=form)

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_session = create_session()
        user = User()

        user.name = form['name'].data
        user.surname = form['surname'].data
        user.fatherhood = form['fatherhood'].data
        user.grade = form['grade'].data
        user.email = form['email'].data
        user.set_password(form['password'].data)

        if db_session.query(User).filter(User.email == user.email).first():
            return render_template("register.html", form=form, message_email="Этот логин уже занят")

        db_session.add(user)
        db_session.commit()

        user = db_session.query(User).filter(User.email == user.email).first()

        data = form['photo'].data.read()
        if data:
            user.photo = f'../static/img/avatars/{user.id}.jpg'
            with open(f'static/img/avatars/{user.id}.jpg', 'wb') as file:
                file.write(data)
        else:
            user.photo = f'../static/img/avatars/default.jpg'

        login_user(user)
        db_session.commit()

        return redirect("/")
    else:
        return render_template("register.html", form=form)


@app.route('/')
def news():
    db_session = create_session()

    all_news = sorted(db_session.query(OlimpiadsGroupNews).all(), key=lambda x: x.date)
    news_in_rows = []

    for i in range(0, len(all_news), 3):
        news_in_rows.append(all_news[i: min(len(all_news), i + 3)])

    return render_template("news.html", news=news_in_rows)


@app.route('/olimpiads')
def olimpiads():
    db_session = create_session()
    all_olimpiads = db_session.query(OlimpiadsGroup).all()
    db_session.close()

    olimpiads_in_rows = []

    for i in range(0, len(all_olimpiads), 3):
        olimpiads_in_rows.append(all_olimpiads[i: min(len(all_olimpiads), i + 3)])

    return render_template("olimpiads.html", olimpiads=olimpiads_in_rows)


@app.route('/particular_olimpiad/<int:olimpiad_id>')
def particular_olimpiad(olimpiad_id):
    db_session = create_session()
    item = db_session.query(OlimpiadsGroup).filter(OlimpiadsGroup.id == olimpiad_id).first()

    subjects = item.subjects.split(', ')

    all_news = sorted(db_session.query(OlimpiadsGroupNews).filter(
        OlimpiadsGroupNews.olimpiad_group_id == olimpiad_id).all(), key=lambda x: x.date)
    news_in_rows = []

    for i in range(0, min(len(all_news), 2), 2):
        news_in_rows.append(all_news[i: min(len(all_news), i + 2)])

    timetable = TimeTable(item.grades, item.subjects)
    for olimpiad in item.olimpiads:
        timetable.add(olimpiad.subject, olimpiad.grade, olimpiad.registration_data.date)

    return render_template("particular_olimpiad.html", olimpiad=item, subjects=subjects,
                           news=news_in_rows, timetable=timetable)


@app.route('/learning')
def learn():
    form = TaskForm()
    return render_template("learning.html", form=form)


@app.route('/tasks/<int:olimpiad_id>', methods=["GET", "POST"])
def tasks(olimpiad_id):
    db_session = create_session()
    olimpiad = db_session.query(OlimpiadsGroup).filter(OlimpiadsGroup.id == olimpiad_id).first()
    form = TaskForm()
    if form.validate_on_submit():
        res_olimp = db_session.query(Olimpiad).filter(Olimpiad.subject == form["subject"].data,
                                                      Olimpiad.grade == form["grade"].data,
                                                      Olimpiad.olimpiads_group_id == olimpiad.id).first()

        if res_olimp:
            return render_template("tasks.html", form=form, olimpiad=olimpiad, file=res_olimp.tasks)
        else:
            return render_template("tasks.html", form=form, olimpiad=olimpiad,
                                   message="Задания для такого предмета или класса не найдены")
    else:
        return render_template("tasks.html", form=form, olimpiad=olimpiad)


@app.route('/register_olimp/<int:olimpiad_id>', methods=["GET", "POST"])
@login_required
def register_olimp(olimpiad_id):
    db_session = create_session()
    olimpiad = db_session.query(OlimpiadsGroup).filter(OlimpiadsGroup.id == olimpiad_id).first()

    form = RegisterOlimpForm()
    if form.validate_on_submit():
        subject = form['subject'].data
        grade = form['grade'].data
        city = form['city'].data
        res_olimp = db_session.query(Olimpiad).filter(Olimpiad.olimpiads_group_id == olimpiad.id,
                                                      Olimpiad.subject == subject,
                                                      Olimpiad.grade == grade,
                                                      Olimpiad.city == city).first()
        u = db_session.query(User).filter(User.email == current_user.email).first()

        if res_olimp:
            u.olimpiads.append(res_olimp)
            db_session.commit()
            return redirect("/olimpiads")
        else:
            return render_template("register_olimp.html", form=form, olimpiad=olimpiad,
                                   message="Олимпиады по выбранным параметрам не найдено")
    return render_template("register_olimp.html", form=form, olimpiad=olimpiad)


@app.route('/particular_news/<int:news_id>')
def particular_news(news_id):
    db_session = create_session()
    item = db_session.query(OlimpiadsGroupNews).filter(OlimpiadsGroupNews.id == news_id).first()
    paragraphs = item.text.split('\n\n')

    return render_template("particular_news.html", news=item, paragraphs=paragraphs)


def main():
    global_init('db/olimpiads_manager.sqlite')
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
