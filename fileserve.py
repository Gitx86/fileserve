#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, send_from_directory
import os

UPLOAD_FOLDER = '/home/ubttest/Documents/test'  # Specify the path to the folder where files will be uploaded
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Specify the file extensions allowed to be uploaded

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Function to check if a file is allowed to be uploaded based on its extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Function to handle file upload"""
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # Check if the file has a valid filename
        if file.filename == '':
            return redirect(request.url)

        # Check if the file is allowed to be uploaded
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return '''
    <!doctype html>
    <html>
    <head>
    <title>File Transfer</title>
    </head>
    <body>
    <h1>File Transfer</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Function to display the uploaded file"""
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)

