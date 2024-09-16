
FROM python:3.10
WORKDIR /applover
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]