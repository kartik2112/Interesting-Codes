# Hiding Content behind images
## Psst... Have you ever wanted to send messages that can be understood only by some of your friends without others knowing about it?
### Then this is the right place.

This code will help you hide your text over a set of images

## Prerequisites
* MATLAB or equivalent on both the sender's and receiver's machine
* Paint by the sender who will write text in images

## Usage
* Create n images with resolution exactly same as image.jpg their names should begin with textHidden Eg. textHidden1.png.
  Preferably download the following image and edit in paint to add your content. This is because the code will use the resolution of the image to be sent. So if you use a higher resolution image then only part of it will appear to be hidden
  These are the images that should hold your code words like the following image:
  
  ![Example Image](textHidden1.png)
  
* Use Codes.txt to specify bit planes for n images
* Run HiddenText_Reveal.m. This will generate n images that have your code messages encoded
* Now you can decode using Bitplane_Slicing_1411113.m

For transmitting these code messages, send Codes.txt and imageX.png. Here X goes from 1 to no of images

Eg. Here the code message image is merged into image.jpg by replacing the 2nd LSB of each pixel

![Example Image](textHidden1.png) 

\+

![Example Image](image.jpg)

=

![Example Image](image1.png)

The last 2 images look the same don't they
But the last one has your code.

...use this tool carefully to send your code messages to your spy team :-P
