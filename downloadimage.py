import shutil
import requests

def download_image(url, image_name):
    response = requests.get(url, stream=True)
    with open(f'data/img/{image_name}.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

