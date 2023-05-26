from PIL import Image
from base64 import b64encode, b64decode
from flask import Flask, request, jsonify
from flask_cors import CORS
from uuid import uuid4
import os
from qrcode import QRCode, constants

from create import create_image

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/create', methods=['POST'])
def create():
  # リクエストの取得
  request_json = request.get_json()
  has_img = True
  if request_json['logo']:
    logo_base = request_json['logo']
    logo_image = b64decode(logo_base[22:])
    logo_image_name = str(uuid4()) + '.png'
    with open(logo_image_name, 'wb') as f:
      f.write(logo_image)
  else:
    #200*200の白い画像を作成
    logo_image = Image.new('RGBA', (200, 200), (255, 255, 255, 255))
    logo_image_name = str(uuid4()) + '.png'
    logo_image.save(logo_image_name)
    has_img = False
  name = request_json['name']
  status = request_json['department']
  use_qr = request_json['use_qr']
  qr = request_json['qr']
  generation_id = create_image(logo_image_name, name, status, use_qr, qr, has_img)
  if logo_image_name:
    os.remove(logo_image_name)
  with open(f'output_{generation_id}.png', 'rb') as f:
    output_image = f.read()
  os.remove(f'output_{generation_id}.png')
  return output_image
if __name__ == '__main__':
  app.run(debug=True, port=5001)