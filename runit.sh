# kdesudo "docker build -t mongo-flask ."
rm foo.log* # clear logs
docker rm -f mongo-flask # remove old container - if any
# docker run -d --name=mongod mongo
docker run -p 80:80 --rm=true --link mongod:db --name=mongo-flask -v `pwd`:/usr/src/app jessedusty/mongo-flask # start new container
