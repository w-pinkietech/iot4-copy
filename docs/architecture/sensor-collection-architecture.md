# センサー収集システム アーキテクチャ設計書

## 概要

本ドキュメントは、既存のNode-REDベースのIoTシステムから、よりメンテナンス性の高いPython/FastAPIベースのアーキテクチャへの移行設計を記述します。

## 現状の課題

1. **Node-REDの複雑性**: 大規模なフロー管理が困難
2. **密結合**: センサードライバーとNode-REDが密に結合
3. **メンテナンス性**: 1人での保守が限界
4. **AI活用の制限**: ビジュアルプログラミングではAI支援が限定的

## 新アーキテクチャの設計方針

- **シンプル**: 技術スタックを最小限に
- **疎結合**: 各コンポーネントの独立性を確保
- **保守性**: 1人でも管理可能な構成
- **AI親和性**: テキストベースのコードでAI支援を最大化
- **ポータビリティ**: コレクター層以上は任意のLinux環境で動作
- **スケーラビリティ**: 複数のエッジデバイスからのデータ収集に対応

## システム構成図

### エッジゲートウェイアーキテクチャ概要

```mermaid
graph TB
    subgraph "Edge Gateway Layer"
        subgraph "RPi4 Gateway A"
            RPi4HAL[Edge Gateway Service<br/>- 複数センサー統合管理<br/>- ローカル設定管理<br/>- 自己完結型データ送信]
            RPi4DB[(MariaDB<br/>ローカル設定)]
            RPi4Sensors[BravePI + I2C/GPIO<br/>センサー群]
        end
        
        subgraph "RPi5 Gateway B"
            RPi5HAL[Edge Gateway Service<br/>- libgpiod対応<br/>- 複数センサー統合管理<br/>- ローカル設定管理]
            RPi5DB[(MariaDB<br/>ローカル設定)]
            RPi5Sensors[センサー群]
        end
        
        subgraph "Other Gateway C"
            OtherHAL[Edge Gateway Service<br/>- デバイス固有実装<br/>- センサー統合管理]
            OtherDB[(MariaDB<br/>ローカル設定)]
            OtherSensors[センサー群]
        end
    end
    
    subgraph "Collection/Application Layer (任意のLinux環境)"
        MQTT[MQTT Broker<br/>mosquitto]
        Collector[Data Collector Service<br/>- 自己完結型データ処理<br/>- しきい値判定<br/>- イベント処理]
        InfluxDB[(InfluxDB<br/>時系列データのみ)]
        Streamlit[Streamlit<br/>統合管理UI]
        Grafana[Grafana<br/>ダッシュボード]
        API[REST API<br/>外部連携]
    end
    
    %% Edge Gateway internal connections
    RPi4Sensors -.-> RPi4HAL
    RPi4HAL -.->|設定参照| RPi4DB
    
    RPi5Sensors -.-> RPi5HAL
    RPi5HAL -.->|設定参照| RPi5DB
    
    OtherSensors -.-> OtherHAL
    OtherHAL -.->|設定参照| OtherDB
    
    %% Edge to Collection connections
    RPi4HAL -->|自己完結型<br/>MQTTメッセージ| MQTT
    RPi5HAL -->|自己完結型<br/>MQTTメッセージ| MQTT
    OtherHAL -->|自己完結型<br/>MQTTメッセージ| MQTT
    
    %% Collection Layer connections
    MQTT --> Collector
    Collector --> InfluxDB
    
    %% Application Layer connections
    Streamlit --> InfluxDB
    Grafana --> InfluxDB
    API --> InfluxDB
    
    %% Styling
    classDef edge fill:#ff7f0e,stroke:#fff,stroke-width:2px,color:#fff
    classDef collection fill:#2ca02c,stroke:#fff,stroke-width:2px,color:#fff
    classDef application fill:#1f77b4,stroke:#fff,stroke-width:2px,color:#fff
    classDef storage fill:#d62728,stroke:#fff,stroke-width:2px,color:#fff
    
    class RPi4HAL,RPi5HAL,OtherHAL,RPi4Sensors,RPi5Sensors,OtherSensors,RPi4DB,RPi5DB,OtherDB edge
    class MQTT,Collector collection
    class Streamlit,Grafana,API application
    class InfluxDB storage
```

