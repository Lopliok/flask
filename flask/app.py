import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cesta k souboru pro ukládání záznamů
DATA_FILE = 'records.json'

# Funkce pro načtení záznamů ze souboru
def load_records():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Pokud soubor neexistuje, vrátíme prázdný seznam
    except json.JSONDecodeError:
        return []  # Pokud je soubor poškozený, vrátíme prázdný seznam

# Funkce pro uložení záznamů do souboru
def save_records(records):
    with open(DATA_FILE, 'w') as file:
        json.dump(records, file, indent=4)

@app.route('/add', methods=['POST'])
def add_record():
    try:
        # Získání dat z požadavku
        user = request.json.get('user')
        item = request.json.get('item')
        price = request.json.get('price')

        # Ověření, zda jsou všechna pole vyplněna
        if not user or not item or not price:
            return jsonify({'error': 'All fields (user, item, price) are required.'}), 400

        # Načtení aktuálních záznamů
        records = load_records()

        # Přidání nového záznamu
        record = {'user': user, 'item': item, 'price': price}
        records.append(record)

        # Uložení záznamů do souboru
        save_records(records)

        return jsonify({'message': 'Record added successfully.', 'record': record}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/records', methods=['GET'])
def get_records():
    try:
        # Načtení záznamů ze souboru
        records = load_records()
        return jsonify({'records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
