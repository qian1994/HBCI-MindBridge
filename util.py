import os
def find_json_files(folder_path):
     # 获取指定文件夹下所有文件和文件夹
    files = os.listdir(folder_path)
    json_files = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        # 判断是否是文件夹
        if os.path.isdir(file_path):
            # 递归查找子文件夹中的 JSON 文件
            json_files += find_json_files(file_path)
        # 判断是否是 JSON 文件
        elif file.endswith('.json'):
            # 将 JSON 文件的完整地址添加到列表中
            json_files.append(file_path)
    return json_files
