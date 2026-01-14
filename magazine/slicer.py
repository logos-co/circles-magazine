from PIL import Image
from pathlib import Path
import os


def split_image(file_path: str) -> tuple[Image.Image, Image.Image]:
    """
    Split the image 
    """
    img = Image.open(file_path)
    img = img.convert("RGB")       # now safe for JPEG
    # img.save("output.jpg", "JPEG")
    width, height = img.size

    # crop left and right halves
    left = img.crop((0, 0, width // 2, height))
    right = img.crop((width // 2, 0, width, height))

    return left, right

def get_folder(prompt: str) -> str:
    folder = input(prompt)
    if not os.path.exists(folder):
        raise Exception(f"Folder {folder} does not exist")
    
    return folder



if __name__ == "__main__":
    magazine_folder = get_folder("Magazine folder: ")
    save_folder = get_folder("Save folder: ")

    left_folder = os.path.join(save_folder, "left")
    os.makedirs(left_folder, exist_ok=True)
    right_folder = os.path.join(save_folder, "right")
    os.makedirs(right_folder, exist_ok=True)

    for path in Path(magazine_folder).rglob("*.png"):
        left, right = split_image(path)
        left.save(os.path.join(left_folder, path.name), "PNG")
        right.save(os.path.join(right_folder, path.name), "PNG")