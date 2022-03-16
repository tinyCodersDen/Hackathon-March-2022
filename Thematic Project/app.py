# This is the main Driver Code for the Project
# This includes all the routes and Operations I perform on databases and the email senders
# Importing Modules:
import pymongo
import os
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from bson import ObjectId
from flask import Flask,render_template,request,redirect
from decouple import config

# Initializing Variables:
mykey = config('SENDGRID_API_KEY',default='')
mongo_string = config('mongo_string',default='')
sender_email = config('sender_email',default='')
app = Flask(__name__)
client = pymongo.MongoClient(mongo_string)
db = client.ScheduleBuddy
# Starting/Homepage route:
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        return redirect('/app')
    return render_template('home.html')
# Main Application route:
@app.route('/app',methods=['GET','POST'])
def main():
    tasks = db.Tasks.find()
    if request.method=='POST':
        # Here I will add a document to the MongoDB database
        document = {}
        document['Title'] = request.form['title']
        document['description'] = request.form['Body']
        document['Time'] = request.form['time']
        db.Tasks.insert_one(document)
        tasks = db.Tasks.find()
        # I am checking if email field is filled in
        # If the condition satisfies, then it will send an automatic email to the user via SendGrid
        if request.form['email'].strip()!='':
            # Entering Sender and email Body credentials
            message = Mail(
            from_email=sender_email,
            to_emails=request.form["email"],
            subject='You Added a New Task',
            html_content="<h1>This is an automated message:</h1> <p>You enabled an email reminder of your new task card in your to-do List:</p> <h1>Task Title: {}</h1> <h1>Description of Task: {}</h1> <h1>Time of Task: {}</h1>".format(document['Title'],document['description'],document['Time']))
            # I am sending and printing some important information for debuging
            try:
                sg = SendGridAPIClient(mykey)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
        return render_template('app.html', tasks=tasks)
    return render_template('app.html', tasks=tasks)
# Route for deleting a Task
@app.route('/delete/<task_id>')
def delete(task_id):
    db.Tasks.delete_one({'_id':ObjectId(task_id)})
    return redirect('/app')
# Route for checking current status
@app.route('/status',methods=['GET','POST'])
def status():
    rows = []
    if request.method=='POST':
        tasks = db.Tasks.find()
        rows = []
        # I am looping through the Mongo DB and fetching information such as the date, time, and status
        # This is used to show info about their tasks to the user.
        for task in tasks:
            row = []
            mytime = task["Time"]
            mytime=mytime[2:]
            # Converting string to datetime and formating it:
            datetime_object = datetime.datetime.strptime(mytime,'%y-%m-%dT%H:%M')
            formatted_object = datetime_object.strftime('%m-%d-%Y %H:%M')
            row.append(formatted_object)
            row.append(task['Title'])
            # Using a time checking system to determine the status of the date
            date = datetime_object.date()
            if date==datetime.datetime.now().date():
                row.append('Started')
            elif datetime_object>datetime.datetime.now():
                row.append('Pending')
            elif datetime_object<datetime.datetime.now():
                row.append('Finished')
            rows.append(row)
    return render_template('status.html',rows = rows)
if __name__=='__main__':
    app.run(debug=True)
