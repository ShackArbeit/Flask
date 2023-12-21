# 引入 OS 模組
import os
# 從 Flask 中引入會使用到的物件
from flask import Flask, flash, request, redirect, render_template, jsonify,send_file
# 從 Werkzeug 中引入會使用到的物件
from werkzeug.utils import secure_filename
# 從 shp.py 檔案中引入  Shp_To_GeoJson 函式，用於轉檔用的
from shp import Shp_To_GeoJson;
# 從 shp.py 檔案中引入  Read_GeoJson 函式，用於返回轉檔後的檔案的
from shp import Read_GeoJson;
import zipfile
from io import BytesIO




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
@app.route('/',  methods=['POST'])
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
        flash('已經成功上傳檔案了 !', 'upload')
        return redirect('/')

# 這裡為將 Shp 檔案轉檔的路由設定
@app.route('/shp', methods=['POST'])
def shp_to_geojson():
    Shp_To_GeoJson()
    flash('.shp 檔案已經成功轉為 GEJSON 檔了 !，請查看')
    return redirect('/')
# 這裡為將轉成 geojson 的檔案返回給前端的路由設定
@app.route('/getShp')
def get_geojson():
     geojson_contents =Read_GeoJson()
     return jsonify(geojson_contents)
# 這裡為讓使用者可以從前端將 geojson 檔案下載下來的路由設定
@app.route('/download')
def DownLoad():

    # 取得當前檔案下的路徑
    current_path = os.getcwd()
    # 所有 GeoJSON 檔案所在的資料夾路徑
    geojson_folder_path = current_path
    # 建立一個空的 Array 存放所有的 Geojson 檔案
    download_files_array = []
    # 建立存放 Zip 資料夾的緩衝區
    zip_buffer = BytesIO()

    # 使用 zipfile.ZipFile 物件壓縮所有的 Geojson 檔案到 Zip 資料夾
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
    # 將所有的 .geojson 檔案透過 Iterate 方法遍歷一次
        for filename in os.listdir(geojson_folder_path):
            if filename.endswith('.geojson'):
        # 在遍歷的時候要定義每一個 geojson 檔案的當前路徑
                file_path = os.path.join(geojson_folder_path, filename)
        # 將每一個 Geojson 的路徑放進之前定義的 Array 內
                download_files_array.append(file_path)
                print("已下載的 GeoJSON 檔案如下 : ")
                print(file_path)
                print(filename)
        # 將各別的路徑寫入 Zip 資料夾內
        for file in download_files_array:
            zip_file.write(file, os.path.basename(file))
    # 確保所有的檔案都在 Zip 資料夾內
    zip_buffer.seek(0)
    # 返回 Zip 資料夾到前端
    return send_file(zip_buffer, download_name='files.zip', as_attachment=True)


# 以下為 KML 的首頁路由使用樣板引擎 KML.html
@app.route('/')
@app.route('/kml')
def upload_form_KML():
     return render_template('KLM.html')
# 以下為 KML 首頁上傳檔案的路由設定
@app.route('/kml',methods=['POST','GET'])
def upload_KLM():
    # 確保前端的請求方法是 POST 方法
    if request.method == 'POST':
    # 檢查請求中是否包含名為 'files[]' 的檔案，如果沒有則顯示錯誤消息並重新導向回原來的頁面。
    # 這裡的 files[] 對應的是前端 Input 標籤中 name 屬性的屬性值
        if 'KMLfiles[]' not in request.files:
    # 使用 flash 函式報錯，類似 JS 中的 console.error('...')
            flash('沒有選取任何檔案 !')
            return redirect(request.url)
    #  從請求中取得所有 'files[]' 的檔案列表。
        files = request.files.getlist('KMLfiles[]')
    # 使用 Iterate 方法遍歷所有上傳的檔案
        for file in files:
    # 確保檔案有上傳且上傳的檔案格式(檔名)符合要求
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
    # 若上述條件都成立就將此檔案放入所創建接收的資料夾內
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('已經成功上傳檔案了 !', 'conversion')
        return redirect('/kml')

@app.route('/kml/covert')
def CoverKML():
    



# 在本地端 POST=5000運行
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)