from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# new_row = Table(task='This is string field!', deadline=datetime.strptime('01-24-2020', '%m-%d-%Y').date())
# session.add(new_row)
# session.commit()

# rows = session.query(Table).all()
# print(rows)
# first_row = rows[0] # In case rows list is not empty

# print(first_row.task) # Will print value of the string_field
# print(first_row.id) # Will print the id of the row.
# print(first_row) # Will print the string that was returned by __repr__ method


def menu():

    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

def selection():
    return int(input())

menu()
my_choice = selection()
print()

while True:

    if my_choice == 1:
        today = datetime.today()
        month_today = today.strftime('%b')
        day_today = today.day
        time_today = today.time
        print('Today ' + str(day_today) + ' ' + month_today + ':')
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for row in rows:
                print(row)
        print()

    elif my_choice == 2:
        today = datetime.today()
        month_today = today.strftime('%b')
        weekday = today.weekday()
        fullname_weekday = today.strftime('%A')
        day_today = today.day
        time_today = today.time
        for day in range(0, 7):
            new_day = today + timedelta(days=day)
            fullname_weekday = new_day.strftime('%A')
            day_today = new_day.day
            rows = session.query(Table).filter(Table.deadline == new_day.date()).all()
            print(fullname_weekday + ' ' + str(day_today) + ' ' + month_today + ':')
            if len(rows) == 0:
                print('Nothing to do!')
            else:
                for row in rows:
                    print(row)
            print()

    elif my_choice == 3:
        print('All tasks:')
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for row in rows:
                print(str(row.id) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
        print()

    elif my_choice == 4:
        today = datetime.today()
        month_today = today.strftime('%b')
        weekday = today.weekday()
        fullname_weekday = today.strftime('%A')
        day_today = today.day
        time_today = today.time

        rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('Nothing is missed!')
        else:
            for row in rows:
                print(str(row.id) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
        print()

    elif my_choice == 5:
        new_task = input('Enter task:\n')
        new_deadline = datetime.strptime(input('Enter deadline:\n'), '%Y-%m-%d')
        new_row = Table(task=new_task, deadline=new_deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')

    elif my_choice == 6:
        print('Choose the number of the task you want to delete:')
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('Nothing to delete!\n')
        else:
            for row in rows:
                print(str(row.id) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
            # row_numb_to_delete = rows[int(input())-1]
            session.query(Table).filter(Table.id == int(input())).delete()
            #session.delete(row_numb_to_delete)
            session.commit()
            print('The task has been deleted!\n')

    else:
        print('Bye!')
        break
    menu()
    my_choice = selection()
    print()

