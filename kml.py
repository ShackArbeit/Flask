# 引入 Geopandas 模組
import geopandas as gpd
# 引入 OS 模組
import os
from fiona.drvsupport import supported_drivers

supported_drivers['LIBKML'] = 'rw'
supported_drivers['libkml'] = 'rw'
supported_drivers['KML'] = 'rw'
supported_drivers['kml'] = 'rw'

# import kml2geojson
import shutil


# 取得當前檔案下的路徑
current_path = os.getcwd()
subfolder_name= "ReceiveUpload"
subfolder_name2='KML'
# 取得接收從前端上傳檔案的資料夾的路徑
subfolder_path = os.path.join(current_path, subfolder_name)
subfolder_path2=os.path.join(current_path,subfolder_name2)

# os.makedirs(subfolder_path2, exist_ok=True)

def KML_To_GEO():
    # 定義空的陣列，用於儲存上傳副檔名有 .kml 的檔案
    kml_files_Array = []
    for filename in os.listdir(subfolder_path):
        if filename.endswith('.kml'):
            # 將副檔名為 .kml 的檔案放入所定義的空陣列內
            kml_files_Array.append(filename)

    print("從前端上傳副檔名為 .kml 的檔案如下 : ")
    print(subfolder_path2)

    for kml_File in kml_files_Array:
        # 因為 Geopandas 模組 是使用路徑找到所要轉檔的檔案，所以先將要檔案路徑定義出來
        kml_File_path = os.path.join(subfolder_path, kml_File)
        try:
            gdf = gpd.read_file(kml_File_path, driver='KML')

            output_geojson = os.path.join(subfolder_path2, f"{os.path.splitext(kml_File)[0]}.geojson")

            gdf.to_file(output_geojson)
            print(f"成功轉換 KML 到 GeoJSON: {kml_File}")
            print(f"GeoJSON Output Path: {output_geojson}")

        except Exception as e:
            print(f"轉換 KML 到 GeoJSON 時發生錯誤: {kml_File}")
            print(f"錯誤訊息: {e}")

    print('以下為從 KML 轉成 GeoJSON 的檔案 : ')

