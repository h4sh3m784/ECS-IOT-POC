FROM ubuntu:15.04

COPY . /h4sh3m784/ECS-IOT-POC

WORKDIR /h4sh3m784/ECS-IOT-POC

RUN pip install -r requirements.txt

USER root

ENTRYPOINT ["python"]

CMD ["app.py"]
