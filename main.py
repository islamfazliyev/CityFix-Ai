from flask import Flask, jsonify, request
from src.form_module import create_form, delete_form, get_form

app = Flask(__name__)

form = []

@app.route('/api/create_form/', methods=['POST'])
def c_f():
    data = request.get_json()
    if not data or 'topic' not in data or 'desc' not in data:
        return jsonify({"error": "Eksik veya yanlış formatta veri gönderildi (id, topic, desc zorunludur)."}), 400
    create_form(data['topic'], data['desc'], data.get('tags', []), form)
    return jsonify({"message": "Form kaydı başarıyla oluşturuldu"}), 201

@app.route('/api/get_form/', methods=['GET'])
def g_f():
    get = get_form()
    return get

@app.route('/api/delete_form/<int:target_id>', methods=['DELETE'])
def d_f(target_id):
    body = request.get_json()

    if not body or "id" not in body:
        return jsonify({"error": "id missing"}), 400
    
    target_id = body["id"]

    try:
        current_form_data = get_form()
    except FileNotFoundError:
        return jsonify({"error": "No forms found to delete from."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Data file is corrupted or empty."}), 500

    initial_length = len(current_form_data)
    
    delete_form(current_form_data, target_id)
    
    final_length = len(current_form_data)

    if final_length < initial_length:
        return jsonify({"message": f"Form with id {target_id} successfully deleted"}), 200
    else:
        return jsonify({"error": f"Form with id {target_id} not found"}), 404

    

if __name__ == '__main__':
    app.run(debug=True)