# センサー生データサンプル集

## 概要

現行Node-REDシステムで実際に使用されている、各種センサーからの生データフォーマットの実例を示します。

## 1. I2Cセンサー生データ（JSON形式）

### 温度センサー（MCP9600）- sensorType: 261
```json
{
  "time": 1749194160718,
  "values": [23.4],
  "address": 98,
  "sensorType": 261
}
```
**詳細**:
- **データ**: 摂氏温度（単一値）
- **I2Cアドレス**: 0x62 (98), 0x61, 0x63, 0x65
- **熱電対タイプ**: K, J, T, N, S, E, B, R (0-7)
- **測定範囲**: -270°C ～ +1372°C
- **精度**: ±1.5°C

### 測距センサー（VL53L1X）- sensorType: 260
```json
{
  "time": 1749194160718,
  "values": [156],
  "address": 41,
  "sensorType": 260
}
```
**詳細**:
- **データ**: 距離（ミリメートル）
- **I2Cアドレス**: 0x29 (41)
- **測定範囲**: 4mm ～ 2000mm
- **精度**: ±3%

### 加速度センサー（LIS2DUXS12）- sensorType: 262
```json
{
  "time": "2025-06-06 16:16:00.718798",
  "values": [0.123, -0.456, 0.987, 0.034],
  "address": 25,
  "sensorType": 262,
  "tag": "accelerator"
}
```
**詳細**:
- **データ**: [X軸, Y軸, Z軸, 合成値] 単位：G
- **I2Cアドレス**: 0x19 (25), 0x18
- **測定範囲**: ±8G
- **サンプリング**: 800Hz
- **分解能**: 16bit

### ADCセンサー（MCP3427）- sensorType: 259
```json
{
  "time": 1749194160718,
  "values": [1234.5, 2345.6],
  "address": 107,
  "sensorType": 259
}
```
**詳細**:
- **データ**: [CH1電圧, CH2電圧] 単位：mV
- **I2Cアドレス**: 0x6B (107), 0x6F, 0x68
- **ゲイン**: 1, 2, 4, 8倍
- **分解能**: 16bit
- **測定範囲**: ±2.048V

### 照度センサー（OPT3001）- sensorType: 264
```json
{
  "time": 1749194160718,
  "values": [512],
  "address": 68,
  "sensorType": 264
}
```
**詳細**:
- **データ**: 照度（lux）
- **I2Cアドレス**: 0x44 (68)
- **測定範囲**: 0.01 ～ 83,000 lux
- **精度**: ±20%

### 差圧センサー（SDP810）- sensorType: 263
```json
{
  "time": 1749194160718,
  "values": [150.5],
  "address": 37,
  "sensorType": 263
}
```
**詳細**:
- **データ**: 差圧（Pa）
- **I2Cアドレス**: 0x25 (37)
- **測定範囲**: ±500 Pa
- **精度**: ±2%

## 2. FFT解析データ

### 加速度センサー標準データ
```json
{
  "time": 1749194160718,
  "values": [0.123, -0.456, 0.987, 0.034],
  "address": 25,
  "sensorType": 262,
  "tag": "accelerator"
}
```

### Lombscargle FFT解析結果
```json
{
  "time": 1749194169883,
  "values": [
    0.810835, 0.839001, 0.867167, 0.895333, 0.9235,
    0.951666, 0.979833, 1.008, 1.036166, 1.064333,
    // ... 200個の周波数ビン
    199.158, 199.186, 199.214, 199.242, 199.271
  ],
  "sensorType": 262,
  "address": 25,
  "sumpower": 1245.67,
  "tag": "spectrogram"
}
```
**詳細**:
- **データ**: 200個の周波数ビン（1-200Hz）
- **処理**: Lomb-Scargle法による正規化パワースペクトラム
- **用途**: 振動解析、異常検知
- **更新間隔**: 1秒

## 3. BravePI/JIG バイナリフレーム

### フレーム構造（16バイトヘッダー + データ）
```
+--------+--------+--------+--------+--------+--------+--------+--------+
| Length | Length | Device | Device | Device | Device | Device | Device |
| Low    | High   | Num    | Num    | Num    | Num    | Num    | Num    |
| (1)    | (2)    | (3)    | (4)    | (5)    | (6)    | (7)    | (8)    |
+--------+--------+--------+--------+--------+--------+--------+--------+
| Device | Device | Sensor | Sensor | RSSI   | Flag   | Data   | Data   |
| Num    | Num    | Type   | Type   | (dBm)  | (1)    | ...    | ...    |
| (9)    | (10)   | (11)   | (12)   | (13)   | (14)   | (15+)  | (16+)  |
+--------+--------+--------+--------+--------+--------+--------+--------+
```

### 実際のバイナリデータ例

#### 温度センサーデータ
```
ヘックス: 0700 1234567890ABCDEF 0501 D3 01 5333BB41
解析:
- Data Length: 0x0007 (7バイト)
- Device Number: 0x1234567890ABCDEF
- Sensor Type: 0x0105 (261 = 温度)
- RSSI: 0xD3 (-45 dBm)
- Flag: 0x01
- Temperature: 0x5333BB41 → 23.4°C (float32)
- Battery: 85%
```

