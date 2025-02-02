import os
from langkit import lang_config
import string
import random


def _get_data_home() -> str:
    package_dir = os.path.dirname(__file__)
    data_path = os.path.join(package_dir, lang_config.data_folder)
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    return data_path


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))