## エッジゲートウェイアーキテクチャ詳細

### Layer 1: Edge Gateway Layer（エッジゲートウェイ層）

**責務**
- 複数センサーの統合管理
- ローカル設定としきい値の管理
- 自己完結型MQTTメッセージの送信

**Edge Gateway Service**
```python
# edge/gateway_service.py
class EdgeGatewayService:
    def __init__(self, gateway_id: str):
        self.gateway_id = gateway_id
        self.db = LocalMariaDB()  # ローカル設定DB
        self.sensors = load_sensor_drivers()
        self.mqtt_client = MQTTClient()
    
    async def collect_and_publish(self):
        for sensor in self.sensors:
            # センサー値読み取り
            value = sensor.read()
            
            # ローカル設定を取得
            config = self.db.get_sensor_config(sensor.id)
            
            # 自己完結型メッセージを構築
            message = {
                "timestamp": datetime.utcnow().isoformat(),
                "gateway_id": self.gateway_id,
                "sensor": {
                    "id": sensor.id,
                    "type": config.sensor_type,
                    "name": config.name,
                    "unit": config.unit,
                    "value": value
                },
                "thresholds": {
                    "high": config.threshold_high,
                    "low": config.threshold_low
                },
                "metadata": {
                    "location": config.location,
                    "calibration": config.offset
                }
            }
            
            await self.mqtt_client.publish("sensors/data", message)
```

**デバイス固有実装**
- **RPi4**: RPi.GPIO + BravePI Hub
- **RPi5**: libgpiod + 新GPIO API
- **Orange Pi/Jetson**: デバイス固有ライブラリ

### Layer 2: Collection/Application Layer（統合処理層）

**責務**
- 自己完結型メッセージの受信と処理
- 時系列データの永続化
- 統合ダッシュボードとAPI提供

**技術スタック**
- MQTT Broker (mosquitto)
- FastAPI + asyncio
- InfluxDB (時系列データのみ)
- Streamlit (統合管理UI)
- Grafana (可視化)

**Data Collector Service**
```python
# collector/data_collector.py
class DataCollectorService:
    def __init__(self):
        self.influxdb = InfluxDBClient()
        self.mqtt_client = MQTTClient()
    
    async def on_sensor_message(self, message):
        data = json.loads(message)
        
        # メッセージに全ての情報が含まれているので、
        # 外部設定を参照せずに処理可能
        sensor_value = data["sensor"]["value"]
        thresholds = data["thresholds"]
        
        # しきい値判定
        if sensor_value > thresholds["high"]:
            await self.trigger_alert(data)
        
        # InfluxDBに保存（設定情報もタグとして保存）
        await self.influxdb.write({
            "measurement": data["sensor"]["type"],
            "tags": {
                "gateway_id": data["gateway_id"],
                "sensor_id": data["sensor"]["id"],
                "location": data["metadata"]["location"]
            },
            "fields": {
                "value": sensor_value
            },
            "timestamp": data["timestamp"]
        })
```

**特徴**
- **設定非依存**: MQTTメッセージが自己完結
- **シンプル**: 設定同期やAPI呼び出し不要
- **堅牢**: ネットワーク障害に強い
- **スケーラブル**: 複数ゲートウェイからの統合処理

## エッジゲートウェイ対応ディレクトリ構造

