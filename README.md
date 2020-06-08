# RishaCar

A Restful API for a carpool mobile application `RichaCar`
Using Python(Tornado) and MongoDB
---
## Requirements

For development, you will need 
- Python
- A python global package, Pip, installed in your environement.
- MongoDB

### Python

you can download it from [here](https://www.python.org/downloads)

### Pip

you can download it from [here](https://pip.pypa.io/en/stable/installing)

### MongoDB

you can download it from [here](https://www.mongodb.com/download-center)

---

## Install

    $ git clone https://github.com/saraheisa/rishacar
    $ cd rishacar
    $ pip install

## Configure app

You may need to change MongoDB's connection address in `lib/DBConnection.py`
if it's different in your machine, commonly it's the same

## Running the project

### Start DB
    run 
    $ C:\path\to\mongodb\bin\mongod.exe

If you're using VSCode you can use [Azure extension]('https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb') to connect to DB

### Start the app
    $ python app.py