## Set up

install docker and docker-buildx packages

create the assets directory with the images that will be processed

to create the docker image from the Dockerfile run:
> $ docker buildx build -t smartable .

to run the container interactively run:
> $ docker run -it smartable /bin/bash
