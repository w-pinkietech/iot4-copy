# ソフトウェア仕様書 BravePI メインボード BVPMB-01 REV 1.2

> **公式仕様書**: [BravePI メインボード BVPMB-01 公式仕様書 (Google Drive)](https://drive.google.com/file/d/1yfrWPkb5cJCD_FizM9DuRC5_uimsXSmu/view)

## 目次

1. [製品概要](#1-製品概要)
2. [機能概要](#2-機能概要)
   - 2-1. [BraveRoute 通信機能](#2-1-braveroute-通信機能)
   - 2-2. [NFC Tag 機能](#2-2-nfc-tag-機能)
   - 2-3. [パラメータ変更/取得機能](#2-3-パラメータ変更取得機能)
   - 2-4. [DFU 機能](#2-4-dfu-機能)
3. [パラメータ情報](#3-パラメータ情報)
4. [Config モード時 Bluetooth 通信仕様](#4-config-モード時-bluetooth-通信仕様)
   - 4-1. [基本情報](#4-1-基本情報)
   - 4-2. [Advertise/ScanResponse Packet](#4-2-advertisescanresponse-packet)
   - 4-3. [Service](#4-3-service)
5. [コマンド仕様](#5-コマンド仕様)
   - 5-1. [UART 通信機能](#5-1-uart-通信機能)
   - 5-2. [Uplink コマンド](#5-2-uplink-コマンド)
   - 5-3. [Downlink コマンド](#5-3-downlink-コマンド)
6. [製品到着から使用開始までの流れ](#6-製品到着から使用開始までの流れ)
7. [Revision 管理](#7-revision-管理)

## 1. 製品概要

本製品は、BravePI トランスミッターとラズベリーパイとの通信を UART にて中継します。

```
[NFC] ←→ [BravePI メインボード] ←(Bluetooth)→ [BravePI トランスミッター]
                    ↓
                 (UART)
                    ↓
            [Raspberry Pi]
```

## 2. 機能概要

### 2-1. BraveRoute 通信機能

ラズベリーパイに接続することにより UART を介して、BravePI トランスミッターからの Uplink を取得することができます。また、BravePI トランスミッターに UART を介して、Downlink を行うことができます。コマンドの詳細は「[5. コマンド仕様](#5-コマンド仕様)」を参照ください。

### 2-2. NFC Tag 機能

本製品は NFC Tag を有しており、専用スマホアプリを起動し、本製品にスマホを近づけることで以下の各種設定や情報取得することができます。

| 項目 | 動作概要 |
|:---:|:---:|
| デバイス再起動要求 | 本製品を再起動します |
| Config モード移行要求 | 本製品を Config モードに移行します |
| Company ID 取得要求 | 本製品の Company ID を取得します |
| デバイス ID 紐づけ登録 | 本製品と紐づくデバイス ID を登録します |
| デバイス ID 紐づけ削除 | 本製品と紐づくデバイス ID を削除します |
| デバイス ID 紐づけ取得 | 本製品と紐づくデバイス ID を取得します |
| DFU モード移行要求 | 本製品を DFU モードに移行します |

### 2-3. パラメータ変更/取得機能

本製品のパラメータ情報は取得・変更することができます。本製品の変更・取得可能なパラメータは以下の「[3. パラメータ情報](#3-パラメータ情報)」を参照ください。

本製品のパラメータの取得・変更方法は以下になります。

- 専用アプリの NFC 機能を使用
- Config モード時の BLE 機能を使用

### 2-4. DFU 機能

専用アプリを使用することで、本製品の FW を更新することができます。本製品の FW の更新は、専用アプリ以外では行うことができません。

## 3. パラメータ情報

本製品のパラメータを以下に示します。

| パラメータ項目 | 設定情報 |
|:---:|:---|
| Company ID | 本製品と通信を行うために必要な ID。<br>この ID が一致している BravePI トランスミッターと通信を行います。 |
| Filter Device ID | 本製品と通信を行うデバイスの Device ID。<br>16個まで保存可能です。<br>登録された Device ID を持つ BravePI トランスミッターとのみ通信を行います。 |
| Bluetooth Mode | Bluetooth 通信モードの設定情報を以下に示します。<br><br>**設定値と説明:**<br>- `0x00`: Long Range<br>- `0x01`: Legacy<br>- 上記以外: Long Range |

## 4. Config モード時 Bluetooth 通信仕様

Config モード時用の Bluetooth 通信プロファイル仕様を以下に示します。

### 4-1. 基本情報

| 項目 | 値 |
|:---:|:---:|
| Advertising Interval | 100ms |
| Min Connection Interval | 50ms |
| Max Connection Interval | 70ms |
| Slave Latency | 0 |
| Supervision Timeout | 6000ms |

### 4-2. Advertise/ScanResponse Packet

#### Advertise データ

| Index | Data | Description | Comment |
|:---:|:---:|:---:|:---|
| 0 | 0x02 | Length | |
| 1 | 0x01 | Advertising Field Type | FLAGS |
| 2 | 0x06 | Flag type | LE ONLY GENERAL DISCOVER MODE |
| 3 | 0x11 | Length | |
| 4 | 0x07 | Advertising Field Type | Complete List of 128-bit Service Class UUIDs |
| 5-20 | - | Service UUID | 57791000-a129-4d7f-93a6-87f82b59f6a4 |
| 21 | 0x06 | Length | |
| 22 | 0x09 | Advertising Field Type | Complete Local Name |
| 23-29 | - | Local Name | BPBConf |

#### ScanResponse データ

なし

### 4-3. Service

UUID フォーマット: `5779xxxx-a129-4d7f-93a6-87f82b59f6a4`

以下の Service/Characteristic の UUID は上記 UUID の xxxx (Alias) の部分に各 Service/Characteristic の Alias を設定した値になります。

| Service Name | Alias | Characteristic Name |
|:---:|:---:|:---:|
| BraveGATE Info | 0x1100 | COMPANY ID<br>CLEAR_FILTER<br>SET_FILTER<br>REQ_NOTIFY_FILTER<br>NOTIFY_FILTER<br>BV CODE |
| Device Setting | 0x1200 | BLE MODE |
| DeviceInfo | 0x1300 | DEVICE_ID<br>FW_VERSION<br>DFU_REQUEST<br>REGISTER |

#### 4-3-1. BraveGATE Info Service

| Characteristic Name | Property | Alias | Size | Description |
|:---:|:---:|:---:|:---:|:---|
| COMPANY ID | Write/Read | 0x1101 | 6 | Company ID を変更・取得を行います |
| CLEAR_FILTER | Write | 0x1102 | 1 | 0x2F を送信することで、本製品と通信する全てのデバイスの Device ID 登録を消去します |
| SET_FILTER | Write | 0x1103 | 9 | インデックスを指定して、本製品と通信するデバイスの Device ID を登録します |
| REQ_NOTIFY_FILTER | Write | 0x1104 | 1 | 本製品と通信するデバイスの Device ID を取得するためのリクエストを送信します |
| NOTIFY_FILTER | Notify | 0x1105 | 9 | REQ_NOTIFY_FILTER のレスポンスとして、登録されている Device ID を通知します |
| BV CODE | Read | 0x1106 | 8 | BraveGATE のコード情報を取得します |

#### 4-3-2. Device Setting Service

| Characteristic Name | Property | Alias | Size | Description |
|:---:|:---:|:---:|:---:|:---|
| BLE MODE | Write/Read | 0x1201 | 1 | Bluetooth 通信モードの設定・取得を行います<br>- 0x00: Long Range<br>- 0x01: Legacy |

#### 4-3-3. Device Info Service

| Characteristic Name | Property | Alias | Size | Description |
|:---:|:---:|:---:|:---:|:---|
| DEVICE_ID | Read | 0x1301 | 8 | 本製品の Device ID を取得します |
| FW_VERSION | Read | 0x1302 | 3 | ファームウェアバージョンを取得します<br>Format: Major.Minor.Patch |
| DFU_REQUEST | Write | 0x1303 | 1 | 0x01 を送信することで DFU モードに移行します |
| REGISTER | Write/Read | 0x1304 | 可変 | デバイス登録情報の設定・取得を行います |

## 5. コマンド仕様

### 5-1. UART 通信機能

UART 通信の仕様を以下に示します。

| 項目 | 設定値 |
|:---:|:---:|
| デバイス | /dev/ttyAMA0 |
| ボーレート | 38400 bps |
| データビット | 8 bit |
| ストップビット | 1 bit |
| パリティ | なし |
| フロー制御 | なし |

### 5-2. Uplink コマンド

BravePI トランスミッターから受信したデータを Raspberry Pi に転送します。

#### フレームフォーマット

```
[Header(4bytes)] [Payload(可変長)] [Checksum(1byte)]
```

#### Header 構成

| Offset | Size | Description |
|:---:|:---:|:---|
| 0 | 1 | Protocol Version (0x01) |
| 1 | 1 | Message Type |
| 2-3 | 2 | Payload Length (Little Endian) |

#### Message Type

| Value | Description |
|:---:|:---|
| 0x10 | センサーデータ |
| 0x11 | ステータス情報 |
| 0x12 | エラー通知 |
| 0x20 | コマンドレスポンス |

### 5-3. Downlink コマンド

#### 5-3-1. エンドデバイスコマンド

BravePI トランスミッターへ送信するコマンド。

| Command | Value | Description | Parameter |
|:---:|:---:|:---|:---|
| READ_SENSOR | 0x30 | センサー値読み取り | Device ID (8bytes) |
| SET_CONFIG | 0x31 | 設定変更 | Device ID (8bytes) + Config Data |
| RESET_DEVICE | 0x32 | デバイスリセット | Device ID (8bytes) |

#### 5-3-2. 設定コマンド

BravePI メインボード自体の設定を行うコマンド。

| Command | Value | Description | Parameter |
|:---:|:---:|:---|:---|
| GET_VERSION | 0x40 | バージョン取得 | なし |
| SET_COMPANY_ID | 0x41 | Company ID 設定 | Company ID (6bytes) |
| GET_COMPANY_ID | 0x42 | Company ID 取得 | なし |
| ENTER_CONFIG_MODE | 0x43 | Config モード移行 | なし |
| REBOOT | 0x44 | 再起動 | なし |

## 6. 製品到着から使用開始までの流れ

1. **製品の接続**
   - BravePI メインボードを Raspberry Pi の GPIO ヘッダーに接続
   - 電源供給を確認（LED 点灯）

2. **初期設定**
   - 専用アプリで NFC 経由で Company ID を設定
   - 必要に応じて Filter Device ID を登録

3. **通信モード設定**
   - Bluetooth Mode を環境に応じて設定（Long Range/Legacy）

4. **動作確認**
   - UART 通信の疎通確認
   - BravePI トランスミッターとの通信確認

5. **運用開始**
   - Node-RED などのアプリケーションから UART 経由でデータ取得

## 7. Revision 管理

| Revision | Date | Description |
|:---:|:---:|:---|
| 1.0 | 2023/04/01 | 初版リリース |
| 1.1 | 2023/06/15 | NFC Tag 機能追加 |
| 1.2 | 2023/09/01 | Bluetooth Long Range モード対応 |

## 8. 関連ドキュメント

本仕様書に関連する技術文書およびシステム統合ガイドへのリンクを以下に示します。

### 8-1. システム統合ドキュメント

#### Node-RED統合アーキテクチャ
- **[BravePI/BraveJIG統合アーキテクチャ](../architecture/bravepi-bravejig-integration.md)**
  - BravePIとBraveJIGのNode-REDシステムへの統合方法
  - 通信プロトコルフレーム構造の詳細説明
  - センサータイプ対応表（Type ID: 289-296）
  - データフローシーケンス図
  - MariaDB/InfluxDB設定スキーマ

#### 技術分析
- **[Node-REDアーキテクチャ詳細技術分析](../analysis/technical-analysis.md)**
  - シリアル通信設定の詳細（/dev/ttyAMA0, 38400 baud）
  - GPIO設定詳細（BCM16-27ピン割り当て）
  - MQTTトピック構成（DwlResp/+, JIResp/+, UlReq/+等）
  - アクセスタイプ定義（0: Bluetooth, 1: I2C, 3: LAN, 4: USB）

### 8-2. 新システム移行ガイド

#### プラグイン実装
- **[BravePIプラグイン詳細実装](../../new-system/implementation/bravepi-plugin-implementation.md)**
  - 疎結合アーキテクチャへの統合方法
  - Pythonプラグイン実装例
  - プロトコルフレーム解析処理
  - センサータイプ別値抽出メソッド
  - 品質指標計算アルゴリズム（RSSI/バッテリーベース）

### 8-3. プロトコル仕様補足

#### フレームフォーマット詳細
本仕様書5章で定義されたUARTフレームフォーマットは、以下の拡張仕様も含みます：

```
完全フレーム構造:
+----------+----------+----------+----------+----------+----------+
| Protocol | Type     | Length   | Timestamp| Device # | Data...  |
| (1 byte) | (1 byte) | (2 bytes)| (4 bytes)| (8 bytes)| (n bytes)|
+----------+----------+----------+----------+----------+----------+
```

- **Timestamp**: Unix時間（秒単位）、Little Endian
- **Device #**: 8バイト固定長、NULL文字でパディング

#### メッセージタイプ拡張
| Type | 名称 | 説明 | 実装状況 |
|------|------|------|----------|
| 0x00 | General Data | 汎用センサーデータ | 実装済 |
| 0x01 | Downlink Response | コマンド応答 | 実装済 |
| 0x02 | JIG Information | JIG固有情報 | 実装済 |
| 0x03 | DFU | ファームウェア更新 | 実装済 |
| 0xFF | Error Response | エラー応答 | 実装済 |

### 8-4. 運用上の注意事項

#### 既知の制約事項
1. **シリアル通信バッファ**: 最大1024バイト/フレーム
2. **同時接続数**: BLEセンサー最大16台
3. **GPIO応答時間**: デバウンス設定により最大25ms遅延

#### トラブルシューティング
- UART通信エラー時は`/dev/ttyAMA0`の権限を確認
- BLE接続不良時はCompany IDの一致を確認
- GPIO入力が不安定な場合はプルアップ抵抗設定を確認

### 8-5. 参考資料

- [現行システムアーキテクチャ概要](../architecture/system-overview.md)
- [データフロー分析](../architecture/data-flow-analysis.md)
- [センサーデータサンプル](../analysis/sensor-data-samples.md)