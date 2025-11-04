from flask import Flask, request, jsonify
from uuid import uuid4
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)


#funções de load e save
def load_json():
    try:
        with open('db.json', 'r') as data:
            return json.load(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_json(data):
    with open('db.json', 'w') as db:
        json.dump(data, db, indent=4)

def load_xml():
    try:
        et = ET.parse('data.xml')
        root = et.getroot()
        data = {child.tag: child.text for child in root}
        return data
    except (FileNotFoundError, ET.ParseError):
        return {}

def save_xml(data):
    root = ET.Element("data")
    for key, value in data.items():
        item = ET.SubElement(root, key)
        item.text = value
    et = ET.ElementTree(root)
    et.write('data.xml')


#rotas
@app.route('/movies/json', methods=['GET'])
def get_json():
    try:
        data = load_json()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movies/xml', methods=['GET'])
def get_xml():
    try:
        data = load_xml()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/movies/jsonc', methods=["POST"])
def create_movieJ():
    try:
        new_data = request.json
        data = load_json()
        data.update(new_data)
        save_json(data)
        return jsonify({"mensagem": "Json adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movies/xmlc', methods=["POST"])
def create_movieX():
    try:
        new_data = request.json
        data = load_xml()
        data.update(new_data)
        save_xml(data)
        return jsonify({"mensagem": "XML adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/movies/delete', methods=['DELETE'])
def delete_data():
    try:
        chave = request.args.get('key')
        json_data = load_json()
        xml_data = load_xml()

        if chave in json_data:
            del json_data[chave]
            save_json(json_data)

        if chave in xml_data:
            del xml_data[chave]
            save_xml(xml_data)

        return jsonify({"mensagem": f"Dados com chave '{chave}' deletados"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

 
if __name__ == '__main__':
    app.run(debug=True)