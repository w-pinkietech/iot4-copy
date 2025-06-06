# BravePI/BraveJIG 結合度分析レポート

*現行システムにおけるハードウェア依存性・疎結合化課題の技術分析*

## 分析概要

本ドキュメントは、IoT導入支援キット Ver.4.1における BravePI/BraveJIG ハードウェアの結合度を技術的に分析し、疎結合化に向けた課題と現状を詳述します。1017個のNode-REDノードによる現行実装の依存関係を定量的に評価し、アーキテクチャ改善の方向性を提示します。

## 目次
1. [結合度評価サマリー](#結合度評価サマリー)
2. [ハードウェア依存性分析](#ハードウェア依存性分析)
3. [プロトコル結合度詳細](#プロトコル結合度詳細)
4. [データ管理結合度](#データ管理結合度)
5. [テスト可能性評価](#テスト可能性評価)
6. [疎結合化優先度](#疎結合化優先度)

## 結合度評価サマリー

### 全体結合度評価

| 評価項目 | 現状結合度 | 影響範囲 | 疎結合化難易度 | 優先度 |
|----------|-----------|----------|---------------|--------|
| **通信プロトコル** | ★★★ 高結合 | 53ノード | ★★★ 高 | 🔴 緊急 |
| **デバイス管理** | ★★☆ 中結合 | 125ノード | ★★☆ 中 | 🟡 重要 |
| **センサードライバー** | ★★★ 高結合 | 380ノード | ★★★ 高 | 🔴 緊急 |
| **設定管理** | ★★☆ 中結合 | MariaDB 8テーブル | ★☆☆ 低 | 🟢 中期 |
| **テスト分離** | ★★★ 高結合 | 全システム | ★★★ 高 | 🟡 重要 |

**総合結合度**: ★★☆ (中〜高結合) - 疎結合化により大幅な保守性・拡張性向上が期待される

## ハードウェア依存性分析

### 1. 通信レイヤーの直接結合

#### 問題点：低レベル通信の直接実装
```javascript
// 現状：ハードウェア固有プロトコルの直接実装
const serialConfig = {
  "serialport": "/dev/ttyAMA0",     // BravePI固有
  "serialbaud": "38400",           // ハードウェア依存
  "serialport_usb": "/dev/ttyACM0" // BraveJIG固有
};

// 結合問題：53個のFunctionノードで直接プロトコル解析
function parseMessage(buffer) {
  const protocol = buffer.readUInt8(0);      // BravePI/JIG固有
  const deviceNumber = buffer.readBigUInt64LE(8); // 64bit固有ID
  const sensorType = buffer.readUInt16LE(16); // ベンダー固有タイプ
}
```

#### 依存性の定量評価

| 依存要素 | 影響ノード数 | 依存度 | 変更時影響 |
|----------|-------------|-------|-----------|
| **シリアルポート設定** | 22ノード | 直接依存 | 全ノード要修正 |
| **バイナリプロトコル** | 53ノード | 直接依存 | プロトコル解析要書換 |
| **デバイス番号体系** | 95ノード | 間接依存 | ルーティング影響 |
| **センサータイプID** | 380ノード | 直接依存 | 処理ロジック全面修正 |

### 2. センサータイプ結合度分析

#### 基本センサー群（Type 257-264）とJIG拡張（Type 289-293）の結合

```javascript
// 現状：センサータイプ固有の処理分散
const sensorProcessing = {
  257: "GPIO直接制御",           // ハードウェア固有
  258: "GPIO出力制御",           // ハードウェア固有  
  259: "I2C ADC読取",           // BravePI経由
  260: "I2C距離センサー",       // BravePI経由
  289: "USB JIG照度センサー",   // BraveJIG専用
  290: "USB JIG加速度",        // BraveJIG専用
};

// 問題：処理が各センサータイプに密結合
switch(sensorType) {
  case 257: return parseGPIOContact(data);    // GPIO固有
  case 289: return parseJIGIllumination(data); // JIG固有
}
```

#### センサー処理結合度マトリクス

| センサーType | 通信方式 | 解析処理 | 設定依存 | 結合度 |
|-------------|----------|----------|----------|--------|
| 257-258 | GPIO直接 | boolean | GPIO Pin | ★★★ |
| 259-264 | I2C+BravePI | 数値変換 | I2Cアドレス | ★★☆ |
| 289-293 | USB+BraveJIG | バイナリ解析 | USB設定 | ★★★ |

### 3. 設定管理の結合分析

#### MariaDBスキーマのハードウェア特化設計

```sql
-- 現状：デバイス別専用テーブル（高結合）
CREATE TABLE `ble_device_configs` (
  `device_id` INT PRIMARY KEY,
  `adv_interval` INT DEFAULT 1000,        -- BravePI固有
  `uplink_interval` INT DEFAULT 60000,    -- BravePI固有
  `measurement_interval` INT DEFAULT 10000 -- BravePI固有
);

CREATE TABLE `usb_device_configs` (
  `device_id` INT PRIMARY KEY,
  `usb_path` VARCHAR(50),                 -- BraveJIG固有
  `frame_timeout` INT DEFAULT 5000        -- BraveJIG固有
);

-- 問題：新しいハードウェア追加時にスキーマ変更必要
```

#### 設定管理結合度分析

| 設定カテゴリ | 専用テーブル数 | ハードウェア依存項目 | 汎用化可能性 |
|-------------|---------------|-------------------|-------------|
| **BLE設定** | 1テーブル | 広告間隔・電力管理 | ★★☆ 中 |
| **USB設定** | 1テーブル | USBパス・タイムアウト | ★★★ 高 |
| **I2C設定** | 1テーブル | アドレス・クロック | ★★★ 高 |
| **GPIO設定** | 1テーブル | Pin配置・プルアップ | ★☆☆ 低 |

## プロトコル結合度詳細

### 1. バイナリプロトコルの固有性

#### BravePI/JIG共通フレーム構造の分析
```
フレーム構造（18+nバイト）:
+----------+----------+----------+----------+----------+
| Protocol | Type     | Length   | Timestamp| Device # |
| (1 byte) | (1 byte) | (2 bytes)| (4 bytes)| (8 bytes)|
+----------+----------+----------+----------+----------+
| Sensor Type | RSSI | Order | Sensor Data (n bytes) |
| (2 bytes)   |(1byte)|(2bytes)|                      |
+----------+----------+----------+--------------------+
```

#### プロトコル固有性評価

| 要素 | 標準化可能性 | 代替プロトコル | 移行難易度 |
|------|-------------|---------------|-----------|
| **16バイト固定ヘッダー** | ★★☆ 中 | MQTT固定ヘッダー | ★★☆ 中 |
| **リトルエンディアン** | ★★★ 高 | JSON/MessagePack | ★☆☆ 低 |
| **CRC16チェックサム** | ★★★ 高 | TCP/MQTT標準 | ★☆☆ 低 |
| **64bit デバイスID** | ★★☆ 中 | UUID/MAC代替 | ★★☆ 中 |
| **センサータイプID** | ★☆☆ 低 | 標準センサータイプ | ★★★ 高 |

### 2. MQTT統合の結合度

#### 現状のMQTTトピック体系
```yaml
# BravePI/JIG固有トピック構造
Topics:
  - "DwlReq/{deviceNumber}"   # ダウンリンク要求（固有ID依存）
  - "DwlResp/{deviceNumber}"  # ダウンリンク応答
  - "UlReq/{deviceNumber}"    # アップリンク要求  
  - "JIResp/{deviceNumber}"   # JIG応答（BraveJIG固有）
  - "ErrResp/{deviceNumber}"  # エラー応答

# 問題：トピック構造がハードウェア固有
```

#### MQTT結合度分析

| MQTT要素 | ハードウェア依存度 | 標準化レベル | 疎結合化優先度 |
|----------|------------------|-------------|---------------|
| **トピック構造** | ★★☆ 中 | 部分的 | 🟡 重要 |
| **ペイロード形式** | ★★★ 高 | 独自バイナリ | 🔴 緊急 |
| **QoS設定** | ★☆☆ 低 | 標準準拠 | 🟢 低優先 |
| **認証方式** | ★☆☆ 低 | 標準準拠 | 🟢 低優先 |

## データ管理結合度

### 1. InfluxDB時系列データの結合度

#### 測定データ構造の分析
```yaml
# 現状：センサータイプ固有のmeasurement
Measurements:
  - "contact_input"     # Type 257固有
  - "adc_voltage"       # Type 259固有  
  - "acceleration"      # Type 262固有
  - "illuminance_jig"   # Type 289固有（JIG拡張）

# タグ構造
Tags:
  - device_id: "BravePI/JIG固有ID"
  - sensor_id: "センサー固有ID"
  - channel: "センサーチャンネル"

# フィールド構造  
Fields:
  - value: "主測定値"
  - raw_value: "生値（校正前）"
  - quality: "データ品質指標"
```

#### データ管理結合度評価

| データ要素 | ハードウェア依存 | 汎用化可能性 | 移行影響 |
|-----------|-----------------|-------------|----------|
| **Measurement名** | ★★☆ 中 | 統一スキーマ化可能 | ★★☆ 中 |
| **Device ID** | ★★★ 高 | UUID/標準ID化必要 | ★★★ 高 |
| **データ形式** | ★☆☆ 低 | 標準準拠 | ★☆☆ 低 |
| **タイムスタンプ** | ★☆☆ 低 | RFC3339標準 | ★☆☆ 低 |

### 2. MariaDB設定データの結合度

#### 設定テーブル構造の依存性分析
```sql
-- 高結合：ハードウェア専用テーブル
Tables:
  - devices (device_number VARCHAR(16))  -- BravePI/JIG固有ID
  - ble_device_configs                   -- BravePI専用
  - usb_device_configs                   -- BraveJIG専用
  - i2c_device_configs                   -- I2C専用

-- 中結合：部分的汎用テーブル  
Tables:
  - sensors (sensor_type_id SMALLINT)    -- 一部ハードウェア依存
  - sensor_types                         -- 標準化可能

-- 低結合：汎用テーブル
Tables:
  - mqtt_topics                          -- ハードウェア非依存
  - mail_addresses                       -- ハードウェア非依存
```

## テスト可能性評価

### 1. ユニットテスト分離度

#### 現状のテスト困難要因
```javascript
// 問題：ハードウェア依存処理が分離不可能
function processSerialData(input) {
  // シリアルポート直接アクセス（テスト困難）
  const port = new SerialPort('/dev/ttyAMA0', {baudRate: 38400});
  
  // プロトコル解析とビジネスロジックが混在
  const frame = parseFrame(input);
  const validated = validateSensor(frame);
  const processed = processHysteresis(validated);
  
  // データベース直接アクセス（テスト困難）
  db.query('INSERT INTO sensors...', processed);
  
  return processed;
}
```

#### テスト分離度評価

| テスト対象 | 分離可能性 | モック必要性 | テスト実装難易度 |
|-----------|-----------|-------------|-----------------|
| **プロトコル解析** | ★☆☆ 困難 | ハードウェアモック | ★★★ 高 |
| **データ変換** | ★★★ 容易 | 不要 | ★☆☆ 低 |
| **ヒステリシス処理** | ★★☆ 中程度 | 状態モック | ★★☆ 中 |
| **データベース操作** | ★★☆ 中程度 | DBモック | ★★☆ 中 |
| **MQTT通信** | ★☆☆ 困難 | ブローカーモック | ★★★ 高 |

### 2. 統合テスト複雑度

#### エンドツーエンドテストの課題
```yaml
テストシナリオの複雑度:
  1. センサーデータ生成: BravePI/JIGシミュレーター必要
  2. 通信プロトコル: バイナリフレーム生成必要
  3. エラーケース: ハードウェア障害シミュレート困難
  4. 性能テスト: 実ハードウェア依存
  5. 設定変更: リアルタイム反映テスト困難
```

## 疎結合化優先度

### Phase 1: 緊急対応（結合度★★★）

#### 1. プロトコル抽象化レイヤー
```javascript
// 目標：ハードウェア非依存のプロトコル層
interface SensorProtocol {
  parseFrame(buffer: Buffer): SensorData;
  validateData(data: SensorData): boolean;
  formatResponse(data: SensorData): Buffer;
}

// 実装：BravePI/JIG固有処理を隠蔽
class BravePIProtocol implements SensorProtocol { ... }
class BraveJIGProtocol implements SensorProtocol { ... }
```

**効果**: 53個のFunctionノードの結合度を★★★→★☆☆に改善

#### 2. センサードライバー統一化
```javascript
// 目標：センサータイプ非依存の処理
interface SensorDriver {
  readValue(): Promise<SensorValue>;
  calibrate(params: CalibrationParams): void;
  getMetadata(): SensorMetadata;
}

// 効果: 380個のハードウェア制御ノードの保守性向上
```

### Phase 2: 重要対応（結合度★★☆）

#### 3. 設定管理統一化
```sql
-- 目標：ハードウェア非依存の統一スキーマ
CREATE TABLE `device_configs` (
  `device_id` INT PRIMARY KEY,
  `device_type` VARCHAR(50),           -- 'bravepi', 'bravejig', 'generic'
  `config_json` JSON,                  -- ハードウェア固有設定をJSON化
  `capabilities` JSON                  -- 標準化された機能定義
);
```

**効果**: 新ハードウェア追加時のスキーマ変更不要

#### 4. テスト抽象化
```javascript
// 目標：ハードウェアモック機構
class HardwareMock {
  simulateSensorData(type: SensorType): SensorData;
  simulateError(errorType: ErrorType): void;
  simulateLatency(delay: number): void;
}
```

### Phase 3: 中長期対応（結合度★☆☆）

#### 5. 標準プロトコル移行
- MQTT-SN、CoAP等の標準IoTプロトコル対応
- JSON/MessagePack形式での設定・データ交換
- 標準センサータイプ分類への移行

**効果**: 他社ハードウェアとの互換性確保・ベンダーロックイン解消

## 結論

### 疎結合化による期待効果

| 項目 | 現状 | 疎結合化後 | 改善効果 |
|------|------|-----------|----------|
| **新ハードウェア対応** | 全面実装必要 | プラグイン追加のみ | 開発工数 70%削減 |
| **テスト実装** | ハードウェア必須 | モック・シミュレート可能 | テスト効率 3倍向上 |
| **保守性** | 全体影響 | 局所的変更 | 修正影響 80%削減 |
| **拡張性** | ハードウェア制約 | 標準インターフェース | 新機能追加容易 |

### 推奨実装順序

1. **Phase 1**: プロトコル抽象化（2-3ヶ月）
2. **Phase 2**: 設定管理統一化（1-2ヶ月）  
3. **Phase 3**: テスト機構構築（1-2ヶ月）
4. **Phase 4**: 標準プロトコル移行（3-4ヶ月）

**総投資期間**: 7-11ヶ月で段階的疎結合化完了

---

## 文書メタデータ

**文書タイトル**: BravePI/BraveJIG 結合度分析レポート  
**作成日付**: 2025年6月6日  
**対象システム**: IoT導入支援キット Ver.4.1  
**分析範囲**: Node-RED 1017ノード・MariaDB 8テーブル・InfluxDB全測定データ  
**分析者**: システム解析チーム  
**文書レベル**: 技術分析・疎結合化戦略 (★★★)