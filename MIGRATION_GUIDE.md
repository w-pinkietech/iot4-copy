# Node-RED IoTシステム 移行ガイド

## 概要

このドキュメントは、現在のNode-REDベースのIoT導入支援キット Ver.4.1を別のサービスやアーキテクチャに移行するための包括的なガイドです。システムの段階的な移行手順、必要な資料作成、リスク管理について詳述します。

## 目次

1. [移行戦略](#移行戦略)
2. [事前調査・分析手順](#事前調査分析手順)
3. [移行準備フェーズ](#移行準備フェーズ)
4. [段階的移行手順](#段階的移行手順)
5. [代替アーキテクチャ選択肢](#代替アーキテクチャ選択肢)
6. [リスク評価と対策](#リスク評価と対策)
7. [検証・テスト手順](#検証テスト手順)
8. [運用移行手順](#運用移行手順)

---

## 移行戦略

### 移行アプローチ

| アプローチ | メリット | デメリット | 適用場面 |
|------------|----------|------------|----------|
| **Big Bang移行** | 短期間で完了、シンプル | 高リスク、ダウンタイム長 | 小規模システム、開発環境 |
| **段階的移行** | 低リスク、検証しながら進行 | 期間長い、複雑 | 本番環境、重要システム |
| **パラレル移行** | 超低リスク、比較検証可能 | コスト高、リソース要求大 | ミッションクリティカル |
| **パイロット移行** | 段階的リスク検証 | 全体工期長期化 | 新技術採用時 |

### 推奨移行戦略：**段階的移行**

1. **フェーズ1**: データ収集層の移行
2. **フェーズ2**: データ処理・保存層の移行  
3. **フェーズ3**: UI・可視化層の移行
4. **フェーズ4**: 外部連携・通知機能の移行

---

## 事前調査・分析手順

### 1. 現行システム分析

#### 1.1 システム構成の詳細把握

```bash
# 必要作業一覧
□ Node-REDフロー全体の機能分析（flows.json解析）
□ 使用ノードとその依存関係の特定
□ カスタムPythonドライバーの機能分析
□ データベーススキーマの詳細把握
□ 外部連携仕様の文書化
□ パフォーマンス要件の測定
□ セキュリティ要件の整理
```

**実行手順**:

```bash
# 1. Node-REDフロー構成分析
cd /home/kenta/pinkie/iot4-copy/.node-red
jq '.[] | select(.type=="tab") | {id: .id, label: .label}' flows.json > tabs_analysis.json

# 2. 使用ノード種別統計
jq '[.[] | select(.type != "tab" and .type != "subflow") | .type] | group_by(.) | map({type: .[0], count: length})' flows.json > node_statistics.json

# 3. データベース接続情報抽出
grep -r "mysql\|influx" flows.json > db_connections.txt

# 4. MQTT設定情報抽出
grep -r "mqtt" flows.json > mqtt_config.txt

# 5. HTTP API エンドポイント抽出
grep -r "api/v2" flows.json > api_endpoints.txt
```

#### 1.2 依存関係マッピング

**Pythonライブラリ依存関係**:
```bash
# センサードライバー依存関係調査
find .node-red/python -name "*.py" -exec grep -H "import\|from" {} \; > python_dependencies.txt

# システムライブラリ使用状況
grep -r "subprocess\|os\|sys" .node-red/python/ > system_dependencies.txt
```

**Node-REDモジュール依存関係**:
```bash
# package.json解析
jq '.dependencies' .node-red/package.json > nodered_dependencies.json

# カスタムノード使用状況
grep -r "node-red-contrib\|node-red-node" flows.json > custom_nodes.txt
```

#### 1.3 データフロー分析

**データ処理パターンの特定**:
```bash
# Function ノードのJavaScriptコード抽出
jq '.[] | select(.type=="function") | {id: .id, name: .name, func: .func}' flows.json > function_nodes.json

# Change ノード変換ルール抽出  
jq '.[] | select(.type=="change") | {id: .id, name: .name, rules: .rules}' flows.json > change_rules.json

# Switch ノード条件分岐抽出
jq '.[] | select(.type=="switch") | {id: .id, name: .name, rules: .rules}' flows.json > switch_conditions.json
```

### 2. 移行要件定義

#### 2.1 機能要件マトリックス

| 機能カテゴリ | 現行実装 | 移行必須 | 移行推奨 | 廃止可能 | 新規追加 |
|--------------|----------|----------|----------|----------|----------|
| **センサーデータ収集** | Node-RED + Python | ✓ | - | - | - |
| **I2C通信** | Python drivers | ✓ | - | - | - |
| **GPIO制御** | Node-RED GPIO | ✓ | - | - | - |
| **シリアル通信** | Node-RED Serial | ✓ | - | - | - |
| **BLE通信** | Node-RED BLE | - | ✓ | - | - |
| **データ保存** | MySQL + InfluxDB | ✓ | - | - | - |
| **リアルタイム可視化** | Node-RED Dashboard | ✓ | - | - | - |
| **MQTT通信** | Aedes broker | - | ✓ | - | - |
| **メール通知** | Node-RED Email | - | ✓ | - | - |
| **REST API** | Node-RED HTTP | ✓ | - | - | - |
| **ユーザー管理** | なし | - | - | - | ✓ |
| **ログ管理** | 基本的なみ | - | - | - | ✓ |

#### 2.2 非機能要件

```yaml
パフォーマンス:
  データ収集頻度: 1Hz以上 (現行同等)
  同時接続数: 10デバイス以上
  レスポンス時間: 1秒以内 (API)
  データ保持期間: 90日以上

可用性:
  稼働率: 99.0%以上
  復旧時間: 30分以内
  バックアップ: 日次自動

拡張性:
  センサー追加: プラグイン形式
  デバイス数: 100台まで対応
  データ量: 月間10GB対応

セキュリティ:
  ネットワーク: ローカルネット前提
  認証: Basic認証以上
  通信: HTTPS対応
```

---

## 移行準備フェーズ

### 1. 移行チーム編成

| 役割 | 責任範囲 | 必要スキル |
|------|----------|------------|
| **プロジェクトマネージャー** | 全体統括、スケジュール管理 | PM経験、IoTシステム理解 |
| **システムアーキテクト** | 移行先設計、技術選定 | アーキテクチャ設計、複数技術スタック |
| **バックエンド開発者** | データ処理、API開発 | Python/Go/Java等、DB設計 |
| **フロントエンド開発者** | UI/UX、ダッシュボード | React/Vue等、データ可視化 |
| **インフラエンジニア** | 環境構築、デプロイ | Docker/K8s、クラウド |
| **テストエンジニア** | 品質保証、性能検証 | テスト自動化、IoTテスト |
| **システム管理者** | 運用設計、移行作業 | Linux管理、データ移行 |

### 2. 環境準備

#### 2.1 開発環境構築

```bash
# 1. 現行システムのクローン環境構築
# Raspberry Pi環境の複製
sudo dd if=/dev/mmcblk0 of=backup_image.img bs=4M status=progress

# 2. 開発用環境セットアップ  
# Docker環境での現行システム再現
docker-compose -f docker-compose.dev.yml up -d

# 3. 移行先技術スタックの検証環境
# 例：Python FastAPI + React環境
mkdir migration-poc && cd migration-poc
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn sqlalchemy

# 4. データ移行検証環境
# テストデータの準備
mysqldump -h localhost -u root iotkit > test_data.sql
influx backup --org fitc --bucket iotkit ./influx_backup/
```

#### 2.2 移行ツール準備

```bash
# データ移行スクリプト準備
mkdir migration-tools && cd migration-tools

# 1. 設定データ移行スクリプト
cat > migrate_config.py << 'EOF'
#!/usr/bin/env python3
"""
Node-RED flows.json から設定データを抽出し、
新システム用設定フォーマットに変換するスクリプト
"""
import json
import yaml

def extract_device_configs(flows_file):
    # flows.json からデバイス設定を抽出
    pass

def convert_to_new_format(config_data):
    # 新システム用フォーマットに変換
    pass
EOF

# 2. データスキーマ変換スクリプト
cat > migrate_schema.py << 'EOF'
#!/usr/bin/env python3
"""
MariaDB/InfluxDB スキーマを新システム用に変換
"""
EOF

# 3. APIエンドポイント変換マッピング
cat > api_mapping.yaml << 'EOF'
# Node-RED HTTP endpoints → 新API endpoint マッピング
endpoints:
  - old: "GET /api/v2/device"
    new: "GET /v1/devices"
    converter: "device_list_converter"
  - old: "POST /api/v2/device/:deviceId/sensor/value"
    new: "POST /v1/devices/{device_id}/sensors/data"
    converter: "sensor_data_converter"
EOF
```

---

## 段階的移行手順

### フェーズ1: データ収集層移行

#### 目標
- センサードライバーの移行
- ハードウェアインターフェース層の再実装
- データ収集の動作確認

#### 作業内容

**1.1 センサードライバー移行**

```bash
# 現行Pythonドライバーの分析
cd .node-red/python
for driver in *.py; do
    echo "=== $driver ==="
    python -m py_compile $driver
    python -c "import ast; print(ast.dump(ast.parse(open('$driver').read())))" > ${driver}.ast
done

# 新システム用ドライバー実装
mkdir -p ../migration-target/sensors/
# I2Cセンサードライバーのリファクタリング
```

**ドライバー移行チェックリスト**:
```bash
□ vl53l1x.py (距離センサー) → sensors/distance.py
□ mcp3427.py (ADC) → sensors/adc.py  
□ mcp9600.py (熱電対) → sensors/thermocouple.py
□ lis2duxs12.py (加速度) → sensors/accelerometer.py
□ opt3001.py (照度) → sensors/light.py
□ sdp810.py (差圧) → sensors/pressure.py
□ lombscargle.py (信号処理) → utils/signal_processing.py
```

**1.2 通信層実装**

```python
# 例：新システム用I2C通信抽象化レイヤー
class I2CInterface:
    def __init__(self, bus_number=1):
        self.bus = smbus2.SMBus(bus_number)
    
    def read_sensor(self, address, register, length=1):
        return self.bus.read_i2c_block_data(address, register, length)
    
    def write_sensor(self, address, register, data):
        return self.bus.write_i2c_block_data(address, register, data)

# センサー基底クラス
class BaseSensor:
    def __init__(self, interface, address):
        self.interface = interface
        self.address = address
    
    def read(self):
        raise NotImplementedError
    
    def configure(self, **kwargs):
        raise NotImplementedError
```

**1.3 動作確認**

```bash
# センサー個別テスト
python -m pytest tests/sensors/test_distance.py -v
python -m pytest tests/sensors/test_adc.py -v

# 統合テスト
python -m pytest tests/integration/test_sensor_collection.py -v

# パフォーマンステスト
python tests/performance/sensor_throughput_test.py
```

### フェーズ2: データ処理・保存層移行

#### 目標
- データベース設計の最適化
- データ処理ロジックの移行
- データ永続化機能の実装

#### 作業内容

**2.1 データベース設計**

```sql
-- 新システム用データベーススキーマ設計
-- PostgreSQL/MySQL対応

-- デバイス管理テーブル
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- センサー定義テーブル  
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    device_id INTEGER REFERENCES devices(id),
    sensor_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(20),
    config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- センサーデータテーブル（時系列）
CREATE TABLE sensor_data (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensors(id),
    timestamp TIMESTAMP NOT NULL,
    value NUMERIC(10,4),
    metadata JSONB,
    INDEX idx_sensor_timestamp (sensor_id, timestamp)
);
```

**2.2 データ処理API実装**

```python
# FastAPI による REST API実装例
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from .models import Device, Sensor, SensorData
from .database import get_db

app = FastAPI(title="IoT Data API", version="2.0.0")

@app.get("/v1/devices")
async def list_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return {"devices": devices}

@app.post("/v1/devices/{device_id}/sensors/data")
async def store_sensor_data(
    device_id: int, 
    data: SensorDataSchema,
    db: Session = Depends(get_db)
):
    # データ検証
    sensor = db.query(Sensor).filter(
        Sensor.device_id == device_id,
        Sensor.id == data.sensor_id
    ).first()
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    # データ保存
    sensor_data = SensorData(
        sensor_id=data.sensor_id,
        timestamp=data.timestamp,
        value=data.value,
        metadata=data.metadata
    )
    db.add(sensor_data)
    db.commit()
    
    return {"status": "success"}
```

**2.3 データ移行スクリプト**

```python
#!/usr/bin/env python3
"""
Node-RED系データベースから新システムへのデータ移行
"""
import asyncio
from sqlalchemy import create_engine
from influxdb_client import InfluxDBClient

async def migrate_config_data():
    """MariaDB 設定データの移行"""
    old_engine = create_engine("mysql://root@localhost/iotkit")
    new_engine = create_engine("postgresql://user:pass@localhost/iotkit_v2")
    
    # devices テーブル移行
    with old_engine.connect() as old_conn:
        devices = old_conn.execute("SELECT * FROM devices").fetchall()
        
    with new_engine.connect() as new_conn:
        for device in devices:
            # データ変換処理
            new_conn.execute(
                "INSERT INTO devices (name, device_type, config) VALUES (%s, %s, %s)",
                (device.name, device.type, json.dumps(device.config))
            )

async def migrate_timeseries_data():
    """InfluxDB 時系列データの移行"""
    old_client = InfluxDBClient(url="http://localhost:8086", token="old-token")
    new_client = InfluxDBClient(url="http://localhost:8087", token="new-token")
    
    # バッチでデータ移行
    query = '''
    from(bucket:"iotkit")
    |> range(start: -90d)
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    results = old_client.query_api().query(query)
    
    for table in results:
        for record in table.records:
            # 新フォーマットに変換してバッチ挿入
            pass

if __name__ == "__main__":
    asyncio.run(migrate_config_data())
    asyncio.run(migrate_timeseries_data())
```

### フェーズ3: UI・可視化層移行

#### 目標  
- Node-RED Dashboardの機能をWebアプリに移行
- リアルタイム更新機能の実装
- ユーザビリティの向上

#### 作業内容

**3.1 フロントエンド設計**

```javascript
// React + TypeScript構成例
// src/types/sensor.ts
export interface SensorData {
  id: number;
  sensorId: number;
  timestamp: Date;
  value: number;
  unit: string;
}

export interface Device {
  id: number;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'error';
  sensors: Sensor[];
}

// src/components/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { useWebSocket } from '../hooks/useWebSocket';

const Dashboard: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const { lastMessage } = useWebSocket('ws://localhost:8000/ws');

  useEffect(() => {
    if (lastMessage) {
      const newData = JSON.parse(lastMessage.data);
      setSensorData(prev => [...prev.slice(-100), newData]);
    }
  }, [lastMessage]);

  return (
    <div className="dashboard">
      <h1>IoT ダッシュボード</h1>
      <LineChart width={800} height={400} data={sensorData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>
    </div>
  );
};
```

**3.2 リアルタイム通信実装**

```python
# WebSocket実装 (FastAPI)
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # センサーデータの更新を待機・配信
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**3.3 UI コンポーネント移行マッピング**

| Node-RED Dashboard | 新UI実装 | ライブラリ |
|-------------------|----------|------------|
| ui_chart | LineChart/AreaChart | Recharts/Chart.js |
| ui_gauge | CircularProgress | Material-UI |
| ui_text | Typography | Material-UI |
| ui_button | Button | Material-UI |
| ui_switch | Switch | Material-UI |
| ui_slider | Slider | Material-UI |
| ui_form | Form | React Hook Form |
| ui_table | DataGrid | Material-UI |

### フェーズ4: 外部連携・通知機能移行

#### 目標
- MQTT通信機能の移行
- メール通知機能の移行  
- 外部API連携の実装

#### 作業内容

**4.1 MQTT通信実装**

```python
# MQTT Publisher/Subscriber実装
import asyncio
from aiomqtt import Client, MqttError

class MQTTHandler:
    def __init__(self, broker_host="localhost", broker_port=1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = None

    async def connect(self):
        self.client = Client(self.broker_host, self.broker_port)
        await self.client.__aenter__()

    async def publish_sensor_data(self, device_id: str, sensor_data: dict):
        topic = f"sensors/{device_id}/data"
        payload = json.dumps(sensor_data)
        await self.client.publish(topic, payload)

    async def subscribe_commands(self, callback):
        await self.client.subscribe("commands/+/+")
        async for message in self.client.messages:
            await callback(message.topic, message.payload)
```

**4.2 通知システム実装**

```python
# 統合通知システム
from abc import ABC, abstractmethod
from typing import List

class NotificationChannel(ABC):
    @abstractmethod
    async def send(self, message: str, recipients: List[str]):
        pass

class EmailNotification(NotificationChannel):
    def __init__(self, smtp_config):
        self.smtp_config = smtp_config
    
    async def send(self, message: str, recipients: List[str]):
        # SMTPサーバー経由でメール送信
        pass

class MQTTNotification(NotificationChannel):
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    
    async def send(self, message: str, recipients: List[str]):
        # MQTTトピックに通知発行
        await self.mqtt_client.publish("notifications/alert", message)

class NotificationService:
    def __init__(self):
        self.channels: List[NotificationChannel] = []
    
    def add_channel(self, channel: NotificationChannel):
        self.channels.append(channel)
    
    async def send_alert(self, sensor_id: int, value: float, threshold: float):
        message = f"センサー {sensor_id} が閾値 {threshold} を超過しました: {value}"
        
        for channel in self.channels:
            await channel.send(message, ["admin@example.com"])
```

---

## 代替アーキテクチャ選択肢

### 1. マイクロサービス アーキテクチャ

#### 構成
```mermaid
graph TB
    subgraph "エッジデバイス"
        SENSOR[センサー]
        GATEWAY[ゲートウェイ<br/>Python/Go]
    end
    
    subgraph "クラウド/オンプレミス"
        subgraph "APIゲートウェイ"
            NGINX[Nginx]
        end
        
        subgraph "マイクロサービス"
            DATA_SVC[データ収集サービス<br/>Python/FastAPI]
            DEVICE_SVC[デバイス管理サービス<br/>Go/Gin]
            ALERT_SVC[アラートサービス<br/>Node.js/Express]
            AUTH_SVC[認証サービス<br/>Python/Django]
        end
        
        subgraph "データストア"
            POSTGRES[(PostgreSQL)]
            TIMESCALE[(TimescaleDB)]
            REDIS[(Redis)]
        end
        
        subgraph "フロントエンド"
            REACT[React SPA]
            MOBILE[React Native]
        end
        
        subgraph "外部連携"
            MQTT_BROKER[MQTT Broker]
            EMAIL[Email Service]
        end
    end
    
    SENSOR --> GATEWAY
    GATEWAY --> NGINX
    NGINX --> DATA_SVC
    NGINX --> DEVICE_SVC
    NGINX --> ALERT_SVC
    NGINX --> AUTH_SVC
    
    DATA_SVC --> TIMESCALE
    DEVICE_SVC --> POSTGRES
    ALERT_SVC --> REDIS
    AUTH_SVC --> POSTGRES
    
    REACT --> NGINX
    MOBILE --> NGINX
    
    ALERT_SVC --> MQTT_BROKER
    ALERT_SVC --> EMAIL
```

**技術スタック**:
```yaml
フロントエンド:
  - React 18 + TypeScript
  - Material-UI / Ant Design
  - Recharts / Chart.js
  - WebSocket クライアント

バックエンド:
  - Python FastAPI (データ処理)
  - Go Gin (デバイス管理)  
  - Node.js Express (リアルタイム通信)
  - Django (認証・管理)

データベース:
  - PostgreSQL (リレーショナルデータ)
  - TimescaleDB (時系列データ)
  - Redis (キャッシュ・セッション)

メッセージング:
  - Apache Kafka (データストリーミング)
  - Eclipse Mosquitto (MQTT)
  - RabbitMQ (タスクキュー)

インフラ:
  - Docker + Kubernetes
  - Nginx (ロードバランサー)
  - Grafana (監視・可視化)
  - Prometheus (メトリクス)
```

**メリット**:
- 高い拡張性とメンテナンス性
- 技術スタックの柔軟性
- 障害の局所化
- チーム分割開発可能

**デメリット**:  
- 複雑性の増加
- 運用コストの増大
- ネットワーク通信オーバーヘッド

### 2. サーバーレス アーキテクチャ

#### 構成（AWS Lambda例）
```mermaid
graph TB
    subgraph "エッジ"
        IOT_DEVICE[IoTデバイス]
        IOT_CORE[AWS IoT Core]
    end
    
    subgraph "データ処理"
        LAMBDA1[Lambda<br/>データ処理]
        LAMBDA2[Lambda<br/>アラート処理]  
        LAMBDA3[Lambda<br/>API]
    end
    
    subgraph "データストレージ"
        TIMESTREAM[(Amazon Timestream)]
        DYNAMODB[(DynamoDB)]
        S3[(S3)]
    end
    
    subgraph "フロントエンド"
        CLOUDFRONT[CloudFront]
        S3_WEB[S3 Static Website]
        REACT_APP[React SPA]
    end
    
    subgraph "通知・連携"
        SNS[Amazon SNS]
        SQS[Amazon SQS]  
        SES[Amazon SES]
    end
    
    IOT_DEVICE --> IOT_CORE
    IOT_CORE --> LAMBDA1
    LAMBDA1 --> TIMESTREAM
    LAMBDA1 --> DYNAMODB
    LAMBDA1 --> LAMBDA2
    LAMBDA2 --> SNS
    SNS --> SES
    
    CLOUDFRONT --> S3_WEB
    S3_WEB --> REACT_APP
    REACT_APP --> LAMBDA3
    LAMBDA3 --> TIMESTREAM
    LAMBDA3 --> DYNAMODB
```

**技術スタック**:
```yaml
クラウド (AWS):
  - Lambda (サーバーレス関数)
  - IoT Core (デバイス接続)
  - Timestream (時系列DB)
  - DynamoDB (NoSQL)
  - API Gateway (API管理)
  - CloudFront (CDN)
  - SES (メール送信)
  - SNS (通知)

開発:
  - Python/Node.js (Lambda関数)
  - React (フロントエンド)
  - Serverless Framework
  - AWS CDK
```

**メリット**:
- 自動スケーリング
- 運用コスト最小化
- 高可用性
- 使用量ベース課金

**デメリット**:
- ベンダーロックイン
- コールドスタート問題
- 複雑なローカル開発
- 制約の多い実行環境

### 3. エッジコンピューティング アーキテクチャ

#### 構成
```mermaid
graph TB
    subgraph "エッジノード"
        EDGE1[エッジノード1<br/>Docker Swarm]
        EDGE2[エッジノード2<br/>K3s]
        EDGE3[エッジノード3<br/>Docker Compose]
    end
    
    subgraph "エッジアプリケーション"
        DATA_COLLECTOR[データ収集]
        LOCAL_DB[(SQLite/InfluxDB)]
        LOCAL_UI[ローカルUI]
        SYNC_AGENT[同期エージェント]
    end
    
    subgraph "クラウド"
        CLOUD_API[クラウドAPI]
        CLOUD_DB[(クラウドDB)]
        ANALYTICS[分析プラットフォーム]
        DASHBOARD[統合ダッシュボード]
    end
    
    EDGE1 --> DATA_COLLECTOR
    EDGE2 --> DATA_COLLECTOR  
    EDGE3 --> DATA_COLLECTOR
    
    DATA_COLLECTOR --> LOCAL_DB
    LOCAL_DB --> LOCAL_UI
    LOCAL_DB --> SYNC_AGENT
    
    SYNC_AGENT --> CLOUD_API
    CLOUD_API --> CLOUD_DB
    CLOUD_DB --> ANALYTICS
    ANALYTICS --> DASHBOARD
```

**技術スタック**:
```yaml
エッジ:
  - K3s / Docker Swarm
  - Python/Go (軽量アプリ)
  - SQLite / InfluxDB Lite
  - MQTT / HTTP
  - Progressive Web App

クラウド:
  - Kubernetes
  -時系列データベース
  - 機械学習プラットフォーム
  - BI/Analytics ツール
```

**メリット**:
- 低レイテンシ
- オフライン対応
- 帯域幅節約
- プライバシー保護

**デメリット**:
- エッジデバイス管理の複雑さ
- データ一貫性の課題
- セキュリティ対策の分散化

### 4. イベント駆動アーキテクチャ

#### 構成
```mermaid
graph TB
    subgraph "イベントソース"
        SENSORS[センサー群]
        DEVICES[デバイス群]
        USERS[ユーザー操作]
    end
    
    subgraph "イベントストリーミング"
        KAFKA[Apache Kafka]
        SCHEMA_REG[Schema Registry]
        KAFKA_CONNECT[Kafka Connect]
    end
    
    subgraph "イベント処理"
        STREAM_PROC[Stream Processing<br/>Kafka Streams/Flink]
        CEP[Complex Event Processing]
        ML_PIPELINE[ML Pipeline]
    end
    
    subgraph "データストア"
        EVENT_STORE[(Event Store)]
        OLTP[(OLTP DB)]
        OLAP[(OLAP DB)]
        CACHE[(Cache)]
    end
    
    subgraph "消費者"
        ALERTING[アラートサービス]
        DASHBOARD[ダッシュボード]
        ANALYTICS[分析サービス]
        EXTERNAL[外部システム]
    end
    
    SENSORS --> KAFKA
    DEVICES --> KAFKA
    USERS --> KAFKA
    
    KAFKA --> STREAM_PROC
    KAFKA --> CEP
    KAFKA --> ML_PIPELINE
    
    STREAM_PROC --> EVENT_STORE
    CEP --> OLTP
    ML_PIPELINE --> OLAP
    
    KAFKA --> ALERTING
    KAFKA --> DASHBOARD
    KAFKA --> ANALYTICS
    KAFKA --> EXTERNAL
```

**技術スタック**:
```yaml
イベントストリーミング:
  - Apache Kafka
  - Apache Pulsar
  - Amazon Kinesis

ストリーム処理:
  - Apache Flink
  - Kafka Streams  
  - Apache Storm

データストア:
  - Apache Cassandra
  - ClickHouse
  - Amazon DynamoDB

アプリケーション:
  - Spring Boot (Java)
  - Akka (Scala)
  - Node.js + TypeScript
```

**メリット**:
- 高いスケーラビリティ
- 疎結合アーキテクチャ
- リアルタイム処理
- 監査ログの完全性

**デメリット**:
- 最終一貫性モデル
- デバッグの困難さ
- 複雑なエラーハンドリング

---

## リスク評価と対策

### 1. 技術リスク

| リスク項目 | 影響度 | 確率 | 対策 |
|------------|--------|------|------|
| **ハードウェア互換性** | 高 | 中 | 事前検証環境での十分なテスト |
| **パフォーマンス劣化** | 高 | 中 | 負荷テスト、段階的移行 |
| **データ消失** | 高 | 低 | バックアップ戦略、ロールバック計画 |
| **セキュリティ脆弱性** | 中 | 中 | セキュリティ監査、ペネトレーションテスト |
| **依存関係問題** | 中 | 高 | 依存関係管理、コンテナ化 |

### 2. 運用リスク

| リスク項目 | 影響度 | 確率 | 対策 |
|------------|--------|------|------|
| **スキル不足** | 高 | 中 | 事前研修、外部サポート |
| **運用手順の未整備** | 中 | 中 | 運用手順書作成、自動化 |
| **監視・ログ不備** | 中 | 高 | 監視システム構築、アラート設定 |
| **バックアップ戦略不備** | 高 | 中 | 定期バックアップ、復旧テスト |

### 3. プロジェクトリスク

| リスク項目 | 影響度 | 確率 | 対策 |
|------------|--------|------|------|
| **スケジュール遅延** | 中 | 高 | バッファ確保、並行作業計画 |
| **要件変更** | 中 | 中 | アジャイル開発、変更管理プロセス |
| **リソース不足** | 高 | 中 | 事前リソース計画、外部委託検討 |
| **ステークホルダー合意** | 中 | 中 | 定期報告、デモンストレーション |

---

## 検証・テスト手順

### 1. 単体テスト

#### センサードライバーテスト
```python
# tests/sensors/test_distance_sensor.py
import pytest
from unittest.mock import Mock, patch
from sensors.distance import VL53L1XSensor

class TestVL53L1XSensor:
    def setup_method(self):
        self.mock_i2c = Mock()
        self.sensor = VL53L1XSensor(self.mock_i2c, address=0x29)
    
    def test_read_distance(self):
        # モックデータ設定
        self.mock_i2c.read_i2c_block_data.return_value = [0x00, 0x64]  # 100mm
        
        # テスト実行
        distance = self.sensor.read()
        
        # 検証
        assert distance == 100
        self.mock_i2c.read_i2c_block_data.assert_called_once()
    
    def test_sensor_error_handling(self):
        # I2Cエラーのシミュレーション
        self.mock_i2c.read_i2c_block_data.side_effect = OSError("I2C error")
        
        # エラーハンドリングの検証
        with pytest.raises(SensorError):
            self.sensor.read()
```

#### API エンドポイントテスト
```python  
# tests/api/test_devices.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestDeviceAPI:
    def test_get_devices(self):
        response = client.get("/v1/devices")
        assert response.status_code == 200
        assert "devices" in response.json()
    
    def test_create_device(self):
        device_data = {
            "name": "テストセンサー",
            "device_type": "temperature",
            "config": {"sampling_rate": 60}
        }
        response = client.post("/v1/devices", json=device_data)
        assert response.status_code == 201
        assert response.json()["name"] == "テストセンサー"
```

### 2. 統合テスト

#### エンドツーエンドデータフローテスト
```python
# tests/integration/test_data_flow.py
import asyncio
import pytest
from sensors.mock import MockSensorDevice
from api.client import APIClient
from database import DatabaseConnection

@pytest.mark.asyncio
class TestDataFlow:
    async def test_sensor_to_database_flow(self):
        # 1. モックセンサーデバイス作成
        mock_sensor = MockSensorDevice(device_id="test_001")
        
        # 2. APIクライアント初期化
        api_client = APIClient(base_url="http://localhost:8000")
        
        # 3. データベース接続
        db = DatabaseConnection()
        
        # 4. データ送信
        sensor_data = await mock_sensor.read()
        response = await api_client.post_sensor_data("test_001", sensor_data)
        assert response.status_code == 200
        
        # 5. データベース確認
        await asyncio.sleep(1)  # 非同期処理完了待ち
        stored_data = await db.get_latest_sensor_data("test_001")
        assert stored_data.value == sensor_data.value
```

### 3. パフォーマンステスト

#### 負荷テストスクリプト
```python
# tests/performance/load_test.py
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def send_sensor_data(session, device_id, data):
    async with session.post(
        f"http://localhost:8000/v1/devices/{device_id}/sensors/data",
        json=data
    ) as response:
        return response.status

async def load_test():
    # 100デバイス、1000リクエスト/秒をシミュレーション
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for device_id in range(100):
            for _ in range(10):  # 各デバイスから10req/sec
                data = {
                    "sensor_id": 1,
                    "timestamp": time.time(),
                    "value": 25.5
                }
                task = send_sensor_data(session, f"device_{device_id}", data)
                tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # 結果分析
        success_count = sum(1 for status in results if status == 200)
        total_requests = len(results)
        duration = end_time - start_time
        
        print(f"成功率: {success_count/total_requests*100:.2f}%")
        print(f"スループット: {total_requests/duration:.2f} req/sec")
        print(f"平均レスポンス時間: {duration/total_requests*1000:.2f} ms")

if __name__ == "__main__":
    asyncio.run(load_test())
```

### 4. ハードウェア検証テスト

#### センサー精度テスト
```bash
#!/bin/bash
# hardware_validation.sh

echo "=== センサー精度検証テスト ==="

# 1. 距離センサー精度テスト
echo "距離センサー精度テスト開始..."
python tests/hardware/distance_accuracy_test.py

# 2. 温度センサー校正テスト  
echo "温度センサー校正テスト開始..."
python tests/hardware/temperature_calibration_test.py

# 3. ADC精度テスト
echo "ADC精度テスト開始..."
python tests/hardware/adc_precision_test.py

# 4. GPIO動作テスト
echo "GPIO動作テスト開始..."
python tests/hardware/gpio_functionality_test.py

echo "=== ハードウェア検証完了 ==="
```

---

## 運用移行手順

### 1. 移行前チェックリスト

#### システム準備
```bash
□ 移行先環境の構築完了
□ データベーススキーマ作成完了
□ アプリケーションデプロイ完了
□ ネットワーク設定確認
□ セキュリティ設定確認
□ 監視システム設定完了
□ バックアップシステム稼働確認
□ ログ収集システム稼働確認
```

#### データ移行準備
```bash
□ 現行システムの完全バックアップ作成
□ データ移行スクリプトの動作確認
□ テストデータでの移行テスト完了
□ データ整合性検証ツール準備
□ ロールバック手順の確認
□ データ移行時間の見積もり完了
```

#### チーム準備
```bash
□ 移行チームの役割分担確認
□ 緊急連絡体制の構築
□ 移行手順書の最終確認
□ 移行当日のタイムライン作成
□ エスカレーション手順の確認
```

### 2. 移行実行手順

#### 移行当日作業フロー
```mermaid
gantt
    title 移行当日スケジュール
    dateFormat  HH:mm
    axisFormat  %H:%M
    
    section 準備作業
    最終バックアップ作成     :done, backup, 18:00, 19:00
    現行システム停止確認     :done, stop, 19:00, 19:30
    移行チーム召集           :done, team, 19:30, 20:00
    
    section データ移行
    設定データ移行           :active, config, 20:00, 21:00
    時系列データ移行         :crit, timeseries, 21:00, 23:00
    データ整合性確認         :verify, 23:00, 23:30
    
    section システム起動
    新システム起動           :startup, 23:30, 00:30
    疎通テスト実行           :test, 00:30, 01:00
    監視システム確認         :monitor, 01:00, 01:30
    
    section 切り替え
    DNSカットオーバー       :cutover, 01:30, 02:00
    動作確認                :final, 02:00, 03:00
```

#### 詳細作業手順

**フェーズ1: 移行前最終確認 (18:00-20:00)**
```bash
# 1. 最終バックアップ作成
sudo systemctl stop node-red
mysqldump -h localhost -u root iotkit > final_backup_$(date +%Y%m%d_%H%M).sql
influx backup --org fitc --bucket iotkit ./final_influx_backup_$(date +%Y%m%d_%H%M)/

# 2. 移行先環境最終確認  
curl -f http://new-system:8000/health || exit 1
docker-compose -f docker-compose.prod.yml ps

# 3. 移行チェックリスト実行
python migration_scripts/pre_migration_check.py
```

**フェーズ2: データ移行実行 (20:00-23:30)**
```bash
# 1. 設定データ移行
python migration_scripts/migrate_config_data.py \
    --source mysql://root@localhost/iotkit \
    --target postgresql://user:pass@new-system/iotkit_v2 \
    --log-level INFO

# 2. 時系列データ移行（並列実行）
python migration_scripts/migrate_timeseries_data.py \
    --source http://localhost:8086 \
    --target http://new-system:8087 \
    --parallel 4 \
    --batch-size 1000

# 3. データ整合性確認
python migration_scripts/verify_data_integrity.py \
    --source-config config/old_system.yaml \
    --target-config config/new_system.yaml
```

**フェーズ3: システム切り替え (23:30-03:00)**
```bash
# 1. 新システム本格起動
docker-compose -f docker-compose.prod.yml up -d
kubectl apply -f k8s/production/

# 2. ヘルスチェック
curl -f http://new-system:8000/health
curl -f http://new-system:8000/v1/devices

# 3. エンドツーエンドテスト
python tests/e2e/production_smoke_test.py

# 4. DNSカットオーバー
# Route53 / CloudFlare 等でDNSレコード更新
aws route53 change-resource-record-sets \
    --hosted-zone-id Z1D633PJN98FT9 \
    --change-batch file://dns_change.json

# 5. 最終動作確認
python tests/e2e/post_migration_test.py
```

### 3. ロールバック手順

#### 緊急ロールバック（15分以内）
```bash
#!/bin/bash
# emergency_rollback.sh

echo "=== 緊急ロールバック開始 ==="

# 1. DNS設定を旧システムに戻す
aws route53 change-resource-record-sets \
    --hosted-zone-id Z1D633PJN98FT9 \
    --change-batch file://dns_rollback.json

# 2. 旧システムサービス再起動
sudo systemctl start node-red
docker-compose -f docker/docker-compose.yml up -d

# 3. 動作確認
curl -f http://old-system:1880/ui/ || exit 1

echo "=== ロールバック完了 ==="
```

#### データロールバック（1時間以内）
```bash
#!/bin/bash
# data_rollback.sh

echo "=== データロールバック開始 ==="

# 1. 新システム停止
docker-compose -f docker-compose.prod.yml down

# 2. データベース復元
mysql -h localhost -u root iotkit < final_backup_$(date +%Y%m%d)_*.sql
influx restore --org fitc --bucket iotkit ./final_influx_backup_$(date +%Y%m%d)_*/

# 3. 旧システム完全復旧
sudo systemctl start node-red
docker-compose -f docker/docker-compose.yml up -d

echo "=== データロールバック完了 ==="
```

### 4. 移行後作業

#### 移行完了チェックリスト
```bash
□ 全センサーからのデータ受信確認
□ ダッシュボード表示動作確認
□ アラート機能動作確認
□ API エンドポイント動作確認
□ パフォーマンス指標確認
□ エラーログ確認
□ 監視アラート設定確認
□ バックアップシステム動作確認
□ 外部連携機能確認
□ ユーザーアクセス確認
```

#### 移行後監視（1週間）
```bash
# 毎日実行する監視スクリプト
#!/bin/bash
# post_migration_monitoring.sh

# システムリソース確認
echo "=== システムリソース確認 ==="
docker stats --no-stream
df -h
free -h

# アプリケーション健全性確認
echo "=== アプリケーション確認 ==="
curl -f http://localhost:8000/health
python scripts/check_data_flow.py

# エラーログ確認
echo "=== エラーログ確認 ==="
tail -n 100 /var/log/iotkit/error.log | grep ERROR

# パフォーマンス確認
echo "=== パフォーマンス確認 ==="
python scripts/performance_check.py
```

#### 最適化作業
```bash
# 移行後1週間以降に実行
□ パフォーマンスチューニング
□ データベースインデックス最適化
□ 不要データの削除
□ キャッシュ設定調整
□ 監視閾値調整
□ バックアップ戦略見直し
□ セキュリティ設定強化
□ ドキュメント更新
```

---

## まとめ

このマイグレーションガイドは、Node-REDベースのIoTシステムを別のアーキテクチャに移行するための包括的な手順書です。

### 重要なポイント

1. **段階的アプローチ**: リスクを最小化するため、システムを4つのフェーズに分けて段階的に移行
2. **十分な事前準備**: 移行前の詳細な分析と検証により、想定外のトラブルを防止
3. **ロールバック戦略**: 問題発生時の迅速な復旧手順を事前に準備
4. **継続的監視**: 移行後の安定稼働を確保するための監視体制構築

### 成功の鍵

- **チーム連携**: 開発・インフラ・運用チーム間の密接な連携
- **リスク管理**: 各フェーズでのリスク評価と対策実施
- **品質保証**: 十分なテストによる品質確保
- **ユーザーサポート**: 移行による影響の最小化とユーザーサポート

このガイドに従って移行を実施することで、現行システムの機能を維持しながら、より拡張性と保守性に優れた新システムへの安全な移行が可能になります。