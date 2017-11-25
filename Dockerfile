FROM python:3.6.1

# set working directory
RUN mkdir -p /app
WORKDIR /app

# add requirements (to leverage docker cache)
ADD ./requirements.txt /app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD . /app

# Run server
CMD python manage.py runserver -h 0.0.0.0