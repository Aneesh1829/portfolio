from flask import Flask, render_template, request, redirect
import csv
import smtplib
from email.mime.text import MIMEText
import os

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')




app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def send_email(data):
    subject = f"New Contact Form Submission: {data['subject']}"
    body = f"Email: {data['email']}\nMessage:\n{data['message']}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # send to yourself

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

def write_to_file(data):
  with open('database.txt', mode='a') as database:
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
  with open('database.csv', mode='a', newline='') as database2:
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([email,subject,message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            send_email(data)  # <-- send email on submission
            return redirect('/thankyou.html')
        except Exception as e:
            return f"Did not save to database. Error: {e}"
    else:
        return 'Something went wrong. Try again!!'

    
if __name__ == "__main__":
    app.run(host="0.0.0.0")