```
iot-gateway-system/
├── edge-gateway/            # エッジゲートウェイ層（各ゲートウェイで実行）
│   ├── gateway_service.py   # ゲートウェイサービス
│   ├── sensors/             # センサードライバー
│   │   ├── __init__.py
│   │   ├── base.py         # 基底クラス
│   │   ├── i2c/
│   │   │   ├── vl53l1x.py   # 測距センサー
│   │   │   ├── opt3001.py   # 照度センサー
│   │   │   ├── mcp3427.py   # ADCセンサー
│   │   │   ├── mcp9600.py   # 熱電対センサー
│   │   │   ├── lis2duxs12.py # 加速度センサー
│   │   │   └── sdp610.py    # 差圧センサー
│   │   ├── gpio/
│   │   │   └── gpio.py      # GPIO入出力
│   │   ├── serial/
│   │   │   └── brave.py     # BravePIシリアル通信
│   │   └── brave_hub/
│   │       └── brave_hub.py # BravePI Hub管理
│   ├── hardware/            # ハードウェア抽象化層
│   │   ├── __init__.py
│   │   ├── interfaces.py    # 抽象インターフェース
│   │   ├── rpi4/
│   │   │   ├── gpio.py     # RPi4 GPIO実装
│   │   │   └── i2c.py      # RPi4 I2C実装
│   │   ├── rpi5/
│   │   │   ├── gpio.py     # RPi5 GPIO実装（libgpiod）
│   │   │   └── i2c.py      # RPi5 I2C実装
│   │   └── mock/
│   │       ├── gpio.py     # テスト用モック
│   │       └── i2c.py      # テスト用モック
│   ├── database/            # ローカルMariaDB管理
│   │   ├── models.py       # SQLAlchemyモデル
│   │   ├── migrations/     # DBマイグレーション
│   │   └── init.sql        # 初期化スクリプト
│   ├── config/
│   │   └── gateway_config.yml # ゲートウェイ設定
│   └── requirements-gateway.txt # ゲートウェイ用依存関係
│
├── collection-server/       # 統合処理層（任意のLinux環境）
│   ├── main.py             # FastAPIアプリケーション
│   ├── data_collector.py   # MQTTデータ受信・処理
│   ├── storage.py          # InfluxDB書き込み
│   ├── alert_manager.py    # アラート処理
│   ├── api/                # REST API
│   │   ├── __init__.py
│   │   ├── routers/
│   │   │   ├── gateways.py # ゲートウェイ管理
│   │   │   ├── sensors.py  # センサーデータ
│   │   │   └── alerts.py   # アラート管理
│   │   └── models.py       # APIモデル
│   ├── streamlit_app/      # 統合管理UI
│   │   ├── main.py
│   │   ├── pages/
│   │   │   ├── overview.py    # 全体概要
│   │   │   ├── gateways.py    # ゲートウェイ状況
│   │   │   ├── sensors.py     # センサー一覧
│   │   │   └── alerts.py      # アラート管理
│   │   └── components/
│   │       ├── charts.py      # グラフコンポーネント
│   │       └── tables.py      # テーブルコンポーネント
│   ├── config/
│   │   └── server_config.yml
│   └── requirements-server.txt
│
├── common/                  # 共通ライブラリ（全層で使用）
│   ├── __init__.py
│   ├── mqtt_client.py       # MQTT共通クライアント
│   ├── message_format.py    # 自己完結型メッセージ定義
│   ├── config_loader.py     # 設定ファイル読み込み
│   ├── logger.py            # ロギング設定
│   └── models/              # 共通データモデル
│       ├── sensor_data.py   # センサーデータ構造
│       ├── gateway_info.py  # ゲートウェイ情報
│       └── alert_rule.py    # アラートルール
│
├── infrastructure/          # インフラストラクチャ構成
│   ├── docker/              # Dockerコンテナ構成（Collection層用）
│   │   ├── docker-compose.yml       # 開発環境用
│   │   ├── docker-compose.prod.yml  # 本番環境用
│   │   ├── influxdb/
│   │   │   ├── Dockerfile
│   │   │   └── config/
│   │   ├── grafana/
│   │   │   ├── Dockerfile
│   │   │   ├── dashboards/
│   │   │   └── provisioning/
│   │   └── mosquitto/
│   │       ├── Dockerfile
│   │       └── config/
│   ├── gateway-setup/       # ゲートウェイセットアップ
│   │   ├── mariadb/
│   │   │   ├── install.sh
│   │   │   └── init.sql
│   │   └── systemd/
│   │       └── gateway-service.service
│   ├── systemd/             # Collection層systemdサービス
│   │   ├── collector-service.service
│   │   └── streamlit-app.service
│   └── ansible/             # デプロイメント自動化
│       ├── playbooks/
│       │   ├── deploy-gateway.yml
│       │   └── deploy-server.yml
│       └── inventory/
│
├── tests/                   # テストコード
│   ├── test_gateway/
│   │   ├── test_sensors/
│   │   └── test_message_format/
│   ├── test_server/
│   │   ├── test_collector/
│   │   └── test_api/
│   └── test_common/
│
├── docs/                    # ドキュメント
│   ├── deployment/          # デプロイメントガイド
│   │   ├── gateway-setup.md
│   │   └── server-setup.md
│   ├── api/                 # API仕様
│   │   └── message-format.md # MQTTメッセージ仕様
│   └── troubleshooting/     # トラブルシューティング
│
├── scripts/                 # 運用スクリプト
│   ├── deploy_gateway.sh    # ゲートウェイデプロイ
│   ├── deploy_server.sh     # サーバーデプロイ
│   ├── gateway_health.py    # ゲートウェイヘルスチェック
│   └── sync_config.py       # 設定同期（必要に応じて）
│
└── config/                  # 全体設定
    ├── message_schema.json  # MQTTメッセージスキーマ
    └── environments/        # 環境別設定
        ├── development.yml
        ├── staging.yml
        └── production.yml
```

