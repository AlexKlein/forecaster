# App for getting weather forecast over API

In this project I realized API with GET requests to getting weather forecast.

## Description

This repository consists of:

```
- loader of current weather forecast by city;
- loader of weekly weather forecast by city.
```

## Classes

Also the project contains a couple of classes, there are:
1. `task_status` - for definition of task statuses;
2. `task_manager` - for creation of multiprocesses handling.

## Asynchronous

Implemented async load for rubrics dictionary and both fact tables.

## Docker

When you need to build docker with app, then you have to follow this steps:
1. `docker build -t forecaster:latest .` - you will build image and load it to docker-machine;
2. `docker run --rm -d --net=host forecaster:latest` - you will start app with united host of container and docker-machine;
3. `http://192.168.99.100/` - you will check how container was started.

## Docker-compose

When you need to start the app with all infrastructure, you have to make this steps:
1. Set environment variables in [YML-file](./project/docker-compose.yml) 
2. `docker-compose up --build -d` - in this step app will builds and tables will create in pgSQL DB