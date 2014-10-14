import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT description, max_grade, title FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    title: %s
    description: %s
    max_grade: %s""" % (row[2], row[0], row[1])

def get_student_grade(project, github):
    query = """SELECT grade FROM Grades WHERE project_title = ? AND student_github = ?"""
    DB.execute(query, (project, github))
    row = DB.fetchone()
    print """\
    Project: %s
    Student Github: %s
    Grade: %s""" % (project, github, row[0])

def get_all_grades(github):
    query = """SELECT grade, project_title FROM Grades WHERE student_github = ?"""
    for row in DB.execute(query, (github,)):
        print """\
        Project: %s, grade %s""" % (row[1], row[0])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def make_new_project(title, description, max_grade):
    insert_statement = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(insert_statement, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s, %s, with maximum grade %s" % (title, description, max_grade)

def give_grade_to_student(project, github, grade):
    insert_statement = """INSERT INTO Grades VALUES (?, ?, ?)"""
    DB.execute(insert_statement, (github, project, grade))
    CONN.commit()
    print "Successfully added grade %s for student %s for project %s" % (grade, github, project)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_grade_for":
            get_student_grade(*args)
        elif command == "give_grade":
            give_grade_to_student(*args)
        elif command == "all_grades_for_student":
            get_all_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
