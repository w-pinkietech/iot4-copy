# プログラム実行時アーキテクチャ

## 概要

IoT導入支援キット Ver.4.1のRaspberry Pi上で実行されているプログラムとその動作について詳細に説明します。本システムは、複数のセンサーデバイスからデータを収集し、Node-REDを中心としたデータ処理パイプラインで処理します。

## 実行プログラム一覧

### 1. Pythonセンサードライバー

I2C接続されたセンサーを制御し、定期的にデータを取得するPythonプログラムが実行されています。

| ファイル名 | センサー | 機能 | 実行間隔 |
|-----------|---------|------|----------|
| `lis2duxs12.py` | LIS2DUXS12 | 3軸加速度測定（±8G、800Hz） | 1秒 |
| `vl53l1x.py` | VL53L1X | ToF距離測定（4mm～2m） | 1秒 |
| `opt3001.py` | OPT3001 | 照度測定（0.01～83,000 lux） | 1秒 |
| `mcp3427.py` | MCP3427 | 2ch ADC電圧測定（16bit） | 1秒 |
| `mcp9600.py` | MCP9600 | 熱電対温度測定（-270～+1372°C） | 1秒 |
| `sdp810.py` | SDP810-500 | 差圧測定（±500 Pa） | 1秒 |
| `lombscargle.py` | - | 加速度データのFFT解析 | リアルタイム |

#### 実行方法
```bash
python3 ./.node-red/python/<センサー名>.py [オプション]
```

#### 共通オプション
- `-i/--interval`: 出力間隔（ミリ秒）
- `-a/--address`: I2Cアドレス（一部センサーのみ）

### 2. Node-REDプロセス

Node-REDはポート1880で実行され、以下の処理を行います：

- **データ収集**: シリアル通信、Pythonプログラム実行
- **データ処理**: プロトコル解析、値変換、検証
- **データ配信**: MQTT、データベース保存、WebSocket配信

### 3. 通信プロセス

#### MQTTブローカー（Mosquitto）
- **ポート**: 1883（プライマリ）、51883（セカンダリ）
- **役割**: 内部メッセージング、リアルタイムデータ配信

#### シリアル通信
- **BravePI**: `/dev/ttyAMA0` (38400 baud)
- **BraveJIG**: `/dev/ttyACM0-9` (38400 baud)

### 4. データベースプロセス

#### InfluxDB
- **ポート**: 8086
- **役割**: 時系列センサーデータの保存
- **保持期間**: 30日（デフォルト）

#### MariaDB
- **ポート**: 3306
- **役割**: デバイス設定、メタデータの保存

## データフロー

### 1. センサーデータ取得フロー

```mermaid
graph LR
    subgraph "物理センサー層"
        I2C[I2Cセンサー]
        BLE[BLEセンサー]
        IND[産業用センサー]
    end

    subgraph "通信インターフェース層"
        PY[Pythonドライバー]
        BPI[BravePI]
        BJG[BraveJIG]
    end

    subgraph "データ収集層"
        EXEC[Execノード]
        SER1[Serialノード<br>/dev/ttyAMA0]
        SER2[Serialノード<br>/dev/ttyACM0-9]
    end

    I2C --> PY
    BLE --> BPI
    IND --> BJG
    
    PY --> EXEC
    BPI --> SER1
    BJG --> SER2
```

### 2. データ処理フロー

```mermaid
graph TB
    subgraph "Node-RED処理"
        IN[データ入力]
        PARSE[プロトコル解析<br>Functionノード]
        CONV[データ変換<br>・値の正規化<br>・単位変換<br>・較正処理]
        VAL[データ検証<br>・範囲チェック<br>・品質管理<br>・ヒステリシス]
        ROUTE[ルーティング]
    end

    subgraph "データ出力"
        MQTT[MQTTブローカー<br>localhost:1883]
        INFLUX[InfluxDB<br>時系列データ]
        MARIA[MariaDB<br>設定データ]
        WS[WebSocket<br>リアルタイム配信]
        API[REST API<br>外部連携]
    end

    IN --> PARSE
    PARSE --> CONV
    CONV --> VAL
    VAL --> ROUTE
    
    ROUTE --> MQTT
    ROUTE --> INFLUX
    ROUTE --> MARIA
    ROUTE --> WS
    ROUTE --> API
```

