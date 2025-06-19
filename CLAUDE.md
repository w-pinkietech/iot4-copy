# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際のClaude Code (claude.ai/code) への指針を提供します。

## プロジェクト概要

IoT導入支援キット Ver.4.1 - 産業用IoTデータ収集・可視化システム
- 現在: Node-REDベースのシステム（Raspberry Pi 4上で動作）
- 移行中: Python/FastAPIベースの新システムへ

### 実行環境
- Node.js: v20.19.1
- Python: 3.11.2
- npm: 10.8.2

## 重要なコマンド

```bash
# システム起動
cd docker && docker-compose up -d

# システム停止
cd docker && docker-compose down

# I2Cデバイス確認
sudo i2cdetect -y 1

# MQTTメッセージ監視
mosquitto_sub -h localhost -t "#" -v

# Node-REDログ確認
sudo journalctl -u node-red -f
```

## アーキテクチャ要点

### データベース接続情報
- **MariaDB**: 127.0.0.1:3306, DB: iotkit, User: iotkit, Pass: iotkit-password
- **InfluxDB**: 127.0.0.1:8086, Org: fitc, Bucket: iotkit, Token: influxdb-iotkit-secret-token

### 主要ポート
- Node-RED: 1880
- MQTT: 1883, 51883
- MariaDB: 3306
- InfluxDB: 8086

### ディレクトリ構造
- `docs/current-system/`: 現行Node-REDシステムのドキュメント
- `docs/new-system/`: 新Python/FastAPIシステムのドキュメント
- `desktop/`: Raspberry Pi設定スクリプト
- `docker/`: データベースコンテナ設定

## 開発時の注意

1. Node-REDフローは日本語名を使用
2. コミットメッセージ規約: feat, fix, docs, style, refactor, test, chore
3. 現在Python/FastAPIへの移行計画が進行中
4. 詳細なドキュメントは `docs/README.md` を参照