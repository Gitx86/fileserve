#!/bin/python3

from flask import Flask

app = Flask(__name__) #point to this location

@app.route("/") #basically index location

def index():
    return "Test something here"
    pass


app.run(host="0.0.0.0", port=80)



