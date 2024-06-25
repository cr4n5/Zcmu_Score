# Zcmu_Score

浙江中医药大学成绩自动查询并邮箱提醒

## 使用

1.安装依赖

```shell
pip install requests
pip install yagmail
```

2.修改配置文件

在`config.json`中填写学号、密码、邮箱smtp服务器、邮箱账号、邮箱授权码、接收邮箱

```json
{
    "login": {
        "username": "2019xxxxxx",
        "password": "xxxxxxxx"
    },
    "smtp_email": {
        "user": "",
        "password": "",
        "host": "",
        "email_to": [
            ""
        ]
    }
}
```

3.运行

```shell
python Zcmu_Score.py
```
