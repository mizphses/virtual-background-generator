from PIL import Image, ImageDraw, ImageFont
import cv2
from qrcode import QRCode, constants
from uuid import uuid4
import os

def create_image(logo_image, name, status, has_qr, qr, has_img):
  # 画像の生成
  base_image = Image.new('RGBA', (1920, 1080), (255, 255, 255, 255))
  if not has_img:
    sage = int(base_image.size[1] / 8.5)
  else:
    sage = 0
  logo = Image.open(logo_image)
  logo_aspect_ratio = logo.size[0] / logo.size[1]
  logo = logo.resize((int(base_image.size[1] / 8.5 * logo_aspect_ratio), int(base_image.size[1] / 8.5)), Image.ANTIALIAS)
  base_image.paste(logo, (50, 50), logo)
  draw = ImageDraw.Draw(base_image)
  font = ImageFont.truetype('fonts/jp-semi.otf', 70)
  draw.text((70, int(base_image.size[1] / 6) - sage), name, (0, 0, 0), font=font)
  font = ImageFont.truetype('fonts/jp-semi.otf', 40)
  draw.text((70, int(base_image.size[1] / 6) + 90 - sage), status, (0, 0, 0), font=font)
  font = ImageFont.truetype('fonts/jp-semi.otf', 20)
  draw.text((70, base_image.size[1] - 80), '© 2023 mizphses / citrusnet', (0, 0, 0), font=font)
  draw.text((70, base_image.size[1] - 50), 'Create with mizphses.com/virtualBg', (0, 0, 0), font=font)
  if has_qr:
    qr_image = QRCode(
      version=1,
      error_correction=constants.ERROR_CORRECT_L,
      box_size=10,
      border=4,
    )
    qr_image.add_data(qr)
    qr_image.make(fit=True)
    qr_image = qr_image.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.resize((int(base_image.size[1] / 5), int(base_image.size[1] / 5)), Image.ANTIALIAS)
    draw.rectangle((base_image.size[0] - 60 - qr_image.size[0], 40, base_image.size[0] - 40, 60 + qr_image.size[1]), fill=(0, 0, 0, 255))
    base_image.paste(qr_image, (base_image.size[0] - 50 - qr_image.size[0], 50), qr_image)
    # ちょうど背景に黒い四角形を描画
  generation_id = str(uuid4())
  base_image.save(f'output_{generation_id}.png')
  return generation_id

if __name__ == '__main__':
  create_image('logo.png', 'mizphses', 'Citrusnet', True, 'https://mizphses.com')
