# -*- coding: utf-8 -*-

from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
import qrcode

TEMPLATE_PATH = 'files\\ticket_sample2.png'
FONT_PATH = 'files\\Roboto-Regular.ttf'
FONT_SIZE = 60

BLACK = (0, 0, 0, 255)
NAME_OFFSET = (120, 793)
EMAIL_OFFSET = (120, 885)

AVATAR_RESIZE = (450, 450)
AVATAR_OFFSET = (120, 160)

QR_OFFSET = (1645, 300)


def generate_ticket(name, email):
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    response = requests.get(url=f'https://robohash.org/bgset_bg2/{email}?size=600x600')
    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)

    qr = generate_code(email=email)
    qr_image = Image.open(qr)
    qr_image.thumbnail(AVATAR_RESIZE)

    base.paste(avatar, AVATAR_OFFSET)
    base.paste(qr_image, QR_OFFSET)

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    base.show()

    return temp_file




def generate_code(email):
    code_text = email

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )

    qr.add_data(code_text)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image_like = BytesIO()
    image.save(image_like, 'png')

    return image_like


generate_ticket(name='Попыт', email='simple_dimple@gmail.com')
