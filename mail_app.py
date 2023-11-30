from flask import Flask, request, jsonify, render_template
from email.message import EmailMessage
import ssl
import smtplib

app = Flask(__name__)
email_password = 'dgov ecti pefj znvj'


@app.route('/')
def index():
    return render_template('mail_index.html')


@app.route('/pass', methods=['POST'])
def pass_data():
    if request.method == 'POST':
        email_sender = request.json.get('from_email')
        subject = request.json.get('subject')
        message = request.json.get('message')
        valid_emails = request.json.get('valid_emails')

        if email_sender and subject and message and valid_emails:
            send_emails(email_sender, subject, message, valid_emails)

            return jsonify({'message': 'Data received and processed successfully'})
        else:
            return jsonify({'error': 'Missing data'})


def send_emails(email_sender, subject, message, valid_emails):
    context = ssl.create_default_context()
    em = EmailMessage()
    em['From'] = email_sender
    em['Subject'] = subject
    em.set_content(message)

    to_email = ', '.join(valid_emails)
    em['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)


if __name__ == '__main__':
    app.run(debug=True)
