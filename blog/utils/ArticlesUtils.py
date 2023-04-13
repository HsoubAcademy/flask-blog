import os
import secrets
from blog import cfg


def save_image(image_file):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image_file.filename)
    image_new_name = random_hex + file_ext
    image_path = os.path.join(cfg.IMAGES_DIR, image_new_name)
    image_file.save(image_path)
    return image_new_name
