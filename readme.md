# Millionaire Game
A simple quiz game based on django framework

## Installation
>This project come with a sqlite database which contain 8 questions to speed things for you. You can choose how to use this repository
### Use ready-to-use Sqlite database
```
git clone https://github.com/mohsenone/millionaire.git
cd millionarie
pip install -r requirements.txt
python manage.py runserver
# now go to localhost:8000 and login with username admin and password aaaAAA123@
```

### Clean start
```
git clone https://github.com/mohsenone/millionaire.git
cd millionarie
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
# now go to localhost:8000 and login with your username and password
```