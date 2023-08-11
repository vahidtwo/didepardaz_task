# didepardaz_task

## project setup

1- Go inside the project
```
cd Project_name
```

2- SetUp venv
```
virtualenv venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```
5.1- Create database
```sql
create database didepardaz_task;
```
5.2- Create tables
```
python manage.py migrate
```

6- run the project
```
python manage.py runserver
```
7- load data
```
python manage.py loaddata ./**/fixtures/*
```
!note for use admin-panel create superuser
```
python manage.py createsuperuser
```

