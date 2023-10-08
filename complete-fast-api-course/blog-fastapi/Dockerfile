FROM python:3.9-slim

WORKDIR /blog-fastapi

COPY ./requirements.txt .

COPY ./pyproject.toml .

RUN apt-get update && pip install -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000