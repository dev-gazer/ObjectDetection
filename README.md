# ObjectDetection
Sure, a livestream object detection code with OpenCV. I bet you weren't able to find one Dockerized and as a Web Application, so I decided to make it available for you to try it out!.
Its window shoud be something like that, maybe less funnier :P:
![alt text](https://github.com/dev-gazer/ObjectDetection/blob/master/how_it_detects.png)

The output on Telegram, on the other hand, will be something like this:
![alt text](https://github.com/dev-gazer/ObjectDetection/blob/master/output_on_telegram.jpg)

### Installation
##### Prerequisites
- [Docker](https://docs.docker.com/v17.09/engine/installation/#supported-platforms)
- [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

##### Clone the project

```sh
$ git clone https://github.com/dev-gazer/ObjectDetection.git
```


##### Start the service
```sh
$ cd ObjectDetection/src
$ sudo docker build -t ObjectDetection .
$ sudo docker run -it -p 5000:5000 --device /dev/video0 ObjectDetection
```
NOTE1: Be aware that you must specify the path to your device in docker run. The command "--device /dev/video0" refers to it. 
NOTE2: You may need to use a different port than port 5000. In this case use an available port on your host.


##### Stop the service
```sh
$ sudo docker stop ObjectDetection
$ docker rm ObjectDetection
```
