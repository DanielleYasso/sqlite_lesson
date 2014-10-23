from flask import Flask, render_template, request, redirect, flash
import hackbright_app

app = Flask(__name__)
# added for flash - including for testing exercise
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")

    row = hackbright_app.get_student_by_github(student_github)
    if not row:
        flash("Please enter a valid student github")
        return redirect("/")
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
    if not data:
        flash("Please enter a valid project title")
        return redirect("/")
    html = render_template("project.html", project=project_title,
                                           project_data=data)
    return html

if __name__ == "__main__":
    app.run(debug=True)