#!/bin/bash
source venv/Scripts/activate
export FLASK_APP=flaskr
export FLASK_ENV=development
python -m flask run
