#!/usr/bin/env python3
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

download_file_template='''
    <!doctype html>
    <html>
    <head>
    <title>File Transfer</title>
    </head>
    <body>
    <h1>Uploaded Files</h1>
    <ul>
    {}
    </ul>
    </body>
    </html>
'''


def allowed_file(filename):
    """Function to check if a filename has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def findfile(fileName):
    # Function to find files within the folder, return the path
    print('file location is:')
    for root,dir,files in os.walk(app.config['UPLOAD_FOLDER']):
        if fileName in files:
            print(root)
            return root
        if fileName in dir:
            return (root)
    pass

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Function to handle file upload"""
    if request.method == 'POST':
        # Check if any files were uploaded
        if 'file' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('file')

        # Loop through all the uploaded files
        for file in files:
            # Check if the file has a valid filename
            if file.filename == '':
                continue

            # Check if the file is allowed to be uploaded
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('uploaded_files'))

    return '''
    <!doctype html>
    <html>
    <head>
    <title>File Transfer</title>
    </head>
    <body>
    <h1>File Transfer</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file multiple>
         <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

@app.route('/uploads')
def uploaded_files():
    """Function to display a list of uploaded files"""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return download_file_template.format(''.join('<li><a href="{}">{}</a></li>'.format(url_for('download_file', filename=filename), filename) for filename in files))

@app.route('/uploads/<filename>')
def download_file(filename):
    """Function to download a file"""
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename) 
    itempath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    print('The file name/path selected is ' + filename)
    # print(os.path.isdir(itempath))
    fileLocation = findfile(filename)
    #itempath = fileLocation
    print(itempath)
    if os.path.isdir(itempath):
        items = os.listdir(itempath)
        print('Reached into path')
        return download_file_template.format(''.join('<li><a href="{}">{}</a></li>'.format(url_for('download_file', filename=filename), filename) for filename in items))
    else:
        print('output file')
        #return send_from_directory(app.config['UPLOAD_FOLDER'], filename) 
        
        return send_from_directory(fileLocation, filename)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)

