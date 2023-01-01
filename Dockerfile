FROM python:3.9.16-alpine
WORKDIR /app
COPY src ./
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD [ "python", "app.py"]