## インフラストラクチャ構成

### デプロイメント構成例

```mermaid
graph TB
    subgraph "Edge Device 1 (RPi4)"
        EdgeService1[Hardware Access Service<br/>ネイティブ実行]
        EdgeHW1[センサー群]
    end
    
    subgraph "Edge Device 2 (RPi5)"
        EdgeService2[Hardware Access Service<br/>ネイティブ実行]
        EdgeHW2[センサー群]
    end
    
    subgraph "Data Collection Server (任意のLinux)"
        subgraph "Native Services"
            CollectorApp[Collector Service<br/>FastAPI]
            StreamlitApp[Streamlit UI]
        end
        
        subgraph "Docker Services"
            MQTT[MQTT Broker<br/>mosquitto]
            InfluxDB[(InfluxDB)]
            MariaDB[(MariaDB)]
            Grafana[Grafana]
        end
    end
    
    subgraph "Cloud/Remote (Optional)"
        CloudAPI[REST API<br/>外部連携]
        CloudUI[Web Dashboard]
    end
    
    %% Edge to Collection
    EdgeService1 -->|MQTT| MQTT
    EdgeService2 -->|MQTT| MQTT
    
    %% Collection layer
    MQTT --> CollectorApp
    CollectorApp --> InfluxDB
    CollectorApp --> MariaDB
    StreamlitApp --> MariaDB
    Grafana --> InfluxDB
    
    %% Cloud integration
    CloudAPI --> InfluxDB
    CloudAPI --> MariaDB
    
    %% Hardware connections
    EdgeHW1 -.-> EdgeService1
    EdgeHW2 -.-> EdgeService2
    
    %% Styling
    classDef edge fill:#ff7f0e,stroke:#fff,stroke-width:2px,color:#fff
    classDef collection fill:#2ca02c,stroke:#fff,stroke-width:2px,color:#fff
    classDef container fill:#1f77b4,stroke:#fff,stroke-width:2px,color:#fff
    classDef cloud fill:#9467bd,stroke:#fff,stroke-width:2px,color:#fff
    
    class EdgeService1,EdgeService2,EdgeHW1,EdgeHW2 edge
    class CollectorApp,StreamlitApp collection
    class MQTT,InfluxDB,MariaDB,Grafana container
    class CloudAPI,CloudUI cloud
```

### 層別ポート構成

