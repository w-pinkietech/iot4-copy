# REST API リファレンス

## 概要

IoT導入支援キット Ver.4.1のREST API仕様について説明します。このAPIを使用して、外部システムからデバイス管理、センサーデータ操作、システム監視を行うことができます。

## ベースURL

```
http://localhost:1880/api/v2
```

## 認証

現在のバージョンでは基本認証またはAPIキーベースの認証を使用します。

```bash
# Basic認証
curl -u username:password http://localhost:1880/api/v2/device

# APIキー認証 (ヘッダー)
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:1880/api/v2/device
```

## エンドポイント一覧

### デバイス管理

#### デバイス一覧取得
```http
GET /api/v2/device
```

**レスポンス例:**
```json
{
  "devices": [
    {
      "id": "device_001",
      "name": "センサーノード1",
      "type": "sensor_node",
      "status": "online",
      "location": "工場A-1F",
      "last_seen": "2024-01-01T12:00:00Z",
      "sensors": [
        {
          "id": 1,
          "type": "temperature",
          "name": "温度センサー",
          "unit": "℃"
        }
      ]
    }
  ],
  "total": 1
}
```

#### 特定デバイス取得
```http
GET /api/v2/device/{deviceId}
```

**パラメータ:**
- `deviceId`: デバイスID

**レスポンス例:**
```json
{
  "id": "device_001",
  "name": "センサーノード1",
  "type": "sensor_node", 
  "status": "online",
  "config": {
    "sampling_rate": 60,
    "alert_threshold": 35.0
  },
  "sensors": [
    {
      "id": 1,
      "type": "temperature",
      "name": "温度センサー",
      "unit": "℃",
      "last_value": 23.5,
      "last_updated": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### デバイス登録
```http
POST /api/v2/device
```

**リクエストボディ:**
```json
{
  "name": "新しいセンサー",
  "type": "temperature_sensor",
  "location": "工場B-2F",
  "config": {
    "sampling_rate": 30,
    "alert_threshold": 40.0
  },
  "sensors": [
    {
      "type": "temperature",
      "name": "温度センサー",
      "unit": "℃"
    }
  ]
}
```

**レスポンス:**
```json
{
  "id": "device_002",
  "message": "Device created successfully",
  "status": "success"
}
```

#### デバイス更新
```http
PUT /api/v2/device/{deviceId}
```

#### デバイス削除
```http
DELETE /api/v2/device/{deviceId}
```

### センサーデータ

#### センサーデータ送信
```http
POST /api/v2/device/{deviceId}/sensor/value
```

**リクエストボディ:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "values": {
    "temperature": 24.1,
    "humidity": 66.8,
    "pressure": 1013.25
  }
}
```

#### センサーデータ取得
```http
GET /api/v2/device/{deviceId}/sensor/value
```

**クエリパラメータ:**
- `from`: 開始日時 (ISO 8601)
- `to`: 終了日時 (ISO 8601)
- `limit`: 取得件数上限 (デフォルト: 100)
- `sensor_type`: センサータイプフィルタ

**例:**
```bash
curl "http://localhost:1880/api/v2/device/device_001/sensor/value?from=2024-01-01T00:00:00Z&to=2024-01-01T23:59:59Z&limit=50"
```

**レスポンス:**
```json
{
  "device_id": "device_001",
  "data": [
    {
      "timestamp": "2024-01-01T12:00:00Z",
      "sensor_type": "temperature",
      "value": 23.5,
      "unit": "℃"
    },
    {
      "timestamp": "2024-01-01T12:01:00Z", 
      "sensor_type": "temperature",
      "value": 23.7,
      "unit": "℃"
    }
  ],
  "total": 2
}
```

#### 全デバイスデータ取得
```http
GET /api/v2/device/sensor/value
```

### デバイス制御

#### デジタル出力制御
```http
POST /api/v2/device/{deviceId}/output
```

**リクエストボディ:**
```json
{
  "channel": 1,
  "value": true,
  "duration": 5000
}
```

**レスポンス:**
```json
{
  "device_id": "device_001",
  "channel": 1,
  "status": "success",
  "message": "Output activated"
}
```

### センサータイプ管理

#### センサータイプ一覧
```http
GET /api/v2/sensor
```

**レスポンス:**
```json
{
  "sensor_types": [
    {
      "id": 257,
      "name": "接点入力",
      "unit": "-",
      "range": "0-1"
    },
    {
      "id": 259,
      "name": "ADC",
      "unit": "mV", 
      "range": "±2000"
    }
  ]
}
```

#### センサータイプ登録
```http
POST /api/v2/sensor
```

### システム情報

#### システム状態
```http
GET /api/v2/system/status
```

**レスポンス:**
```json
{
  "status": "healthy",
  "uptime": 86400,
  "services": {
    "node_red": "running",
    "mariadb": "running", 
    "influxdb": "running",
    "mqtt": "running"
  },
  "resources": {
    "cpu_usage": 15.2,
    "memory_usage": 512,
    "disk_usage": 2048
  }
}
```

#### ヘルスチェック
```http
GET /api/v2/health
```

**レスポンス:**
```json
{
  "status": "OK",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## エラーレスポンス

### エラーコード

| ステータスコード | 説明 |
|-----------------|------|
| 400 | Bad Request - リクエスト形式エラー |
| 401 | Unauthorized - 認証エラー |
| 403 | Forbidden - 権限エラー |
| 404 | Not Found - リソースが見つからない |
| 422 | Unprocessable Entity - バリデーションエラー |
| 500 | Internal Server Error - サーバー内部エラー |

### エラーレスポンス形式

```json
{
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "Device with ID 'device_999' not found",
    "details": {
      "device_id": "device_999",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  }
}
```

## レート制限

| エンドポイント | 制限 |
|---------------|------|
| GET系 | 100 requests/minute |
| POST/PUT/DELETE | 60 requests/minute |
| センサーデータ送信 | 1000 requests/minute |

制限超過時のレスポンス:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

## SDKとサンプルコード

### Python SDK
```python
import requests
from datetime import datetime

class IoTKitAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_devices(self):
        response = requests.get(f"{self.base_url}/device", headers=self.headers)
        return response.json()
    
    def send_sensor_data(self, device_id, data):
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "values": data
        }
        response = requests.post(
            f"{self.base_url}/device/{device_id}/sensor/value",
            json=payload,
            headers=self.headers
        )
        return response.json()

# 使用例
api = IoTKitAPI("http://localhost:1880/api/v2", "your-api-key")
devices = api.get_devices()
result = api.send_sensor_data("device_001", {"temperature": 25.3})
```

### JavaScript SDK
```javascript
class IoTKitAPI {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async getDevices() {
        const response = await fetch(`${this.baseUrl}/device`, {
            headers: this.headers
        });
        return response.json();
    }
    
    async sendSensorData(deviceId, data) {
        const payload = {
            timestamp: new Date().toISOString(),
            values: data
        };
        const response = await fetch(`${this.baseUrl}/device/${deviceId}/sensor/value`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });
        return response.json();
    }
}

// 使用例
const api = new IoTKitAPI('http://localhost:1880/api/v2', 'your-api-key');
const devices = await api.getDevices();
const result = await api.sendSensorData('device_001', {temperature: 25.3});
```

## 関連資料
- [WebSocket API](./websocket.md)
- [MQTT トピック仕様](./mqtt-topics.md)
- [API使用例](./examples/)
- [認証・セキュリティ](../guides/security.md)