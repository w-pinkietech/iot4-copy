# REST API リファレンス

## 概要

IoT導入支援キット Ver.4.1のREST API仕様について説明します。このAPIを使用して、外部システムからデバイス管理、センサーデータ操作を行うことができます。

## ベースURL

```
http://localhost:1880/api/v2
```

## 認証

**注意**: 現在の実装では認証は実装されていません。将来的なセキュリティ強化のため、本番環境では適切な認証機構の実装を推奨します。

## 実装済みエンドポイント一覧

### デバイス管理

#### デバイス一覧取得
```http
GET /api/v2/device
```

**レスポンス例:**
```json
[
  {
    "device_id": "device_001",
    "device_name": "センサーノード1",
    "device_type": "sensor_node",
    "created_at": "2024-01-01T12:00:00Z"
  }
]
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
  "device_id": "device_001",
  "device_name": "センサーノード1",
  "device_type": "sensor_node",
  "sensors": [
    {
      "sensor_id": 1,
      "sensor_type": 257,
      "sensor_name": "接点入力1"
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
  "device_name": "新しいセンサー",
  "device_type": "temperature_sensor",
  "sensors": [
    {
      "sensor_type": 259,
      "sensor_name": "ADCセンサー"
    }
  ]
}
```

**レスポンス:**
```json
{
  "device_id": "device_002",
  "message": "Device created successfully"
}
```

#### デバイス削除
```http
DELETE /api/v2/device/{deviceId}
```

**パラメータ:**
- `deviceId`: デバイスID

**レスポンス:**
```json
{
  "message": "Device deleted successfully"
}
```

### センサーデータ

#### センサーデータ取得
```http
GET /api/v2/device/{deviceId}/sensor/value
```

**パラメータ:**
- `deviceId`: デバイスID

**レスポンス例:**
```json
{
  "device_id": "device_001",
  "values": [
    {
      "sensor_id": 1,
      "sensor_type": 257,
      "value": 1,
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### センサーデータ送信
```http
POST /api/v2/device/{deviceId}/sensor/value
```

**リクエストボディ:**
```json
{
  "sensor_id": 1,
  "value": 1
}
```

**レスポンス:**
```json
{
  "message": "Sensor value updated"
}
```

#### センサーログ取得
```http
GET /api/v2/device/sensor/log
```

**クエリパラメータ (オプション):**
- `device_id`: デバイスIDでフィルタ
- `sensor_type`: センサータイプでフィルタ
- `limit`: 取得件数制限

**レスポンス例:**
```json
[
  {
    "device_id": "device_001",
    "sensor_id": 1,
    "sensor_type": 257,
    "value": 1,
    "timestamp": "2024-01-01T12:00:00Z"
  }
]
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
  "value": 1
}
```

**レスポンス:**
```json
{
  "device_id": "device_001",
  "channel": 1,
  "value": 1,
  "message": "Output updated"
}
```

### センサータイプ管理

#### センサータイプ一覧取得
```http
GET /api/v2/sensor
```

**レスポンス:**
```json
[
  {
    "sensor_type": 257,
    "type_name": "接点入力",
    "unit": "-"
  },
  {
    "sensor_type": 259,
    "type_name": "ADC",
    "unit": "mV"
  }
]
```

#### 特定センサータイプ取得
```http
GET /api/v2/sensor/{sensorType}
```

**パラメータ:**
- `sensorType`: センサータイプID (257-264, 289-293)

**レスポンス:**
```json
{
  "sensor_type": 257,
  "type_name": "接点入力",
  "unit": "-",
  "description": "デジタル入力（ON/OFF）"
}
```

## エラーレスポンス

### 一般的なエラー形式

```json
{
  "error": "エラーメッセージ"
}
```

### HTTPステータスコード

| ステータスコード | 説明 |
|-----------------|------|
| 200 | 成功 |
| 400 | Bad Request - リクエスト形式エラー |
| 404 | Not Found - リソースが見つからない |
| 500 | Internal Server Error - サーバー内部エラー |

## 実装上の注意事項

### 未実装機能

以下の機能は現在の実装には含まれていません：

1. **認証・認可機能**
   - APIキー認証
   - Basic認証
   - アクセス制御

2. **レート制限**
   - リクエスト数制限
   - 帯域幅制限

3. **高度な機能**
   - ページネーション
   - 詳細なクエリフィルタ
   - バッチ操作

4. **システム管理エンドポイント**
   - システム状態 (`/api/v2/system/status`)
   - ヘルスチェック (`/api/v2/health`)

5. **デバイス更新API**
   - PUT `/api/v2/device/{deviceId}`

### データベース構造

APIは以下のMariaDBテーブルと連携しています：

- `devices`: デバイス基本情報
- `sensors`: センサー設定
- `sensor_types`: センサータイプ定義
- `sensor_logs`: センサーデータログ（InfluxDBも併用）

### 使用例

#### cURLでのデバイス一覧取得
```bash
curl http://localhost:1880/api/v2/device
```

#### cURLでのセンサーデータ送信
```bash
curl -X POST http://localhost:1880/api/v2/device/device_001/sensor/value \
  -H "Content-Type: application/json" \
  -d '{"sensor_id": 1, "value": 1}'
```

#### Node.jsでの使用例
```javascript
const fetch = require('node-fetch');

// デバイス一覧取得
async function getDevices() {
    const response = await fetch('http://localhost:1880/api/v2/device');
    return await response.json();
}

// センサーデータ送信
async function sendSensorData(deviceId, sensorId, value) {
    const response = await fetch(`http://localhost:1880/api/v2/device/${deviceId}/sensor/value`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sensor_id: sensorId,
            value: value
        })
    });
    return await response.json();
}
```

## 関連資料
- [システムアーキテクチャ](../architecture/system-overview.md)
- [センサータイプ仕様](../analysis/sensor-data-samples.md)
- [Node-REDフロー詳細](../architecture/node-red-flows.md)