### 3. BLEデータ処理詳細

```mermaid
sequenceDiagram
    participant BLE as BLEセンサー
    participant BPI as BravePI
    participant UART as UART通信
    participant NR as Node-RED
    participant MQTT as MQTT

    BLE->>BPI: Bluetoothデータ送信
    BPI->>BPI: フレーム構築<br>[Length][DeviceID][Type][RSSI][Flag][Data]
    BPI->>UART: バイナリフレーム送信
    UART->>NR: シリアルデータ受信
    NR->>NR: ヘッダー解析（14バイト）
    NR->>NR: センサータイプ判定
    NR->>NR: データデコード処理
    NR->>MQTT: JSON形式で配信
```

## データフォーマット

### 1. Pythonドライバー出力（JSON）

```json
{
    "time": "2024-01-15 10:30:00.123456",
    "values": [0.1, 0.2, 0.3],
    "address": 25,
    "sensorType": 262,
    "tag": "accelerator"
}
```

### 2. BravePI/JIGフレーム構造

```
ヘッダー（14バイト）:
+--------+--------+--------+--------+--------+--------+
| Length | Device Number (8)    | Type   | RSSI   | Flag |
| (2)    |                      | (2)    | (1)    | (1)  |
+--------+--------+--------+--------+--------+--------+

データ部（可変長）:
+--------+--------+--------+
| センサーデータ (n bytes)  |
+--------+--------+--------+
```

### 3. MQTT配信フォーマット

```json
{
    "deviceNumber": "1234567890ABCDEF",
    "sensorType": 261,
    "rssi": -45,
    "battery": 85,
    "values": [23.4],
    "timestamp": "2024-01-15T10:30:00.123Z",
    "quality": "good"
}
```

## プロセス管理

### 1. 起動順序

1. データベースサービス（MariaDB、InfluxDB）
2. MQTTブローカー（Mosquitto）
3. Node-RED
4. Pythonセンサードライバー（Node-REDから起動）

### 2. 監視とログ

- **Node-REDログ**: `/var/log/node-red.log`
- **Pythonドライバー**: 標準出力をNode-REDが取得
- **シリアル通信**: Node-REDのデバッグノードで監視

### 3. エラーハンドリング

- **センサー初期化失敗**: プロセス終了、Node-REDが再起動
- **通信タイムアウト**: 10秒でタイムアウト、再接続試行
- **データ検証エラー**: 異常値をフィルタリング、ログ記録

## パフォーマンス特性

### 1. データ処理能力

- **センサーデータ**: 最大100Hz/センサー
- **Node-RED処理**: 1017ノードで構成
- **MQTT配信**: 1000msg/秒以上

### 2. リソース使用状況

- **CPU**: Node-RED 20-40%、Pythonドライバー 各1-5%
- **メモリ**: Node-RED 200-400MB、全体で1GB以下
- **ストレージ**: InfluxDB 1GB/月（標準構成）

## セキュリティ考慮事項

1. **通信**: 内部通信はlocalhost限定
2. **認証**: REST APIはトークン認証
3. **アクセス制御**: ポート1880は外部公開なし
4. **データ保護**: センシティブデータのマスキング

## トラブルシューティング

### よくある問題

1. **センサーが認識されない**
   - I2Cアドレスの確認: `i2cdetect -y 1`
   - 配線の確認
   - プルアップ抵抗の確認

2. **データが取得できない**
   - Node-REDのフロー確認
   - シリアルポートの権限確認
   - プロセスの重複起動確認

3. **パフォーマンス低下**
   - データベースのクリーンアップ
   - Node-REDフローの最適化
   - 不要なログの削除

## まとめ

本システムは、複数のセンサーデバイスからのデータを統合的に処理する複雑なアーキテクチャを持っています。Pythonドライバー、Node-RED、各種通信プロトコルが連携し、リアルタイムでのデータ収集・処理・配信を実現しています。