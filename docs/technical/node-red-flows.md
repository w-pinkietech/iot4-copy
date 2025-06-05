# Node-RED IoT導入支援キット Ver.4.1 - フロー詳細ドキュメント

## 概要

このドキュメントは、Node-RED IoT導入支援キット Ver.4.1 の flows.json ファイルに定義された全機能の詳細な技術仕様書です。本システムは産業用IoTセンサー監視プラットフォームとして設計されており、複数の通信プロトコル、豊富なセンサータイプ、リアルタイム可視化機能を提供します。

## システム構成

### 1. メインタブ構成

本システムは以下の9つの主要機能タブで構成されています：

#### 1.1 PI・JIG・I2C・GPIO タブ (baa69f6c03978bf4)

**目的**: ハードウェアインターフェース制御
**主要機能**:
- Raspberry Pi GPIOピン制御
- I2Cデバイス通信
- JIG（治具）制御インターフェース
- シリアル通信プロトコル処理

**ノード構成**:
- Function ノード: 53個（データ処理ロジック）
- Link ノード: 85個（フロー間連携）
- Change ノード: 42個（データ変換）
- Serial ノード: 22個（シリアル通信）
- GPIO ノード: 10個（デジタルI/O制御）

**通信プロトコル**:
```
メインUART: /dev/ttyAMA0 (38400 baud)
USB Serial: /dev/ttyACM0～9 (38400 baud)
I2C: 標準I2Cプロトコル
GPIO: デジタル入出力制御
```

#### 1.2 ダッシュボード タブ (5991e0363629fd30)

**目的**: リアルタイムデータ可視化
**主要機能**:
- センサーデータのリアルタイム表示
- グラフィカルユーザーインターフェース
- アラート・通知システム
- データエクスポート機能

**UI構成**:
- Template ノード: 42個（カスタムUI要素）
- Junction ノード: 20個（データ配信）
- Chart ノード: 15個（グラフ表示）
- Gauge ノード: 12個（メーター表示）

**ダッシュボード構成**:
| タブ順序 | タブ名 | 英語名 | アイコン | 機能 |
|---------|--------|---------|----------|------|
| 1 | ダッシュボード | Dashboard | fa-tachometer | メイン監視画面 |
| 2 | デバイス | Devices | devices | デバイス一覧・管理 |
| 3 | センサーログ | Sensor Log | fa-line-chart | データログ表示 |
| 4 | Bluetoothデバイス | Bluetooth Devices | fa-bluetooth | BLE機器管理 |
| 5 | ルーター | Router | router | ネットワーク設定 |
| 6 | モジュール | Module | fa-cubes | モジュール管理 |
| 7 | 設定 | Settings | settings | システム設定 |
| 8 | インフォ | Info | fa-info | システム情報 |
| 9 | その他 | Other | fa-question | その他機能 |

#### 1.3 デバイス登録 タブ (81159351db9223bf)

**目的**: IoTデバイスのライフサイクル管理
**主要機能**:
- 新規デバイス登録
- デバイス設定変更
- デバイス削除・無効化
- デバイス状態監視

**API エンドポイント**:
```http
GET    /api/v2/device              # 全デバイス取得
GET    /api/v2/device/:deviceId    # 特定デバイス取得
POST   /api/v2/device              # 新規デバイス登録
DELETE /api/v2/device/:deviceId    # デバイス削除
```

**データベース構造**:
- MySQL: デバイス設定・メタデータ保存
- テーブル: devices, device_config, device_status

#### 1.4 センサーログ タブ (ce55e77ffc367d5a)

**目的**: 時系列データ管理・分析
**主要機能**:
- センサーデータの時系列保存
- データ分析・集計
- ログデータエクスポート
- 履歴データ可視化

**データストレージ**:
```
InfluxDB v2.0:
- Host: 127.0.0.1:8086
- Database: iotkit
- Retention Policy: 90日間
```

**ノード構成**:
- Function ノード: 15個（データ処理）
- InfluxDB ノード: 7個（時系列DB操作）
- JSON ノード: 5個（データフォーマット変換）

