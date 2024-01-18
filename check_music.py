import fnmatch
import os
import json
import difflib
import re

"""
TODO:
    1. 解决重复歌曲的bug（已解决）
    2. 加入模糊查找，比如只查找前5个字符/前2个单词, 确认查找，缩小匹配范围
    3. git的commit和日志
"""

def get_all_directories_in_target_folder(target_folder):
    dir_list = {}
    for root, dirs, files in os.walk(target_folder):
        for dir in dirs:
            join_path = os.path.join(root, dir)
            dir_list[dir.lower()] = join_path
    return dir_list
    


def find_song(root, potential_path, song_names, singer):
    
    def is_substring_present_regex(full_string, substring):
        pattern = re.compile(re.escape(substring), re.IGNORECASE)
        return bool(pattern.search(full_string))

    def search_files(pattern, root):
        # 指定返回的匹配的文件条目的最大数量
        MAX_NUM = 3
        # 存储符合查找结果的文件列表
        matches = []
        # 查找文件
        for path, dirs, files in os.walk(root):
            for filename in fnmatch.filter(files, '*' + pattern + '*'):
                matches.append(os.path.join(path, filename))
        # 如果文件列表太长，排除掉matches里面可能无关的结果
        if len(matches) > MAX_NUM:
            print(f'Trimming possible redundant results of: {pattern}-{singer}...', end=' ')
            print(f'The max allowed number of results is {MAX_NUM}')
            reduced_matches = []
            # 通过歌手查找排除无关结果
            for match_file in matches:
                if is_substring_present_regex(match_file, singer):
                    reduced_matches.append(match_file)
            matches = reduced_matches

        return matches
    
    # 对于某个歌手下所有歌曲所有查找结果
    search_result = []
    # 当前寻找的文件的可能结果
    possible_files = {}
    # 没找到的歌曲列表
    not_found_list = []
    # 如果匹配到可能的歌手文件夹
    if potential_path != ' ':
        # 对该歌手的所有歌曲
        for song_name in song_names:
            # 处理并写入搜索结果
            possible_files[song_name] = search_files(song_name, potential_path)
            # 将找不到的歌放到not_found_list里
            if len(possible_files[song_name]) == 0:
                not_found_list.append(song_name)
    
    # 如果没有在歌手文件夹中找到或无匹配的歌手文件夹（这里的if是故意的，不是语法错误！）
    if potential_path == ' ' or len(not_found_list) != 0:
        for song_name in song_names:
            possible_files[song_name] = search_files(song_name, root)
    
    # 将结果放到search_result里    
    search_result.append(possible_files)

    return search_result



if __name__ == "__main__":

    # 读取json文件
    with open('./sort_music/json/Netease_Music.json', 'r', encoding='utf-8') as json_file:
        song_info = json.load(json_file)

    # 指定电脑上的音乐文件夹路径
    target_folder = "D:\\Music"   
    # 得到所有目标文件夹下的所有子文件夹名称的列表
    target_dir_dict = get_all_directories_in_target_folder(target_folder)
    lower_target_dir_list = list(target_dir_dict.keys())

    # 找到歌曲的结果
    result = {}
    for singer, song in song_info.items():

        print(f"Checking songs for {singer}...")
        singer = singer.lower()

        # 尝试进行模糊匹配
        potential_folders = difflib.get_close_matches(singer, lower_target_dir_list, n=3, cutoff=0.3)
        # 如果能匹配到可能的歌手文件夹
        if len(potential_folders) != 0:
            # 在对应的文件夹下寻找是否存在歌曲
            result[singer] = find_song(target_folder, target_dir_dict[potential_folders[0]], song, singer)
        else:
            result[singer] = find_song(target_folder, ' ', song, singer)                     

    # 将 JSON 字符串写入文件
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=2, ensure_ascii=False)

    print("JSON 文件已生成")



    