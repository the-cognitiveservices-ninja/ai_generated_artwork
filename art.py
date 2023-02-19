import openai
import urllib.request
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
from datetime import datetime
import sys

# parameters - adjust to your needs
number_of_images = 2
image_size = "1024x1024"
additional_keywords = (
    ", HD photograph, nikon camera, studio lighting, on Kodak TriX film"
)
# parematers end - do not touch the rest


openai.api_key = os.environ["OPENAI_API_KEY"]

def send_openai_request(engine, prompt, max_tokens=1000):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response


prompt_base = "Generate a detailed Dall-E prompt with several adjectives for "
prompt_details = sys.argv[1]
model = "text-davinci-003"

response = send_openai_request(model, prompt_base + prompt_details)

def send_openai_request(engine, prompt, max_tokens=1000):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response

generated_prompt = response["choices"][0]["text"]
image_generation_prompt = f"{generated_prompt} {additional_keywords}"

response = openai.Image.create(
    prompt=image_generation_prompt,
    n=number_of_images,
    size=image_size,
)


timestamp_string = response.created
datetime_string = datetime.fromtimestamp(timestamp_string).strftime("%Y%m%d%H%M%S")


def get_images(response):
    image_list = []
    for imgurl in response.data:
        image_list.append(imgurl.url)
    return image_list


image_list = get_images(response)
print(image_list)


def download_images(image_list, datetime_string):
    os.mkdir(f"images/{datetime_string}")
    for i in range(len(image_list)):
        urllib.request.urlretrieve(image_list[i], f"images/{datetime_string}/{i}.png")

download_images(image_list, datetime_string)


def display_images(image_list):
    for i in range(len(image_list)):
        img = mpimg.imread(f"images/{datetime_string}/{i}.png")
        plt.imshow(img)
        plt.show()


display_images(image_list)
print(image_generation_prompt)
