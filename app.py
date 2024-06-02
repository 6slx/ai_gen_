from flask import Flask, request, jsonify
import requests
import json
import hashlib
import time

app = Flask(__name__)

def generate_uuid():
    # Generate a UUID using a combination of current timestamp and a hash of the text
    timestamp = str(time.time()).encode('utf-8')
    return hashlib.sha1(timestamp).hexdigest()

def gen_photo(text, num, seed=-1, steps=50, guidance_scale=10, sampler='Euler a'):
    url = 'https://cognise.art/api/mobile/txt2img/generate/v4'
    head = {
        'Authorization': 'token 7bb91a6699cc3794750101ce0354d80195f07c04'
    }

    unique_user_uuid = generate_uuid()

    js = {
        "batch_size": num,
        "generation_id": 7,
        "generation_prompt": text,
        "generation_seed": seed,
        "generation_steps": steps,
        "guidance_scale": guidance_scale,
        "hit_point": "mobile",
        "img_ratio": "square",
        "negative_prompt": "",
        "sampler_index": sampler,
        "sampler_name": sampler,
        "sid": 19,
        "tz": "Africa/Cairo",
        "user_uuid": unique_user_uuid
    }

    try:
        response = requests.post(url, headers=head, json=js)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed"}

    if 'data' in results and 'images' in results['data']:
        image_urls = ['https://storage.cognise.art' + img['image'] for img in results['data']['images']]
        return {"image_urls": image_urls}
    else:
        return {"error": "No images found"}

@app.route('/gen', methods=['GET'])
def generate_images():
    text = request.args.get('text', '')
    num = request.args.get('num', '')

    try:
        num = int(num)
    except ValueError:
        return jsonify({"error": "Amount should be an integer (only numbers)!"}), 400

    if num > 4:
        return jsonify({"error": "You can't generate more than 4 images in one request"}), 400

    results = gen_photo(text, num)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)








#   python -m venv venv