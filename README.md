### Local Development

I am using a Docker container to avoid installing everything locally.

To build the image (it will install the dependencies listed in `requirements.txt`):

    docker build .

Since we have a `docker-compose.yml` file, we can instead run:

    docker-compose build

Creating the Django Application (this was needed to be done just once):

    docker-compose run app sh -c "django-admin.py startproject app ."