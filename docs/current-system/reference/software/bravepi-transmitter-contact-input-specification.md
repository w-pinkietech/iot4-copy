# BravePI トランスミッター ファームウェア仕様書 (接点入力センサー版)

**公式仕様書**: [ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (接点入力センサー版) REV 1.0](https://drive.google.com/file/d/1lQ48Ksxfq7UVOn2v0UXmGy8ciN99YVgR/view)

---

**Braveridge**
# ソフトウェア仕様書
## BravePI トランスミッター専用 ファームウェア (接点入力センサー版)
### REV 1.0
DESIGNED BY Braveridge Co., Ltd.

---

## 目次

- [1. 製品概要](#1-製品概要)
- [2. 機能概要](#2-機能概要)
  - [2-1. Sensor データ取得機能](#2-1-sensor-データ取得機能)
    - [2-1-1. 計測モード](#2-1-1-計測モード)
  - [2-2. LED 表示機能](#2-2-led-表示機能)
  - [2-3. Bluetooth 通信機能](#2-3-bluetooth-通信機能)
    - [2-3-1. Uplink](#2-3-1-uplink)
    - [2-3-2. Downlink](#2-3-2-downlink)
  - [2-4. NFCTag 通信機能](#2-4-nfctag-通信機能)
  - [2-5. パラメータ変更/取得機能](#2-5-パラメータ変更取得機能)
    - [2-5-1. パラメータ変更方法について](#2-5-1-パラメータ変更方法について)
    - [2-5-2. パラメータ取得方法について](#2-5-2-パラメータ取得方法について)
    - [2-5-3. 変更可能なパラメータについて](#2-5-3-変更可能なパラメータについて)
  - [2-6. DFU 機能](#2-6-dfu-機能)
- [3. パラメータ情報](#3-パラメータ情報)
- [4. Config モード時 Bluetooth通信仕様](#4-config-モード時-bluetooth通信仕様)
  - [4-1. 基本情報](#4-1-基本情報)
  - [4-2. Advertise/Scan Response Packet](#4-2-advertisescan-response-packet)
  - [4-3. Service](#4-3-service)
    - [4-3-1. BraveGATEInfo Service](#4-3-1-bravegateinfo-service)
    - [4-3-2. DeviceSettingInfo Service](#4-3-2-devicesettinginfo-service)
    - [4-3-3. SensorSettingInfo Service](#4-3-3-sensorsettinginfo-service)
    - [4-3-4. DeviceInfo Service](#4-3-4-deviceinfo-service)
- [5. 動作フロー](#5-動作フロー)
- [6. Uplink データ仕様](#6-uplink-データ仕様)
  - [6-1. Sensor 情報](#6-1-sensor-情報)
  - [6-2. パラメータ情報](#6-2-パラメータ情報)
- [7. Downlink データ仕様](#7-downlink-データ仕様)
  - [7-1. 即時 Uplink 要求](#7-1-即時-uplink-要求)
  - [7-2. パラメータ情報設定要求](#7-2-パラメータ情報設定要求)
  - [7-3. パラメータ情報取得要求](#7-3-パラメータ情報取得要求)
  - [7-4. デバイス Config 移行要求](#7-4-デバイス-config-移行要求)
  - [7-5. デバイス再起動要求](#7-5-デバイス再起動要求)
- [8. 電池駆動時の各設定における電池持ち](#8-電池駆動時の各設定における電池持ち)
- [9. 製品到着から使用開始までの流れ](#9-製品到着から使用開始までの流れ)
  - [9-1. BravePI トランスミッターの設定](#9-1-bravepi-トランスミッターの設定)
  - [9-2. BravePI トランスミッターと BravePI メインボードの紐付け](#9-2-bravepi-トランスミッターと-bravepi-メインボードの紐付け)
- [10. Revision 管理](#10-revision-管理)

---

## 1. 製品概要

本仕様書は、BravePI トランスミッターに接点入力センサーボードを接続した際に使用するファームウェア(以降、本製品とする)のソフトウェア仕様を記載したものです。

本仕様書は、対象とするハードウェアを以下に示します。

**<BravePI トランスミッター>**

| 製品名 | 型番 |
| :--- | :--- |
| BravePI トランスミッター (CR123A) | BVPTB-01 |
| BravePI トランスミッター (USB) | BVPTU-01 |

**<BravePI センサーボード>**

| 製品名 | 型番 |
| :--- | :--- |
| BravePI 接点入力ドライボード | BVPSID-01 |
| BravePI 接点入力ウェットボード | BVPSIW-01 |

BravePI トランスミッターは、取得した接点入力センサーの値をペアリングされた BravePI メインボードに通知します。

[画像: BravePI トランスミッターがNFCとBluetoothでBravePI メインボードに接続されている図]

---

## 2. 機能概要

### 2-1. Sensor データ取得機能

本製品は、接続した接点入力センサー(Dry/Wet)の値を送信することができます。

#### 2-1-1. 計測モード

本製品は以下の計測モードで接点入力センサーの情報を取得することができます。

| 測定モード | 説明 |
| :--- | :--- |
| 検知モード | 接点入力変化があった場合に通知します |

### 2-2. LED 表示機能

本製品は、本製品の状態をLEDで表示します。

| 優先 | 状態 | LED | | | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | **赤** | **緑** | **青** | |
| 高 | LowBattery 状態 | 点滅 | | | 1秒点灯、3秒消灯を繰り返す |
| 1 | Config モード | | 点滅 | | 1秒点灯、3秒消灯を繰り返す |
| | PowerON | | | 点灯 | 2秒点灯 |
| | PowerOFF | 点灯 | | | 2秒点灯 |
| 低 | 上記以外(通常動作中) | | | | 無灯 |

### 2-3. Bluetooth 通信機能

本製品は接続されたセンサー基板から取得されたセンサー情報を Bluetooth 通信で BravePI メインボードに通知します。また、BravePI メインボード経由で本製品に対して設定や指示等を Downlink することも可能です。

#### 2-3-1. Uplink

以下の情報を Uplink することができます。

| Uplink 情報 | Uplink タイミング |
| :--- | :--- |
| センサーデータ | パラメータで指定された Uplink 間隔 |
| パラメータ情報 | Downlink でパラメータ情報取得要求された場合 |

#### 2-3-2. Downlink

以下の指示を Downlink することができます。

| Downlink 情報 | 動作概要 |
| :--- | :--- |
| 即時 Uplink 要求 | 現在のセンサー情報の Uplink 要求します。 |
| パラメータ情報設定要求 | 本製品のパラメータ情報を設定します。 |
| パラメータ情報取得要求 | 本製品のパラメータ情報の Uplink 要求します。 |
| デバイス Config 移行 | 本製品を Config モードに移行します。 |
| デバイス再起動 | 本製品を再起動します。 |

### 2-4. NFCTag 通信機能

本製品は NFCTag を有しており、専用スマホアプリより各種設定や情報取得することができます。
以下が NFCTag 機能で専用スマホアプリより行える操作になります。

| 項目 | 動作概要 | 備考 |
| :--- | :--- | :--- |
| デバイス再起動 | 本製品を再起動する。 | |
| 電源ON 要求 | 本製品を電源OFFから復帰する。 | |
| 電源OFF 要求 (NFCTag のみ有効) | 本製品を電源OFFにする | 電源OFF状態の場合は、本要求は無視されます。 |
| Config モード移行要求 | 本製品を Config モードに移行します。 | 電源OFF状態の場合は、本要求は無視されます。 |

### 2-5. パラメータ変更/取得機能

本製品のパラメータ情報の変更/取得することができます。

#### 2-5-1. パラメータ変更方法について

本製品のパラメータ情報の変更は以下の方法で行えます。

- BravePI メインボードからパラメータ情報を Downlink することで変更することができます。
- 本製品を Config モードにすることで、Bluetooth 経由で変更することができます。

#### 2-5-2. パラメータ取得方法について

本製品のパラメータ情報の設定は以下の方法で行えます。

- BravePI メインボードからパラメータ取得要求を Downlink することでパラメータ情報を Uplink します。
- 本製品を Config モードにすることで、Bluetooth 経由で取得することができます。

#### 2-5-3. 変更可能なパラメータについて

本製品の変更/取得可能なパラメータに関しては「[3. パラメータ情報](#3-パラメータ情報)」を参照下さい。

### 2-6. DFU 機能

専用スマホアプリを使用することで、本製品のファームウェアの書き換えができます。
本製品のファームウェアの書き換えは、専用スマホアプリ以外からは行えません。

---

## 3. パラメータ情報

本製品のパラメータを以下に示します。

| パラメータ項目 | 設定情報 |
| :--- | :--- |
| DeviceID | BravePI メインボードと通信する為に必要な、DeviceID. |
| SensorID | BravePI メインボードと通信する為に必要な、SensorID |
| タイムゾーン設定 | タイムゾーン設定に関する設定情報を以下に示します<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| 日本時間<br>`0x01` \| UTC<br>上記以外 \| 日本時間 |
| BLE Mode | Bluetooth 通信モードの設定情報を以下に示します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| LongRange<br>`0x01` \| Legacy<br>上記以外 \| Long Range |
| Tx Power | Bluetooth 通信の送信電波出力の設定情報を以下に示します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| ±0dBm<br>`0x01` \| +4dBm<br>`0x02` \| -4dBm<br>`0x03` \| -8dBm<br>`0x04` \| -12dBm<br>`0x05` \| -16dBm<br>`0x06` \| -20dBm<br>`0x07` \| -40dBm<br>`0x08` \| +8dBm<br>上記以外 \| ±0dBm |
| Advertise Interval | Advertise を発信する間隔設定情報を以下に示します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x0064` \| 100ms 周期に Advertise を発信します。<br> : \| :<br>`0x03E8` \| 1000ms 周期に Advertise を発信します。<br>:<br>`0x2710` \| 10000ms 周期に Advertise を発信します。<br>上記以外 \| 1000ms 周期に Advertise を発信する設定になります。 |
| Sensor Uplink Interval | Sensor 情報データを Uplink する間隔を設定する<br><br><計測モードが「瞬時値モード」の場合><br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00000001` \| 1 秒周期に Sensor 情報データを Uplink します。<br>: \| :<br>`0x00000E10` \| 3600秒(1H)周期に Sensor 情報データを Uplink します<br>: \| :<br>`0x00015180` \| 86400秒(24H)周期に Sensor 情報データを Uplink します。<br>上記以外 \| 1000ms 周期に Advertise を発信する設定になります。<br><br><計測モードが「検知モード」の場合><br>本設定は無視されます。<br><br><計測モードが「サンプリングモード」の場合><br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00000001` \| 1 秒周期に Sensor 情報データを Uplink します。<br>: \| :<br>`0x00000E10` \| 3600秒(1H)周期に Sensor 情報データを Uplink します。<br>: \| :<br>`0x00015180` \| 86400秒(24H)周期に Sensor 情報データを Uplink します。<br>上記以外 \| 1000ms 周期に Advertise を発信する設定になります。 |
| 計測モード | Sensor 情報の扱いを設定します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| 瞬時値モード: Uplink タイミング時の現在の値を通知します。<br>`0x01` \| 検知モード: ヒステリシス検知したことを通知します。<br>`0x02` \| サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します。<br>上記以外 \| 瞬時値モードの設定になります。 |
| チャタリング時間 | チャタリング時間を設定します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x0000` \| チャタリング検知なし<br>`0x0001` \| 1ms以上信号状態維持で接点入力ありと判断します<br>:<br>`0x03E8` \| 1000ms以上信号状態維持で接点入力ありと判断します。<br>上記以外 \| チャタリング検知なし設定になります。 |

---

## 4. Config モード時 Bluetooth通信仕様

Config モード時用の Bluetooth 通信プロファイル仕様を以下に示します。

### 4-1. 基本情報

| 項目 | 値 |
| :--- | :--- |
| Advertising Interval | 1000ms |
| Min Connection Interval | 20ms |
| Max Connection Interval | 40ms |
| Slave Latency | 0 |
| Supervision Timeout | 6000ms |

### 4-2. Advertise/Scan Response Packet

**<Advertise データ>**

| Index | Data | Description | Comment |
| :--- | :--- | :--- | :--- |
| 0 | `0x02` | Length | |
| 1 | `0x01` | Advertising Field Type | FLAGS |
| 2 | `0x06` | Flag type | LE ONLY GENERAL DISCOVER MODE |
| 3 | `0x11` | Length | |
| 4 | `0x07` | Advertising Field Type | Complete List of 128-bit Service Class UUIDs |
| 5-20 | 右記 | Service UUID | 57791000-a129-4d7f-93a6-87f82b59f6a4 |
| 21 | `0x06` | Length | |
| 22 | `0x09` | Advertising Field Type | Complete Local Name |
| 23-28 | 右記 | Local Name | BvPiTm |

**<ScanResponse データ>**
なし

### 4-3. Service

`677eXXXX-79f2-4584-91f9-098db93d0781`
以下の Service/Characteristic の UUID は上記 UUID の XXXX (Alias)の部分に各 Service/Characteristic の Alias を設定した値になります。

| Service Name | Alias | Characteristic Name |
| :--- | :--- | :--- |
| BraveGATEInfo | `0x1000` | BV DEVICEID<br>BV COMPANYID<br>BV SENSORID |
| DeviceSetting | `0x2000` | TIME ZONE<br>BLE MODE<br>TX POWER<br>ADV INTERVAL<br>UPLINK INTERVAL |
| SensorSetting | `0x3000` | SENS_READ_REQ<br>SENS_READ_RESP<br>SENS MODE<br>CHATTERING TIME |
| DeviceInfo | `0x4000` | DEVICEID<br>FW VERSION<br>HW_VERSION<br>BATTERY<br>DFU_TYPE<br>DFU_REQUEST<br>REGISTER |

#### 4-3-1. BraveGATEInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| BV DEVICEID | Read | `0x1001` | `0x00` | bvDeviceId [8byte] |
| BV COMPANYID | Read | `0x1002` | `0x00` | bvCompanyId [8byte] |
| BV SENSORID | Read | `0x1003` | `0x00` | bvSensorId [2byte] |

**<BraveGATEInfo Service の詳細>**

■ **BV_DEVICEID**
BravePI メインボードとの通信に必要な DeviceID を Read できます。

■ **BV_COMPANYID**
BravePI メインボードとの通信に必要な CompanyID を Read できます。

■ **BV_SENSORID**
BravePI メインボードとの通信に必要な SensorID を Read できます。

#### 4-3-2. DeviceSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| TIME ZONE | Read/Write | `0x2001` | `0x00` | timeZone[1byte] |
| BLE MODE | Read/Write | `0x2002` | `0x00` | bleMode[1byte] |
| TX POWER | Read/Write | `0x2003` | `0x00` | txPower[1byte] |
| ADV_INTERVAL | Read/Write | `0x2004` | `0x00` | advInterval [2byte] |
| UPLINK INTERVAL | Read/Write | `0x2005` | `0x00` | uplinkInterval [4byte] |

**<DeviceSettingInfo Service の詳細>**

■ **TIME_ZONE**
タイムゾーンを設定します。
| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | 日本時間 |
| `0x01` | UTC |
| 上記以外 | 日本時間 |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

■ **BLE_MODE**
Bluetooth 通信モードの設定情報を以下に示します。
| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | Long Range |
| `0x01` | Legacy |
| 上記以外 | LongRange |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

■ **TX_POWER**
Bluetooth 通信モードの設定情報を以下に示します。
| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | ±0dBm |
| `0x01` | +4dBm |
| `0x02` | -4dBm |
| `0x03` | -8dBm |
| `0x04` | -12dBm |
| `0x05` | -16dBm |
| `0x06` | -20dBm |
| `0x07` | -40dBm |
| `0x08` | +8dBm |
| 上記以外 | ±0dBm |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

■ **ADV_INTERVAL**
Advertise を発信する間隔を設定します。
| 設定値 | 説明 |
| :--- | :--- |
| `0x0064` | 100ms 周期に Advertise を発信します。 |
| : | : |
| `0x03E8` | 1000ms 周期に Advertise を発信します。 |
| : | : |
| `0x2710` | 10000ms 周期に Advertise を発信します。 |
| 上記以外 | 1000ms 周期に Advertise を発信する設定になります。 |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。
※エンディアンはリトルエンディアン。

■ **UPLINK_INTERVAL**
Sensor 情報データを Uplink する間隔を設定する。

<計測モードが「瞬時値モード」の場合>
| 設定値 | 説明 |
| :--- | :--- |
| `0x00000001` | 1秒周期に Sensor 情報データを Uplink します |
| : | |
| `0x00000E10` | 3600秒(1時間)周期に Sensor 情報データを Uplink します |
| `0x00015180` | 86400秒(24時間)周期に Sensor 情報データを Uplink します。 |
| 上記以外 | 1000ms 周期に Advertise を発信する設定になります。 |

<計測モードが「検知モード」の場合>
本設定は無視されます。

<計測モードが「サンプリングモード」の場合>
| 設定値 | 説明 |
| :--- | :--- |
| `0x00000001` | 1秒周期に Sensor 情報データを Uplink します |
| : | : |
| `0x00000E10` | 3600秒(1時間)周期に Sensor 情報データを Uplink します。 |
| : | : |
| `0x00015180` | 86400秒(24時間)周期に Sensor 情報データを Uplink します。 |
| 上記以外 | 1000ms 周期に Advertise を発信する設定になります。 |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。
※エンディアンはリトルエンディアン。

#### 4-3-3. SensorSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| SENS_READ_REQ | Write | `0x3001` | `0x00` | sensorReq[1byte] |
| SENS READ RESP | Notify | `0x3002` | `0x00` | sensorValue[4byte] |
| SENS MODE | Read/Write | `0x3003` | `0x00` | sensorMode[1byte] |
| CHATTERING TIME | Read/Write | `0x3004` | `0x00` | chatteringTime [2byte] |

**<SensorSettingInfo Service の詳細>**

■ **SENS_READ_REQ**
`0x01` を write すると現在のセンサー情報取得開始します。

■ **SENS_READ_RESP**
SENS_READ_REQ に対する応答で、現在の接点入力センサー値を Notify します。
※失敗時は、`0xFFFFFFFF` を返します。
※エンディアンはリトルエンディアン。

■ **SENS_MODE**
Sensor 情報の扱いを設定する。
| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | 瞬時値モード: Uplink タイミング時の現在の値を通知します |
| `0x01` | 検知モード: ヒステリシス検知したことを通知します。 |
| `0x02` | サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します |
| 上記以外 | 瞬時値モード設定になります。 |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

■ **CHATTERING_TIME**
チャタリング時間を設定する。
| 設定値 | 説明 |
| :--- | :--- |
| `0x0000` | チャタリング検知なし |
| `0x0001` | 1ms以上信号状態維持で接点入力ありと判断します。 |
| : | : |
| `0x03E8` | 1000ms以上信号状態維持で接点入力ありと判断します。 |
| 上記以外 | チャタリング検知なし設定になります。 |
※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

#### 4-3-4. DeviceInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| DEVICEID | Read | `0x4001` | `0x00` | nordicDeviceId [8byte] |
| FW VERSION | Read | `0x4002` | `0x00` | fwVersion [3byte] |
| HW VERSION | Read | `0x4003` | `0x00` | hwVersion [3byte] |
| BATTERY | Read | `0x4004` | `0x00` | batteryLevel [1byte] |
| DFU TYPE | Read | `0x4005` | `0x00` | dfuType[1byte] |
| DFU_REQUEST | Write | `0x4006` | `0x00` | dfuRequest[1byte] |
| REGISTER | Write | `0x4007` | `0x00` | register[3byte] |

**<DeviceInfo Service の詳細>**

■ **DEVICEID**
Nordic のチップのユニークな ID を読み出せます。

■ **FW_VERSION**
本製品のFWバージョンを読み出せます。
例: Ver1.2.9の場合は、`[0x01, 0x02, 0x09]` で通知されます。

■ **HW_VERSION**
本製品のHWバージョンを読み出せます。
例: Ver1.2.9の場合は、`[0x01, 0x02, 0x09]` で通知されます。

■ **BATTERY**
本製品の現在のバッテリーレベル(%)を読み出せます。

■ **DFU_TYPE**
固定で `0x01` が読み出されます。

■ **DFU_REQUEST**
`0x01` を Write すると、Bluetooth 切断し、DFU モードに移行します。

■ **REGISTER**
`0x66a781` を write すると変更された変更されて全ての情報を保存し、変更した設定を有効にします。

---

## 5. 動作フロー

[画像: 動作フロー]

POWER ON -> NFCTag検知

- YES: NFC要求処理実行 -> POWER OFF中
- NO: POWER OFF中

POWER OFF中
- YES: (ループバック to NFCTag検知)
- NO: Configモード中

Configモード中
- YES: Configモード中動作 -> (ループバック to NFCTag検知)
- NO: センサーReadタイミング

センサーReadタイミング
- YES: センサー情報Read実行 -> Uplinkタイミング
- NO: Uplinkタイミング

Uplinkタイミング
- YES: Uplink実行 -> Downlink受信
- NO: Downlink受信

Downlink受信 -> Downlink受信処理実行 -> (ループバック to NFCTag検知)

---

## 6. Uplink データ仕様

BravePI メインボードから通知される情報ついて以下に示す。

### 6-1. Sensor 情報

SensorID: `0x0101`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| DataLength | 2 | Data 部分のデータ長 | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0101` | |
| RSSI | 1 | Bluetooth 電波強度 | |
| Flag | 1 | `0x00`:継続データなし | |
| **Data 領域** | | | |
| Battery Level | 1 | バッテリーレベル(%) | |
| sampleNum | 2 | サンプル数 | |
| Status | 4 | 現在の接点状態 | OFF(0)/ON(1) |

※エンディアンはリトルエンディアンになります。

### 6-2. パラメータ情報

SensorID: `0x0000`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| DataLength | 2 | Data 部分のデータ長 | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0000` | |
| RSSI | 1 | Bluetooth 電波強度 | |
| Flag | 1 | `0x00`:継続データなし | |
| **Data 領域** | | | |
| SensorID | 2 | `0x0101` 固定 | |
| FW Version | 3 | 本製品のFWバージョン | Ver1.2.9の場合は、`[0x01,0x02,0x09]` |
| TimeZone | 1 | タイムゾーン設定 | |
| BLE Mode | 1 | Bluetooth 通信モードの設定情報 | |
| Tx Power | 1 | Bluetooth 通信の送信電波出力 | |
| Advertise Interval | 2 | Advertise を発信する間隔 | |
| Sensor Uplink Interval | 4 | Sensor 情報データを Uplink する間隔 | |
| Sensor Read Mode | 1 | 計測モード | |
| Chattering Time | 2 | チャタリング時間 | |

※エンディアンはリトルエンディアンになります。

---

## 7. Downlink データ仕様

BravePI メインボードから送信する情報ついて以下に示す。

### 7-1. 即時 Uplink 要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00` 固定 | |
| DataLength | 2 | `0x0000` | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0101` | |
| CMD | 1 | `0x00` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| Data | | なし | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-2. パラメータ情報設定要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00` 固定 | |
| DataLength | 2 | `0x0009` | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0000` | |
| CMD | 1 | `0x05` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| SensorID | 2 | `0x0101` | |
| TimeZone | 1 | タイムゾーン設定 | |
| Tx Power | 1 | Bluetooth 通信の送信電波出力 | |
| Advertise Interval | 2 | Advertise を発信する間隔 | |
| Sensor Read Mode | 1 | 計測モード | |
| Chattering Time | 2 | チャタリング時間 | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-3. パラメータ情報取得要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00`固定 | |
| DataLength | 2 | `0x0001` | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0000` | |
| CMD | 1 | `0x0D` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| Data | 1 | `0x00` | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-4. デバイス Config 移行要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00` 固定 | |
| DataLength | 2 | `0x0000` | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0000` | |
| CMD | 1 | `0xFC` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| Data | | なし | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-5. デバイス再起動要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00` 固定 | |
| DataLength | 2 | `0x0000` | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0000` | |
| CMD | 1 | `0xFD` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| Data | | なし | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

---

## 8. 電池駆動時の各設定における電池持ち

本製品を電池駆動させた場合の代表的な設定におけるおおよその電池持ちを以下に示します。

**<Bluetooth モード: Legacy の場合>**

| パラメータ設定情報 | | 接点入力センサー情報 | 電池持ち |
| :--- | :--- | :--- | :--- |
| 計測モード | Advertise Interval / TxPower | センサー / 接点状態 | (日) |
| 検知モード | 100ms / 0dBm | Dry / ON 状態 | 7 |
| | | Dry / OFF 状態 | 133 |
| | | Wet / ON 状態 | 7 |
| | | Wet / OFF 状態 | 133 |
| | 1000ms / 0dBm | Dry / ON 状態 | 7 |
| | | Dry / OFF 状態 | 385 |
| | | Wet / ON 状態 | 7 |
| | | Wet / OFF 状態 | 382 |

**<Bluetooth モード: Long Range の場合>**

| パラメータ設定情報 | | | 接点入力センサー情報 | 電池持ち |
| :--- | :--- | :--- | :--- | :--- |
| 計測モード | TxPower | Advertise Interval | センサー / 接点状態 | (日) |
| 検知モード | 0dBm | 100ms | Dry / ON 状態 | 6 |
| | | | Dry / OFF 状態 | 42 |
| | | | Wet / ON 状態 | 6 |
| | | | Wet / OFF 状態 | 42 |
| | | 1000ms | Dry / ON 状態 | 7 |
| | | | Dry / OFF 状態 | 232 |
| | | | Wet / ON 状態 | 7 |
| | | | Wet / OFF 状態 | 236 |

---

## 9. 製品到着から使用開始までの流れ

### 9-1. BravePI トランスミッターの設定

BravePI トランスミッター側の設定手順について以下に示します。

1. トランスミッターからセンサーを外した状態にする。
2. トランスミッターに電池又はUSB給電する。
3. 専用のiPhoneアプリを起動する。
4. iPhone アプリから接点入力センサー用の「ファームウェア書き込み」を実行する。
5. iPhone アプリから接点入力センサー用の「パラメータ設定」を実行する。
6. トランスミッターに接点入力センサーを取り付ける。
7. iPhone アプリからトランスミッターに電源ON(再起動)操作を行う。

次に BravePI トランスミッターと BravePI メインボードの紐付けを実行して下さい。

### 9-2. BravePI トランスミッターと BravePI メインボードの紐付け

BravePI トランスミッターと BravePI メインボードの紐付け手順について以下に示します。

1. 専用のiPhoneアプリを起動する。
2. iPhone アプリから「ペアリング」を実行する。

以上で設定は終了です。

---

## 10. Revision 管理

| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023/11/28 | Ver1.0.0 | 初版 |

※上記、製品仕様や機能、デザインは変更となる可能性がございます。あらかじめご了承ください。

---

**Braveridge**

BravePIとその製品に関する詳しい情報は、弊社Webサイトで御確認ください。
[https://www.braveridge.com/](https://www.braveridge.com/)

- **株式会社Braveridge 本社**
  〒819-0373 福岡県福岡市西区周船寺3-27-2
  (Tel): 092-834-5789 / (Fax): 092-807-7718

- **株式会社Braveridge 糸島工場**
  〒819-1122 福岡県糸島市東1999-19
  - Apple MFi Manufacture ライセンス認定工場(ライトニングコネクタ製品工場)