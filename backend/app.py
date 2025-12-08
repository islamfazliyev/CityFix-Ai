import os
from flask import Flask, jsonify, request, send_from_directory
from src.form_module import create_form, delete_form, get_form, submit_form
from src.comments_module import create_comment, delete_comment
from src.login_register_module import login, register
from src.ai_module import add_ai_tags_to_data
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__)

CORS(app, supports_credentials=True)

form = []
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#forums
data = f"./data/data.json"
#create

@app.route('/api/create_form/', methods=['POST'])
def c_f():
    if 'image' not in request.files:
        return jsonify({"error": "Resim dosyası gerekli"}), 400

    image = request.files['image']
    topic = request.form.get('topic')
    desc = request.form.get('desc')
    
    manual_tags = [] 

    if not topic or not desc:
        return jsonify({"error": "topic ve desc zorunludur"}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(image_path)

    created_id = create_form(
        image_filename=filename, 
        topic=topic, 
        description=desc, 
        tags=manual_tags
    )

    if created_id:
        try:

            add_ai_tags_to_data(created_id, image_path)
        except Exception as e:
            print(f"AI Tag hatası: {e}")
            
    return jsonify({"message": "Form başarıyla oluşturuldu", "id": created_id}), 201


#get
@app.route('/api/get_form/', methods=['GET'])
def g_f():
    get = get_form()
    return get

#delete
@app.route('/api/delete_form/<int:target_id>', methods=['DELETE'])
def d_f(target_id):
    try:
        current_form_data = get_form()
    except FileNotFoundError:
        return jsonify({"error": "No forms found to delete from."}), 404
    except Exception:
        return jsonify({"error": "Data file is corrupted or empty."}), 500

    initial_length = len(current_form_data)
    
    delete_form(current_form_data, target_id)
    
    final_length = len(current_form_data)

    if final_length < initial_length:
        return jsonify({"message": f"Form with id {target_id} successfully deleted"}), 200
    else:
        return jsonify({"error": f"Form with id {target_id} not found"}), 404

#submit
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

#Login/Register

#login
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json

    tc = data.get("tc")
    password = data.get("password")

    if not tc or not password:
        return {"error": "tc and password required"}, 400

    result = login(tc, password)
    return result

#Register
@app.route('/api/register', methods=['POST'])
def api_register():
    data_in = request.json

    tc = data_in.get("tc")
    name = data_in.get("name")
    last_name = data_in.get("last_name")
    phone_number = data_in.get("phone_number")
    password = data_in.get("password")

    if not all([tc, name, last_name, phone_number, password]):
        return {"error": "all fields required"}, 400

    result = register(tc, name, last_name, phone_number, password)

    if result == "tc_exists":
        return {"status": "tc_exists"}, 409

    if result == "phone_exists":
        return {"status": "phone_exists"}, 409

    if result is True:
        return {"status": "success"}, 201

    return {"status": "error"}, 500

#AI

#TXT2TAG
@app.route('/api/txt2tag', methods=['POST'])
def define_tags():
    temp_image_path = None 

    try:
        
        if 'id' not in request.form or 'image' not in request.files:
            return jsonify({"error": "Eksik form verisi: 'id' veya 'image' dosyası gerekli."}), 400

        item_id = int(request.form['id'])
        image_file = request.files['image']

        filename = secure_filename(image_file.filename)
        temp_image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(temp_image_path)

        add_ai_tags_to_data(item_id, temp_image_path)
        
        return jsonify({
            "message": f"Yapay zeka etiketleri başarıyla oluşturuldu ve ID {item_id} için eklendi.",
            "id": item_id
        }), 200

    
    except ValueError:
        return jsonify({"error": "Geçersiz ID formatı veya veri yapısı hatası."}), 400
    
    except FileNotFoundError as e:
        return jsonify({"error": f"Dosya hatası: {str(e)}"}), 404
        
    except KeyError as e:
        return jsonify({"error": f"Veri bulunamadı: {str(e)}"}), 404
        
    except Exception as e:
        print(f"Sunucu İç Hatası: {e}") 
        return jsonify({"error": "Etiket oluşturma sırasında beklenmeyen bir sunucu hatası oluştu."}), 500
    
    finally:
        if temp_image_path and os.path.exists(temp_image_path):
            os.remove(temp_image_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