#### 1.5 BLEトランスミッター タブ (8b336f5f9ef68ac3)

**目的**: Bluetooth Low Energy 通信管理
**主要機能**:
- BLEデバイス検索・ペアリング
- ワイヤレスセンサーデータ受信
- モバイルデバイス連携
- BLE通信プロトコル処理

**対応BLE機能**:
- GATT サービス管理
- Characteristic 読み書き
- Notification 受信
- デバイス状態監視

#### 1.6 ルーター タブ (fd4a567e7561fa40)

**目的**: ネットワーク通信・ルーティング
**主要機能**:
- HTTP リクエスト処理
- データルーティング
- 外部API連携
- ネットワーク設定管理

**HTTP エンドポイント**:
- デバイス管理API
- センサーデータAPI
- 設定管理API
- ステータス監視API

#### 1.7 モジュール タブ (ecf79cf3748850a8)

**目的**: 拡張モジュール管理
**主要機能**:
- 動的モジュール読み込み
- プラグイン管理
- カスタムセンサー追加
- 機能拡張インターフェース

#### 1.8 設定 タブ (51957a5eab717266)

**目的**: システム設定・構成管理
**主要機能**:
- MQTT ブローカー設定
- データベース接続設定
- センサー校正パラメータ
- メール通知設定

**設定項目**:
```yaml
MQTT:
  primary_broker: localhost:1883
  secondary_broker: localhost:51883
  
Database:
  mysql_host: 127.0.0.1:3306
  mysql_database: iotkit
  influxdb_host: 127.0.0.1:8086
  influxdb_database: iotkit
  
Email:
  smtp_server: 設定可能
  smtp_port: 設定可能
  authentication: 設定可能
```

#### 1.9 その他 タブ (2d4457c90808f33a)

**目的**: 補助機能・ユーティリティ
**主要機能**:
- システム診断
- デバッグ機能
- テスト用ツール
- 開発者向け機能

### 2. サブフロー（再利用可能コンポーネント）

#### 2.1 Tab Transition (f89f5e3b86cd59d6)
**機能**: UI タブ間の遷移制御
**入力**: タブID、遷移イベント
**出力**: 画面切り替え命令

#### 2.2 Type2Config (c91ae0a3d8355cfb)
**機能**: 設定タイプの変換処理
**入力**: 設定データ、タイプ情報
**出力**: 変換後設定データ

#### 2.3 Str2Json (8ebeefef09059e86)
**機能**: 文字列からJSONへの解析
**入力**: JSON文字列
**出力**: JSONオブジェクト
**エラー処理**: 不正JSON検出・例外処理

#### 2.4 Init Config (cb5ec79ce8b445f4)
**機能**: システム初期化処理
**実行タイミング**: システム起動時
**処理内容**: 
- デフォルト設定読み込み
- データベース接続確認
- 初期状態設定

#### 2.5 Update Sensor (9a1bb339c6988af7)
**機能**: センサーデータ更新処理
**入力**: センサーID、測定値、タイムスタンプ
**処理**: 
- データ検証
- データベース更新
- リアルタイム配信

#### 2.6 All Devices (9240fdb206d57ffc)
**機能**: 全デバイス情報取得
**出力**: デバイスリスト、状態情報
**用途**: 一括監視、ステータス確認

#### 2.7 Update Device (6e08da7314bcfdec)
**機能**: デバイス設定更新
**入力**: デバイスID、設定データ
**処理**: 設定検証、データベース更新、デバイス通知

#### 2.8 IP (5c990f7436d9ded3)
**機能**: IPアドレス管理
**処理**: ネットワーク情報取得、IP設定管理

#### 2.9 BravePI Output (8d853eb576531593)
**機能**: BravePI デバイス出力制御
**入力**: 出力チャンネル、制御値
**出力**: デジタル出力制御

### 3. センサータイプと測定対象

#### 3.1 デジタル I/O センサー
```
接点入力/接点出力:
- デジタル信号の入出力
- カウンター機能
- 状態変化検出
- パルス計数
```

