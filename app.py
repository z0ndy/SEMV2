from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import csv,os,random
from methods import *

def save_uploaded_file(file):
    # Save the uploaded file to a temporary location
    temp_folder = 'temp'
    os.makedirs(temp_folder, exist_ok=True)
    file_path = os.path.join(temp_folder, file.filename)
    file.save(file_path)
    return file_path


years = [1,2,3,4]
branches = ['CSE', 'IT', 'AIDS', 'AIML', 'Chemical Engineering', 'Civil', 'Mechanical', 'ECE', 'EEE']
sections =["Section 1","Section 2","Section 3","Section 4","Section 5"]
details = [years,branches,sections]
authenticated = False
app = Flask(__name__)
cluster = MongoClient('mongodb+srv://gvarshithreddy8:Varshith1@cluster0.xzgxe3m.mongodb.net/?retryWrites=true&w=majority')



db = cluster.sem
studentdata = db.studentdata

if "studentyear" not in db.list_collection_names():
    studentyear = db.create_collection("studentyear")
else:
    studentyear = db.studentyear
    
#new code
# year1 = studentyear.find_one(1)
# try:
#     students = year1['branches'][0]['sections'][0]['students']
# except KeyError or NameError:
#     print("No students uploaded yet in the requested branch and section")
# else:
#     for student in students:
#         print(student)
#new code end

@app.route("/")
def home():
    return render_template("home.html", title = "SEM")


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if not authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the selected values from the form
        year = int(request.form.get('year'))
        branch = str(request.form.get('branch'))
        section = str(request.form.get('section'))
        if 'csvFile' not in request.files:
            return 'No file uploaded'

        file = request.files['csvFile']

        if file.filename == '':
            return 'No file selected'

        if file and allowed_file(file.filename):
            print(section)
            print("ESXRCDTVFGBHJNK MSRDCTVFBJNKMDCTFVYGBUHNIJMOK<DCTFVYGBUHNIJMCTFVYGBUHN")
            file_path = save_uploaded_file(file)
            # Pass the selected values and the file to the add_students_many method
            add_students_many(cluster,year, branch, section, file_path)
            os.remove(file_path)

            # Redirect to a success page or render a success template
            return 'File uploaded and processed successfully'

    return render_template('admin.html',years = years, branches=branches, sections= sections )

@app.route('/login', methods=['GET', 'POST'])
def login():
    global authenticated  # Access the global variable

    if authenticated:
        # If already authenticated, redirect to the admin page
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Perform authentication here
        if username == 'admin' and password == 'password':
            # Authentication successful
            authenticated = True
            return redirect(url_for('admin'))
        else:
            # Authentication failed
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/allocate', methods = ['GET','POST'])
def allocate():
    if request.method=='POST':
        year = int(request.form.get('year'))
        branch = request.form.get('branch')
        section = int(request.form.get('section'))
        num_experiments = int(request.form.get('experiments'))
        student_data = get_students(studentyear,year,branch,section)
        experiment_data = allocate_students(num_experiments, student_data )



        return render_template('sortresults.html',experiments = enumerate(experiment_data))
    return render_template('experiment_allocation.html', years = years, branches = branches, sections = sections, len = len(sections) )


@app.route('/edit',methods = ['GET','POST'])
def edit():
        
    return render_template('get_student_details.html',students=details,len = len(details[2]))

@app.route('/view_students/',methods = ["GET",'POST'])
def view_students():
    if request.method=="POST":
        global students
        students = {
            'year':int(request.form.get("year")),
            'branch': request.form.get("branch"),
            'section': int(request.form.get('section'))
        }
        students_details = get_students(studentyear,students['year'],students['branch'],students['section'])
        
        return render_template('view_students.html',students_details = students_details)
    


@app.route('/edit_student/<rollno>')
def edit_student(rollno):
    if request.method == "GET":
        student_rollno = int(rollno)
        student={}
        students_details = get_students(studentyear,students['year'],students['branch'],students['section'])
        for i in students_details:
            #print(i)

            if student_rollno == i['rollno']:
                student["studentname"] = i['studentname']
                student["rollno"] = i['rollno']
        

    return render_template('edit_student.html', student = student)

@app.route('/changeDB_student', methods = ["POST"])
def changeDB_student():
    
    return "Data changed successfully"

if __name__ == '__main__':
    app.run()

app.run(debug=True)