# 技術仕様

## 📊 システム技術仕様概要

IoT導入支援キット Ver.4.1の詳細技術仕様を説明します。

### プラットフォーム仕様

| カテゴリ | 項目 | 仕様 | 備考 |
|----------|------|------|------|
| **ハードウェア** | 基盤 | Raspberry Pi 4B (ARM64) | 4GB RAM推奨 |
| | CPU | ARM Cortex-A72 Quad-core 1.5GHz | 64bit処理 |
| | ストレージ | 32GB Class 10 microSD | 64GB推奨 |
| | 電源 | USB-C 5V/3A | 15W消費電力 |
| **OS・ランタイム** | OS | Raspbian OS Bullseye | Debian 11ベース |
| | Node.js | v20.19.1 | LTS版 |
| | Python | v3.11.2 | センサードライバー用 |
| | npm | v10.8.2 | パッケージ管理 |
| **コア処理** | Node-RED | v3.0+ | ワークフローエンジン |
| |総ノード数 | 1017個 | 9タブ構成 |
| | 処理性能 | <100ms応答 | リアルタイム処理 |

### ネットワーク・通信仕様

#### 基本ネットワーク
```yaml
Ethernet:
  インターフェース: Gigabit Ethernet (eth0)
  IPアドレス: DHCP自動取得 (固定IP設定可能)
  
Wi-Fi:
  規格: 802.11ac (2.4GHz/5GHz dual-band)
  セキュリティ: WPA2/WPA3
  
Bluetooth:
  バージョン: Bluetooth 5.0 + BLE
  用途: BLEセンサー通信
```

#### サービスポート
```yaml
Node-RED:
  Web UI: 1880 (HTTP)
  Dashboard: 1880/ui (HTTP)
  API: 1880/api/v2 (REST)
  
データベース:
  MariaDB: 3306 (TCP)
  InfluxDB: 8086 (HTTP)
  
メッセージング:
  MQTT Primary: 1883 (TCP)
  MQTT Secondary: 51883 (TCP)
  
管理:
  SSH: 22 (TCP)
```

## 🔌 ハードウェアインターフェース仕様

### GPIO仕様
```yaml
GPIOピン配置 (40pin):
  電源:
    - 3.3V: Pin 1, 17
    - 5V: Pin 2, 4
    - GND: Pin 6, 9, 14, 20, 25, 30, 34, 39
    
  I2C (主要センサーバス):
    - SDA: Pin 3 (GPIO 2)
    - SCL: Pin 5 (GPIO 3)
    - 電圧レベル: 3.3V
    - クロック: 400kHz (Fast-mode)
    - プルアップ: 1.8kΩ内蔵
    
  UART (BravePI通信):
    - TX: Pin 8 (GPIO 14)
    - RX: Pin 10 (GPIO 15)
    - ボーレート: 38400bps
    - フレーム: 8N1
    
  汎用GPIO (デジタルI/O):
    - 入力: Pin 11, 13, 15, 16, 18, 19, 21, 23
    - 出力: Pin 12, 22, 24, 26, 29, 31, 32, 33
    - 電圧レベル: 3.3V
    - 最大電流: 16mA per pin
```

### USB仕様
```yaml
USB3.0 ポート:
  数量: 2ポート
  用途: BraveJIG接続、外部ストレージ
  
USB2.0 ポート:
  数量: 2ポート  
  用途: キーボード・マウス、USBセンサー
  
USB-C電源:
  入力: 5V/3A (15W)
  保護: 過電流・過電圧保護
```

## 📊 センサーシステム仕様

