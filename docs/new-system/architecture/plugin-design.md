# プラグイン設計アーキテクチャ

本文書は、IoTシステム疎結合化プロジェクトにおけるプラグインアーキテクチャの設計原則と実装例をまとめたものです。

## 1. SOLID原則の適用例

### 1.1 単一責任の原則（SRP）

**悪い例（複数の責任）:**
```python
class BravePIHandler:
    def __init__(self):
        self.uart = serial.Serial('/dev/ttyAMA0', 38400)
        self.db = sqlite3.connect('sensors.db')
        self.mqtt_client = paho.mqtt.Client()
    
    def process_data(self):
        # 1. シリアル通信（ハードウェア制御）
        raw_data = self.uart.read(1024)
        
        # 2. プロトコル解析（ビジネスロジック）
        if raw_data[0] == 0x10 and raw_data[1] == 0x00:
            sensor_type = raw_data[16]
            value = struct.unpack('>f', raw_data[17:21])[0]
        
        # 3. データベース保存（永続化）
        self.db.execute("INSERT INTO sensors VALUES (?, ?)", (sensor_type, value))
        
        # 4. MQTT送信（通信）
        self.mqtt_client.publish('sensors/data', json.dumps({'value': value}))
        
        # 5. ログ出力（ロギング）
        print(f"Processed: {value}")
```

**良い例（責任の分離）:**
```python
# 通信層の責任のみ
class SerialReader:
    def __init__(self, port: str, baudrate: int):
        self.uart = serial.Serial(port, baudrate)
    
    def read_raw_data(self) -> bytes:
        return self.uart.read(1024)

# プロトコル解析の責任のみ
class BravePIProtocol:
    def parse(self, raw_data: bytes) -> dict:
        if raw_data[0] == 0x10 and raw_data[1] == 0x00:
            return {
                'sensor_type': raw_data[16],
                'value': struct.unpack('>f', raw_data[17:21])[0]
            }
        raise ValueError("Invalid protocol")

# データ配信の責任のみ
class DataPublisher:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    
    def publish(self, topic: str, data: dict):
        self.mqtt_client.publish(topic, json.dumps(data))
```

### 1.2 開放閉鎖の原則（OCP）

**良い例（拡張に開いて、修正に閉じている）:**
```python
from abc import ABC, abstractmethod

# プロトコルの抽象基底クラス
class Protocol(ABC):
    @abstractmethod
    def parse(self, raw_data: bytes) -> dict:
        pass

# BravePI実装
class BravePIProtocol(Protocol):
    def parse(self, raw_data: bytes) -> dict:
        # BravePI固有の解析ロジック
        return {'type': 'bravepi', 'data': parsed_data}

# 新しいプロトコルの追加（既存コードの修正不要）
class ModbusProtocol(Protocol):
    def parse(self, raw_data: bytes) -> dict:
        # Modbus固有の解析ロジック
        return {'type': 'modbus', 'data': parsed_data}

# プロトコルを使用するクラス（変更不要）
class ProtocolProcessor:
    def __init__(self, protocol: Protocol):
        self.protocol = protocol
    
    def process(self, raw_data: bytes) -> dict:
        return self.protocol.parse(raw_data)
```

### 1.3 依存性逆転の原則（DIP）

**良い例（抽象に依存）:**
```python
from abc import ABC, abstractmethod

# 抽象インターフェース
class DataStore(ABC):
    @abstractmethod
    def save(self, data: dict) -> None:
        pass

class MessageBroker(ABC):
    @abstractmethod
    def publish(self, topic: str, data: dict) -> None:
        pass

# 高レベルモジュール（抽象に依存）
class DataProcessor:
    def __init__(self, store: DataStore, broker: MessageBroker):
        self.store = store
        self.broker = broker
    
    def process(self, data: dict):
        # ビジネスロジック
        processed = self.transform(data)
        self.store.save(processed)
        self.broker.publish('processed', processed)
    
    def transform(self, data: dict) -> dict:
        # データ変換ロジック
        return data

# 低レベルモジュール（抽象を実装）
class SQLiteStore(DataStore):
    def save(self, data: dict) -> None:
        # SQLite固有の実装
        pass

class MQTTBroker(MessageBroker):
    def publish(self, topic: str, data: dict) -> None:
        # MQTT固有の実装
        pass
```

## 2. プラグインインターフェース定義

### 2.1 基本インターフェース

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SensorData:
    """統一センサーデータ形式"""
    device_id: str
    sensor_type: str
    value: Any
    unit: str
    timestamp: datetime
    quality: str = "good"  # good, bad, uncertain
    metadata: Dict[str, Any] = None

