FROM python:3.9-slim

WORKDIR /usr/src/app

# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Do not buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && pip install --upgrade-pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000