### I2Cセンサー仕様
```yaml
サポートセンサー:
  温湿度センサー (BME280):
    - 温度範囲: -40°C〜+85°C (±1.0°C精度)
    - 湿度範囲: 0〜100%RH (±3%RH精度)
    - 気圧範囲: 300〜1100hPa (±1hPa精度)
    - I2Cアドレス: 0x76, 0x77
    
  距離センサー (VL53L1X):
    - 測定範囲: 4cm〜400cm
    - 精度: ±3mm (short range), ±3% (long range)
    - 測定周期: 最大50Hz
    - I2Cアドレス: 0x29
    
  照度センサー (OPT3001):
    - 測定範囲: 0.01〜83,865 lux
    - 分解能: 16bit
    - ノイズ除去: 50Hz/60Hz rejection
    - I2Cアドレス: 0x44, 0x45
    
  加速度センサー (MPU6050):
    - 測定範囲: ±2g, ±4g, ±8g, ±16g
    - 分解能: 16bit
    - サンプリング: 最大1kHz
    - I2Cアドレス: 0x68, 0x69
```

### シリアル通信仕様
```yaml
BravePI (UART):
  ポート: /dev/ttyAMA0
  ボーレート: 38400 bps
  フレーム: 8bit, No parity, 1 stop bit
  フロー制御: なし
  プロトコル: バイナリフレーム
  
BraveJIG (USB):
  ポート: /dev/ttyACM[0-9]
  ボーレート: 38400 bps
  フレーム: 8bit, No parity, 1 stop bit
  フロー制御: RTS/CTS
  プロトコル: 拡張バイナリフレーム
```

## 💾 データベース仕様

### MariaDB（設定・メタデータ）
```yaml
基本設定:
  バージョン: 10.9+
  エンジン: InnoDB
  文字コード: utf8mb4_unicode_ci
  接続情報:
    ホスト: 127.0.0.1
    ポート: 3306
    データベース: iotkit
    ユーザー: iotkit
    パスワード: iotkit-password

主要テーブル:
  devices: デバイス基本情報 (AUTO_INCREMENT PRIMARY KEY)
  sensors: センサー設定・校正値 (FOREIGN KEY制約)
  sensor_types: センサータイプ定義 (257-264, 289-293)
  sensor_channels: チャンネル・単位定義
  *_device_configs: 通信別設定 (BLE, USB, I2C, GPIO, HTTP)
  
パフォーマンス:
  最大同時接続: 50
  トランザクション: ACID準拠
  バックアップ: 毎日自動バックアップ
```

### InfluxDB（時系列データ）
```yaml
基本設定:
  バージョン: 2.6+
  接続情報:
    ホスト: 127.0.0.1
    ポート: 8086
    組織: fitc
    バケット: iotkit
    トークン: influxdb-iotkit-secret-token
    
データ構造:
  measurement: センサータイプ名 (temperature, humidity, distance...)
  tags: device_id, sensor_id, channel (インデックス化)
  fields: value, raw_value, quality, status
  timestamp: RFC3339形式 (ナノ秒精度)
  
性能・保持:
  書き込み性能: >10,000 points/sec
  クエリ性能: <50ms (一般的な時系列クエリ)
  圧縮率: 平均90% (SNAPPY算法)
  保持期間: 90日間 (設定変更可能)
  自動削除: 期間経過後の自動削除
```

## 🌐 API・通信プロトコル仕様

### REST API仕様
```yaml
Base URL: http://localhost:1880/api/v2
Content-Type: application/json
認証: なし (ローカル環境専用)

主要エンドポイント:
  デバイス管理:
    GET /device                    # 全デバイス取得
    GET /device/{deviceId}         # 特定デバイス取得
    POST /device                   # 新規デバイス登録
    PUT /device/{deviceId}         # デバイス更新
    DELETE /device/{deviceId}      # デバイス削除
    
  センサーデータ:
    GET /device/{deviceId}/sensor/value    # センサー値取得
    POST /device/{deviceId}/sensor/value   # データ送信
    GET /device/{deviceId}/sensor/history  # 履歴データ取得
    
  システム管理:
    GET /system/status             # システム状態取得
    GET /sensor/type               # センサータイプ一覧
    POST /system/restart           # システム再起動
```

