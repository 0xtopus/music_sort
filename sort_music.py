import json
import os
import sys

""" 
    说明：
        第一个参数是路径
        第二个参数是输出json文件的名字
        示例：
            python ./sort_music.py D:/Music Music.json
"""


def get_all_files(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        """ for dir in dirs:
            print(dir) """
        # print(sorted(files))
        for file in files:
            file_list.append(file)
    return file_list
    
def extract_singer_and_songname(file_name):
    file_name, _ = os.path.splitext(file_name)     # 删除后缀
    try:
        #! 请根据实际情况选择song_name和singer的顺序！
        song_name, singer  = file_name.rsplit(' - ', 1)  # 分离歌手和歌曲名
    except ValueError:
        singer = "unknow"
        song_name = file_name
    # print(f'{singer} &&&& {song_name}')
    return [singer, song_name]; 

def write_to_json(file_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(file_data, json_file, indent=2, ensure_ascii=False)


# 参数示例：python sort_music.py "文件夹路径" "输出json文件的名称.json"
if __name__ == "__main__":
    # 检查参数数量是否符合要求
    if len(sys.argv) != 3:
        print("Please enter directory path!")
        sys.exit(1)

    folder_path = sys.argv[1]   # 使用参数作为文件夹路径
    print(f'Generating output file {sys.argv[2]}...')
    #output_json_file = 'SongList' # 输出json文件的名称
    file_data = {}

    files = sorted(get_all_files(folder_path))  # 得到含有目录下所有file文件名的list
    
    for file in files:
        singer, song_name = extract_singer_and_songname(file) # 分离歌手和歌曲名

        if singer in file_data:
            file_data[singer].append(song_name) # 如果歌手已经在字典中，将新的歌曲名添加到对应的列表中
        else:
            file_data[singer] = [song_name] # 如果歌手不在字典中，创建一个新的列表并将歌曲名添加进去
            
    # 写入json
    write_to_json(file_data, sys.argv[2])
    # TODO：写测试
