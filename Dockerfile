FROM python:3.10-slim


WORKDIR /app


COPY . .


RUN pip install --upgrade pip && pip install -r requirements.txt


ENV PYTHONDONTWRITEBYTECODE=1


CMD ["python", "-m", "cli.cli"]
