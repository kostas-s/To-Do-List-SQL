from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import sys


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def print_menu():
    print()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    inp = input()
    print()
    if inp == '1':
        print_todays_tasks()
    elif inp == '2':
        print_weeks_tasks()
    elif inp == '3':
        print_all_tasks()
    elif inp == '4':
        print_missed_tasks()
    elif inp == '5':
        add_task()
    elif inp == '6':
        delete_task()
    elif inp == '0':
        sys.exit()


def print_missed_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
    print("Missed tasks:")
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for idx, row in enumerate(rows):
            print(f"{idx + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")

def delete_task():
    print("Choose the number of the task you want to delete:")
    rows = session.query(Table).order_by(Table.deadline).all()
    for idx, row in enumerate(rows):
        print(f"{idx + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
    try:
        inp = int(input())
        if inp > 0 and inp <= len(rows):
            row_to_del = rows[inp - 1]
            session.delete(row_to_del)
            session.commit()
        else:
            raise ValueError
    except (TypeError, ValueError):
        print("Input incorrect, try again!")



def print_weeks_tasks():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = datetime.today()
    for idx in range(0, 7):
        target_day = today + timedelta(days=idx)
        rows = session.query(Table).filter(Table.deadline == target_day.date()).all()
        print(f"{days[target_day.weekday()]} {target_day.day} {target_day.strftime('%b')}:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i, row in enumerate(rows):
                print(str(i + 1) + ". " + str(row))
        print()



def print_all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for idx, row in enumerate(rows):
            date = row.deadline
            print(f"{idx + 1}. {row}. {date.day} {date.strftime('%b')}")


def add_task():
    print("Enter task")
    entry = input()
    print("Enter deadline")
    date = input()
    date = datetime.strptime(date, "%Y-%m-%d")
    new_row = Table(task=entry, deadline=date)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def print_todays_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print("Today:")
        print("Nothing to do!")
    else:
        for idx, row in enumerate(rows):
            date = row.deadline
            print(f"Today {date.day} {date.strftime('%b')}:")
            print(str(idx + 1) + ". " + str(row))


Base.metadata.create_all(engine)
while True:
    print_menu()




