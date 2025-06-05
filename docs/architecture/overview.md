# IoT導入支援キット Ver.4.1 アーキテクチャドキュメント

## 目次
1. [概要](#概要)
2. [プロジェクト構造](#プロジェクト構造)
3. [システムアーキテクチャ](#システムアーキテクチャ)
4. [データフロー](#データフロー)
5. [コンポーネント詳細](#コンポーネント詳細)
6. [センサータイプと設定](#センサータイプと設定)

## 概要

IoT導入支援キット Ver.4.1は、福岡県工業技術センター（FITC）が開発した包括的なIoTデータ収集・可視化システムです。Raspberry Pi上で動作し、様々なセンサーからのデータ収集、保存、可視化、アラート機能を提供します。

### 主な特徴
- 13種類の産業用センサーをサポート
- マルチプロトコル対応（I2C、GPIO、Serial、BLE、HTTP、MQTT）
- デュアルデータベースアーキテクチャ（MariaDB + InfluxDB）
- Node-REDベースのビジュアルプログラミング
- リアルタイムダッシュボード
- メール通知とMQTT連携

## プロジェクト構造

```
iot4-copy/
├── README.md                    # プロジェクト概要
├── desktop/                     # Raspberry Piデスクトップ設定
│   ├── first.sh                # 初期設定スクリプト
│   ├── chrome-IoT導入支援キット_Ver.4.1.desktop
│   └── chrome-Node-RED___IoT導入支援キットVer.4.1.desktop
├── docker/                      # Dockerコンテナ設定
│   ├── docker-compose.yml      # サービス定義
│   ├── init.sql               # MariaDBスキーマ
│   ├── mariadb/
│   │   └── Dockerfile
│   └── influxdb/
│       └── Dockerfile
└── .node-red/                  # Node-RED設定（gitignore）
    ├── flows.json             # フロー定義
    ├── settings.js            # Node-RED設定
    ├── package.json           # 依存関係
    ├── python/                # センサードライバー
    │   ├── vl53l1x.py        # 距離センサー
    │   ├── mcp3427.py        # ADC
    │   ├── mcp9600.py        # 熱電対
    │   ├── lis2duxs12.py     # 加速度センサー
    │   ├── opt3001.py        # 照度センサー
    │   ├── sdp810.py         # 差圧センサー
    │   └── lombscargle.py    # 信号処理
    └── static/               # Webフロントエンド
        ├── css/
        └── js/               # 可視化コンポーネント
```

## システムアーキテクチャ

```mermaid
graph TB
    subgraph "ハードウェア層"
        S1[I2Cセンサー]
        S2[GPIOデバイス]
        S3[シリアルデバイス]
        S4[BLEデバイス]
        S5[HTTPセンサー]
    end
    
    subgraph "通信層"
        I1[I2C Bus]
        I2[GPIO Pins]
        I3[Serial/USB]
        I4[Bluetooth]
        I5[HTTP/REST]
        I6[MQTT Broker]
    end
    
    subgraph "処理層（ホスト）"
        NR[Node-RED<br/>:1880]
        PY[Pythonドライバー]
        MQTT[Aedes MQTT<br/>:1883]
    end
    
    subgraph "データ層（Docker）"
        DB1[MariaDB<br/>:3306<br/>設定・メタデータ]
        DB2[InfluxDB<br/>:8086<br/>時系列データ]
    end
    
    subgraph "プレゼンテーション層"
        UI[ダッシュボード<br/>:1880/ui/]
        FLOW[フローエディタ<br/>:1880/#flow/]
        API[REST API]
    end
    
    subgraph "外部連携"
        EMAIL[メール通知]
        MQTTEXT[外部MQTT]
        GPIO_OUT[GPIO出力]
    end
    
    S1 --> I1
    S2 --> I2
    S3 --> I3
    S4 --> I4
    S5 --> I5
    
    I1 --> PY
    I2 --> NR
    I3 --> NR
    I4 --> NR
    I5 --> NR
    I6 --> NR
    
    PY --> NR
    NR --> MQTT
    
    NR --> DB1
    NR --> DB2
    
    NR --> UI
    NR --> FLOW
    NR --> API
    
    NR --> EMAIL
    NR --> MQTTEXT
    NR --> GPIO_OUT
    
    style NR fill:#ff6b6b,stroke:#333,stroke-width:4px
    style DB1 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style DB2 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style UI fill:#95e1d3,stroke:#333,stroke-width:2px
```

## データフロー

### 1. センサーデータ収集フロー

```mermaid
sequenceDiagram
    participant Sensor as センサー
    participant Driver as ドライバー
    participant NodeRED as Node-RED
    participant InfluxDB as InfluxDB
    participant Dashboard as ダッシュボード
    
    Sensor->>Driver: 測定値
    Driver->>NodeRED: データ送信
    NodeRED->>NodeRED: データ処理
    NodeRED->>InfluxDB: 時系列データ保存
    NodeRED->>Dashboard: リアルタイム表示
    
    alt 閾値超過
        NodeRED->>NodeRED: アラート判定
        NodeRED-->>Email: メール通知
        NodeRED-->>MQTT: MQTT発行
    end
```

### 2. デバイス登録フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant UI as ダッシュボード
    participant NodeRED as Node-RED
    participant MariaDB as MariaDB
    
    User->>UI: デバイス情報入力
    UI->>NodeRED: 登録リクエスト
    NodeRED->>MariaDB: デバイス保存
    
    NodeRED->>MariaDB: センサー設定保存
    NodeRED->>MariaDB: 通信設定保存
    
    MariaDB-->>NodeRED: 保存完了
    NodeRED-->>UI: 登録完了通知
    UI-->>User: 完了表示
```

## コンポーネント詳細

### Node-REDフロー構成

| タブ名 | 機能 | 説明 |
|--------|------|------|
| PI・JIG・I2C・GPIO | ハードウェアインターフェース | センサーとの通信制御 |
| ダッシュボード | UI表示 | リアルタイムグラフとステータス |
| デバイス登録 | デバイス管理 | 新規デバイスの登録と設定 |
| センサーログ | データ記録 | InfluxDBへの時系列データ保存 |
| BLEトランスミッター | BLE通信 | Bluetoothデバイスとの連携 |
| ルーター | データルーティング | センサーデータの振り分け |
| モジュール | 共通機能 | 再利用可能な処理ブロック |
| 設定 | システム設定 | MQTT、メール等の設定管理 |

### データベーススキーマ

#### MariaDB（設定管理）

```mermaid
erDiagram
    devices ||--o{ sensors : has
    devices ||--o| ble_device_configs : has
    devices ||--o| usb_device_configs : has
    devices ||--o| i2c_device_configs : has
    devices ||--o| gpio_device_configs : has
    devices ||--o| http_device_configs : has
    
    sensors ||--|| sensor_types : belongs_to
    sensor_types ||--o{ sensor_channels : has
    
    sensors ||--o{ sensor_mqtt_topics : publishes_to
    sensors ||--o{ sensor_mail_addresses : sends_to
    sensors ||--o{ sensor_gpio_outputs : controls
    
    mqtt_topics ||--|| mqtt_brokers : uses
    mail_addresses ||--|| mail_servers : uses
    
    devices {
        int id PK
        string name
        boolean i2c
        boolean gpio
        boolean serial
        boolean ble
        boolean http
    }
    
    sensors {
        int id PK
        int device_id FK
        int sensor_type_id FK
        string name
        float hysteresis
        int debounce
        float offset
        boolean toggle
        boolean invert
        int photo
    }
    
    sensor_types {
        int id PK
        string name
        string unit
    }
```

#### InfluxDB（時系列データ）

- **Organization**: fitc
- **Bucket**: iotkit
- **Measurements**: センサータイプごとに自動作成
- **Tags**: device_id, sensor_id, channel
- **Fields**: value, timestamp

### 主要Node-REDモジュール

| モジュール | 用途 |
|-----------|------|
| node-red-contrib-aedes | MQTTブローカー機能 |
| node-red-contrib-influxdb | InfluxDB連携 |
| node-red-dashboard | Webダッシュボード |
| node-red-node-mysql | MariaDB連携 |
| node-red-node-pi-gpio | GPIO制御 |
| node-red-node-serialport | シリアル通信 |
| node-red-contrib-buffer-parser | バイナリデータ解析 |

## センサータイプと設定

### サポートセンサー一覧

| ID | タイプ | 測定項目 | 範囲 | 単位 |
|----|--------|----------|------|------|
| 257 | 接点入力 | ON/OFF | 0-1 | - |
| 258 | 接点出力 | ON/OFF | 0-1 | - |
| 259 | ADC | 電圧（2ch） | ±2000 | mV |
| 260 | 測距 | 距離 | 0-2000 | mm |
| 261 | 熱電対 | 温度 | -50-2000 | ℃ |
| 262 | 加速度 | X,Y,Z,合成 | ±6.5 | G |
| 263 | 差圧 | 圧力 | ±500 | Pa |
| 264 | 照度 | 明るさ | 40-83865 | lux |

### センサー設定パラメータ

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| hysteresis | ヒステリシス閾値 | 0.0 |
| debounce | デバウンス時間（秒） | 0 |
| offset | オフセット補正値 | 0.0 |
| toggle | トグル動作有効化 | false |
| invert | 出力反転 | false |
| photo | 写真撮影トリガー | 0 |

### 通信プロトコル設定

#### MQTT設定
- ブローカー: localhost:1883
- 認証: iotkit / iotkit-password
- QoS: 0（デフォルト）

#### メール設定
- SMTPサーバー: localhost:25
- 認証: なし（デフォルト）
- アラート条件: センサーごとに設定可能

### 初期設定フロー

```mermaid
graph LR
    A[first.sh実行] --> B[ファイルシステム拡張]
    B --> C[システム再起動]
    C --> D[docker-compose up]
    D --> E[MariaDB初期化]
    D --> F[InfluxDB初期化]
    E --> G[init.sql実行]
    F --> H[Organization/Bucket作成]
    G --> I[Node-RED起動]
    H --> I
    I --> J[ダッシュボードアクセス可能]
```

## まとめ

IoT導入支援キットは、ハードウェアアクセスが必要な部分（Node-RED、Pythonドライバー）をホスト上で実行し、データ管理部分（MariaDB、InfluxDB）をDocker化することで、柔軟性と保守性を両立させた設計となっています。

このハイブリッドアーキテクチャにより、Raspberry Piの GPIO やI2Cバスへの直接アクセスを維持しながら、データベースの可搬性とバージョン管理の利便性を確保しています。