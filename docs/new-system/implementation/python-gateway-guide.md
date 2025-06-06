# BravePI Gateway Python実装ガイド

*BravePI/JIGデータ汎用化ゲートウェイの開発実装書*

## 概要

本ドキュメントは、BravePI/JIG専用バイナリプロトコルを汎用JSON形式に変換するPythonゲートウェイの実装ガイドです。AI駆動開発に最適化され、マルチプラットフォーム対応を前提とした設計となっています。

## 目次
1. [プロジェクト構成](#プロジェクト構成)
2. [コア実装](#コア実装)
3. [API設計](#api設計)
4. [テスト戦略](#テスト戦略)
5. [デプロイメント](#デプロイメント)
6. [拡張計画](#拡張計画)

## プロジェクト構成

### ディレクトリ構造
```
bravepi-gateway/
├── src/
│   ├── __init__.py
│   ├── models/              # データモデル定義
│   │   ├── __init__.py
│   │   └── sensor_data.py   # 汎用センサーデータモデル
│   ├── converters/          # プロトコル変換器
│   │   ├── __init__.py
│   │   ├── base.py         # 基底変換器クラス
│   │   ├── bravepi_converter.py  # BravePI専用変換器
│   │   └── bravejig_converter.py # BraveJIG専用変換器
│   ├── api/                 # FastAPI実装
│   │   ├── __init__.py
│   │   ├── main.py         # APIエントリーポイント
│   │   ├── routes/         # APIルート定義
│   │   └── websocket.py   # WebSocket処理
│   ├── hardware/           # ハードウェア抽象化
│   │   ├── __init__.py
│   │   ├── interface.py    # 抽象インターフェース
│   │   ├── rpi4b.py       # RPi4B実装
│   │   └── mock.py        # モック実装
│   └── utils/              # ユーティリティ
│       ├── __init__.py
│       └── logger.py       # ロギング設定
├── tests/                  # テストコード
│   ├── __init__.py
│   ├── test_converters.py
│   ├── test_api.py
│   └── fixtures/          # テストデータ
├── docs/                   # 技術文書
├── scripts/                # 運用スクリプト
│   ├── generate_test_data.py
│   └── benchmark.py
├── docker/                 # Docker設定
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt        # 依存関係
├── requirements-dev.txt    # 開発用依存関係
├── .env.example           # 環境変数テンプレート
├── pyproject.toml         # プロジェクト設定
└── README.md              # プロジェクト概要
```

### 技術スタック
```yaml
言語: Python 3.11+
フレームワーク:
  - FastAPI (Web API)
  - Pydantic (データ検証)
  - uvicorn (ASGIサーバー)
  
通信:
  - WebSocket (リアルタイム通信)
  - pyserial (シリアル通信)
  
テスト:
  - pytest
  - pytest-asyncio
  - pytest-cov
  
開発ツール:
  - black (コードフォーマッター)
  - mypy (型チェック)
  - ruff (リンター)
```

## コア実装

### 1. データモデル定義

```python
# src/models/sensor_data.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Any, Optional, Dict, Union, Literal
from enum import Enum

class DataQuality(str, Enum):
    """データ品質指標"""
    GOOD = "good"
    UNCERTAIN = "uncertain"
    BAD = "bad"
    MAINTENANCE = "maintenance"

class UniversalSensorData(BaseModel):
    """
    汎用センサーデータモデル
    全てのセンサータイプで統一的に使用する標準形式
    """
    # 必須フィールド
    device_id: str = Field(
        ..., 
        description="デバイス識別子（例: bravepi-12345678）",
        pattern="^[a-zA-Z0-9-_]+$"
    )
    sensor_type: str = Field(
        ..., 
        description="センサータイプ（例: temperature, contact_input）"
    )
    value: Union[float, bool, int, Dict[str, float]] = Field(
        ..., 
        description="測定値（センサータイプに応じた型）"
    )
    unit: str = Field(
        ..., 
        description="単位（例: ℃, mm, V, lux）"
    )
    
    # オプションフィールド
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="測定時刻（UTC）"
    )
    quality: DataQuality = Field(
        default=DataQuality.GOOD,
        description="データ品質指標"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="追加メタデータ（元のセンサータイプID、プロトコル情報等）"
    )
    
    # バリデーション
    @validator('value')
    def validate_value_type(cls, v, values):
        """センサータイプに応じた値の型検証"""
        sensor_type = values.get('sensor_type')
        if sensor_type and sensor_type.startswith('contact'):
            if not isinstance(v, bool):
                raise ValueError(f"Contact sensor must return boolean, got {type(v)}")
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "device_id": "bravepi-12345678",
                "sensor_type": "temperature",
                "value": 25.5,
                "unit": "℃",
                "timestamp": "2025-06-06T10:30:00Z",
                "quality": "good",
                "metadata": {
                    "source": "bravepi",
                    "raw_sensor_type": 261
                }
            }
        }
```

### 2. BravePI/JIG変換器実装

```python
# src/converters/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
from ..models.sensor_data import UniversalSensorData

class BaseConverter(ABC):
    """変換器基底クラス"""
    
    @abstractmethod
    def parse_frame(self, data: bytes) -> Dict[str, Any]:
        """生データからフレーム情報を抽出"""
        pass
    
    @abstractmethod
    def extract_value(self, sensor_type: int, payload: bytes) -> Tuple[Any, str]:
        """ペイロードから値と単位を抽出"""
        pass
    
    @abstractmethod
    def convert(self, data: bytes) -> UniversalSensorData:
        """生データを汎用形式に変換"""
        pass
```

```python
# src/converters/bravepi_converter.py
import struct
import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np

from .base import BaseConverter
from ..models.sensor_data import UniversalSensorData, DataQuality

logger = logging.getLogger(__name__)

class BravePIConverter(BaseConverter):
    """
    BravePI/JIG バイナリプロトコル変換器
    38400baud UART通信で受信したバイナリデータを解析
    """
    
    # プロトコル定数
    HEADER_SIZE = 18
    PROTOCOL_VERSION = 1
    
    # センサータイプ定義
    SENSOR_TYPES = {
        # 基本センサー (257-264)
        257: {
            "name": "contact_input",
            "unit": "",
            "data_type": bool,
            "description": "接点入力（デジタル信号）"
        },
        258: {
            "name": "contact_output",
            "unit": "",
            "data_type": bool,
            "description": "接点出力（デジタル制御）"
        },
        259: {
            "name": "analog_voltage",
            "unit": "mV",
            "data_type": float,
            "channels": 2,
            "description": "ADC電圧測定（2チャンネル）"
        },
        260: {
            "name": "distance",
            "unit": "mm",
            "data_type": float,
            "range": (0, 2000),
            "description": "測距センサー（VL53L1X等）"
        },
        261: {
            "name": "temperature",
            "unit": "℃",
            "data_type": float,
            "range": (-50, 2000),
            "description": "熱電対温度センサー"
        },
        262: {
            "name": "acceleration",
            "unit": "G",
            "data_type": dict,
            "axes": ["x", "y", "z"],
            "range": (-6.5, 6.5),
            "description": "3軸加速度センサー"
        },
        263: {
            "name": "differential_pressure",
            "unit": "Pa",
            "data_type": float,
            "range": (-500, 500),
            "description": "差圧センサー"
        },
        264: {
            "name": "illuminance",
            "unit": "lux",
            "data_type": float,
            "range": (40, 83865),
            "description": "照度センサー（OPT3001等）"
        },
        # JIG拡張センサー (289-293)
        289: {
            "name": "illuminance_jig",
            "unit": "lux",
            "data_type": float,
            "high_precision": True,
            "description": "高精度照度センサー（JIG接続）"
        },
        290: {
            "name": "acceleration_jig",
            "unit": "G",
            "data_type": dict,
            "axes": ["x", "y", "z"],
            "fft_capable": True,
            "description": "高精度3軸加速度（FFT解析対応）"
        },
        291: {
            "name": "temperature_humidity_jig",
            "unit": "℃/%",
            "data_type": dict,
            "channels": ["temperature", "humidity"],
            "description": "温湿度複合センサー"
        },
        292: {
            "name": "pressure_jig",
            "unit": "hPa",
            "data_type": float,
            "absolute": True,
            "description": "絶対圧センサー"
        },
        293: {
            "name": "distance_jig",
            "unit": "mm",
            "data_type": float,
            "long_range": True,
            "description": "長距離測距センサー"
        }
    }
    
    def parse_frame(self, data: bytes) -> Dict[str, Any]:
        """
        BravePIフレーム構造を解析
        
        フレーム構造:
        - Protocol (1 byte): プロトコルバージョン
        - Type (1 byte): メッセージタイプ
        - Length (2 bytes): ペイロード長（リトルエンディアン）
        - Timestamp (4 bytes): Unix時刻（リトルエンディアン）
        - Device Number (8 bytes): デバイス固有ID（リトルエンディアン）
        - Sensor Type (2 bytes): センサータイプID（リトルエンディアン）
        - Payload (n bytes): センサーデータ
        """
        if len(data) < self.HEADER_SIZE:
            raise ValueError(
                f"Invalid frame size: {len(data)} bytes "
                f"(minimum {self.HEADER_SIZE} required)"
            )
        
        try:
            frame = {
                'protocol': data[0],
                'msg_type': data[1],
                'length': struct.unpack('<H', data[2:4])[0],
                'timestamp': struct.unpack('<I', data[4:8])[0],
                'device_number': struct.unpack('<Q', data[8:16])[0],
                'sensor_type': struct.unpack('<H', data[16:18])[0],
                'payload': data[18:] if len(data) > 18 else b'',
                'rssi': None,  # BLE接続時のみ
                'crc': None    # CRC16（実装予定）
            }
            
            # プロトコルバージョンチェック
            if frame['protocol'] != self.PROTOCOL_VERSION:
                logger.warning(
                    f"Unknown protocol version: {frame['protocol']}"
                )
            
            return frame
            
        except struct.error as e:
            raise ValueError(f"Frame parsing error: {e}")
    
    def extract_value(self, sensor_type: int, payload: bytes) -> Tuple[Any, str]:
        """
        センサータイプに応じてペイロードから値を抽出
        """
        if sensor_type not in self.SENSOR_TYPES:
            logger.warning(f"Unknown sensor type: {sensor_type}")
            return {"raw": payload.hex()}, "hex"
        
        sensor_info = self.SENSOR_TYPES[sensor_type]
        data_type = sensor_info["data_type"]
        unit = sensor_info["unit"]
        
        try:
            # ブール型（接点入力/出力）
            if data_type == bool:
                if len(payload) >= 1:
                    return bool(payload[0]), unit
                return False, unit
            
            # 単一float値
            elif data_type == float:
                if len(payload) >= 4:
                    value = struct.unpack('<f', payload[:4])[0]
                    
                    # 範囲チェック
                    if "range" in sensor_info:
                        min_val, max_val = sensor_info["range"]
                        if not (min_val <= value <= max_val):
                            logger.warning(
                                f"Value {value} out of range "
                                f"[{min_val}, {max_val}] for {sensor_info['name']}"
                            )
                    
                    return round(value, 3), unit
                return 0.0, unit
            
            # 複数値（辞書型）
            elif data_type == dict:
                # 3軸加速度
                if sensor_type in [262, 290]:
                    if len(payload) >= 12:
                        x = struct.unpack('<f', payload[0:4])[0]
                        y = struct.unpack('<f', payload[4:8])[0]
                        z = struct.unpack('<f', payload[8:12])[0]
                        
                        # 合成加速度も計算
                        composite = np.sqrt(x**2 + y**2 + z**2)
                        
                        return {
                            "x": round(x, 3),
                            "y": round(y, 3),
                            "z": round(z, 3),
                            "composite": round(composite, 3)
                        }, unit
                
                # 温湿度
                elif sensor_type == 291:
                    if len(payload) >= 8:
                        temp = struct.unpack('<f', payload[0:4])[0]
                        humidity = struct.unpack('<f', payload[4:8])[0]
                        return {
                            "temperature": round(temp, 2),
                            "humidity": round(humidity, 1)
                        }, unit
                
                # ADC 2チャンネル
                elif sensor_type == 259:
                    if len(payload) >= 8:
                        ch1 = struct.unpack('<f', payload[0:4])[0]
                        ch2 = struct.unpack('<f', payload[4:8])[0]
                        return {
                            "channel1": round(ch1, 1),
                            "channel2": round(ch2, 1)
                        }, unit
            
            return None, ""
            
        except Exception as e:
            logger.error(f"Value extraction error: {e}")
            return None, ""
    
    def assess_data_quality(self, frame: Dict[str, Any], value: Any) -> DataQuality:
        """
        データ品質を評価
        """
        # タイムスタンプの妥当性チェック
        current_time = datetime.utcnow().timestamp()
        time_diff = abs(current_time - frame['timestamp'])
        
        if time_diff > 3600:  # 1時間以上のずれ
            return DataQuality.UNCERTAIN
        
        # RSSI値によるBLE通信品質（実装予定）
        if frame.get('rssi') is not None:
            if frame['rssi'] < -80:
                return DataQuality.UNCERTAIN
        
        # 値の妥当性（センサータイプ別）
        # TODO: センサー固有の品質評価ロジック
        
        return DataQuality.GOOD
    
    def convert(self, data: bytes) -> UniversalSensorData:
        """
        BravePIバイナリデータを汎用形式に変換
        """
        # フレーム解析
        frame = self.parse_frame(data)
        
        sensor_type = frame['sensor_type']
        if sensor_type not in self.SENSOR_TYPES:
            raise ValueError(f"Unsupported sensor type: {sensor_type}")
        
        sensor_info = self.SENSOR_TYPES[sensor_type]
        
        # 値抽出
        value, unit = self.extract_value(sensor_type, frame['payload'])
        if value is None:
            raise ValueError(f"Failed to extract value from payload")
        
        # データ品質評価
        quality = self.assess_data_quality(frame, value)
        
        # 汎用データモデルに変換
        return UniversalSensorData(
            device_id=f"bravepi-{frame['device_number']}",
            sensor_type=sensor_info['name'],
            value=value,
            unit=unit,
            timestamp=datetime.fromtimestamp(frame['timestamp']),
            quality=quality,
            metadata={
                "source": "bravepi",
                "protocol_version": frame['protocol'],
                "message_type": frame['msg_type'],
                "raw_sensor_type": sensor_type,
                "description": sensor_info.get('description', ''),
                "payload_size": len(frame['payload'])
            }
        )

# BraveJIG用コンバーター（同様の構造で実装）
class BraveJIGConverter(BravePIConverter):
    """
    BraveJIG USB接続デバイス用コンバーター
    基本的にBravePIと同じプロトコルだが、USB経由で高精度センサーに対応
    """
    
    def __init__(self):
        super().__init__()
        # JIG固有の設定があればここに追加
        self.usb_timeout = 5000  # USB通信タイムアウト（ms）
    
    def convert(self, data: bytes) -> UniversalSensorData:
        """BraveJIG固有の処理を追加"""
        result = super().convert(data)
        result.metadata["source"] = "bravejig"
        result.metadata["connection"] = "usb"
        return result
```

### 3. FastAPI実装

```python
# src/api/main.py
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json

from ..converters.bravepi_converter import BravePIConverter, BraveJIGConverter
from ..models.sensor_data import UniversalSensorData
from .websocket import ConnectionManager

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPIアプリケーション
app = FastAPI(
    title="BravePI Gateway API",
    description="BravePI/JIGデータを汎用JSON形式に変換するゲートウェイAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定（開発用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket接続管理
manager = ConnectionManager()

# コンバーターインスタンス
converters = {
    "bravepi": BravePIConverter(),
    "bravejig": BraveJIGConverter()
}

# インメモリデータストア（デモ用）
sensor_data_store: List[UniversalSensorData] = []
MAX_STORE_SIZE = 1000

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info("BravePI Gateway API starting up...")
    # TODO: シリアルポート接続初期化
    # TODO: データベース接続初期化

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info("BravePI Gateway API shutting down...")
    # TODO: 接続クリーンアップ

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "name": "BravePI Gateway API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "api_docs": "/docs",
            "convert": "/api/v1/convert/{source}",
            "websocket": "/ws/sensor-stream",
            "health": "/health",
            "metrics": "/metrics"
        }
    }

@app.post("/api/v1/convert/{source}", response_model=UniversalSensorData)
async def convert_sensor_data(source: str, request: Request):
    """
    センサーデータ変換エンドポイント
    
    Parameters:
        source: データソース ("bravepi" or "bravejig")
        request: バイナリデータを含むリクエスト
    
    Returns:
        変換された汎用センサーデータ
    """
    if source not in converters:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown source: {source}. Valid sources: {list(converters.keys())}"
        )
    
    try:
        # バイナリデータ取得
        data = await request.body()
        if not data:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # 変換実行
        converter = converters[source]
        result = converter.convert(data)
        
        # データストアに保存（デモ用）
        sensor_data_store.append(result)
        if len(sensor_data_store) > MAX_STORE_SIZE:
            sensor_data_store.pop(0)
        
        # WebSocketクライアントにブロードキャスト
        await manager.broadcast(result.dict())
        
        logger.info(
            f"Converted {source} data: "
            f"device={result.device_id}, "
            f"type={result.sensor_type}, "
            f"value={result.value}"
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Conversion error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/data/latest")
async def get_latest_data(limit: int = 100):
    """最新のセンサーデータを取得"""
    return sensor_data_store[-limit:]

@app.get("/api/v1/data/by-device/{device_id}")
async def get_device_data(device_id: str, limit: int = 100):
    """特定デバイスのデータを取得"""
    device_data = [
        data for data in sensor_data_store 
        if data.device_id == device_id
    ]
    return device_data[-limit:]

@app.websocket("/ws/sensor-stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocketエンドポイント
    リアルタイムセンサーデータストリーミング
    """
    await manager.connect(websocket)
    try:
        while True:
            # クライアントからのメッセージ待機
            message = await websocket.receive_text()
            
            # コマンド処理
            try:
                cmd = json.loads(message)
                if cmd.get("type") == "subscribe":
                    device_id = cmd.get("device_id")
                    await websocket.send_json({
                        "type": "subscribed",
                        "device_id": device_id,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                elif cmd.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })
            except json.JSONDecodeError:
                # バイナリデータとして処理
                if len(message) > 0:
                    # デフォルトでBravePIとして処理
                    try:
                        result = converters["bravepi"].convert(message.encode())
                        await websocket.send_json(result.dict())
                        await manager.broadcast(result.dict(), exclude=websocket)
                    except Exception as e:
                        await websocket.send_json({
                            "type": "error",
                            "message": str(e)
                        })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_connections": len(manager.active_connections),
        "data_points": len(sensor_data_store)
    }

@app.get("/metrics")
async def get_metrics():
    """メトリクスエンドポイント"""
    # センサータイプ別統計
    type_stats: Dict[str, int] = {}
    device_stats: Dict[str, int] = {}
    
    for data in sensor_data_store:
        type_stats[data.sensor_type] = type_stats.get(data.sensor_type, 0) + 1
        device_stats[data.device_id] = device_stats.get(data.device_id, 0) + 1
    
    return {
        "total_data_points": len(sensor_data_store),
        "active_websocket_connections": len(manager.active_connections),
        "sensor_type_distribution": type_stats,
        "device_distribution": device_stats,
        "timestamp": datetime.utcnow().isoformat()
    }
```

```python
# src/api/websocket.py
from typing import List, Dict, Optional
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocket接続管理クラス"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[WebSocket, Dict[str, any]] = {}
    
    async def connect(self, websocket: WebSocket):
        """新規接続を受け入れる"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.subscriptions[websocket] = {
            "device_ids": [],  # 購読デバイスID
            "sensor_types": []  # 購読センサータイプ
        }
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """接続を切断する"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """特定のクライアントにメッセージを送信"""
        await websocket.send_text(message)
    
    async def broadcast(self, message: dict, exclude: Optional[WebSocket] = None):
        """全クライアントにメッセージをブロードキャスト"""
        disconnected_clients = []
        
        for connection in self.active_connections:
            if connection == exclude:
                continue
                
            try:
                # 購読フィルタリング
                if self._should_send_to_client(connection, message):
                    await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected_clients.append(connection)
        
        # 切断されたクライアントをクリーンアップ
        for client in disconnected_clients:
            self.disconnect(client)
    
    def _should_send_to_client(self, websocket: WebSocket, message: dict) -> bool:
        """クライアントの購読設定に基づいてメッセージを送信すべきか判断"""
        subscription = self.subscriptions.get(websocket, {})
        
        # デバイスIDフィルタ
        device_ids = subscription.get("device_ids", [])
        if device_ids and message.get("device_id") not in device_ids:
            return False
        
        # センサータイプフィルタ
        sensor_types = subscription.get("sensor_types", [])
        if sensor_types and message.get("sensor_type") not in sensor_types:
            return False
        
        return True
    
    def update_subscription(self, websocket: WebSocket, device_ids: List[str] = None, 
                          sensor_types: List[str] = None):
        """クライアントの購読設定を更新"""
        if websocket in self.subscriptions:
            if device_ids is not None:
                self.subscriptions[websocket]["device_ids"] = device_ids
            if sensor_types is not None:
                self.subscriptions[websocket]["sensor_types"] = sensor_types
```

## テスト戦略

### 1. ユニットテスト

```python
# tests/test_converters.py
import pytest
import struct
from datetime import datetime
from src.converters.bravepi_converter import BravePIConverter
from src.models.sensor_data import UniversalSensorData, DataQuality

class TestBravePIConverter:
    """BravePIコンバーターのテスト"""
    
    @pytest.fixture
    def converter(self):
        return BravePIConverter()
    
    def create_test_frame(
        self, 
        sensor_type: int, 
        payload: bytes,
        device_number: int = 12345678,
        timestamp: int = None
    ) -> bytes:
        """テスト用フレームを生成"""
        if timestamp is None:
            timestamp = int(datetime.utcnow().timestamp())
        
        frame = bytearray(18 + len(payload))
        frame[0] = 1  # protocol
        frame[1] = 0  # msg_type
        struct.pack_into('<H', frame, 2, len(payload))  # length
        struct.pack_into('<I', frame, 4, timestamp)     # timestamp
        struct.pack_into('<Q', frame, 8, device_number) # device_number
        struct.pack_into('<H', frame, 16, sensor_type)  # sensor_type
        frame[18:] = payload  # payload
        
        return bytes(frame)
    
    def test_parse_frame_valid(self, converter):
        """正常なフレームの解析テスト"""
        test_data = self.create_test_frame(261, b'\x00\x00\x48\x42')  # 50.0
        frame = converter.parse_frame(test_data)
        
        assert frame['protocol'] == 1
        assert frame['msg_type'] == 0
        assert frame['device_number'] == 12345678
        assert frame['sensor_type'] == 261
        assert len(frame['payload']) == 4
    
    def test_parse_frame_invalid_size(self, converter):
        """不正なサイズのフレームテスト"""
        with pytest.raises(ValueError, match="Invalid frame size"):
            converter.parse_frame(b'short')
    
    def test_temperature_conversion(self, converter):
        """温度センサー変換テスト"""
        # 25.5℃のfloat値
        payload = struct.pack('<f', 25.5)
        test_data = self.create_test_frame(261, payload)
        
        result = converter.convert(test_data)
        
        assert result.device_id == "bravepi-12345678"
        assert result.sensor_type == "temperature"
        assert result.value == 25.5
        assert result.unit == "℃"
        assert result.quality == DataQuality.GOOD
        assert result.metadata["source"] == "bravepi"
        assert result.metadata["raw_sensor_type"] == 261
    
    def test_contact_input_conversion(self, converter):
        """接点入力変換テスト"""
        # ON状態
        test_data = self.create_test_frame(257, b'\x01')
        result = converter.convert(test_data)
        
        assert result.sensor_type == "contact_input"
        assert result.value is True
        assert result.unit == ""
        
        # OFF状態
        test_data = self.create_test_frame(257, b'\x00')
        result = converter.convert(test_data)
        assert result.value is False
    
    def test_acceleration_conversion(self, converter):
        """加速度センサー変換テスト"""
        # X=1.0, Y=2.0, Z=3.0
        payload = struct.pack('<fff', 1.0, 2.0, 3.0)
        test_data = self.create_test_frame(262, payload)
        
        result = converter.convert(test_data)
        
        assert result.sensor_type == "acceleration"
        assert isinstance(result.value, dict)
        assert result.value["x"] == 1.0
        assert result.value["y"] == 2.0
        assert result.value["z"] == 3.0
        assert "composite" in result.value
        assert result.unit == "G"
    
    def test_temperature_humidity_conversion(self, converter):
        """温湿度センサー変換テスト"""
        # 温度=22.5℃, 湿度=65.0%
        payload = struct.pack('<ff', 22.5, 65.0)
        test_data = self.create_test_frame(291, payload)
        
        result = converter.convert(test_data)
        
        assert result.sensor_type == "temperature_humidity_jig"
        assert result.value["temperature"] == 22.5
        assert result.value["humidity"] == 65.0
        assert result.unit == "℃/%"
    
    def test_unknown_sensor_type(self, converter):
        """未知のセンサータイプテスト"""
        test_data = self.create_test_frame(999, b'invalid')
        
        with pytest.raises(ValueError, match="Unsupported sensor type"):
            converter.convert(test_data)
    
    def test_data_quality_assessment(self, converter):
        """データ品質評価テスト"""
        # 古いタイムスタンプ（2時間前）
        old_timestamp = int(datetime.utcnow().timestamp()) - 7200
        test_data = self.create_test_frame(
            261, 
            struct.pack('<f', 25.0),
            timestamp=old_timestamp
        )
        
        result = converter.convert(test_data)
        assert result.quality == DataQuality.UNCERTAIN
    
    @pytest.mark.parametrize("sensor_type,expected_name", [
        (257, "contact_input"),
        (258, "contact_output"),
        (259, "analog_voltage"),
        (260, "distance"),
        (261, "temperature"),
        (262, "acceleration"),
        (263, "differential_pressure"),
        (264, "illuminance"),
        (289, "illuminance_jig"),
        (290, "acceleration_jig"),
    ])
    def test_all_sensor_types(self, converter, sensor_type, expected_name):
        """全センサータイプの基本変換テスト"""
        # 最小限のペイロード
        payload = b'\x00' * 12
        test_data = self.create_test_frame(sensor_type, payload)
        
        result = converter.convert(test_data)
        assert result.sensor_type == expected_name
```

### 2. API統合テスト

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
import struct
from datetime import datetime

from src.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

class TestAPI:
    """APIエンドポイントのテスト"""
    
    def create_test_data(self, sensor_type: int = 261, value: float = 25.0) -> bytes:
        """テスト用バイナリデータ作成"""
        frame = bytearray(22)
        frame[0] = 1  # protocol
        frame[1] = 0  # msg_type
        struct.pack_into('<H', frame, 2, 4)  # length
        struct.pack_into('<I', frame, 4, int(datetime.utcnow().timestamp()))
        struct.pack_into('<Q', frame, 8, 12345678)  # device_number
        struct.pack_into('<H', frame, 16, sensor_type)
        struct.pack_into('<f', frame, 18, value)
        return bytes(frame)
    
    def test_root_endpoint(self, client):
        """ルートエンドポイントテスト"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "BravePI Gateway API"
        assert "endpoints" in data
    
    def test_convert_bravepi(self, client):
        """BravePI変換エンドポイントテスト"""
        test_data = self.create_test_data(261, 30.5)
        
        response = client.post(
            "/api/v1/convert/bravepi",
            content=test_data,
            headers={"Content-Type": "application/octet-stream"}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["device_id"] == "bravepi-12345678"
        assert result["sensor_type"] == "temperature"
        assert result["value"] == 30.5
        assert result["unit"] == "℃"
    
    def test_convert_invalid_source(self, client):
        """無効なソースのテスト"""
        response = client.post(
            "/api/v1/convert/invalid",
            content=b"dummy"
        )
        assert response.status_code == 400
        assert "Unknown source" in response.json()["detail"]
    
    def test_convert_empty_data(self, client):
        """空データのテスト"""
        response = client.post(
            "/api/v1/convert/bravepi",
            content=b""
        )
        assert response.status_code == 400
    
    def test_health_check(self, client):
        """ヘルスチェックテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_metrics_endpoint(self, client):
        """メトリクスエンドポイントテスト"""
        # まずデータを送信
        test_data = self.create_test_data()
        client.post("/api/v1/convert/bravepi", content=test_data)
        
        # メトリクス取得
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_data_points" in data
        assert data["total_data_points"] >= 1
    
    def test_latest_data(self, client):
        """最新データ取得テスト"""
        # テストデータ送信
        for i in range(5):
            test_data = self.create_test_data(261, 20.0 + i)
            client.post("/api/v1/convert/bravepi", content=test_data)
        
        # 最新データ取得
        response = client.get("/api/v1/data/latest?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3
    
    def test_device_data(self, client):
        """デバイス別データ取得テスト"""
        # テストデータ送信
        test_data = self.create_test_data()
        client.post("/api/v1/convert/bravepi", content=test_data)
        
        # デバイスデータ取得
        response = client.get("/api/v1/data/by-device/bravepi-12345678")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(d["device_id"] == "bravepi-12345678" for d in data)
```

### 3. パフォーマンステスト

```python
# tests/test_performance.py
import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import struct
from datetime import datetime

from src.converters.bravepi_converter import BravePIConverter

class TestPerformance:
    """パフォーマンステスト"""
    
    @pytest.fixture
    def converter(self):
        return BravePIConverter()
    
    def create_test_data(self, count: int) -> list:
        """大量のテストデータ生成"""
        data_list = []
        for i in range(count):
            frame = bytearray(22)
            frame[0] = 1
            frame[1] = 0
            struct.pack_into('<H', frame, 2, 4)
            struct.pack_into('<I', frame, 4, int(datetime.utcnow().timestamp()))
            struct.pack_into('<Q', frame, 8, i)
            struct.pack_into('<H', frame, 16, 261)  # temperature
            struct.pack_into('<f', frame, 18, 20.0 + (i % 10))
            data_list.append(bytes(frame))
        return data_list
    
    def test_conversion_speed(self, converter):
        """変換速度テスト"""
        test_data = self.create_test_data(1000)
        
        start_time = time.time()
        for data in test_data:
            converter.convert(data)
        end_time = time.time()
        
        elapsed = end_time - start_time
        conversions_per_second = 1000 / elapsed
        
        print(f"\nConversion speed: {conversions_per_second:.2f} conversions/sec")
        assert conversions_per_second > 1000  # 最低1000変換/秒
    
    def test_concurrent_conversion(self, converter):
        """並行変換テスト"""
        test_data = self.create_test_data(100)
        
        def convert_data(data):
            return converter.convert(data)
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(convert_data, test_data))
        end_time = time.time()
        
        assert len(results) == 100
        elapsed = end_time - start_time
        print(f"\nConcurrent conversion time: {elapsed:.3f} seconds")
    
    @pytest.mark.asyncio
    async def test_async_performance(self, converter):
        """非同期パフォーマンステスト"""
        test_data = self.create_test_data(1000)
        
        async def convert_async(data):
            # 実際のI/O操作をシミュレート
            await asyncio.sleep(0.001)
            return converter.convert(data)
        
        start_time = time.time()
        tasks = [convert_async(data) for data in test_data]
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        elapsed = end_time - start_time
        print(f"\nAsync conversion time: {elapsed:.3f} seconds")
        assert len(results) == 1000
```

## デプロイメント

### 1. Docker設定

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

# マルチアーキテクチャ対応
ARG TARGETPLATFORM
ARG TARGETARCH

WORKDIR /app

# システム依存パッケージ
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# RPi用追加パッケージ（条件付き）
RUN if [ "$TARGETARCH" = "arm64" ] || [ "$TARGETARCH" = "armv7" ]; then \
    pip install --no-cache-dir RPi.GPIO smbus2; \
    fi

# アプリケーションコピー
COPY src/ ./src/
COPY scripts/ ./scripts/

# 環境変数
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# ポート公開
EXPOSE 8000

# 実行コマンド
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  gateway:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      args:
        TARGETARCH: ${TARGETARCH:-amd64}
    container_name: bravepi-gateway
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
      - INFLUXDB_URL=http://influxdb:8086
      - INFLUXDB_TOKEN=${INFLUXDB_TOKEN}
      - INFLUXDB_ORG=fitc
      - INFLUXDB_BUCKET=sensor_data
    volumes:
      - ./logs:/app/logs
    devices:
      # RPi用デバイスマッピング
      - /dev/ttyAMA0:/dev/ttyAMA0  # UART
      - /dev/ttyACM0:/dev/ttyACM0  # USB
      - /dev/i2c-1:/dev/i2c-1      # I2C
    privileged: true  # GPIO/I2Cアクセス用
    restart: unless-stopped
    networks:
      - iot-network
    depends_on:
      - influxdb

  influxdb:
    image: influxdb:2.7-alpine
    container_name: influxdb
    ports:
      - "8086:8086"
    environment:
      - INFLUXDB_DB=sensor_data
      - INFLUXDB_ADMIN_USER=admin
      - INFLUXDB_ADMIN_PASSWORD=${INFLUXDB_ADMIN_PASSWORD}
      - INFLUXDB_HTTP_AUTH_ENABLED=true
    volumes:
      - influxdb-data:/var/lib/influxdb2
      - ./influxdb/config.yml:/etc/influxdb2/config.yml
    networks:
      - iot-network

  # 開発用可視化ツール
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    networks:
      - iot-network
    depends_on:
      - influxdb

networks:
  iot-network:
    driver: bridge

volumes:
  influxdb-data:
  grafana-data:
```

### 2. 環境設定

```bash
# .env.example
# Application
LOG_LEVEL=INFO
API_KEY=your-secret-api-key

# Serial Communication
SERIAL_PORT=/dev/ttyAMA0
SERIAL_BAUDRATE=38400
USB_PORTS=/dev/ttyACM0,/dev/ttyACM1

# Database
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your-influxdb-token
INFLUXDB_ORG=fitc
INFLUXDB_BUCKET=sensor_data

# Security
INFLUXDB_ADMIN_PASSWORD=secure-password
GRAFANA_PASSWORD=grafana-password

# Hardware specific
ENABLE_GPIO=true
ENABLE_I2C=true
GPIO_PINS=16,25,5,23,18,6,13,17,24,27
I2C_BUS=1
```

### 3. 起動スクリプト

```bash
#!/bin/bash
# scripts/start.sh

# 環境変数読み込み
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# プラットフォーム検出
ARCH=$(uname -m)
case $ARCH in
    aarch64|arm64)
        export TARGETARCH=arm64
        ;;
    armv7l)
        export TARGETARCH=armv7
        ;;
    x86_64)
        export TARGETARCH=amd64
        ;;
esac

echo "Starting BravePI Gateway on $TARGETARCH..."

# Docker Compose起動
docker-compose -f docker/docker-compose.yml up -d

# ログ表示
docker-compose -f docker/docker-compose.yml logs -f gateway
```

```bash
#!/bin/bash
# scripts/setup.sh

# Python仮想環境セットアップ
python3 -m venv venv
source venv/bin/activate

# 依存関係インストール
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# pre-commit フック設定
pre-commit install

# テスト実行
pytest tests/ -v

echo "Setup complete!"
```

## 拡張計画

### Phase 1: 基本機能実装（完了）
- ✅ BravePI/JIGバイナリプロトコル解析
- ✅ 汎用JSON形式への変換
- ✅ REST API実装
- ✅ WebSocketサポート
- ✅ 基本的なテストスイート

### Phase 2: データ永続化（1-2週間）
```yaml
実装項目:
  - InfluxDB統合
  - データ保存・取得API
  - Grafanaダッシュボード
  - データ集計・分析機能
```

### Phase 3: リアルタイム処理（2-3週間）
```yaml
実装項目:
  - シリアルポート監視
  - 自動データ取得
  - アラート・通知機能
  - エッジコンピューティング
```

### Phase 4: マルチデバイス対応（3-4週間）
```yaml
実装項目:
  - ESP32/Arduino対応
  - 汎用MQTTデバイス対応
  - Modbus対応
  - カスタムプロトコル対応
```

### Phase 5: エンタープライズ機能（4-6週間）
```yaml
実装項目:
  - 認証・認可（JWT/OAuth2）
  - マルチテナント対応
  - 監査ログ
  - 高可用性構成
```

## 技術的考慮事項

### パフォーマンス最適化
```python
# 最適化ポイント
1. バイナリ解析の高速化
   - Cython利用検討
   - NumPy活用

2. 非同期処理
   - asyncio活用
   - 並行処理最適化

3. キャッシング
   - Redis導入
   - インメモリキャッシュ

4. データベース最適化
   - バッチ書き込み
   - 時系列圧縮
```

### セキュリティ対策
```yaml
実装予定:
  - API認証（APIキー/JWT）
  - HTTPS/TLS対応
  - 入力検証強化
  - レート制限
  - 監査ログ
```

### 監視・運用
```yaml
実装予定:
  - Prometheus メトリクス
  - 構造化ログ（JSON）
  - ヘルスチェック強化
  - 自動復旧機能
```

---

## 文書メタデータ

**文書タイトル**: BravePI Gateway Python実装ガイド  
**作成日付**: 2025年6月6日  
**対象システム**: BravePI/JIGデータ変換ゲートウェイ  
**実装言語**: Python 3.11+  
**フレームワーク**: FastAPI + Pydantic  
**文書レベル**: 実装ガイド・技術仕様 (★★★)