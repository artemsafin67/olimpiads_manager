from flask import Flask, render_template, request, redirect, make_response, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data.forms.loginForm import LoginForm
from data.forms.registerForm import RegisterForm
from data.forms.taskForm import TaskForm
from data.forms.registerOlimpForm import RegisterOlimpForm
from data.forms.editProfileForm import EditProfileForm
from data.forms.addOlimpiadsGroupForm import AddOlimpiadsGroupForm

from data.forms.addNewsForm import AddNewsForm

import datetime

from data.database.all_for_session import create_session, global_init

from data.tables.olimpiad import Olimpiad
from data.tables.olimpiadsGroupNews import OlimpiadsGroupNews
from data.tables.olimpiadsGroup import OlimpiadsGroup
from data.tables.olimpiadRegistration import OlimpiadRegistration
from data.tables.user import User

from useful_things import TimeTable
import threading
from mailing import make_everything_work

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gjlk;fdgnfedbf80094223r9fomzc,vl0eruhrwlk v'

login_manager = LoginManager()
login_manager.init_app(app)


# Here will be a block for user management


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


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        db_session = create_session()
        current_user.name = form['name'].data
        current_user.surname = form['surname'].data
        current_user.fatherhood = form['fatherhood'].data
        current_user.grade = form['grade'].data
        current_user.set_password(form['password'].data)

        data = form['photo'].data.read()
        if data:
            current_user.photo = f'../static/img/avatars/{current_user.id}.jpg'
            with open(f'static/img/avatars/{current_user.id}.jpg', 'wb') as file:
                file.write(data)
        if not data and not current_user.photo:
            current_user.photo = f'../static/img/avatars/default.jpg'

        db_session.merge(current_user)
        db_session.commit()

        return redirect("/")

    if request.method == "GET":
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.fatherhood.data = current_user.fatherhood
        form.grade.data = current_user.grade
        form.email.data = current_user.email

    return render_template("edit_profile.html", form=form)


# Here will be a block for news management


@app.route('/', methods=["GET", "POST"])
def news():
    db_session = create_session()

    all_news = sorted(db_session.query(OlimpiadsGroupNews).all(), key=lambda x: x.date, reverse=True)
    news_in_rows = []

    for i in range(0, len(all_news), 3):
        news_in_rows.append(all_news[i: min(len(all_news), i + 3)])

    return render_template("news.html", news=news_in_rows)


@app.route('/particular_news/<int:news_id>')
def particular_news(news_id):
    db_session = create_session()
    item = db_session.query(OlimpiadsGroupNews).filter(OlimpiadsGroupNews.id == news_id).first()
    paragraphs = item.text.split('\n\n')

    return render_template("particular_news.html", news=item, paragraphs=paragraphs)


# Here will be a block for olimpiads management


@app.route('/why_olimps')
def why_olimps():
    return render_template("why_olimps.html")


@app.route('/olimpiads')
def olimpiads():
    db_session = create_session()
    all_olimpiads = db_session.query(OlimpiadsGroup).all()
    db_session.close()

    olimpiads_in_rows = []

    for i in range(0, len(all_olimpiads), 3):
        olimpiads_in_rows.append(all_olimpiads[i: min(len(all_olimpiads), i + 3)])

    return render_template("olimpiads.html", olimpiads=olimpiads_in_rows)


@app.route('/user_olimpiads')
@login_required
def user_olimpiads():
    db_session = create_session()
    user = db_session.query(User).filter(User.email == current_user.email).first()
    all_olimpiads = user.olimpiads
    olimpiads_in_rows = []

    for i in range(0, len(all_olimpiads), 3):
        olimpiads_in_rows.append(all_olimpiads[i: min(len(all_olimpiads), i + 3)])

    return render_template("user_olimpiads.html", olimpiads=olimpiads_in_rows)


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


@app.route('/delete_olimp/<int:olimp_id>')
@login_required
def delete_olimp(olimp_id):
    db_session = create_session()
    user = db_session.query(User).filter(User.email == current_user.email).first()
    olimp = db_session.query(Olimpiad).filter(Olimpiad.id == olimp_id).first()
    user.olimpiads.remove(olimp)
    db_session.commit()
    return redirect('/user_olimpiads')


