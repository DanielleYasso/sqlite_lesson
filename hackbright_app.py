import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    try:
        print """\
        Student: %s %s
        Github account: %s"""%(row[0], row[1], row[2])
    except TypeError:
        print "Student '%s' not found" % github
        print "To add student '%s' to student list, use the command 'new_student'" % github

def get_project_by_title(title):
    query = """SELECT description, max_grade, title FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    Title: %s
    Description: %s
    Max_grade: %s""" % (row[2], row[0], row[1])

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

def get_all_students():
    query = """SELECT github FROM Students"""
    for github in DB.execute(query):
        print github[0]

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

def list_commands():
    print "Commands available:"
    for command, info in COMMANDS.iteritems():
        print "%s:\n\t%s \n\tformat: %s \n" % (command, info[1], info[2])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        try:
            COMMANDS[command][0](*args)
        except TypeError:
            print "Incorrect syntax. Use 'help' for specific query formatting."
        except KeyError:
            print "Command not recognized. Please use 'help' to view valid commands."

    CONN.close()

COMMANDS = {
            "student":      [get_student_by_github, "lists student information", "student <github>"],
            "new_student":  [make_new_student, "adds a new student to the student list", "new_student <first_name> <last_name> <github>"],
            "project":      [get_project_by_title, "gets a project by title", "project <title>"],
            "new_project":  [make_new_project, "adds a new project to project list", "new_project <title> <description> <max_grade>"],
            "get_grade_for": [get_student_grade, "gets a student's grade for a project", "get_grade_for <project> <github>"],
            "give_grade":   [give_grade_to_student, "gives project grade to student", "give_grade <project> <github> <grade>"],
            "all_grades_for_student": [get_all_grades, "lists all grades for a student", "all_grades_for_student <github>"],
            "get_students": [get_all_students, "lists all available students", "get_students"],
            "help": [list_commands, "lists available commands", ""]
            }

if __name__ == "__main__":
    main()
