# parent image (python 3.10)
FROM python:3.10-slim

# working directory
WORKDIR /code

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1


# install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

# expose port 8000
EXPOSE 8000

# run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