#### Edge Layer
| サービス | 実行環境 | ポート | 用途 |
|---------|---------|--------|------|
| Hardware Access Service | Native | - | MQTTクライアント |

#### Collection Layer
| サービス | 実行環境 | ポート | 用途 |
|---------|---------|--------|------|
| MQTT Broker | Docker | 1883 | デバイス間通信 |
| Collector Service | Native | 8000 | データ収集API |
| Streamlit UI | Native | 8501 | 設定管理 |
| InfluxDB | Docker | 8086 | 時系列DB |
| MariaDB | Docker | 3306 | 設定DB |
| Grafana | Docker | 3000 | 可視化 |

#### Application Layer
| サービス | 実行環境 | ポート | 用途 |
|---------|---------|--------|------|
| REST API | Native/Cloud | 8080 | 外部連携 |

### 各層の技術選択理由

**Edge Layer（エッジデバイス層）**
- **ネイティブ実行**: ハードウェア直接アクセス必須
- **軽量実装**: リソース制約のあるSBC環境

**Collection Layer（データ収集層）**
- **ハイブリッド構成**: 
  - アプリケーション: ネイティブ（性能重視）
  - データベース: Docker（運用性重視）

**Application Layer（アプリケーション層）**
- **完全抽象化**: ハードウェア非依存
- **クラウド対応**: スケーラビリティ確保

## データフロー

### 1. 自己完結型データフロー

```mermaid
flowchart LR
    Sensors[複数センサー] --> Gateway[Edge Gateway]
    Gateway --> LocalDB[(ローカルMariaDB)]
    Gateway --> Message[自己完結型<br/>MQTTメッセージ]
    
    Message --> MQTT[MQTT Broker]
    MQTT --> Collector[Data Collector]
    Collector --> InfluxDB[(InfluxDB)]
    Collector --> Alert{しきい値判定}
    Alert -->|超過| Notify[通知]
    
    InfluxDB --> Grafana[Grafana]
    InfluxDB --> Streamlit[Streamlit]
    
    style Sensors fill:#ff7f0e,stroke:#fff,color:#fff
    style Gateway fill:#ff7f0e,stroke:#fff,color:#fff
    style LocalDB fill:#ff7f0e,stroke:#fff,color:#fff
    style Message fill:#2ca02c,stroke:#fff,color:#fff
    style MQTT fill:#2ca02c,stroke:#fff,color:#fff
    style Collector fill:#2ca02c,stroke:#fff,color:#fff
    style InfluxDB fill:#d62728,stroke:#fff,color:#fff
    style Grafana fill:#1f77b4,stroke:#fff,color:#fff
    style Streamlit fill:#1f77b4,stroke:#fff,color:#fff
```

