from PIL import Image
from pathlib import Path
import uuid
import os

def crop_center(img, target_w, target_h):
    w, h = img.size
    left = (w - target_w) // 2
    top = (h - target_h) // 2
    right = left + target_w
    bottom = top + target_h
    return img.crop((left, top, right, bottom))

from PIL import Image
from pathlib import Path
import uuid

def crop_by_align(img, target_w, target_h, align):
    w, h = img.size

    # Визначаємо позицію
    align = align.lower()
    if '-' in align:
        vertical, horizontal = align.split('-')
    elif align in ("center",):
        vertical, horizontal = "center", "center"
    else:
        # fallback
        vertical, horizontal = "center", "center"

    # Горизонтальна позиція
    if horizontal == "left":
        left = 0
    elif horizontal == "center":
        left = (w - target_w) // 2
    elif horizontal == "right":
        left = w - target_w
    else:
        left = (w - target_w) // 2

    # Вертикальна позиція
    if vertical == "top":
        top = 0
    elif vertical == "center":
        top = (h - target_h) // 2
    elif vertical == "bottom":
        top = h - target_h
    else:
        top = (h - target_h) // 2

    # Перевірка меж
    left = max(0, min(left, w - target_w))
    top = max(0, min(top, h - target_h))
    right = left + target_w
    bottom = top + target_h

    return img.crop((left, top, right, bottom))

def process_template(image_path: Path, template_data: dict):
    img = Image.open(image_path)
    output_info = []

    for idx, fmt in enumerate(template_data["formats"]):
        width = fmt["width"]
        height = fmt["height"]
        align = fmt.get("align", "center")

        cropped = crop_by_align(img, width, height, align)

        out_path = Path("user_data") / f"{uuid.uuid4().hex}.jpg"
        cropped.save(out_path)

        output_info.append({
            "path": out_path,
            "width": width,
            "height": height,
            "align": align
        })

    return output_info
