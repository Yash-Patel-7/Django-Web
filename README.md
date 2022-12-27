# Django Web Application

## Deployment to Heroku

1. Create a new app on heroku : https://www.heroku.com/
2. Under the Settings tab on heroku, set the following environment variables:
   1. EMAIL = 'email_address'
   2. PASSWORD = 'password'
   3. SECRET_KEY = Python > secrets.token_hex(100)
   4. DEBUG_VALUE = 'False'
   5. DATABASE_URL = Set by Heroku
   6. HOST_1 = 'url'
   7. HOST_2 = 'url'
   8. HOST_3 = 'url'
   9. ORIGIN = 'url'
4. Install the python version found in runtime.txt : https://www.python.org/downloads/
5. Download this repository and place the Junjut-master folder onto the desktop
6. Open up the terminal for macOS
7. Set up a new virtual environment: 
   1. python3 -m venv desktop/django_env && source desktop/django_env/bin/activate && cd desktop/Junjut-master
8. Install the dependencies found in requirements.txt:
   1. pip3 install Django==3.2.5 && pip3 install asgiref==3.4.1 && pip3 install dj-database-url==0.5.0 && pip3 install gunicorn==20.1.0 && pip3 install psycopg2-binary==2.9.1 && pip3 install pytz==2021.1 && pip3 install sqlparse==0.4.1 && pip3 install whitenoise==5.2.0 && pip3 install django-csp==3.7 && pip3 install django-permissions-policy==4.1.0 && pip3 install django-heroku==0.3.1
10. Under the Deploy tab on heroku, follow the instructions for Heroku CLI to push the Junjut-master repository
11. Run the terminal on the server:
    1. heroku run bash
13. Set up the database:
    1. python3 manage.py migrate && python3 -c 'from home.database import *; db_create()'
14. Create an account for the website administrator
15. Give admin permissions to your account:
    1. python3 -c "from account.database import *; db_admin('email_address', True)"

## Tech Stack

![django-logo-negative 1d528e2cb5fb](https://user-images.githubusercontent.com/117030897/209620257-bc18241b-9ce7-4f70-bbb8-0b7aea1d73a0.png)
![Python-logo-notext svg](https://user-images.githubusercontent.com/117030897/209620264-9a8f2df4-65b5-4cac-87ce-1d7044502bd4.png)
![1 eUTK5gvvm8H1_kGR_S6Ncg](https://user-images.githubusercontent.com/117030897/209688138-500a39ea-cb44-4a88-8bfd-370d95ed9977.png)
![javascript-vs-html-vs-css-1024x683](https://user-images.githubusercontent.com/117030897/209620263-6d6f4658-40bb-43b1-9cd6-edebb54ecfc6.jpg)
![Happy-User](https://user-images.githubusercontent.com/117030897/209620261-610a014b-cabf-4d35-9dec-3ac6b7e71c6a.png)
![maxresdefault](https://user-images.githubusercontent.com/117030897/209688395-978874fd-d922-4de3-be6c-eb291d728774.jpg)
![Heroku_logo svg](https://user-images.githubusercontent.com/117030897/209688239-7b02ff3f-e7b0-485a-9b38-bf45878e4b3d.png)