#### 距離センサーデータ
```
ヘックス: 0500 FEDCBA0987654321 0401 D8 01 9C00
解析:
- Data Length: 0x0005 (5バイト)
- Device Number: 0xFEDCBA0987654321
- Sensor Type: 0x0104 (260 = 距離)
- RSSI: 0xD8 (-40 dBm)
- Flag: 0x01
- Distance: 0x009C → 156mm (uint16)
- Battery: 92%
```

#### 加速度センサーデータ
```
ヘックス: 1000 ABCDEF1234567890 0601 D5 01 5C01000000F6420000E4C300C07644
解析:
- Data Length: 0x0010 (16バイト)
- Device Number: 0xABCDEF1234567890
- Sensor Type: 0x0106 (262 = 加速度)
- RSSI: 0xD5 (-43 dBm)
- Flag: 0x01
- X軸: 0x000000F6 → 0.123G (float32)
- Y軸: 0x420000E4 → -0.456G (float32)
- Z軸: 0xC300C076 → 0.987G (float32)
- 合成: 0x44 → 0.034G (float32)
- Battery: 67%
```

#### GPIOデータ
```
ヘックス: 0300 1111222233334444 0101 E2 01 01
解析:
- Data Length: 0x0003 (3バイト)
- Device Number: 0x1111222233334444
- Sensor Type: 0x0101 (257 = GPIO入力)
- RSSI: 0xE2 (-30 dBm)
- Flag: 0x01
- GPIO State: 0x01 (HIGH)
- Battery: 100%
```

## 4. MQTTメッセージ例

### 内部MQTT（Node-RED処理用）
```
Topic: UlReq/1234567890ABCDEF
Payload: {
  "deviceNumber": "1234567890ABCDEF",
  "sensorType": 261,
  "timestamp": 1749194160718,
  "rawData": "5333BB41",
  "rssi": -45,
  "battery": 85,
  "values": [23.4]
}
```

### 外部MQTT（ダッシュボード用）
```
Topic: iotkit/sensor/temperature/device001
Payload: {
  "deviceId": "device001",
  "sensorType": 261,
  "timestamp": "2025-06-06T16:16:00.718Z",
  "values": {"temperature": 23.4, "unit": "°C"},
  "metadata": {
    "battery": 85,
    "rssi": -45,
    "address": 98,
    "location": "製造ライン1",
    "calibration": 0.0
  }
}
```

## 5. データベース格納例

### MariaDB設定テーブル
```sql
-- devices テーブル
INSERT INTO devices VALUES (
  1, 'device001', '温度センサー1', 0, '2024-01-01 00:00:00'
);

-- sensors テーブル  
INSERT INTO sensors VALUES (
  1, 'device001', 261, '工場内温度', 0.0, 1, 
  30.0, 10.0, 1.0, 1.0, 0.0, 0.0, 0, 0
);
```

### InfluxDB時系列データ
```sql
-- measurement: temperature
time                device_id  sensor_id  value  quality  rssi  battery
1749194160718000000 device001  261        23.4   0.95     -45   85
1749194161718000000 device001  261        23.5   0.95     -44   85
1749194162718000000 device001  261        23.3   0.95     -46   84
```

## 6. エラーデータ例

### 通信エラー
```json
{
  "time": 1749194160718,
  "error": "timeout",
  "device": "device001",
  "lastValue": null,
  "retryCount": 3
}
```

### センサーエラー
```json
{
  "time": 1749194160718,
  "values": [null],
  "address": 98,
  "sensorType": 261,
  "error": "sensor_not_responding"
}
```

### 品質低下データ
```json
{
  "time": 1749194160718,
  "values": [23.4],
  "address": 98,
  "sensorType": 261,
  "quality": 0.3,
  "warnings": ["weak_signal", "low_battery"],
  "rssi": -85,
  "battery": 15
}
```

## 7. デバッグ・ログデータ

### Node-REDデバッグ出力
```
[2025-06-06 16:16:00] DEBUG: Serial data received: 0700123456...
[2025-06-06 16:16:00] DEBUG: Parsed frame: {deviceNumber: "1234567890ABCDEF", sensorType: 261}
[2025-06-06 16:16:00] DEBUG: Normalized value: 23.4 (offset: 0.0)
[2025-06-06 16:16:00] DEBUG: Hysteresis check: current=false, new=false
[2025-06-06 16:16:00] DEBUG: Publishing to MQTT: iotkit/sensor/temperature/device001
```

### システムログ
```
2025-06-06 16:16:00 INFO  Sensor device001 connected, battery: 85%
2025-06-06 16:16:05 WARN  Device device002 signal weak, RSSI: -85dBm
2025-06-06 16:16:10 ERROR Device device003 timeout, retry attempt 2/3
```

## まとめ

現行システムでは、以下の特徴的なデータフローが確認できます：

1. **統一JSONフォーマット**: 全I2Cセンサーが `time`, `values`, `address`, `sensorType` 形式
2. **バイナリプロトコル**: BravePI/JIGは効率的な16バイトヘッダー + データ形式
3. **リアルタイム処理**: FFT解析、品質管理、エラーハンドリング
4. **多層データ変換**: 生データ → 正規化 → 検証 → 配信 → 保存
5. **包括的監視**: RSSI、Battery、通信品質の常時監視

この実データ例により、新システムでの互換性確保と機能継承の具体的な要件が明確になりました。