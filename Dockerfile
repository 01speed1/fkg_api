FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Asegúrate de que pip esté actualizado
RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]