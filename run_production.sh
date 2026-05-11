killall python3

python3 -m pip install -r requirements.txt

FLASK_ENV=production nohup python3 app.py &
