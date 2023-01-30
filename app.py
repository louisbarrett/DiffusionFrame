
import gradio as gr
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
import argparse
import numpy as np

# replace with your own model 
display_type = "epd5in65f"

# gradio inference url
gradio_inference_url = "http://remotehost:7860/run/predict"

def load_image_and_resize(image, size=(224, 224)):
    image = image.resize(size)
    return image


def send_inference_request(prompt_value,negative_prompt="",inference_steps=100,guidance_scale=40,  url=gradio_inference_url):
    response = requests.post(url, json={
    "data": [
        prompt_value,
        inference_steps,
        guidance_scale,
        negative_prompt,
        False,
    ]}).json()
    data = response["data"][0]
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
        epd = epaper.epaper(display_type).EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        image = load_image_and_resize(image, size=(epd.height, epd.width))
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


def diffuse_and_display(prompt, num_inference_steps=100, guidance_scale=1, negative_prompt=None):
    # send the request to the server
    data = send_inference_request(prompt,negative_prompt=negative_prompt,inference_steps=num_inference_steps,guidance_scale=guidance_scale)
    # convert the response to an image
    image = image_from_base64(data)
    # reduce the image to 7 colors
    image = reduce_to_7_colors(image)
    # display the image
    display_image(image)
    return



# prompt from args

argparser = argparse.ArgumentParser()
argparser.add_argument("--learned_embeds_path", type=str,default="./model_output")
argparser.add_argument("--all",type=bool, default=False)
argparser.add_argument("--share",type=bool, default=False)
argparser.add_argument("--port",type=int, default=7860)

gradio_port = argparser.parse_args().port
arg_share = argparser.parse_args().share

gr.Interface(diffuse_and_display,
    [
        "text",
        gr.Slider(2, 800, value=40, label="inference steps"),
        gr.Slider(0.0, 100.0, value=40.0, label="guidance scale"),
        "text",
    ],
analytics_enabled=False,
allow_flagging="never",
title="Diffusion Frame 🖼️",
outputs="text",
description="Uses StableDiffusion to push images to digital picture frame",

).launch(
server_name="0.0.0.0",
server_port=gradio_port,
enable_queue=True,
show_api=False,
share = arg_share,
)