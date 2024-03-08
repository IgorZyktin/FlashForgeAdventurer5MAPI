FROM python:3.10-slim
WORKDIR /app
RUN pip3 install flask==3.0.2
COPY ./adventurer5m .
EXPOSE 5000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000", "--app", "./adventurer5m/app.py", "--debug"]