#### 3.2 アナログセンサー
```
ADC (アナログ-デジタル変換):
- 電圧測定 (0-5V, 0-10V)
- 電流測定 (4-20mA)
- 抵抗値測定
- 分解能: 12bit/16bit
```

#### 3.3 環境センサー
```
温湿度センサー:
- 温度範囲: -40℃ ～ +85℃
- 湿度範囲: 0% ～ 100% RH
- 精度: ±0.3℃, ±3% RH

気圧センサー:
- 測定範囲: 300-1100 hPa
- 精度: ±1 hPa

照度センサー:
- 測定範囲: 0.01 ～ 40,000 lux
- 応答波長: 400-700nm
```

#### 3.4 物理量センサー
```
測距センサー:
- 超音波式: 2cm ～ 400cm
- 赤外線式: 4cm ～ 30cm
- レーザー式: 高精度測定

差圧センサー:
- 測定範囲: ±2.5kPa ～ ±250kPa
- 用途: 流量測定、液位測定

加速度センサー:
- 測定軸: 3軸 (X, Y, Z)
- 測定範囲: ±2g ～ ±16g
- サンプリング周波数: 最大1.6kHz
```

#### 3.5 高温測定
```
熱電対:
- K型: -200℃ ～ +1372℃
- J型: -210℃ ～ +1200℃
- T型: -250℃ ～ +400℃
- 冷接点補償: 自動
```

#### 3.6 画像・音響
```
カメラ:
- 解像度: VGA ～ Full HD
- フォーマット: JPEG, PNG
- ストリーミング対応

スペクトログラム:
- 音響解析: 20Hz ～ 20kHz
- 振動解析: 機械診断用途
- FFT処理: リアルタイム
```

#### 3.7 拡張スロット
```
拡張0-9:
- 10個の追加センサースロット
- カスタムセンサー対応
- プラグイン形式での追加
- 独立設定管理
```

### 4. 通信プロトコル・インターフェース

#### 4.1 MQTT 通信
```yaml
Primary Broker: localhost:1883
Secondary Broker: localhost:51883

Topics:
  DwlResp/+:     # ダウンロード応答
  JIResp/+:      # JIG応答  
  UlReq/+:       # アップロード要求
  ErrResp/+:     # エラー応答
  DfuResp/+:     # DFU応答
```

#### 4.2 データベース接続
```yaml
MySQL Database:
  Host: 127.0.0.1:3306
  Database: iotkit
  用途: 設定・メタデータ保存
  
InfluxDB:
  Host: 127.0.0.1:8086  
  Database: iotkit
  Version: 2.0
  用途: 時系列データ保存
```

#### 4.3 シリアル通信
```yaml
Main UART: /dev/ttyAMA0
  Baud Rate: 38400
  Data Bits: 8
  Stop Bits: 1
  Parity: None
  
USB Serial Ports: /dev/ttyACM0-9
  Baud Rate: 38400
  Flow Control: None
```

### 5. API仕様

#### 5.1 デバイス管理API
```http
GET /api/v2/device
Response: デバイス一覧
{
  "devices": [
    {
      "id": "device_001",
      "name": "センサーノード1",
      "type": "sensor_node",
      "status": "online",
      "last_seen": "2024-01-01T12:00:00Z"
    }
  ]
}

POST /api/v2/device
Request: 新規デバイス登録
{
  "name": "新しいセンサー",
  "type": "temperature",
  "config": {
    "sampling_rate": 60,
    "threshold": 25.0
  }
}
```

#### 5.2 センサーデータAPI
```http
GET /api/v2/device/:deviceId/sensor/value
Response: センサー値取得
{
  "device_id": "device_001",
  "timestamp": "2024-01-01T12:00:00Z",
  "sensors": {
    "temperature": 23.5,
    "humidity": 65.2,
    "pressure": 1013.25
  }
}

POST /api/v2/device/:deviceId/sensor/value  
Request: センサー値送信
{
  "timestamp": "2024-01-01T12:00:00Z",
  "values": {
    "temperature": 24.1,
    "humidity": 66.8
  }
}
```

