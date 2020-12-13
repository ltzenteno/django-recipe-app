### Local Development

Since we have a `docker-compose.yml` file, we can run the following to build our image (*it is needed everytime we update our `requirements.txt` dependencies*):

    docker-compose build

Creating the Django Application (this was needed to be done just once):

    docker-compose run app sh -c "django-admin.py startproject app ."

*NOTE:* _Since I'm using a docker container for local development the IDE won't recognize the dependencies, unless I create a virtualenv (using pyenv) in my host machine tand run pip install there.
Then in the IDE settings choose the correct Python interpreter._

So, when a venv has been created and activated, just do:

    pip install -r requirements.txt

### Tests

to run the tests:

    docker-compose run app sh -c "python manage.py test"

to run the tests _and_ linter:

    docker-compose run app sh -c "python manage.py test && flake8"


### Creating core app

    docker-compose run app sh -c "c startapp core"


### Make migrations when a model has been created / updated

To create the DB migration files when craeting or updating models we have to use the `makemigrations` command along with the app name (i.e. `core)

    docker-compose run app sh -c "python manage.py makemigrations core"