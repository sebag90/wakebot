FROM python:3.14-slim
COPY run.py .

RUN pip install python-telegram-bot
RUN apt update && apt install -y wakeonlan

CMD ["python", "run.py"]
