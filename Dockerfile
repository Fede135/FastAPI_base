FROM python:3.8

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./sql_app /sql_app

COPY ./app /app

# Put keys in the code is a bad practice we should move this to any secrets manager or store them
# encrypted in the database or provide this env variable when execute the docker run.
# To keep the things simple I decided to put this here, at least for now
ENV FOOTBALL_KEY df4c87d4d8ab43b485488a27803f8c05

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
