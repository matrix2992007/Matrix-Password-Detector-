from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pyzipper
import os

app = Flask(__name__)
CORS(app) # عشان يسمح للمتصفح يكلم السيرفر بدون مشاكل أمنية

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# دالة فك التشفير الحقيقية
def crack_logic(zip_path, passwords):
    for pwd in passwords:
        pwd = pwd.strip()
        try:
            with pyzipper.AESZipFile(zip_path) as zf:
                # بيحاول يفك ملف واحد كاختبار للباسورد
                zf.extractall(path=UPLOAD_FOLDER, pwd=str.encode(pwd))
                return pwd
        except:
            continue
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "لم يتم رفع ملف"}), 400
    
    file = request.files['file']
    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(zip_path)

    # قائمة باسوردات تجريبية (ممكن تكبرها زي ما أنت عايز)
    wordlist = ["123456", "password", "admin", "MaTrIx_2026!#", "123123"]
    
    result = crack_logic(zip_path, wordlist)
    
    if result:
        return jsonify({"success": True, "password": result})
    else:
        return jsonify({"success": False, "message": "الباسورد مش في القائمة الحالية"})

if __name__ == '__main__':
    # بيشتغل على بورت 5000
    app.run(debug=True, port=5000)
