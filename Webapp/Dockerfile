#Zugrunde liegendes Image
FROM python:3.9

WORKDIR /Webapp/

#copieren des aktuellen verzeichnisses in / Webapp
ADD . /Webapp
ADD . /Webapp/Web/
COPY ./requirements.txt Webapp/requirements.txt

#installiert alle dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# #Port 80 veröffentlichen
EXPOSE 80

#führt die python app aus
CMD ["fastapi", "run", "/Webapp/main.py", "--proxy-headers", "--port", "80"]