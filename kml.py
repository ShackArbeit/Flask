# 引入 Geopandas 模組
import geopandas as gpd
# 引入 OS 模組
import os
# 引入 JSON 模組
import json
import re
# 引入 fiona.drvsupport 模組來支援將 KML 檔案轉換的驅動物件
from fiona.drvsupport import supported_drivers
# 設定所支援的驅動物件
supported_drivers['LIBKML'] = 'rw'
supported_drivers['libkml'] = 'rw'
supported_drivers['KML'] = 'rw'
supported_drivers['kml'] = 'rw'


# 取得當前檔案下的路徑
current_path = os.getcwd()
# 這為接收從前端送過來的檔案的資料夾
subfolder_name= "ReceiveUpload"
# 這裡為將轉檔為 GEOJSON 檔案收集的資料夾
subfolder_name2='KML'
# 取得接收從前端上傳檔案的資料夾的路徑
subfolder_path = os.path.join(current_path, subfolder_name)
# 取得收集 GEOJSON 檔案資料夾的路徑
subfolder_path2=os.path.join(current_path,subfolder_name2)


# 以下為將 KML 檔案轉換為 GEOJSON 檔案的函式設定
def KML_To_GEO():
    # 定義空的陣列，用於儲存上傳副檔名有 .kml 的檔案
    kml_files_Array = []
    for filename in os.listdir(subfolder_path):
        if filename.endswith('.kml'):
            # 將副檔名為 .kml 的檔案放入所定義的空陣列內
            kml_files_Array.append(filename)
    print("從前端上傳副檔名為 .kml 的檔案如下 : ")
    print(subfolder_path2)
    # 使用 Iterate 方法遍歷所有含有 KML 附檔名的檔案
    for kml_File in kml_files_Array:
    # 因為 Geopandas 模組 是使用路徑找到所要轉檔的檔案，所以先將要檔案路徑定義出來
        kml_File_path = os.path.join(subfolder_path, kml_File)
        try:
    # 讀取含有副檔名為 KML 的檔案並使用 KML 驅動物件支援讀取
            gdf = gpd.read_file(kml_File_path, driver='KML')
    # 設定轉出檔案的存放路徑，這裡確保是從 ReceiveUpload 中轉出
            output_geojson = os.path.join(subfolder_path2, f"{os.path.splitext(kml_File)[0]}.geojson")
    # 將轉檔的檔案放入所指定的存放路徑內
            gdf.to_file(output_geojson)
            print(f"成功轉換 KML 到 GeoJSON: {kml_File}")
            print(f"GeoJSON Output Path: {output_geojson}")
    # 設定轉檔失敗的例外情形
        except Exception as e:
            print(f"轉換 KML 到 GeoJSON 時發生錯誤: {kml_File}")
            print(f"錯誤訊息: {e}")

#  以下為將已經轉為 .geojson 檔案顯示在前端頁面的設定
def Read_KML_JSON():
    # 所有 GeoJSON 檔案所在的資料夾路徑
    geojson_folder_path = subfolder_path2
    
    # 定義空的字典，用於儲存所有副檔名有 .geojson 的檔案的內容
    geojson_contents_dict = {}
    # 將所有的 .geojson 檔案透過 Iterate 方法遍歷一次
    for filename in os.listdir(geojson_folder_path):
        if filename.endswith('.geojson'):
            # 在遍歷的時候要定義每一個 geojson 檔案的當前路徑
            file_path = os.path.join(geojson_folder_path, filename)
            # 讀取該 geojson 檔案
            with open(file_path,"r",encoding="utf-8") as file:
                content = file.read()
                arr = re.findall(r"[0-9]+:[0-9]+\s", content)
                print(len(arr))
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