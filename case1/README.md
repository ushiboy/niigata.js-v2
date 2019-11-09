Case 1 JavaScriptバージョン
=====

# 概要

JavaScript環境でのE2Eテスト実行サンプル。

# 環境準備

`test/driver`ディレクトリ配下にchrome用のWebDriverファイルを設置する。

npmで必要なライブラリをインストール
```
$ npm install
``` 

# テスト実行方法

`docker-compose`でサーバ環境を起動する。

```
$ docker-compose up -d
```

`npm test`でテストを実行する。

```
$ npm test
```

docker環境を停止する場合は次のコマンドを実行する。
```
$ docker-compose down
```

