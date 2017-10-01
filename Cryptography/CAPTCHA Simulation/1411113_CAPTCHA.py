# Prerequisite:

# 1.
# captcha must be installed before running this program
# To do this type in terminal / Powershell:
#     pip3 install captcha   
# If this doesnt work
# Type these:
#     python3
#     import pip
#     pip.main(['install','captcha'])

# 2.
# Image module must also be installed
# To do this type in terminal / Powershell:
#     pip3 install Image   
# If this doesnt work
# Type these:
#     python3
#     import pip
#     pip.main(['install','Image'])


from io import BytesIO
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha

from PIL import Image

import random
R1 = random.randint(4,10)
str1 = ""
while R1>0:
    R2 = random.randint(4,10)
    if R2<6:
        R3 = str(random.randint(4,10))
    else:
        R3 = chr(ord('A')+random.randint(0,25))
    str1 += R3

    R1-=1
# print("Generated Captcha is:",str1)
image = ImageCaptcha(fonts=['arial.ttf','times.ttf'])
data = image.generate(str1)
assert isinstance(data, BytesIO)
image.write(str1, 'out.png')

Image.open('out.png').show()

UInputCaptcha = input("Captcha Calculated and Image generated from text.\nEnter captcha text: ")

if UInputCaptcha == str1:
    print("Correct captcha entered!")
else:
    print("Incorrect captcha entered!!!")