FROM python:3.8

# create app directory
RUN mkdir -p /usr/src/hyperdrive
WORKDIR /usr/src/hyperdrive

# copy requirements.txt to container
COPY requirements.txt /tmp/requirements.txt
# install dependencies
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
# clean
RUN rm /tmp/requirements.txt

COPY app/ /usr/src/hyperdrive

# CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
CMD ["python", "./api_server.py"]

# EXPOSE 8080
