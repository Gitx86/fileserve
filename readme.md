# README

This script aims to create a webpage using flask with upload and download functionality
The goal is to create a download webpage for file transfer without credentials
The upload part of the code is not intended to be used but it is working so I have left it in.

##### Code notes
This code is written with some help from ChatGPT at the start. The AI was not able to give a solution for searching through multiple layers of folders so some part of the logic was re-written. Also the code is somewhat cleaned up with lesser redundencies.

##### Usage
Use at your own risk. I will not be responsible for any damages or coruption which could happen when the file is uploaded, downloaded, or stored within your computer or anything inbetween. That said, this is how you can use this script.

run file + folder e.g.

```sudo ./fileserve testfolder```

alternative to run for different script and folder location (testfolder in documents) e.g. 

```cd ~/Documents; sudo ~/Desktop/fileserve.py  testfolder```

This should point the script to open that specific folder.

##### Requirements 
This program requires Flask 
For Debian base linux, which uses apt package manager:
Either
``` sudo apt install python3-flask```

Or
```
sudo apt install python3-pip3
sudo pip3 install flask
```


##### Update
Edited to use <path:path> as previous ways of involking the webpage had a limitation on not being able to locate documents with the same name
OLD: webpage will aways be (Server Name)/File or folder name
New: webpage will have better indexing (Server Name)/Folder name/File name

