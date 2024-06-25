# Zcmu_Score

浙江中医药大学成绩自动查询并邮箱提醒

## 使用

1.Git clone

```shell
git clone https://github.com/cr4n5/Zcmu_Score.git
```

2.安装依赖

```shell
pip install requests
pip install yagmail
```

3.修改配置文件

在`config.json`中填写学号、密码、邮箱smtp服务器、邮箱账号、邮箱授权码、接收邮箱

```json
{
    "login": {
        "username": "2019xxxxxx",
        "password": "xxxxxxxx"
    },
    "smtp_email": {
        "user": "..@qq.com",
        "password": "xxxxxxx",
        "host": "smtp.qq.com",
        "email_to": [
            "..@qq.com",
            "..@163.com"
        ]
    }
}
```

4.运行

```shell
pwd #/path/to/Zcmu_Score
python Zcmu_Score.py
```
