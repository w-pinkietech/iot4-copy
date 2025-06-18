# インストール・セットアップガイド

## 概要

IoT導入支援キット Ver.4.1の初期インストールから運用開始までの手順を説明します。

## 前提条件

### ハードウェア要件
- **Raspberry Pi 4 Model B** (推奨: 4GB RAM以上)
- **microSD カード**: 32GB以上 (Class 10推奨)
- **センサー類**: I2C/GPIO/シリアル対応センサー
- **ネットワーク**: Ethernet または WiFi接続

### ソフトウェア要件
- **Raspbian OS**: Bullseye以降
- **Docker**: 20.10以降
- **Docker Compose**: 1.29以降
- **Node.js**: 16.x以降

## インストール手順

### 1. システム準備

#### 1.1 Raspbian OSセットアップ
```bash
# システム更新
sudo apt update && sudo apt upgrade -y

# 必要パッケージインストール
sudo apt install -y git curl docker.io docker-compose

# Dockerサービス有効化
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

#### 1.2 I2C/SPI有効化
```bash
# raspi-config実行
sudo raspi-config

# Interface Options > I2C > Enable
# Interface Options > SPI > Enable
# 再起動
sudo reboot
```

### 2. プロジェクトクローン

```bash
# プロジェクトクローン
git clone https://github.com/your-org/iot4-copy.git
cd iot4-copy

# 実行権限付与
chmod +x desktop/first.sh
```

### 3. 初期設定実行

```bash
# first.shスクリプト実行
./desktop/first.sh
```

#### first.shの処理内容
1. ファイルシステム拡張
2. 必要パッケージインストール
3. Docker環境セットアップ
4. データベース初期化
5. Node-RED設定

### 4. サービス起動

```bash
# Docker Composeでサービス起動
cd docker
docker-compose up -d

# サービス状態確認
docker-compose ps
```

### 5. Node-RED起動

```bash
# Node-REDサービス開始
sudo systemctl start node-red

# 自動起動設定
sudo systemctl enable node-red

# 状態確認
sudo systemctl status node-red
```

## 動作確認

### 1. Webアクセス確認

| サービス | URL | 説明 |
|---------|-----|------|
| Node-REDエディタ | http://localhost:1880 | フロー編集画面 |
| ダッシュボード | http://localhost:1880/ui | 監視ダッシュボード |
| SQLite | localhost:3306 | データベース |
| InfluxDB | http://localhost:8086 | 時系列データベース |

### 2. センサー接続確認

```bash
# I2Cデバイス検出
sudo i2cdetect -y 1

# GPIO状態確認
gpio readall

# シリアルポート確認
ls -la /dev/ttyACM* /dev/ttyAMA*
```

### 3. データフロー確認

```bash
# MQTTメッセージ確認
mosquitto_sub -h localhost -t "#" -v

# データベース接続確認
mysql -h localhost -u iotkit -p iotkit
influx -host localhost -port 8086
```

## トラブルシューティング

### よくある問題と解決策

#### Node-REDが起動しない
```bash
# ログ確認
sudo journalctl -u node-red -f

# 設定ファイル確認
cat ~/.node-red/settings.js

# ポート使用状況確認
sudo netstat -tulpn | grep :1880
```

#### センサーが認識されない
```bash
# I2C通信確認
sudo i2cdetect -y 1

# GPIO権限確認
sudo usermod -aG gpio $USER

# デバイスファイル確認
ls -la /dev/i2c-* /dev/spidev*
```

#### データベース接続エラー
```bash
# Dockerコンテナ状態確認
docker-compose ps

# データベースログ確認
docker-compose logs sqlite
docker-compose logs influxdb

# ネットワーク確認
docker network ls
```

### ログファイル場所

| コンポーネント | ログパス |
|---------------|----------|
| Node-RED | ~/.node-red/logs/ |
| SQLite | docker logs iotkit_sqlite |
| InfluxDB | docker logs iotkit_influxdb |
| システム | /var/log/syslog |

## 設定カスタマイズ

### Node-RED設定

```javascript
// ~/.node-red/settings.js
module.exports = {
    uiPort: process.env.PORT || 1880,
    httpAdminRoot: '/admin',
    httpNodeRoot: '/api',
    userDir: '/home/pi/.node-red/',
    flowFile: 'flows.json',
    credentialSecret: 'your-secret-key'
}
```

### データベース設定

```yaml
# docker/docker-compose.yml
version: '3.8'
services:
  sqlite:
    environment:
      MYSQL_ROOT_PASSWORD: your-password
      MYSQL_DATABASE: iotkit
      MYSQL_USER: iotkit
      MYSQL_PASSWORD: your-iotkit-password
```

## セキュリティ設定

### ファイアウォール設定
```bash
# UFW有効化
sudo ufw enable

# 必要ポート開放
sudo ufw allow 1880/tcp  # Node-RED
sudo ufw allow 22/tcp    # SSH
sudo ufw allow from 192.168.1.0/24 to any port 3306  # MySQL (ローカルのみ)
```

### SSL証明書設定
```bash
# Let's Encrypt証明書取得
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Node-RED HTTPS設定
# settings.js にHTTPS設定追加
```

## バックアップ設定

### 自動バックアップスクリプト
```bash
#!/bin/bash
# /home/pi/backup.sh

# Node-RED設定バックアップ
tar -czf /backup/node-red-$(date +%Y%m%d).tar.gz ~/.node-red/

# データベースバックアップ
docker exec iotkit_sqlite sqlite3 /data/iotkit.db ".backup /backup/sqlite-$(date +%Y%m%d).db"

# InfluxDBバックアップ
influx backup --org fitc --bucket iotkit /backup/influx-$(date +%Y%m%d)/

# 古いバックアップ削除（30日以上）
find /backup -name "*.tar.gz" -mtime +30 -delete
find /backup -name "*.sql" -mtime +30 -delete
find /backup -name "influx-*" -type d -mtime +30 -exec rm -rf {} \;
```

### Cronジョブ設定
```bash
# crontabエディタ開く
crontab -e

# 毎日午前2時にバックアップ実行
0 2 * * * /home/pi/backup.sh
```

## 関連資料
- [システムアーキテクチャ](../architecture/overview.md)
- [日常運用ガイド](./operation.md)
- [トラブルシューティング](./troubleshooting.md)