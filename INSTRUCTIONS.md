## Getting started

### Requirements

 * Python 2.6 or Python 2.7 ([install](http://www.python.org/getit/))
 * virtualenv ([install](https://pypi.python.org/pypi/virtualenv))
 * pip ([install](http://www.pip-installer.org/en/latest/installing.html))

### Installing

```
git clone https://github.com/OAButton/server.git /path/to/repo  # clone [the project code](https://github.com/OAButton/server)
cd /path/to/repo  # Switch to the directory where you've cloned the repo
git checkout django  # Switch to the django branch

virtualenv ENV  # Set up a new virtualenv
source env/bin/activate  # Start the virtualenv

sudo pip install -r requirements  # Install the dependencies

cd oabutton  # Switch to the django home directory
python manage.py syncdb  # sync the database
```

### Start the webserver

```
python manage.py runserver
```

 * visit <http://localhost:8000>. Hooray!

### Development

 * You must be in your virtualenv before you start hacking on oabutton.  
 * You can start your virtualenv using (`source env/bin/activate`).
