# Node-RED詳細技術分析ドキュメント

## 目次
1. [システム概要](#システム概要)
2. [フロー構成](#フロー構成)
3. [データベース設計](#データベース設計)
4. [通信プロトコル](#通信プロトコル)
5. [API設計](#api設計)
6. [センサー管理](#センサー管理)
7. [ダッシュボードUI](#ダッシュボードui)
8. [データ処理ロジック](#データ処理ロジック)

## システム概要

IoT導入支援キット Ver.4.1のNode-REDシステムは、多様なセンサータイプとプロトコルをサポートする包括的なIoTプラットフォームです。BravePI・BraveJIGハードウェアを中心とした産業用IoTシステムの中核として機能します。

### システム要件
- **Node-RED**: IoTワークフローの中核エンジン
- **MariaDB**: デバイス・センサー設定の管理
- **InfluxDB**: 時系列センサーデータの蓄積
- **MQTT Broker**: リアルタイム通信
- **Web Dashboard**: ユーザーインターフェース

## フロー構成

### 1. PI・JIG・I2C・GPIO（ハードウェアインターフェース）

**目的**: BravePI/BraveJIGデバイスとの直接通信とGPIO制御

#### シリアル通信設定
```javascript
// シリアルポート設定
{
  "serialport": "/dev/ttyAMA0",
  "serialbaud": "38400",
  "databits": "8",
  "parity": "none",
  "stopbits": "1",
  "bin": "bin",
  "out": "time",
  "addchar": "100"
}
```

#### GPIO設定詳細
| Pin番号 | 方向 | 用途 | デバウンス | プルアップ |
|---------|------|------|------------|------------|
| BCM16 | Input | 接点センサー1 | 25ms | 有効 |
| BCM25 | Input | 接点センサー2 | 25ms | 有効 |
| BCM05 | Input | 接点センサー3 | 25ms | 有効 |
| BCM23 | Input | 接点センサー4 | 25ms | 有効 |
| BCM18 | Input | 接点センサー5 | 25ms | 有効 |
| BCM06 | Output | 制御出力1 | - | - |
| BCM13 | Output | 制御出力2 | - | - |
| BCM17 | Output | 制御出力3 | - | - |
| BCM24 | Output | 制御出力4 | - | - |
| BCM27 | Output | 制御出力5 | - | - |

#### MQTT通信トピック
```javascript
// 使用されるMQTTトピック
const topics = [
  "DwlResp/+",     // ダウンリンク応答
  "JIResp/+",      // JIG応答
  "UlReq/+",       // アップリンク要求
  "ErrResp/+",     // エラー応答
  "DfuResp/+"      // DFU応答
];
```

### 2. デバイス登録（Device Registration）

**目的**: 多様なIoTデバイスの自動検出・登録・管理

#### サポートアクセスタイプ
```javascript
const accessTypes = {
  0: "Bluetooth",     // BravePI送信機
  1: "I2C",          // I2Cセンサー直接接続
  3: "LAN",          // ネットワーク接続デバイス
  4: "USB"           // BraveJIG USBモジュール
};
```

#### デバイス登録SQL
```sql
-- デバイス基本情報登録
INSERT INTO `devices` (
  `device_name`, `device_number`, `access_type`, `sensor_type`
) VALUES (?, ?, ?, ?);

-- I2Cデバイス設定
INSERT INTO `i2c_device_configs` (
  `device_id`, `address`, `measurement_interval`
) VALUES (?, ?, ?);

-- BLEデバイス設定
INSERT INTO `ble_device_configs` (
  `device_id`, `adv_interval`, `uplink_interval`, `measurement_interval`
) VALUES (?, ?, ?, ?);
```

#### センサー設定パラメータ
```javascript
const sensorConfig = {
  channel: "測定チャンネル名",
  channelIndex: "チャンネルインデックス",
  toggle: "トグル動作の有効化",
  hysteresisHigh: "ヒステリシス上限閾値",
  hysteresisLow: "ヒステリシス下限閾値",
  offset: "オフセット補正値",
  debounceHigh: "上限デバウンス時間",
  debounceLow: "下限デバウンス時間",
  takePhoto: "写真撮影トリガー",
  extraMqtt: "追加MQTT発行設定"
};
```

### 3. センサーログ（Sensor Logging）

**目的**: 履歴データの取得・可視化・エクスポート

#### InfluxDBクエリパターン
```flux
// 基本センサーデータクエリ
from(bucket:"iotkit")
  |> range(start: ${startTime}, stop: ${endTime})
  |> filter(fn: (r) => r._measurement == "${measurement}")
  |> filter(fn: (r) => r.device_id == "${deviceId}")
  |> filter(fn: (r) => r.sensor_id == "${sensorId}")
  |> window(every: ${aggregationWindow}s)
  |> ${aggregationFunction}()
  |> group(columns: ["device_id", "sensor_id", "channel"])
  |> sort(columns: ["_time"])

// カウントデータ専用クエリ
from(bucket:"iotkit")
  |> range(start: ${startTime}, stop: ${endTime})
  |> filter(fn: (r) => r._measurement == "count")
  |> difference(nonNegative: false)
  |> map(fn: (r) => ({r with _value: math.abs(x: r._value)}))
```

#### ログタイプ別処理

**1. センサーログ**
- 時系列データの統計処理（mean, median, min, max, first, last）
- 時間窓での集計（秒〜時間単位）
- CSV/XLSX形式でのエクスポート

**2. カウントログ**
- イベント発生回数の追跡
- 差分計算による増分カウント
- 頻度解析とパターン検出

**3. スペクトログラムログ**
- 振動・音響データの周波数解析
- FFT処理による周波数成分抽出
- リアルタイム周波数可視化

### 4. BLEトランスミッター（BLE Transmitter）

**目的**: Bluetooth Low Energyデバイスの電力管理と設定同期

#### 電力管理コマンド
```javascript
// スリープコマンド送信
const sleepCommand = {
  topic: `DwlReq/${deviceNumber}`,
  payload: {
    type: "sleep",
    duration: sleepDuration
  }
};

// 復帰コマンド送信
const resumeCommand = {
  topic: `DwlReq/${deviceNumber}`,
  payload: {
    type: "resume"
  }
};
```

#### 設定同期
```javascript
// デバイス設定取得
const getConfigCommand = {
  topic: `DwlReq/${deviceNumber}`,
  payload: {
    type: "getConfig"
  }
};

// パラメータ設定
const setConfigCommand = {
  topic: `DwlReq/${deviceNumber}`,
  payload: {
    type: "setConfig",
    advertiseInterval: 1000,  // ms
    uplinkInterval: 60000,    // ms
    measurementInterval: 10000 // ms
  }
};
```

## データベース設計

### MariaDBスキーマ詳細

#### 主要テーブル構造

**devices テーブル**
```sql
CREATE TABLE `devices` (
  `device_id` INT AUTO_INCREMENT PRIMARY KEY,
  `device_name` VARCHAR(255) NOT NULL UNIQUE,
  `device_number` VARCHAR(16),
  `access_type` TINYINT,
  `sensor_type` SMALLINT,
  `i2c` BOOLEAN DEFAULT FALSE,
  `gpio` BOOLEAN DEFAULT FALSE,
  `serial` BOOLEAN DEFAULT FALSE,
  `ble` BOOLEAN DEFAULT FALSE,
  `http` BOOLEAN DEFAULT FALSE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**sensors テーブル**
```sql
CREATE TABLE `sensors` (
  `sensor_id` INT AUTO_INCREMENT PRIMARY KEY,
  `device_id` INT,
  `sensor_type_id` SMALLINT,
  `channel` VARCHAR(50),
  `channel_index` TINYINT,
  `toggle` BOOLEAN DEFAULT FALSE,
  `hysteresis_high` FLOAT DEFAULT 0.0,
  `hysteresis_low` FLOAT DEFAULT 0.0,
  `offset` FLOAT DEFAULT 0.0,
  `debounce_high` INT DEFAULT 0,
  `debounce_low` INT DEFAULT 0,
  `take_photo` TINYINT DEFAULT 0,
  `extra_mqtt` BOOLEAN DEFAULT FALSE,
  `invert` BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`)
);
```

#### 通信プロトコル別設定テーブル

**I2C設定**
```sql
CREATE TABLE `i2c_device_configs` (
  `device_id` INT PRIMARY KEY,
  `address` VARCHAR(4),           -- 0x48形式
  `measurement_interval` INT DEFAULT 1000,
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`)
);
```

**BLE設定**
```sql
CREATE TABLE `ble_device_configs` (
  `device_id` INT PRIMARY KEY,
  `adv_interval` INT DEFAULT 1000,
  `uplink_interval` INT DEFAULT 60000,
  `measurement_interval` INT DEFAULT 10000,
  `tx_power` TINYINT DEFAULT 0,
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`)
);
```

#### 連携設定テーブル

**MQTT連携**
```sql
CREATE TABLE `sensor_mqtt_pivots` (
  `sensor_id` INT,
  `mqtt_topic_id` INT,
  PRIMARY KEY (`sensor_id`, `mqtt_topic_id`),
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`),
  FOREIGN KEY (`mqtt_topic_id`) REFERENCES `mqtt_topics`(`mqtt_topic_id`)
);
```

**GPIO連携**
```sql
CREATE TABLE `sensor_gpio_output_pivots` (
  `sensor_id` INT,
  `gpio_output_sensor_id` INT,
  `channel_index` TINYINT,
  PRIMARY KEY (`sensor_id`, `gpio_output_sensor_id`, `channel_index`),
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`)
);
```

## 通信プロトコル

### シリアル通信プロトコル

#### フレーム構造
```
+----------+----------+----------+----------+----------+----------+
| Protocol | Type     | Length   | Timestamp| Device # | Data...  |
| (1 byte) | (1 byte) | (2 bytes)| (4 bytes)| (8 bytes)| (n bytes)|
+----------+----------+----------+----------+----------+----------+
```

#### メッセージタイプ
```javascript
const messageTypes = {
  0x00: "General",      // 一般データ
  0x01: "Downlink",     // ダウンリンク要求
  0x02: "JIG Info",     // JIG情報
  0x03: "DFU",          // ファームウェア更新
  0xFF: "Error"         // エラー応答
};
```

#### データ解析処理
```javascript
function parseMessage(buffer) {
  const protocol = buffer.readUInt8(0);
  const type = buffer.readUInt8(1);
  const length = buffer.readUInt16LE(2);
  const timestamp = buffer.readUInt32LE(4);
  const deviceNumber = buffer.readBigUInt64LE(8);
  
  if (length > 16) {
    const sensorType = buffer.readUInt16LE(16);
    const rssi = buffer.readInt8(18);
    const order = buffer.readUInt16LE(19);
    const data = buffer.slice(21, 4 + length);
    
    return {
      protocol, type, timestamp, deviceNumber,
      sensorType, rssi, order, data
    };
  }
  
  return { protocol, type, timestamp, deviceNumber };
}
```

### MQTT通信設定

#### ブローカー設定
```javascript
const mqttConfig = {
  host: "localhost",
  port: 1883,
  protocol: "mqtt",
  keepalive: 60,
  clean: true,
  username: "iotkit",
  password: "iotkit-password"
};
```

#### トピック管理
```javascript
// デバイス通信トピック
const deviceTopics = {
  downlinkRequest: "DwlReq/{deviceNumber}",
  downlinkResponse: "DwlResp/{deviceNumber}",
  uplinkRequest: "UlReq/{deviceNumber}",
  jigResponse: "JIResp/{deviceNumber}",
  errorResponse: "ErrResp/{deviceNumber}",
  dfuResponse: "DfuResp/{deviceNumber}"
};

// センサーデータトピック（動的生成）
const sensorTopic = `sensor/${deviceId}/${sensorId}/${channel}`;
```

## API設計

### RESTful API エンドポイント

#### デバイス管理API
```javascript
// デバイス情報取得
GET /api/v2/device/:deviceId
Response: {
  deviceId: number,
  deviceName: string,
  deviceNumber: string,
  accessType: number,
  sensorType: number,
  sensors: [{
    sensorId: number,
    channel: string,
    channelIndex: number,
    // ... sensor configuration
  }]
}

// デバイス削除
DELETE /api/v2/device/:deviceId
Response: { success: boolean, message: string }

// センサー値取得
GET /api/v2/device/:deviceId/sensor/value
Response: {
  deviceId: number,
  values: [{
    sensorId: number,
    channel: string,
    value: number,
    timestamp: string,
    unit: string
  }]
}
```

#### センサータイプ管理API
```javascript
// センサータイプ一覧取得
GET /api/v2/sensor/type
Response: [{
  sensorTypeId: number,
  typeName: string,
  unit: string,
  channels: [{
    channelName: string,
    channelIndex: number,
    dataType: string,
    range: { min: number, max: number }
  }]
}]
```

### エラーハンドリング

#### APIエラーレスポンス
```javascript
const errorResponse = {
  error: {
    code: "DEVICE_NOT_FOUND",
    message: "指定されたデバイスが見つかりません",
    details: {
      deviceId: 123,
      timestamp: "2025-01-01T00:00:00Z"
    }
  }
};
```

## センサー管理

### センサータイプ定義

#### 主要センサータイプ
```javascript
const sensorTypes = {
  257: {
    name: "接点入力",
    unit: "",
    channels: ["signal"],
    dataType: "boolean"
  },
  258: {
    name: "接点出力", 
    unit: "",
    channels: ["signal"],
    dataType: "boolean"
  },
  259: {
    name: "ADC",
    unit: "mV",
    channels: ["ch1", "ch2"],
    range: { min: -2000, max: 2000 },
    resolution: 16
  },
  260: {
    name: "測距",
    unit: "mm",
    channels: ["distance"],
    range: { min: 0, max: 2000 },
    accuracy: "±3mm"
  },
  261: {
    name: "熱電対",
    unit: "℃",
    channels: ["temperature"],
    range: { min: -50, max: 2000 },
    thermocoupleTypes: ["K", "J", "T", "N", "S", "E", "B", "R"]
  },
  262: {
    name: "加速度",
    unit: "G",
    channels: ["x", "y", "z", "composite"],
    range: { min: -6.5, max: 6.5 },
    resolution: "16-bit"
  },
  263: {
    name: "差圧",
    unit: "Pa",
    channels: ["pressure"],
    range: { min: -500, max: 500 }
  },
  264: {
    name: "照度",
    unit: "lux",
    channels: ["illuminance"],
    range: { min: 40, max: 83865 }
  }
};
```

### データ処理ロジック

#### ヒステリシス制御
```javascript
function processHysteresis(value, sensor, currentState) {
  if (sensor.toggle) {
    if (currentState) {
      // HIGH状態からの判定
      if (value < sensor.hysteresisLow) {
        return { newState: false, changed: true };
      }
    } else {
      // LOW状態からの判定
      if (value >= sensor.hysteresisHigh) {
        return { newState: true, changed: true };
      }
    }
  }
  return { newState: currentState, changed: false };
}
```

#### デバウンス処理
```javascript
function processDebounce(sensorId, newState, debounceTime) {
  const key = `debounce_${sensorId}`;
  const now = Date.now();
  
  if (global.get(key)) {
    clearTimeout(global.get(key));
  }
  
  const timeoutId = setTimeout(() => {
    // デバウンス時間経過後に状態確定
    global.set(`state_${sensorId}`, newState);
    global.set(key, null);
    
    // 後続処理をトリガー
    node.send({ payload: { sensorId, state: newState } });
  }, debounceTime);
  
  global.set(key, timeoutId);
}
```

#### 値の正規化と補正
```javascript
function normalizeValue(rawValue, sensor) {
  // オフセット補正
  let corrected = rawValue + sensor.offset;
  
  // 反転処理
  if (sensor.invert) {
    corrected = -corrected;
  }
  
  // 精度調整
  const precision = sensor.precision || 2;
  corrected = Math.round(corrected * Math.pow(10, precision)) / Math.pow(10, precision);
  
  return corrected;
}
```

## ダッシュボードUI

### UI設定
```javascript
const uiConfig = {
  theme: {
    name: "theme-light",
    default: "#0068b3",
    baseColor: "#0068b3",
    baseFont: "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen-Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif"
  },
  site: {
    name: "IoT導入支援キット Ver.4.1",
    hideToolbar: false,
    allowSwipe: true,
    lockMenu: false,
    allowTempTheme: true
  }
};
```

### リアルタイム可視化

#### チャートコンポーネント
```javascript
// リアルタイムラインチャート設定
const chartConfig = {
  type: "line",
  data: {
    datasets: [{
      label: "センサー値",
      borderColor: "#0068b3",
      backgroundColor: "rgba(0, 104, 179, 0.1)",
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      x: {
        type: "time",
        time: {
          displayFormats: {
            second: "HH:mm:ss"
          }
        }
      },
      y: {
        beginAtZero: true
      }
    }
  }
};
```

### バージョン情報
```javascript
const systemInfo = {
  version: "Ver.4.1.0-Raspi4 (2025-05-26)",
  copyright: "© 2020-2025 Fukuoka Industrial Technology Center",
  build: "Production",
  platform: "Raspberry Pi 4"
};
```

## まとめ

このNode-REDシステムは、産業用IoTアプリケーションに特化した包括的なプラットフォームを提供します。多様なセンサータイプ、通信プロトコル、データ処理機能を統合し、リアルタイム監視から履歴分析まで幅広いユースケースに対応できる設計となっています。

特に、ヒステリシス制御、デバウンス処理、MQTT連携、GPIO制御など、産業現場で必要な機能を標準装備しており、Raspberry Pi上での安定動作を実現しています。