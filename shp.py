# 引入 Geopandas 模組
import geopandas as gpd
# 引入 OS 模組
import os
# 引入 Json 物件
import json
from flask import send_file

os.environ['SHAPE_RESTORE_SHX'] = 'YES'
# 取得當前檔案下的路徑
current_path = os.getcwd()
subfolder_name = "ReceiveUpload"
# 取得接收從前端上傳檔案的資料夾的路徑
subfolder_path = os.path.join(current_path, subfolder_name)

def Shp_To_GeoJson():
    # 定義空的陣列，用於儲存上傳副檔名有 .shp 的檔案
    shp_files_Array = []
    for filename in os.listdir(subfolder_path):
        if filename.endswith('.shp'):
    # 將副檔名為 .shp 的檔案放入所定義的空陣列內
            shp_files_Array.append(filename)
    print("從前端上傳副檔名為 .shp 的檔案如下 : ")
    for shp_File in shp_files_Array:
    # 因為 Geopandas 模組 是使用路徑找到所要轉檔的檔案，所以先將要檔案路徑定義出來
        shp_File_path = os.path.join(subfolder_path, shp_File)
    # 使用  Geopandas 模組讀取所定義的路徑
        gdf = gpd.read_file(shp_File_path)
    # 將原有 .shp 的副檔名移除
        output_geojson = f'{shp_File[:-4]}.geojson'
    # 執行轉檔作業
        gdf.to_file(output_geojson, driver='GeoJSON')
        print(shp_File)


def Read_GeoJson():
    # 取得當前檔案下的路徑
    current_path = os.getcwd()
    # 所有 GeoJSON 檔案所在的資料夾路徑
    geojson_folder_path = current_path
    
    # 定義空的字典，用於儲存所有副檔名有 .geojson 的檔案的內容
    geojson_contents_dict = {}
    # 將所有的 .geojson 檔案透過 Iterate 方法遍歷一次
    for filename in os.listdir(geojson_folder_path):
        if filename.endswith('.geojson'):
            # 在遍歷的時候要定義每一個 geojson 檔案的當前路徑
            file_path = os.path.join(geojson_folder_path, filename)
            # 讀取該 geojson 檔案
            with open(file_path) as file:
                content = file.read()
            # 因為原本 geojson 的類型是 String ，要先解析成純 Json 的格式類型
                json_content = json.loads(content) 
            # 將轉換為 Json 的檔案放進所定義空的字典
                geojson_contents_dict[filename] = json_content
    print("已轉換的 GeoJSON 檔案如下 : ")
    # 這裡將檔案的名稱及內容印出來，非必要，因為最後會返回 geojson_contents_dict 給前端
    for filename, json_content in geojson_contents_dict.items():
        print(f"File: {filename}")
        print(json_content)
    return geojson_contents_dict



def Download_GeoJosn():
    # 取得當前檔案下的路徑
    current_path = os.getcwd()
    # 所有 GeoJSON 檔案所在的資料夾路徑
    geojson_folder_path = current_path

    # 定義空的字典，用於儲存所有副檔名有 .geojson 的檔案的內容
    geojson_contents_dict = {}

    # 將所有的 .geojson 檔案透過 Iterate 方法遍歷一次
    for filename in os.listdir(geojson_folder_path):
        if filename.endswith('.geojson'):
            # 在遍歷的時候要定義每一個 geojson 檔案的當前路徑
            file_path = os.path.join(geojson_folder_path, filename)
            print("已下載的 GeoJSON 檔案如下 : ")
            print(file_path)
            print(filename)
            return send_file(file_path, as_attachment=True)

    