# Guide to Installation

## Step 1

Install Python 3.9 and newer as it is the version which is supported by Flask.

## Step 2

Initialize new virtual environment in the project directory. Make sure you run this command inside the project directory.

> MacOS/Linux

    python3 -m venv .venv

> Windows

    python -m venv .venv

And make sure you activate your virtual environment using:

> MacOS/Linux

    . .venv/bin/activate

  > Windows

    .venv\Scripts\activate
  
or

    source .venv/Scripts/activate
  
It should shows `(.venv)` in your terminal to indicate that the virtual environment is active.

## Step 3

Install required packages.

    pip install -r requirements.txt

  

## Step 4

Run the app using:

    flask run

or:

    flask --debug run

Your app should be running in `127.0.0.1:5000`. Use `--debug` to auto-reload your server while in development.


# Things to note

Please use strict type checking within your text editor. If you're using VSCode, go to `Settings -> Extensions -> Pylance`, and search for `Type Checking Mode` and select `strict`.

Run `flask db upgrade` in your terminal after cloning/pulling to ensure your database has the latest version of migration.