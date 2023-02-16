FROM yolov5_training:latest

RUN apt-get update && apt-get install -y net-tools
ADD . /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "microservice:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
# docker build -t web .