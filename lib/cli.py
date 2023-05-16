from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Course
from tabulate import tabulate

import ipdb

class CLI:
    all_users = set()
    
    
    def __init__(self):
        self.students = session.query(Student).all() #returns list
        self.courses = session.query(Course).all()
        self.grades = session.query(Grade).all()
        self.user_name = ""
        self.roll_number = ""
        self.user_validate = {
            "teacher_code" : "INSTRUCTOR",
            "student_code" : "STUDENT"
        }
        self.everything = {} # Only used by Instructors
        self.course_info = {}
        self.start()
    
    def start(self):
        print("!!!!!!WELCOME TO GRADEBOOK!!!!!!")
        print()

        # Creating course dictionary
        for course in self.courses:  
            self.course_info[course.name.lower()]= []
        

        #making a global dictionary: self.everything
        
        
        for student in self.students:
            
            self.everything[student.name.lower()]=[]
            
            for grade in student.grades:
                self.everything[student.name.lower()].append((grade.course_name,grade.score))
                self.course_info[grade.course_name.lower()].append(grade.score)
                
        

        # print(f'everything: {self.everything}')
        # print(f'course info: {self.course_info}')
        
       

        self.user_name = input("Name: ")
        validation_code = input("Enter Code: ")
        CLI.all_users.add(self.user_name.lower())
        print(f'all users : {CLI.all_users}')
        
        # INSTRUCTOR CODE
        if validation_code.lower() == self.user_validate["teacher_code"].lower():
            print(f"Welcome Instructor {self.user_name}!")
            print()
            #show all students names
            
            j=[]
            for student in self.everything.keys():
               
                for k in self.everything[student]:
                    j.append([student,k])
                
            print(tabulate(j,headers=["Student Name","Student Report"], tablefmt="pipe"))
            print()
            
            choice = input('''1. Name to check details of particular student - 'Name'\n2. Info About particular Course.\n3. return to main menu - 'menu'\n4. exit application - 'exit'\n''')
            if choice == 'exit':
                quit()
            elif choice.lower() in self.everything:
                print(self.everything[choice])

            # to get details about course, avg_score, total score, total students
            elif choice.lower() in self.course_info:
                # print(self.course_info)
                print(f'Average Score in {choice} is {sum(self.course_info[choice.lower()])/len(self.course_info[choice.lower()])}')
                print(f'Maximum Score in {choice} is {max(self.course_info[choice.lower()])}')
                print(f'Minimum Score in {choice} is {min(self.course_info[choice.lower()])}')


        # STUDENT CODE
        elif validation_code.lower() == self.user_validate["student_code"].lower():
            print(f"Welcome Student {self.user_name}!")
            self.search_student_records()
        else:
            print("Sorry! No such user exists with this Name and code!!! Try Again!")
        quit()
    
    def search_student_records(self):
        student_record =session.query(Student).filter(Student.name==self.user_name)
        grade_info = (session.query(Grade).filter(Grade.student_name==self.user_name))
        for info in student_record:
            self.roll_number = info.id
        print(f'Name: {self.user_name}')
        print(f'Roll Number: {self.roll_number}')
        # print([(grade.student.id,  grade.score,grade.course_name ) for grade in grade_info])
        
        
   

    
if __name__=='__main__':
    engine = create_engine('sqlite:///gradebook.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    CLI()
    

#GOALS:
# Search and Filter: Implement search and filter functionality to
# retrieve specific records based on criteria such as student name,
# course name, grade range, etc.

#Make a dictionary stating that if you are a student than you can only see your grades
# If you are a teacher you can see all grades

# Make a class method that validates code

# Make a set that has info about teacher, student and admin, and admin does not require any code returning user

#all(0 can give user history, who all login in)