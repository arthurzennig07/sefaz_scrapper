from flask import Flask, request, jsonify
from Services import sefaz_es_parser as sefaz
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome Sefaz ES scrapper worker!'

@app.route('/health', methods=['GET'])
def health():
    return 'Welcome Sefaz ES scrapper worker health!'

@app.route('/scrap_this_link', methods=['POST'])
def scrap_some_link():
    req_data = request.get_json()
    link = req_data.get('link')
    print(link)
    compra = sefaz.fetch_and_parse_sefaz_link(link)
    print(compra.to_json())
    return compra.to_json(), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=6644)