class ProtocolPlugin(ABC):
    """プロトコルプラグインの基底クラス"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """プラグインの初期化"""
        pass
    
    @abstractmethod
    def process(self, raw_data: bytes, metadata: Dict[str, Any]) -> SensorData:
        """生データから統一形式への変換"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """プラグイン情報の取得"""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """プラグインの健全性チェック"""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """プラグインの終了処理"""
        pass
```

### 2.2 デバイスドライバインターフェース

```python
class DeviceDriver(ABC):
    """ハードウェア通信ドライバの基底クラス"""
    
    @abstractmethod
    def connect(self) -> bool:
        """デバイスへの接続"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """デバイスからの切断"""
        pass
    
    @abstractmethod
    def read(self, timeout: float = 1.0) -> bytes:
        """生データの読み取り"""
        pass
    
    @abstractmethod
    def write(self, data: bytes) -> bool:
        """データの書き込み"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """接続状態の確認"""
        pass
```

## 3. ベンダー別プラグイン実装例

### 3.1 BravePI Protocol Plugin

```python
import struct
from datetime import datetime
from typing import Dict, Any

class BravePIProtocolPlugin(ProtocolPlugin):
    """BravePI専用プロトコルプラグイン"""
    
    def __init__(self):
        self.sensor_type_map = {
            0x101: ("contact_input", "binary"),
            0x105: ("temperature", "celsius"),
            0x106: ("humidity", "percent"),
            0x111: ("illuminance", "lux"),
            0x109: ("analog_input", "volt"),
        }
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """初期化処理"""
        self.device_prefix = config.get("device_prefix", "bravepi")
        return True
    
    def process(self, raw_data: bytes, metadata: Dict[str, Any]) -> SensorData:
        """BravePIバイナリプロトコルの解析"""
        # フレーム検証
        if len(raw_data) < 21:
            raise ValueError("Invalid frame length")
        
        protocol_byte = raw_data[0]
        message_type = raw_data[1]
        
        if protocol_byte != 0x10:
            raise ValueError(f"Unknown protocol: {protocol_byte:02x}")
        
        # データ抽出
        timestamp = struct.unpack('>I', raw_data[4:8])[0]
        device_number = raw_data[8:16].hex()
        sensor_type_code = struct.unpack('>H', raw_data[16:18])[0]
        
        # センサータイプの識別
        if sensor_type_code not in self.sensor_type_map:
            raise ValueError(f"Unknown sensor type: {sensor_type_code:04x}")
        
        sensor_type, unit = self.sensor_type_map[sensor_type_code]
        
        # 値の抽出
        if sensor_type == "contact_input":
            value = bool(raw_data[18])
        else:
            value = struct.unpack('>f', raw_data[18:22])[0]
        
        return SensorData(
            device_id=f"{self.device_prefix}-{device_number}",
            sensor_type=sensor_type,
            value=value,
            unit=unit,
            timestamp=datetime.fromtimestamp(timestamp),
            metadata={
                "protocol": "bravepi",
                "message_type": message_type,
                "raw_data": raw_data.hex()
            }
        )
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "BravePI Protocol Plugin",
            "version": "1.0.0",
            "protocol": "bravepi",
            "supported_devices": ["BravePI"],
            "supported_sensors": list(self.sensor_type_map.values())
        }
    
    def health_check(self) -> bool:
        return True
    
    def shutdown(self) -> None:
        pass
```

### 3.2 OMRON Protocol Plugin

```python
class OMRONProtocolPlugin(ProtocolPlugin):
    """OMRON環境センサー用プラグイン"""
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        self.device_prefix = config.get("device_prefix", "omron")
        return True
    
    def process(self, raw_data: bytes, metadata: Dict[str, Any]) -> SensorData:
        """OMRON形式データの解析"""
        # データ形式: "T:25.5,H:60.2,P:1013.25"
        data_str = raw_data.decode('utf-8').strip()
        values = {}
        
        for item in data_str.split(','):
            key, value = item.split(':')
            values[key] = float(value)
        
        # 複数センサーの場合は最初のものを返す（実際は複数返すべき）
        if 'T' in values:
            return SensorData(
                device_id=f"{self.device_prefix}-{metadata.get('port', 'unknown')}",
                sensor_type="temperature",
                value=values['T'],
                unit="celsius",
                timestamp=datetime.now(),
                metadata={"protocol": "omron", "all_values": values}
            )
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "OMRON Protocol Plugin",
            "version": "1.0.0",
            "protocol": "omron",
            "supported_devices": ["OMRON 2JCIE-BU01"]
        }
    
    def health_check(self) -> bool:
        return True
    
    def shutdown(self) -> None:
        pass
```

### 3.3 汎用MQTT Plugin

```python
import json

class GenericMQTTPlugin(ProtocolPlugin):
    """汎用MQTT JSON形式プラグイン"""
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        self.device_prefix = config.get("device_prefix", "mqtt")
        return True
    
    def process(self, raw_data: bytes, metadata: Dict[str, Any]) -> SensorData:
        """JSON形式データの解析"""
        data = json.loads(raw_data.decode('utf-8'))
        
        return SensorData(
            device_id=data.get("deviceId", f"{self.device_prefix}-unknown"),
            sensor_type=data.get("type", "unknown"),
            value=data.get("value"),
            unit=data.get("unit", ""),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            quality=data.get("quality", "good"),
            metadata={"protocol": "mqtt_json", "topic": metadata.get("topic")}
        )
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "Generic MQTT Plugin",
            "version": "1.0.0",
            "protocol": "mqtt_json",
            "supported_devices": ["Any MQTT JSON device"]
        }
    
    def health_check(self) -> bool:
        return True
    
    def shutdown(self) -> None:
        pass
```

## 4. プラグイン設定管理

### 4.1 プラグイン設定ファイル (plugin.yaml)

```yaml
# プラグイン設定
plugins:
  # BravePI プラグイン
  - name: bravepi_protocol
    enabled: true
    class: BravePIProtocolPlugin
    module: plugins.bravepi_protocol
    config:
      device_prefix: "bravepi"
      retry_count: 3
      timeout: 30
    topics:
      - "raw/uart/data"
      - "raw/usb_serial/+/data"
  
  # OMRON プラグイン
  - name: omron_protocol
    enabled: true
    class: OMRONProtocolPlugin
    module: plugins.omron_protocol
    config:
      device_prefix: "omron"
    topics:
      - "raw/i2c/+/data"
  
  # 汎用MQTT プラグイン
  - name: generic_mqtt
    enabled: true
    class: GenericMQTTPlugin
    module: plugins.generic_mqtt
    config:
      device_prefix: "generic"
    topics:
      - "devices/+/data"

# デバイスドライバ設定
drivers:
  # UART ドライバ
  - name: uart_driver
    type: uart
    enabled: true
    config:
      port: "/dev/ttyAMA0"
      baudrate: 38400
      data_bits: 8
      parity: "none"
      stop_bits: 1
      timeout: 1.0
    mqtt_topic: "raw/uart/data"
  
  # USB Serial ドライバ
  - name: usb_serial_driver
    type: usb_serial
    enabled: true
    config:
      port_pattern: "/dev/ttyACM*"
      baudrate: 38400
      max_devices: 10
      hot_plug: true
    mqtt_topic_pattern: "raw/usb_serial/{device_id}/data"
  
  # I2C ドライバ
  - name: i2c_driver
    type: i2c
    enabled: true
    config:
      bus: 1
      scan_interval: 5.0
      addresses:
        - 0x48  # 温度センサー
        - 0x76  # 圧力センサー
    mqtt_topic_pattern: "raw/i2c/{address}/data"
```

### 4.2 デバイス個別設定

```yaml
# devices.yaml - デバイス個別の設定
devices:
  # BravePI デバイス
  bravepi-001:
    driver: uart_driver
    plugin: bravepi_protocol
    location: "工場1号棟"
    tags:
      - "production_line_1"
      - "temperature_monitoring"
    calibration:
      temperature:
        offset: -0.5
        scale: 1.0
  
  # BraveJIG デバイス
  bravejig-001:
    driver: usb_serial_driver
    plugin: bravepi_protocol
    serial_number: "BJ2024001"
    location: "品質検査室"
    tags:
      - "quality_control"
      - "high_precision"
  
  # OMRON 環境センサー
  omron-001:
    driver: i2c_driver
    plugin: omron_protocol
    i2c_address: 0x48
    location: "クリーンルーム"
    tags:
      - "clean_room"
      - "environmental_monitoring"
```

## 5. プロジェクト構造

```
iot-gateway/
├── src/
│   ├── drivers/               # デバイスドライバ
│   │   ├── __init__.py
│   │   ├── base_driver.py     # 基底クラス
│   │   ├── uart_driver.py
│   │   ├── usb_serial_driver.py
│   │   └── i2c_driver.py
│   │
│   ├── plugins/               # プロトコルプラグイン
│   │   ├── __init__.py
│   │   ├── base_plugin.py     # 基底クラス
│   │   ├── bravepi_protocol.py
│   │   ├── omron_protocol.py
│   │   └── generic_mqtt.py
│   │
│   ├── core/                  # コア機能
│   │   ├── __init__.py
│   │   ├── plugin_manager.py  # プラグイン管理
│   │   ├── driver_manager.py  # ドライバ管理
│   │   ├── data_processor.py  # データ処理
│   │   └── mqtt_handler.py    # MQTT通信
│   │
│   └── api/                   # REST API
│       ├── __init__.py
│       ├── routes.py
│       └── models.py
│
├── config/                    # 設定ファイル
│   ├── plugin.yaml
│   ├── devices.yaml
│   └── system.yaml
│
├── tests/                     # テスト
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── docs/                      # ドキュメント
├── scripts/                   # ユーティリティスクリプト
└── requirements.txt           # 依存関係
```

---

本文書は、プラグインアーキテクチャの設計原則と実装例を提供し、新規プラグイン開発の指針となることを目的としています。