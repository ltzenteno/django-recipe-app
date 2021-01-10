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

    docker-compose run --rm app sh -c "python manage.py test && flake8"


### Creating core app

    docker-compose run --rm app sh -c "python manage.py startapp core"


### Make migrations when a model has been created / updated

To create the DB migration files when creating or updating models we have to use the `makemigrations` command along with the app name (i.e. `core)

    docker-compose run app sh -c "python manage.py makemigrations core"

To run the containers

    docker-compose up -d

Once we set up the Postgres DB and the needed tables have been created, we can create a super user with:

    docker-compose run app sh -c "python manage.py createsuperuser"

Then I created the user app folder with (no need to run again):

    docker-compose run --rm app sh -c "python manage.py startapp user"

*NOTE:* _following the course, I remove the `user/admin.py` `user/models.py`, `user/migrations` since that exists in `core` app. Also I removed `user/tests.py` since I am creating a `user/tests` folder._


### Creating the recipe app

    docker-compose run --rm app sh -c "python manage.py startapp recipe"