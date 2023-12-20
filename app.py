# 引入 OS 模組
import os
# 從 Flask 中引入會使用到的物件
from flask import Flask, flash, request, redirect, render_template, jsonify 
# 從 Werkzeug 中引入會使用到的物件
from werkzeug.utils import secure_filename

from shp import Shp_To_GeoJson;

from shp import Get_GeoJson;

# 初始化 Flask 模組
app = Flask( __name__, static_folder="static",static_url_path='/static')
# 設定在 Flask 中使用 Session 狀態管理的密碼金鑰
app.secret_key = "secret key"
# 設定檔案的大小，這裡為 16 MB 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 取得當前的路徑
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'ReceiveUpload')

# 若接收上傳檔案的資料夾不存在就創建一個接收資料夾
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
# 將接受的資料夾賦予 Flask 中接受上傳檔案的屬性
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 設定可以接受上傳的檔案類型
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','shp','kml'])

# 設定允許上傳檔案的格式，包含需要有 . 作為分割符號，且 . 後最多只能空白一格
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 在首頁的路由中使用樣板引擎 upload.html
@app.route('/')
def upload_form():
    return render_template('UpLoad.html')

@app.route('/shp', methods=['POST'])
def shp_to_geojson():
    Shp_To_GeoJson()
    flash('.shp 檔案已經成功轉為 GEJSON 檔了 !，請查看')
    return redirect('/')

@app.route('/getShp')
def get_geojson():
     geojson_contents =Get_GeoJson
     return jsonify(geojson_contents)


@app.route('/', methods=['POST'])
def upload_file():
    # 確保前端的請求方法是 POST 方法
    if request.method == 'POST':
    # 檢查請求中是否包含名為 'files[]' 的檔案，如果沒有則顯示錯誤消息並重新導向回原來的頁面。
    # 這裡的 files[] 對應的是前端 Input 標籤中 name 屬性的屬性值
        if 'files[]' not in request.files:
    # 使用 flash 函式報錯，類似 JS 中的 console.error('...')
            flash('No file part')
            return redirect(request.url)
    #  從請求中取得所有 'files[]' 的檔案列表。
        files = request.files.getlist('files[]')
    # 使用 Iterate 方法遍歷所有上傳的檔案
        for file in files:
    # 確保檔案有上傳且上傳的檔案格式(檔名)符合要求
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
    # 若上述條件都成立就將此檔案放入所創建接收的資料夾內
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/')





# 在本地端 POST=5000運行
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)