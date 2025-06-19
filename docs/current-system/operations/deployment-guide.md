# インストール・環境構築ガイド

## 🚀 クイックインストール

### 前提条件
- Raspberry Pi 4 Model B (4GB RAM推奨)
- 32GB以上のmicroSDカード (Class 10以上)
- 安定化電源 (USB-C 5V/3A)
- インターネット接続環境

### 1ステップインストール
```bash
# リポジトリクローン
git clone https://github.com/your-org/iot4-copy.git
cd iot4-copy

# 自動セットアップ実行
./desktop/first.sh

# サービス起動
cd docker && docker-compose up -d
```

## 📋 詳細インストール手順

### Step 1: OS準備
1. **Raspberry Pi OS書き込み**
   ```bash
   # Raspberry Pi Imagerを使用してOSを書き込み
   # 推奨: Raspberry Pi OS Lite (64-bit)
   ```

2. **初期設定**
   ```bash
   # SSH有効化
   sudo systemctl enable ssh
   
   # Wi-Fi設定 (必要に応じて)
   sudo raspi-config
   ```

### Step 2: 依存関係インストール
```bash
# システム更新
sudo apt update && sudo apt upgrade -y

# 必要パッケージインストール
sudo apt install -y \
  git curl docker.io docker-compose \
  python3 python3-pip \
  i2c-tools mosquitto-clients

# Node.js インストール
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# I2C有効化
sudo raspi-config
# -> Interface Options -> I2C -> Enable
```

### Step 3: システムセットアップ
```bash
# プロジェクトクローン
git clone https://github.com/your-org/iot4-copy.git
cd iot4-copy

# 権限設定
chmod +x desktop/first.sh

# セットアップ実行
./desktop/first.sh
```

### Step 4: データベース起動
```bash
# Dockerサービス起動
cd docker
docker-compose up -d

# サービス確認
docker-compose ps
```

### Step 5: Node-RED設定
```bash
# Node-REDインストール
sudo npm install -g --unsafe-perm node-red

# 自動起動設定
sudo systemctl enable nodered.service
sudo systemctl start nodered.service
```

## ⚙️ 設定・カスタマイズ

### データベース接続設定
```yaml
# docker/docker-compose.yml
services:
  mariadb:
    environment:
      MYSQL_ROOT_PASSWORD: root-password
      MYSQL_DATABASE: iotkit
      MYSQL_USER: iotkit
      MYSQL_PASSWORD: iotkit-password
      
  influxdb:
    environment:
      INFLUXDB_DB: iotkit
      INFLUXDB_ADMIN_USER: admin
      INFLUXDB_ADMIN_PASSWORD: admin-password
```

### Node-RED設定
```bash
# 設定ファイル場所
~/.node-red/settings.js

# 主要設定項目
{
    "uiPort": 1880,
    "httpAdminRoot": "/",
    "httpNodeRoot": "/api",
    "userDir": "/home/pi/.node-red/",
    "functionGlobalContext": {},
    "debugMaxLength": 1000
}
```

## 🔍 動作確認

### システム状態確認
```bash
# サービス状態確認
sudo systemctl status nodered
docker-compose ps

# ポート確認
netstat -tlnp | grep -E "(1880|3306|8086|1883)"

# ログ確認
sudo journalctl -u nodered -f
docker-compose logs mariadb
docker-compose logs influxdb
```

### 接続テスト
```bash
# Node-REDアクセステスト
curl http://localhost:1880

# データベース接続テスト
mysql -h 127.0.0.1 -u iotkit -p iotkit
influx -host 127.0.0.1 -port 8086

# MQTT接続テスト
mosquitto_pub -h localhost -t "test" -m "hello"
mosquitto_sub -h localhost -t "test"
```

### ハードウェア確認
```bash
# I2Cデバイス確認
sudo i2cdetect -y 1

# GPIO状態確認
gpio readall

# USB Serial確認
ls -l /dev/ttyACM*
ls -l /dev/ttyAMA*
```

## 🛠️ トラブルシューティング

### 一般的な問題と解決策

#### Node-REDが起動しない
```bash
# メモリ不足確認
free -h

# 権限問題確認
sudo chown -R pi:pi ~/.node-red/

# サービス再起動
sudo systemctl restart nodered
```

#### データベース接続エラー
```bash
# Dockerコンテナ状態確認
docker-compose ps

# ネットワーク確認
docker network ls
docker network inspect docker_default

# コンテナ再起動
docker-compose restart mariadb influxdb
```

#### センサー認識しない
```bash
# I2C接続確認
sudo i2cdetect -y 1

# 権限確認
sudo usermod -a -G i2c,gpio,dialout pi

# デバイス再起動
sudo reboot
```

## 📊 パフォーマンス最適化

### メモリ最適化
```bash
# スワップファイル設定
sudo dphys-swapfile swapoff
sudo vi /etc/dphys-swapfile
# CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### ストレージ最適化
```bash
# ログローテーション設定
sudo vi /etc/logrotate.d/node-red

# 不要ファイル削除
sudo apt autoremove
sudo apt autoclean
```

### ネットワーク最適化
```bash
# 固定IP設定
sudo vi /etc/dhcpcd.conf
# interface eth0
# static ip_address=192.168.1.100/24
# static routers=192.168.1.1
# static domain_name_servers=192.168.1.1
```

## 🔐 セキュリティ設定

### 基本セキュリティ
```bash
# パスワード変更
passwd

# SSH設定強化
sudo vi /etc/ssh/sshd_config
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes

# ファイアウォール設定
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 1880
```

### アプリケーションセキュリティ
```bash
# Node-RED認証設定
vi ~/.node-red/settings.js
# adminAuth: {
#     type: "credentials",
#     users: [{
#         username: "admin",
#         password: "$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6tl8sJogENOMcxWV9DN.",
#         permissions: "*"
#     }]
# }
```

## 🚀 プロダクション配備

### 高可用性設定
```bash
# サービス監視設定
sudo vi /etc/systemd/system/iot-monitor.service

# 自動復旧スクリプト
vi ~/scripts/health-check.sh
chmod +x ~/scripts/health-check.sh

# cron設定
crontab -e
# */5 * * * * /home/pi/scripts/health-check.sh
```

### バックアップ設定
```bash
# 設定バックアップスクリプト
vi ~/scripts/backup.sh
chmod +x ~/scripts/backup.sh

# 定期バックアップ
crontab -e
# 0 2 * * * /home/pi/scripts/backup.sh
```

---

**更新日**: 2025年6月19日  
**対象読者**: システム管理者・運用担当者  
**所要時間**: 約2-3時間（初回インストール）  
**関連資料**: [監視ガイド](monitoring-guide.md) | [保守ガイド](maintenance-guide.md)