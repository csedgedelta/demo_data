FROM python:3.12-slim
WORKDIR /app

COPY /app /app
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3","/app/app.py"]