### MQTT通信仕様
```yaml
ブローカー設定:
  Primary: localhost:1883
  Secondary: localhost:51883 (冗長化)
  実装: Aedes (Node.js MQTT Broker)
  認証: iotkit / iotkit-password
  
QoS Level:
  通常データ: QoS 0 (At most once)
  重要アラート: QoS 1 (At least once)
  設定変更: QoS 2 (Exactly once)
  
トピック体系:
  制御要求: DwlReq/{deviceId}     # ダウンリンク要求
  制御応答: DwlResp/{deviceId}    # ダウンリンク応答
  JIG要求: JIReq/{deviceId}       # JIG制御要求
  JIG応答: JIResp/{deviceId}      # JIG制御応答
  アップリンク: UlReq/{deviceId}  # アップリンクデータ
  エラー応答: ErrResp/{deviceId}  # エラー通知
  ファームウェア: DfuResp/{deviceId} # OTAアップデート
```

## ⚡ 性能・スケーラビリティ仕様

### リアルタイム性能
```yaml
データ収集:
  最大センサー数: 100個
  最大データレート: 10Hz per sensor
  最大総スループット: 1,000 points/sec
  レイテンシ: <100ms (センサー読み取り〜ダッシュボード表示)
  
処理性能:
  CPU使用率: 平均20-30% (Raspberry Pi 4)
  メモリ使用量: 1.5-2GB / 4GB
  ディスクI/O: <10MB/s (通常運用)
  ネットワーク: <1Mbps (通常運用)
```

### 信頼性・可用性
```yaml
システム稼働:
  稼働率目標: 99.5% (年間ダウンタイム43.8時間以内)
  MTBF: >2,000時間 (平均故障間隔)
  MTTR: <1時間 (平均復旧時間)
  
耐障害性:
  自動復旧: センサー通信エラー時の自動再接続
  冗長化: MQTT Broker二重化
  バックアップ: 設定の自動バックアップ
  監視: システム状態の自動監視・アラート
  
データ保護:
  整合性: MariaDB ACID保証
  バックアップ: 日次自動バックアップ
  復旧: Point-in-Time Recovery対応
```

## 🔧 運用・保守仕様

### システム要件
```yaml
最小要件:
  CPU: ARM Cortex-A53 Quad-core (Raspberry Pi 3B+)
  RAM: 2GB
  Storage: 16GB Class 10 microSD
  
推奨要件:
  CPU: ARM Cortex-A72 Quad-core (Raspberry Pi 4B)
  RAM: 4GB
  Storage: 32GB Class 10 microSD (64GB推奨)
  
環境要件:
  動作温度: 0°C〜40°C
  湿度: 20〜80%RH (結露なきこと)
  電源: 安定化5V/3A電源推奨
```

### 保守・診断機能
```yaml
ログ管理:
  システムログ: journalctl -u node-red
  アプリケーションログ: Node-RED内蔵ログ
  センサーログ: InfluxDB内のセンサーデータ
  
診断機能:
  ヘルスチェック: /api/v2/system/health
  リソース監視: CPU・メモリ・ディスク使用量
  通信診断: I2C・Serial・MQTT接続状態
  
アップデート:
  システム: apt update/upgrade
  Node-RED: npm update
  ファームウェア: OTA (Over-The-Air)
```

## 📈 拡張性・カスタマイズ

### センサー拡張
```yaml
対応インターフェース:
  I2C: 最大112デバイス (7bit addressing)
  GPIO: 最大26pin利用可能
  USB: 最大4ポート
  Serial: 最大2ポート (UART + USB)
  
新センサー追加手順:
  1. ハードウェア接続・設定
  2. sensor_types テーブルへの追加
  3. Node-REDフローの作成・設定
  4. ダッシュボードUI追加
  5. テスト・動作確認
```

### 外部システム連携
```yaml
標準インターフェース:
  REST API: HTTP/JSON (OpenAPI 3.0準拠)
  MQTT: IoT標準メッセージング
  WebSocket: リアルタイム双方向通信
  Database: SQL直接アクセス (MariaDB/InfluxDB)
  
カスタム連携:
  Node-RED: Custom Node開発
  Python: 外部スクリプト実行
  HTTP: Webhook・API Call
  File: CSV・JSON Export/Import
```

---

**更新日**: 2025年6月19日  
**対象読者**: 開発者・技術者・システム統合者  
**関連資料**: [センサー仕様](sensor-types.md) | [通信プロトコル](communication-protocols.md)