FROM python:3.8-slim-buster

# Work Directory
WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD  python ./app.py
