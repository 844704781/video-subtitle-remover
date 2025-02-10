##获取进度
```shell
curl http://127.0.0.1:5000/task_progress/1
```

##移除字幕
```shell
curl -X POST http://127.0.0.1:5000/remove_subtitle -H "Content-Type: application/json" -d "{\"task_id\": \"1\", \"video_path\": \"C:\\Users\\watermelon\\Downloads\\videos\\回归家好月圆20\\回归家好月圆1.mp4\", \"sub_area\": [0, 100, 0, 200]}"
```
