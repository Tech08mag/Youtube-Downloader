FROM python:3.11
ADD main.py
RUN pip install -r requirements.txt
CMD [“python”, “./main.py”]