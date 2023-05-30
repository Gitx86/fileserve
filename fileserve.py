#!/usr/bin/env python3
import os
import sys
from flask import Flask, request, redirect, url_for, send_from_directory

# Folder Checker
args = sys.argv
if len(args) <=1:
    print('No Folder Specified')
    exit()

mainFolder = args[1].replace('/','')
currentFolder = os.listdir('.')

if mainFolder in currentFolder:
    print('Folder OK')
    # get full folder path to current folder
    fullPath = os.getcwd() + '/'
    print(fullPath)
else:
    print('No such folder in directory ' + mainFolder)
    print('Possible Folders: ')
    for folder in currentFolder: print('  ' + folder)
    exit()

UPLOAD_FOLDER = mainFolder
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'}

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
            return (root,fileName)
        if fileName in dir:
            return (root,fileName)
    pass

@app.route('/upload', methods=['GET', 'POST'])
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

@app.route('/')
def uploaded_files():
    """Function to display a list of uploaded files"""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # .format(link,name of link)
    return download_file_template.format(''.join('<li><a href="{}">{}</a></li>'.format(UPLOAD_FOLDER, 'test' )))

@app.route('/<path:path>')
def findpath(path):
    """Function to download a file"""
    last_folder=path.split('/')[::-1][0]
    if last_folder == '':
        last_folder=path.replace('/','')
    print('path = '+ path)
    print('last folder = '+last_folder)

    #Folder check
    # if os.path.isdir(UPLOAD_FOLDER + '/' + path):
    #     items = os.listdir(UPLOAD_FOLDER + '/' + path)
    if os.path.isdir(path):
        items = os.listdir(path)
        print(items)
        # .format(path,filename) loop for all the filename in the folder
        retoutput=download_file_template.format(''.join('<li><a href="{}">{}</a></li>'.format(last_folder+'/'+itemname, itemname) for itemname in items))
        return retoutput
    else:
        # Return file
        return send_from_directory(fullPath + path.replace(last_folder,''),last_folder)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)

