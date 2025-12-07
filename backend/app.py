from flask import Flask, jsonify, request
from src.form_module import create_form, delete_form, get_form, submit_form
from src.comments_module import create_comment, delete_comment

app = Flask(__name__)

form = []

#forums

#create
@app.route('/api/create_form/', methods=['POST'])
def c_f():
    data = request.get_json()
    if not data or 'topic' not in data or 'desc' not in data:
        return jsonify({"error": "Eksik veya yanlış formatta veri gönderildi (id, topic, desc zorunludur)."}), 400
    create_form(data['topic'], data['desc'], data.get('tags', []), form)
    return jsonify({"message": "Form kaydı başarıyla oluşturuldu"}), 201

#get
@app.route('/api/get_form/', methods=['GET'])
def g_f():
    get = get_form()
    return get

#submit
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

#delete
@app.route('/api/submit_form/<int:target_id>', methods=['POST'])
def s_f(target_id):
    if submit_form(target_id):
        return {"status": "success", "id": target_id}
    else:
        return {"status": "not_found", "id": target_id}, 404

#comment

#create
@app.route('/api/create_comment/<int:target_id>', methods=['POST'])
def c_c(target_id):
    
    data = request.json
    comment = data.get("comment")

    if not comment:
        return {"error": "comment required"}, 400

    if create_comment(comment, target_id):
        return {"status": "success", "id": target_id}
    else:
        return {"status": "not_found", "id": target_id}, 404

#delete
@app.route('/api/delete_comment/<int:forum_id>/<int:comment_id>', methods=['DELETE'])
def del_c(forum_id, comment_id):
    if delete_comment(forum_id, comment_id):
        return {"status": "success", "deleted_comment": comment_id}
    else:
        return {"status": "not_found"}, 404


if __name__ == '__main__':
    app.run(debug=True)