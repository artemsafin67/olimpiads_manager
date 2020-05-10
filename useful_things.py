# Object for representing timetable


class TimeTable:
    def __init__(self, grades, subjects):
        self.grades = grades.split(', ')
        self.subjects = subjects.split(', ')
        self.dates = {}
        self.empty = True

    def add(self, subject, grade, value):
        self.empty = False
        if subject in self.dates:
            self.dates[subject][grade] = value
        else:
            self.dates[subject] = {grade: value}


