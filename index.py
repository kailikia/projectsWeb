from flask import Flask,render_template,request,redirect,url_for,flash,session
from project import Project
from user import User
import pygal  # First import pygal
import json
import requests

app = Flask(__name__)
app.secret_key = '$ec$r44ceee3d3$55t5frvrffr'

def authenticator():
    if session:
        if session['mse']:
          return True
        else:
          return False

@app.route('/login', methods=['POST'])
def login():
    #Check if user exists
    try:
        user = User.get(User.email == request.form['email'], User.password == request.form['password'])
        # set session
        session['mse'] = True
        session['id'] = user.id
        flash('Logged in Successfully')
        return redirect(url_for('home'))
    except:
        flash('Bad Credentials')
        return render_template('authentication.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/jsonData")
def jsonData():
    joke = requests.get("https://api.icndb.com")
    print(joke.status_code)
    return joke


@app.route('/register', methods=['POST'])
def register():
    #Check if email exists
    try:
        User.get(User.email == request.form['email'])
        flash('User already Exists')
        return render_template('authentication.html')
    except:
        if request.form['password'] == request.form['confirm-password']:
            # if not exists create user
            user = User(name = request.form['username'],
                        email=request.form['email'],
                        password = request.form['password'])
            user.save()
            # set session
            session['mse'] = True
            session['id'] = user.id
            return redirect(url_for('home'))

        flash('Passwords Do not match')
        return render_template('authentication.html')


def setterProjects():
    myId = 12

def barChart():
    projects = Project.select()
    label = 'Amount'
    data =[]
    # Loop through each row get the amount for each in the loop add the amount to an existing list
    for row in projects:
      data.append(row.amount) # Add some values
    bar_chart = pygal.Bar()
    bar_chart.add(label, data)
    bar_graph = bar_chart.render_data_uri()
    return bar_graph

def pieChart():
    projects = Project.select()
    pie_chart = pygal.Pie()
    pie_chart.title = 'Projects Type'
    internal = 0
    external = 0
    for row in projects:
        if row.type == 'Internal':
            internal = internal + 1
        else:
            external = external + 1
    pie_chart.add('Internal', internal)
    pie_chart.add('External', external)

    return pie_chart.render_data_uri()

@app.route('/')
def home():
    if authenticator():
        print('my sess', session['id'])
        projects = Project.select().order_by(Project.id)
        return render_template('index.html',
                           graph_data = barChart(),
                           pie_chart = pieChart(),
                           projectsHtml = projects)
    else:
        return render_template('authentication.html')

@app.route('/save', methods=['POST'])
def save():
    projectOne = Project(title= request.form['titleForm'],
                         type=request.form['typeForm'],
                         start_from = request.form['startDateForm'],
                         end_at = request.form['endDateForm'],
                         description = request.form['descriptionForm'],
                         amount = request.form['amountForm'],
                         status = 1
                         )
    projectOne.save()
    flash('Record Saved Successfully')
    return redirect(url_for('home'))

@app.route("/update/<int:id>", methods=['POST'])
def update(id):
    project = Project.get(Project.id == id)
    project.title = request.form['titleForm']
    project.save()
    flash('Record Updated successfully')
    return redirect(url_for('home'))

@app.route("/delete/<int:id>", methods=['GET'])
def delete(id):
    try:
        project = Project.get(Project.id == id)
        project.delete_instance()
        flash('Record Deleted')
        return  redirect(url_for('home'))
    except:
        return 'Server Error'



if __name__ == '__main__':
    app.run(debug=True,port=5050)