#### 5.3 制御API
```http
POST /api/v2/device/:deviceId/output
Request: デジタル出力制御
{
  "channel": 1,
  "value": true,
  "duration": 5000  // ms
}
```

### 6. データフロー構造

#### 6.1 センサーデータパイプライン
```
[センサー] → [シリアル/GPIO] → [データ検証] → [変換処理] 
    ↓
[MySQL保存] → [InfluxDB保存] → [リアルタイム配信] → [ダッシュボード表示]
    ↓
[アラート判定] → [通知送信] → [ログ記録]
```

#### 6.2 デバイス管理フロー
```
[デバイス登録] → [設定検証] → [データベース保存] → [初期化処理]
    ↓
[状態監視] → [ヘルスチェック] → [ステータス更新] → [アラート生成]
    ↓
[設定変更] → [デバイス通知] → [設定適用] → [動作確認]
```

#### 6.3 通信アーキテクチャ
```
Internal Communication:
  MQTT pub/sub パターン
  
External Communication:  
  HTTP REST API
  
Hardware Communication:
  Serial protocols (UART, USB)
  I2C bus communication
  GPIO digital I/O
  
Wireless Communication:
  Bluetooth Low Energy (BLE)
  WiFi network access
```

### 7. システム特徴・機能

#### 7.1 リアルタイム監視
- 1秒間隔でのデータ更新
- WebSocket による即座の画面反映
- アラート・通知の瞬時配信
- 複数クライアントでの同時監視

#### 7.2 データ永続化
- MySQL: 設定・メタデータの関係DB保存
- InfluxDB: 高速時系列データ保存
- データ圧縮・効率的ストレージ
- 自動データ保持期間管理

#### 7.3 拡張性
- プラグイン形式での新センサー追加
- モジュール方式でのカスタム機能
- REST API による外部システム連携
- 分散センサーノード対応

#### 7.4 信頼性
- 通信エラー時の自動復旧
- データ消失防止機能
- システム状態の常時監視
- 冗長化対応（MQTT セカンダリブローカー）

#### 7.5 ユーザビリティ
- 直感的なWeb ダッシュボード
- モバイル対応レスポンシブデザイン
- 日本語完全対応
- カスタマイズ可能なUI構成

### 8. 技術仕様

#### 8.1 動作環境
```yaml
OS: Raspbian OS (Debian ベース)
Node.js: v16.x 以降
Node-RED: v3.x 以降
Python: v3.9 以降

必要メモリ: 1GB 以上
必要ストレージ: 8GB 以上
ネットワーク: Ethernet/WiFi
```

#### 8.2 依存関係
```yaml
Node-RED パッケージ:
  - node-red-dashboard
  - node-red-contrib-influxdb  
  - node-red-contrib-mysql
  - node-red-node-serialport
  - node-red-contrib-gpio

システムパッケージ:
  - mosquitto (MQTT Broker)
  - mysql-server
  - influxdb
```

#### 8.3 セキュリティ
- ユーザー認証システム
- API アクセストークン
- 通信暗号化対応
- ローカルネットワーク前提設計

### 9. 運用・保守

#### 9.1 ログ管理
- システムログ: /var/log/node-red/
- エラーログ: 自動分類・通知
- 監査ログ: API アクセス記録
- パフォーマンスログ: リソース使用状況

#### 9.2 バックアップ
- 設定データ: 自動定期バックアップ
- センサーデータ: InfluxDB バックアップ
- システム構成: イメージバックアップ対応

#### 9.3 メンテナンス
- 自動アップデート機能
- リモートメンテナンス対応
- 設定変更履歴管理
- システム診断ツール

## まとめ

Node-RED IoT導入支援キット Ver.4.1 は、産業用IoTシステムの構築に必要な全ての要素を統合した包括的なプラットフォームです。豊富なセンサー対応、リアルタイム監視、データ分析機能により、製造業、農業、環境監視等の幅広い分野での活用が可能です。

拡張性とカスタマイズ性を重視した設計により、特定の要件に応じたシステム構築が可能であり、Node-REDの視覚的プログラミング環境により、技術者でなくても直感的にシステムの理解・改修が行えます。