# 環境

+ Python 3.12.7
+ Django 4.2.16
+ Bootstrap 5.0.2
+ 開発環境：Dokcer
+ 本番環境：Heroku
+ 画像保存：Cloudinary

# 環境構築
## dockerを立ち上げる
```
$ docker compose up -d
```

## bashの起動
```
$ docker compose exec web bash
```

## DBマイグレートの実行
```
# python manage.py makemigrations
# python manage.py migrate
```

## Webサーバの起動
```
# python manage.py runserver 0.0.0.0:8000
```