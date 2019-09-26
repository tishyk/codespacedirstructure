import time
import os
import glob
import concurrent.futures
from PIL import Image, ImageFilter

img_names = glob.glob("src_img/photo*")

t1 = time.perf_counter()

size = (1200, 1200)


def process_image(img_name):
    img = Image.open(img_name)

    img = img.filter(ImageFilter.GaussianBlur(15))

    img.thumbnail(size)
    img.save(f'processed/{os.path.basename(img_name)}')
    print(f'{img_name} was processed...')


if __name__ == "__main__":

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image, img_names)
    print(f"Done in {time.perf_counter()}")
