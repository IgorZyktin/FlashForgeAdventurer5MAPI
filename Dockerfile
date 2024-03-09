FROM python:3.10-slim
WORKDIR /app
RUN pip3 install flask==3.0.2
COPY ./adventurer5m ./adventurer5m
EXPOSE 9876
ENV FLASK_APP="./adventurer5m/app.py"
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=9876", "--debug"]
