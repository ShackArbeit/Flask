# 引入 Geopandas 模組
import geopandas as gpd
# 引入 OS 模組
import os
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



def Get_GeoJson(subfolder_path):
    shp_files_Array = []
    geojson_contents = []  # List to store GeoJSON content

    for filename in os.listdir(subfolder_path):
        if filename.endswith('.shp'):
            shp_files_Array.append(filename)

    print("從前端上傳副檔名為 .shp 的檔案如下 : ")

    for shp_File in shp_files_Array:
        shp_File_path = os.path.join(subfolder_path, shp_File)
        gdf = gpd.read_file(shp_File_path)
        output_geojson = f'{shp_File[:-4]}.geojson'
        gdf.to_file(output_geojson, driver='GeoJSON')

        # Read and append GeoJSON content to the list
        with open(output_geojson, 'r') as geojson_file:
            geojson_content = geojson_file.read()
            geojson_contents.append(geojson_content)

        print(shp_File)

    return geojson_contents