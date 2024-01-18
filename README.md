# 音乐整理

自己用python瞎写的音乐整理程序，顺便学习了一下怎么写python代码。

`sort_music.py` 读取文件夹内的音乐文件，如果文件名格式为：`song - singer` 或 `singer - song` （请根据实际情况调整第28行的变量顺序），则读入歌手和歌曲名字，输出到一个json文档中。

json文档的格式：

```json
{
    "Artist1": [
        "Song1",
        "Song2"
    ],
    "Artist2": [
        "Song3",
        "Song4"
    ],
    ...
}
```



`check_music.py` 则读入json文档，然后在指定的文件路径下进行匹配查找，输出查找结果到 `output.json` 中。

输出json的结果：

```json
{
    "Artist1": [
        {
            "Song1": [
                "Path1/of/Song1",
                "Path2/of/Song1"
            ],
            "Song2": [
                "Path1/of/Song2",
                "Path2/of/Song2"
            ]
        }
    ],
    "Artist2": [
        {
            "Song3": [
                "Path1/of/Song3",
                "Path2/of/Song3"
            ],
            "Song4": [
                "Path1/of/Song4",
                "Path2/of/Song4"
            ]
        }
    ],
    ...
}
```

