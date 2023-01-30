#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import requests
import epaper 
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import base64
from io import BytesIO
import cv2
import numpy as np

def load_image_and_resize(image, size=(224, 224)):
    image = image.resize(size)
    return image


def send_inference_request(prompt_value,negative_prompt="",inference_steps=100,guidance_scale=40,  url="http://goldrush:7860/run/predict"):
    response = requests.post(url, json={
    "data": [
        prompt_value,
        inference_steps,
        guidance_scale,
        negative_prompt,
        False,
    ]}).json()
    data = response["data"][0]
    # remove first instance of , and keep the rest
    data = data.split(",", 1)[1]
    return data

def image_from_base64(base64_string):
    imgdata = base64.b64decode(base64_string)
    image = Image.open(BytesIO(imgdata))
    return image

def convert_to_bmp(image):
    # convert to bmp
    image = image.convert("1")
    return image

def display_image(image):
    try:  
        epd = epaper.epaper("epd5in65f").EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        # convert the image to the display format
        # image = convert_to_bmp(image)
        # resize the image to the display size
        image = load_image_and_resize(image, size=(epd.height, epd.width))
        # display image
        epd.display(epd.getbuffer(image))
 
    except IOError as e:
        logging.info(e)
       
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()
    return

def reduce_to_7_colors(image):
    image = image.convert("P", palette=Image.ADAPTIVE, colors=7)
    return image


def diffuse_and_display(prompt_value,negative_prompt="",inference_steps=100,guidance_scale=40):
    # send the request to the server
    data = send_inference_request(prompt_value,negative_prompt,inference_steps,guidance_scale)
    # convert the response to an image
    image = image_from_base64(data)
    # reduce the image to 7 colors
    image = reduce_to_7_colors(image)
    # display the image
    display_image(image)
    return
    
