FROM python:3
WORKDIR /usr/src/app
COPY ./requirements.txt ./
COPY ./ServiceSOAP.py ./
EXPOSE 80
CMD [ "python", "./ServiceSOAP.py"]