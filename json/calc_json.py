import json

# 读取JSON文件
with open('./sort_music/json/Absolute_Music.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 统计值的个数
total_count = 0

# 遍历JSON中的每一个键值对
for key, values in data.items():
    # 遍历每个值并进行计数
    for value in values:
        total_count += 1

# 打印结果
print(total_count)