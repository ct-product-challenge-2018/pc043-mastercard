# start from an official image
FROM python:3

# skip buffering
ENV PYTHONUNBUFFERED 1

# create a directory in the container and set as working directory
RUN mkdir /code
WORKDIR /code

# copy the contents of entire directory to the directory in the container
COPY ./django  /code/

# install required packages
RUN pip install -r requirements.txt

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--bind", ":8000", "asine_me.wsgi:application"]