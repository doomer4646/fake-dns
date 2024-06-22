# ベースイメージとしてPythonを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY . .

# 必要なPythonパッケージをインストール
RUN pip install dnslib

# コンテナ起動時に実行するコマンドを設定
CMD ["python", "dns_server.py"]