### 2. MQTTメッセージ構造

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "gateway_id": "rpi4-factory-001",
  "sensor": {
    "id": "temp-room-01",
    "type": "temperature",
    "name": "工場内温度センサー",
    "unit": "℃",
    "value": 25.3
  },
  "thresholds": {
    "high": 30.0,
    "low": 10.0,
    "hysteresis": 1.0
  },
  "metadata": {
    "location": "製造ライン1",
    "calibration_offset": 0.2,
    "last_calibrated": "2024-01-01T00:00:00Z"
  },
  "quality": {
    "confidence": 0.95,
    "error_status": "ok"
  }
}
```

## 分散アーキテクチャ移行戦略

### Phase 1: ハードウェア抽象化層の構築
1. **抽象インターフェースの定義**
   - GPIO、I2C、Serial通信の統一インターフェース作成
   - RPi4/RPi5/その他SBC対応の実装
   - モック実装によるテスト環境構築

2. **Edge Layer基盤開発**
   - Hardware Access Serviceの基本実装
   - MQTTクライアント機能の実装
   - 設定ファイルによるデバイス管理

### Phase 2: Collection Layer開発
1. **MQTT基盤の構築**
   - mosquitto MQTTブローカーの設定
   - メッセージフォーマットの標準化
   - QoS設定とエラーハンドリング

2. **データ収集サービス開発**
   - MQTTサブスクライバーの実装
   - しきい値判定ロジックの移植
   - InfluxDB書き込み機能

### Phase 3: Application Layer開発
1. **設定管理UIの構築**
   - Streamlitによる管理画面
   - 既存MariaDBスキーマとの連携
   - デバイス登録・設定機能

2. **可視化環境の構築**
   - Grafanaダッシュボードの作成
   - アラート設定とパネル構成

### Phase 4: 段階的移行
1. **パイロット運用**
   - 1台のエッジデバイスで動作確認
   - 既存Node-REDシステムとの並行稼働
   - データ整合性の検証

2. **本格運用**
   - 全エッジデバイスの順次移行
   - パフォーマンス監視と調整
   - Node-REDシステムの段階的停止

## 分散アーキテクチャの利点

### ポータビリティとスケーラビリティ

**Edge Layer（エッジデバイス層）**
- **ハードウェア抽象化**: RPi4/5やその他SBCへの対応
- **軽量実装**: リソース制約下での効率的動作
- **デバイス固有最適化**: 各ハードウェアの特性を活用

**Collection Layer（データ収集層）**
- **ハードウェア非依存**: 任意のLinux環境で動作
- **水平スケーリング**: 複数エッジデバイスからのデータ統合
- **高可用性**: 単一障害点の排除

**Application Layer（アプリケーション層）**
- **クラウド対応**: AWS/Azure/GCPでの運用可能
- **マルチテナント**: 複数サイトの統合管理
- **API連携**: 外部システムとのシームレスな統合

### 技術選定の理由

**MQTT**
- **軽量プロトコル**: IoTデバイスに最適
- **QoS保証**: データ配信の信頼性
- **Pub/Sub**: 疎結合なアーキテクチャ

**ハードウェア抽象化**
- **将来性**: 新しいSBCへの対応容易
- **テスタビリティ**: モック実装による単体テスト
- **保守性**: ハードウェア固有コードの局所化

**既存DB活用**
- **移行コスト削減**: スキーマ変更不要
- **データ継続性**: 過去データの保持
- **実績**: 現行システムでの安定稼働

## セキュリティ考慮事項

1. **認証**: StreamlitとGrafanaに認証機能を実装
2. **通信**: HTTPS/TLSでの暗号化
3. **アクセス制御**: ロールベースの権限管理
4. **監査**: 操作ログの記録

## パフォーマンス目標

- センサーポーリング: 最大100センサー/秒
- データ書き込み: 1000ポイント/秒
- UI応答時間: 1秒以内
- システム稼働率: 99.9%

## 今後の拡張性

1. **センサー追加**: プラグイン形式で容易に追加
2. **クラウド連携**: AWS/Azure IoT Hubへの接続
3. **機械学習**: 異常検知・予測機能の追加
4. **マルチサイト**: 複数拠点の統合管理

## まとめ

本分散アーキテクチャにより、以下の効果が期待できます：

### 技術的メリット
- **ハードウェア互換性**: RPi4/5やその他SBCへの柔軟な対応
- **スケーラビリティ**: 複数エッジデバイスからの統合データ収集
- **保守性**: レイヤー分離による明確な責務分担
- **テスタビリティ**: ハードウェア抽象化によるモック実装

### 運用メリット
- **分散配置**: エッジとコレクションの最適配置
- **段階的移行**: 既存システムからのリスク最小化
- **クラウド対応**: 将来的なクラウド移行の容易性
- **AI支援**: テキストベースコードによる開発効率向上

### ビジネスメリット
- **コスト削減**: 既存資産の有効活用
- **迅速な展開**: 標準化されたデプロイメント
- **将来性**: 新技術への対応力
- **保守効率**: 1人でも管理可能な構成

既存システムの良い部分（MariaDBスキーマ、センサー制御ロジック、ハードウェア資産）を活かしながら、Node-REDの複雑性とハードウェア依存性から脱却し、より現代的で拡張性の高いIoTプラットフォームへの進化を実現します。