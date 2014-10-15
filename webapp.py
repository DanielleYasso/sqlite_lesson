from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    data = get_all_grades(student_github)
    html = render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2],
                                                grades=data)
    return html

def get_all_grades(github):
    return hackbright_app.get_all_grades(github)

@app.route("/project")
def get_grades_for_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    data = hackbright_app.get_grades_for_project(project_title)
    html = render_template("project.html", project=project_title,
                                           project_data=data)
    return html

if __name__ == "__main__":
    app.run(debug=True)