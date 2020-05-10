import schedule
import datetime

import smtplib
from email.mime.text import MIMEText
from email.header import Header


week = datetime.timedelta(days=7)
two_days = datetime.timedelta(days=2)
one_day = datetime.timedelta(days=1)


def choose_users(olimpiads_groups):
    """Goes through olimpiads and sends reminders"""

    for olimpiads_group in olimpiads_groups:
        for olimpiad in olimpiads_group.olimpiads:
            date = olimpiad.registration_data.date
            now = datetime.datetime.now()

            description = f'Олимпиада: {olimpiads_group.name}, Предмет: {olimpiad.subject}, Класс: {olimpiad.grade}, ' \
                          f'Город: {olimpiad.city}, Дата: {olimpiad.registration_data.date.strftime("%d %B")}'

            if date - now < one_day and olimpiad.users:  # Edition for testing
                send_messages(olimpiad.users, templates['one_day'] + f' {description}')
            elif date - now < two_days and olimpiad.users:
                send_messages(olimpiad.users, templates['two_days'] + f' {description}')
            elif date - now < week and olimpiads_group.users:
                send_messages(olimpiad.users, templates['week'] + f' {description}')


def send_messages(users, message):
    """Sends messages"""

    smtp_server = 'smtp.gmail.com'
    login = GMAIL_ADDRESS
    password = GMAIL_PASSWORD
    recipients = [user.email for user in users]

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header('Напоминание об олимпиаде', 'utf-8')
    msg['From'] = login

    sender = smtplib.SMTP(smtp_server, 587)
    sender.starttls()
    sender.login(login, password)

    sender.sendmail(msg['From'], recipients, msg.as_string())
    sender.quit()


def make_mailing_work(groups):
    schedule.every(1).days.do(choose_users, olimpiads_groups=groups)

    while True:
        schedule.run_pending()


templates = {'one_day': "Тут будет нормальное напоминание о олимпиаде, которая состоится через 1 день.",
             'two_days': "Тут будет нормальное напоминание о олимпиаде, которая состоится через 2 дня.",
             'week': "Тут будет нормальное напоминание о олимпиаде, которая состоится через неделю."}