# Here will be a block for adding data


def add_registration(group_id):
    db_session = create_session()

    olimpiad_group = db_session.query(OlimpiadsGroup).filter(OlimpiadsGroup.id == group_id).first()

    for olimpiad in olimpiad_group.olimpiads:
        registr = OlimpiadRegistration()
        registr.date = datetime.datetime(year=2020, month=8, day=25)
        registr.documents = "Паспорт, справка из школы, специальный бланк"
        olimpiad.registration_data = registr

        # print(olimpiad)
        # add = input("Есть информация? ")
        #
        # if add == "Да":
        #     date = datetime.datetime(year=int(input("Год: ")),
        #                              month=int(input("Месяц: ")),
        #                              day=int(input("День: ")))
        #     documents = input("Документы (через символы ', '): ")
        #
        #     registr = OlimpiadRegistration()
        #     registr.date = date
        #     registr.documents = documents
        #
        #     olimpiad.registration_data = registr

    db_session.commit()


@app.route('/add_news', methods=["GET", "POST"])
@login_required
def add_news():
    if current_user.id != 1:
        return redirect('/')

    form = AddNewsForm()

    if form.validate_on_submit():
        db_session = create_session()

        news_to_add = OlimpiadsGroupNews()
        news_to_add.title = form['title'].data
        news_to_add.description = form['description'].data
        news_to_add.text = form['text'].data.replace('\r', '\n')

        if form['is_group_news'] == 'on':
            olimpiad = db_session.query(OlimpiadsGroup).filter(OlimpiadsGroup.name == form['group_name'].data).first()
            if not olimpiad:
                return render_template("add_news.html", form=form, message="Группа олимпиад не найдена")

            news_to_add.olimpiad_group_id = olimpiad.id

        db_session.add(news_to_add)
        db_session.commit()

        data = form['photo'].data.read()
        if data:
            news_to_add = db_session.query(OlimpiadsGroupNews).all()[-1]
            news_to_add.photo = f'../static/img/news/{news_to_add.id}.jpg'

            with open(f'static/img/news/{news_to_add.id}.jpg', 'wb') as file:
                file.write(data)

            db_session.commit()

    return render_template("add_news.html", form=form)


@app.route('/add_groups', methods=["GET", "POST"])
@login_required
def add_groups():
    if current_user.id != 1:
        return redirect('/')

    form = AddOlimpiadsGroupForm()

    if form.validate_on_submit():
        db_session = create_session()

        olimpiads_group = OlimpiadsGroup()
        olimpiads_group.name = form['name'].data
        olimpiads_group.organizer = form['organizer'].data
        olimpiads_group.description = form['description'].data
        olimpiads_group.subjects = form['subjects'].data
        olimpiads_group.grades = form['grades'].data
        olimpiads_group.grades_description = form['grades_description'].data
        olimpiads_group.link = form['link'].data
        olimpiads_group.cities = form['cities'].data

        for grade in olimpiads_group.grades.split(', '):
            for subject in olimpiads_group.subjects.split(', '):
                for city in olimpiads_group.cities.split(', '):
                    olimpiads_group.olimpiads.append(Olimpiad(grade=grade, subject=subject,
                                                              city=city))
        db_session.add(olimpiads_group)
        db_session.commit()

        data = form['photo'].data.read()
        olimpiads_group = db_session.query(OlimpiadsGroup).all()[-1]
        if data:
            olimpiads_group.photo = f'../static/img/olimpiads/{olimpiads_group.id}.jpg'

            with open(f'static/img/olimpiads/{olimpiads_group.id}.jpg', 'wb') as file:
                file.write(data)
        else:
            olimpiads_group.photo = f'../static/img/olimpiads/default.jpg'

        add_registration(olimpiads_group.id)

        db_session.commit()

    return render_template("add_olimpiads_group.html", form=form)


def main():
    global_init('db/olimpiads_manager.sqlite')
    db_session = create_session()

    t1 = threading.Thread(target=make_everything_work, args=(db_session.query(OlimpiadsGroup).all(),))
    t2 = threading.Thread(target=app.run, args=('127.0.0.1', 8080,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
