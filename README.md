## Set up

install docker and docker-buildx packages

create the assets directory with the images that will be processed

to create the docker image from the Dockerfile run:
> $ docker buildx build -t smartable .

to run the container interactively run:
> $ docker run -it smartable /bin/bash

## About SmarTable

Utilizing Tesseract OCR and EasyOCR, SmarTable ensures accurate and efficient extraction of text from menu images, even in challenging scenarios.

Item Categorization: Automatically categorize each menu item by extracting its title, recipe, and price information. This feature simplifies the task of organizing and managing extensive menus.

Smartable is a tool that takes as input an image
of a menu and generates a JSON file.

This JSON will be a collection of all the dishes
in the menu that were read correctly.

Each entry in the JSON represents a dish and it's made up
of a Title, a Recipe and 1 or more Prices. There can be more 
than one price for each dish because sometimes, there are different
prices for each dish, due to different sizes, for example.

In the process of creating a JSON and reading the image, Smartable
needs the number of columns the image has and the number of prices 
for each dish.
Those can be obtained automatically or, preferably, can be given as input.  

## How to Use