import openai
import yaml
import urllib.request
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
from datetime import datetime

# get API Key
#yaml_file = open("apikeys/openai.yml", "r")
#p = yaml.load(yaml_file, Loader=yaml.FullLoader)
#openai.api_key = p["api_key"]


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


# prompt to the language model
prompt_base = "Generate a detailed Dall-E prompt with several adjectives for "  # an introduction text telling the language model what to do
prompt_details = "two boys, two girls visible from behind sitting on the floor infront of brandenburg gate, drinking beer and smoking weed on a sunny day"
additional_keywords = ", HD photograph, nikon camera, studio lighting, on Kodak TriX film"  # these keywords will be added after the language model generated the prompt. Example: "digital art", "oil painting", "water color painting", "high quality"

model = "text-davinci-003"  # the version of the openai language model
# generate a response
response = send_openai_request(model, prompt_base + prompt_details)

# print the response from the language model
generated_prompt = response["choices"][0]["text"]
# define the request
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


response = send_openai_request(model, prompt_base + prompt_details)


generated_prompt = response["choices"][0]["text"]
# image parameters
number_of_images = 2  # how many images you want to generate
image_size = "1024x1024"  # the size of the images
image_generation_prompt = f"{generated_prompt} {additional_keywords}"

# define and send the request to dall-e with the generated prompt
response = openai.Image.create(
    prompt=image_generation_prompt,
    n=number_of_images,
    size=image_size,
)

# set the timestamp for data processing
timestamp_string = response.created
datetime_string = datetime.fromtimestamp(timestamp_string).strftime("%Y%m%d%H%M%S")

# get the image(s) from the response
def get_images(response):
    # generate an empty list for the image urls
    image_list = []

    # store the image urls in the list
    for imgurl in response.data:
        image_list.append(imgurl.url)
    return image_list


image_list = get_images(response)

# display image urls
print(image_list)

# download the images
def download_images(image_list, datetime_string):
    # create a folder for the images
    os.mkdir(f"images/{datetime_string}")

    # download the images
    for i in range(len(image_list)):
        urllib.request.urlretrieve(image_list[i], f"images/{datetime_string}/{i}.png")


download_images(image_list, datetime_string)

# display the images
def display_images(image_list):
    for i in range(len(image_list)):
        img = mpimg.imread(f"images/{datetime_string}/{i}.png")
        plt.imshow(img)
        plt.show()


display_images(image_list)

# display the prompt
print(image_generation_prompt)