FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["unicorn", "app.main:app", "--host", "0.0.0.0", "--post", "8000"]