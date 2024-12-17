# web-scrapping

Setup docker environment and then develop web scrapping tools to use in other projects

## Setup Docker environment
- Create Dockerfile with the content in it as an example
- Run `docker build -t <image_name> .` to build the image from the docker file. Here I run `docker build -t web-scrapping-image .`
- Run `docker images` to see the list of images
- Run `docker run -it <image_name> /bin/bash` to run the image. Here I run `docker run -it web-scrapping-image /bin/bash`