#!/bin/bash
cd ..
docker build --no-cache -t cicd:actuald .
docker tag cicd:actuald registry:5000/actuald:$VERSION
docker push registry:5000/actuald:$VERSION
docker rmi cicd:actuald
