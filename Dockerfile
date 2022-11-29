FROM python:3.10-buster
WORKDIR /app
COPY app /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD python bot_main.py
