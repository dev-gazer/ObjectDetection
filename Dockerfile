FROM ubuntu:20.04
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV LANG C.UTF-8
RUN apt-get update
RUN apt-get install python3-opencv -y python3 python3-pip
RUN pip3 install unidecode==1.1.1 opencv-python==4.5.1.48 opencv-contrib-python==4.5.2.52 requests==2.24.0 Flask==1.0.2 python-dotenv
ADD src /webapp/src
WORKDIR /webapp/src
CMD ["python3", "app.py"]
