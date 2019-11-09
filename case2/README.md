Case 2 Pythonバージョン
=====

# 概要

docker-composeで複数のサーバ環境を立ち上げて、pytestの並列実行プラグインを利用してE2Eテストを並列に行うサンプル。

# 環境準備

`drivers`ディレクトリ配下にchrome用のWebDriverファイルを設置する。

pipで必要なライブラリをインストール
```
$ sudo apt-get install -y python3-venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
``` 

`e2e.config.yml.example`ファイルを複製して`e2e.config.yml`ファイルを作成する。

```
$ cp e2e.config.yml.example e2e.config.yml
```

`e2e.config.yml`ファイルを編集し、立ち上げるサーバ環境分workersのポートを追加する。

```yaml
workers:
  - web_port: 8080
  - web_port: 8081
```

# テスト実行方法

venvを有効にした状態で`startup-servers`コマンドを実行する。

```
$ source venv/bin/activate
$ ./startup-servers
```

dockerサーバが`e2e.config.yml`に設定したworkersの個数分起動するので、`pytest`コマンドに`-n`パラメータで並列実行数（workersの数に合わせる)でテストを実行する。

```
$ pytest -n 2 test
```

docker環境を停止する場合は`halt-servers`コマンドを実行する。
```
$ ./halt-servers
```