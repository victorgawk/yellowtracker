FROM python:3.10.8-alpine
WORKDIR /app
COPY . ./
RUN pip3 install -r requirements.txt
CMD [ "python", "./bot.py"]
