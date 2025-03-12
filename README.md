## Setup

You might want to create a virtual environment first, but this is optional:
`python -m venv venv`, then activate it with `source venv/bin/activate`

If this is the first time you're running this project, you might need to create the database file:
1. `python manage.py makemigrations`
1. `python manage.py migrate`

To populate (and reset) the database, run `python populate_db.py`

## Running

Start the web server with `python manage.py runserver`, you should be able to access it at http://localhost:8000.

The default customer account is `username: a, password: a12345678`

The default manager account is `username: manager, password: manager123`

Run Django shell with `python manage.py shell`

## Testing

The GitLab CI should automatically run all unit tests when you push to the repository.

If you wish to run the tests manually, run `python manage.py test`