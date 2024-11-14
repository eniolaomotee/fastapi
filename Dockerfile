# We'd need to specific our base image
# So in docker if you change your source code it would only run the last step which is the copy .., but if you change the requirements.txt it would run the copy req... and run statement as well.

FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["uvicorn", "app.main:app","--host","0.0.0.0","--port","8000"]


# Using docker compose to spin up your app and config
# Dockerfile is a set of instructions for building our images.
