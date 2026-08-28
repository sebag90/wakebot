FROM python:3.14-slim
COPY run.py .

RUN pip install python-telegram-bot wakeonlan

CMD ["python", "run.py"]
