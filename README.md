# django-pastryshop
A pastryshop that is able to register a user, user can order pastries, can go to cart to check the items, then they can go to checkout page also, and after that user can pay what they have purchase.After the purchase complete users can track their order too.

# Installation:

# Activate the virtual envirenment first,
Install virtualenv
virtualenv is a virtual environment where you can install software and Python packages in a contained development space, which isolates the installed software and packages from the rest of your machine’s global environment. This convenient isolation prevents conflicting packages or software from interacting with each other.

To install virtualenv, we will use the pip3 command, as shown below:
```
pip3 install virtualenv
```
While inside the root directory, create your virtual environment. Let’s call it env.
```
virtualenv env
```
Now, activate the virtual environment with the following command:
```
. env/bin/activate
```

* Install the latest version of django by using:
```
pip install django
```
* Run the command to install the additional packages
```
pip install -r requirements.txt
```
# Database Connectivity
Download and install the postgresql according to your distribution:
```
https://www.postgresql.org/download/
```
## After installing it give the default username 'shivanshu' and password 'root'

now go to the databases and create a new database with the name 'pastryShop'

# After doing everything run the following commands:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py runserver
```
and now open any browser and go to the link:
```
http://127.0.0.1:8000/
```
your website will be running at this link if everything went right!

## For accessing admin panel:
```
http://localhost:8000/admin
```
username:'pastryAdmin'

password:'root'


<hr>
        <div align="center" >Made with :heartbeat: by Shivanshu  </div>
