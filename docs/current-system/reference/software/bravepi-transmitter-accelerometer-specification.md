# BravePI トランスミッター ファームウェア仕様書 (加速度センサー版)

**公式仕様書**: [ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (加速度センサー版) REV 1.1](https://drive.google.com/file/d/13UySHaC7T2BERNwEMvrSKPjhCxIzzXKY/view)

---

**Braveridge**
# ソフトウェア仕様書
## BravePI トランスミッター専用 ファームウェア (加速度センサー版)
### REV 1.1
DESIGNED BY Braveridge Co., Ltd.

---

## 目次

- [1. 概要](#1-概要)
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
- [10. 商標について](#10-商標について)
- [11. Revision 管理](#11-revision-管理)

---

## 1. 概要

本仕様書は、BravePI トランスミッターに加速度センサーボードを接続した際に使用するファームウェア(以降、本製品とする)のソフトウェア仕様を記載したものです。

本仕様書は、対象とするハードウェアを以下に示します。

**<BravePI トランスミッター>**

| 製品名 | 型番 |
| :--- | :--- |
| BravePI トランスミッター (CR123A) | BVPTB-01 |
| BravePI トランスミッター (USB) | BVPTU-01 |

**<BravePI センサーボード>**

| 製品名 | 型番 |
| :--- | :--- |
| BravePI 加速度センサーボード | BVPS3-01 |

本製品は、センサーボードから取得した加速度センサーの値をペアリングされた BravePI メインボードに通知します。

[画像: BravePIトランスミッターがBluetoothとNFCでBravePIメインボードと通信する図]

---

## 2. 機能概要

### 2-1. Sensor データ取得機能

本製品は、接続した加速度センサーの値を送信することができます。

| センサーIC | センサーメーカー |
| :--- | :--- |
| LIS2DUXS12 | ST マイクロエレクトロニクス |

#### 2-1-1. 計測モード

本製品は以下の計測モードで加速度センサーの情報を取得することができます。

| 測定モード | 説明 |
| :--- | :--- |
| 瞬時値モード | Uplink タイミング時に現在の値を取得し通知します |
| 検知モード | 定期的に値を取得し、ヒステリシス検知した場合に通知します。<br>ヒステリシスで指定された検知/復帰の設定範囲は以下になります<br><br>**設定項目** \| **設定範囲**<br>--- \| ---<br>ヒステリシス (High) \| ±0.5~±6.5G(0.5G単位)<br>ヒステリシス (Low) \| ±0.5~±6.5G(0.5G単位) |
| サンプリングモード | 指定したサンプリング周期でサンプリングした値を通知します。<br>サンプリングモード時の設定可能なサンプリング周期は以下とする<br><br>**項目** \| **設定**<br>--- \| ---<br>サンプリング周期 \| 1Hz<br> \| 2Hz<br> \| 5Hz<br> \| 10Hz<br> \| 20Hz<br><br>各サンプリングモード時の最大 Uplink 周期は以下になります<br><br>**サンプリング周期** \| **最大 Uplink 間隔**<br>--- \| ---<br>1Hz \| 6,667 秒<br>2Hz \| 3,333秒<br>5Hz \| 1,333秒<br>10Hz \| 667秒<br>20Hz \| 333秒 |

### 2-2. LED 表示機能

本製品は、本製品の状態をLEDで表示します。

| 優先 | 状態 | LED | | | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | **赤** | **緑** | **青** | |
| 高 | LowBattery 状態 | 点滅 | - | - | 1秒点灯、3秒消灯を繰り返す |
| | Config モード | - | - | 点滅 | 1秒点灯、3秒消灯を繰り返す |
| 1 | PowerON | - | 点灯 | - | 2秒点灯 |
| | PowerOFF | 点灯 | - | - | 2秒点灯 |
| 低 | 上記以外(通常動作中) | - | - | - | 無灯 |

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
| パラメータ情報取得要求 | 本製品のパラメータ情報の Uplink 要求します |
| デバイス Config 移行 | 本製品を Config モードに移行します。 |
| デバイス再起動 | 本製品を再起動します |

### 2-4. NFCTag 通信機能

本製品は NFCTag を有しており、専用スマホアプリより各種設定や情報取得することができます。
以下が NFCTag 機能で専用スマホアプリより行える操作になります。

| 項目 | 動作概要 | 備考 |
| :--- | :--- | :--- |
| デバイス再起動 | 本製品を再起動する。 | |
| 電源ON 要求 | 本製品を電源OFF から復帰する | |
| 電源OFF 要求<br>(NFCTag のみ有効) | 本製品を電源OFFにする。 | 電源OFF状態の場合は、本要求は無視されます。 |
| Config モード移行要求 | 本製品を Config モードに移行します。 | 電源OFF状態の場合は、本要求は無視されます。 |

### 2-5. パラメータ変更/取得機能

本製品のパラメータ情報の変更/取得することができます。

#### 2-5-1. パラメータ変更方法について

本製品のパラメータ情報の変更は以下の方法で行えます。
・BravePI メインボードからパラメータ情報を Downlink することで変更することができます。
・本製品を Config モードにすることで、Bluetooth 経由で変更することができます。

#### 2-5-2. パラメータ取得方法について

本製品のパラメータ情報の設定は以下の方法で行えます。
・BravePI メインボードからパラメータ取得要求を Downlink することでパラメータ情報を Uplink します。
・本製品を Config モードにすることで、Bluetooth 経由で取得することができます。

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
| Tx Power | Bluetooth 通信の送信電波出力の設定情報を以下に示します<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| ±0dBm<br>`0x01` \| +4dBm<br>`0x02` \| -4dBm<br>`0x03` \| -8dBm<br>`0x04` \| -12dBm<br>`0x05` \| -16dBm<br>`0x06` \| -20dBm<br>`0x07` \| -40dBm<br>`0x08` \| +8dBm<br>上記以外 \| ±0dBm |
| Advertise Interval | Advertise を発信する間隔設定情報を以下に示します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x0064` \| 100ms 周期に Advertise を発信します。<br>：<br>`0x03E8` \| 1000ms 周期に Advertise を発信します。<br>：<br>`0x2710` \| 10000ms 周期に Advertise を発信します。<br>上記以外 \| 1000ms 周期に Advertise を発信する設定になります。 |
| Sensor Uplink Interval | Sensor 情報データを Uplink する間隔を設定する<br><br>**<計測モードが「瞬時値モード」の場合>**<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00000001` \| 5秒以下の場合、5秒周期に Sensor 情報データを Uplink します。<br>:<br>`0x00000005` \| 5秒周期に Sensor 情報データを Uplink します<br>:<br>`0x00000E10` \| 3600秒(1H)周期に Sensor 情報データを Uplink します<br>:<br>`0x00015180` \| 86400秒(24H)周期に Sensor 情報データを Uplink します<br>上記以外 \| 60秒周期 Sensor 情報データを Uplink します。<br><br>**<計測モードが「検知モード」の場合>**<br>本設定は無視されます<br><br>**<計測モードが「サンプリングモード」の場合>**<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x0000003C` \| 60秒周期に Sensor 情報データを Uplink します。<br>：<br>`0x00000E10` \| 3600秒(1H)周期に Sensor 情報データを Uplink します。<br>：<br>`0x00015180` \| 86400秒(24H)周期に Sensor 情報データを Uplink します。<br>上記以外 \| 60秒周期に Sensor 情報データを Uplink します。 |
| 計測モード | Sensor 情報の扱いを設定します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| 瞬時値モード: Uplink タイミング時の現在の値を通知します<br>`0x01` \| 検知モード: ヒステリシス検知したことを通知します。<br>`0x02` \| サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します。<br>上記以外 \| 瞬時値モードの設定になります |
| サンプリング周期 | 当該センサー情報を Read する周期を設定します<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| 1Hz: 1000ms 周期にセンサー情報を Read します<br>`0x01` \| 2Hz: 500ms 周期にセンサー情報を Read します。<br>`0x02` \| 5Hz: 200ms 周期にセンサー情報を Read します<br>`0x03` \| 10Hz: 100ms 周期にセンサー情報を Read します。<br>`0x04` \| 20Hz: 50ms 周期にセンサー情報を Read します。<br>上記以外 \| 1Hz 設定になります。 |
| ヒステリシス(High) | High 側のヒステリシスを設定します。<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| ±0.5G の振動検知<br>`0x01` \| ±1.0G の振動検知<br>`0x02` \| ±1.5G の振動検知<br>`0x03` \| ±2.0G の振動検知<br>`0x04` \| ±2.5G の振動検知<br>`0x05` \| ±3.0G の振動検知<br>`0x06` \| ±3.5G の振動検知<br>`0x07` \| ±4.0G の振動検知<br>`0x08` \| ±4.5G の振動検知<br>`0x09` \| ±5.0G の振動検知<br>`0x0a` \| ±5.5G の振動検知<br>`0x0b` \| ±6.0G の振動検知<br>`0x0c` \| ±6.5G の振動検知<br>上記以外 \| ヒステリシス検知しません |
| ヒステリシス(Low) | Low 側のヒステリシスを設定します<br><br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| ±0.5G の振動検知<br>`0x01` \| ±1.0G の振動検知<br>`0x02` \| ±1.5G の振動検知<br>`0x03` \| ±2.0G の振動検知<br>`0x04` \| ±2.5G の振動検知<br>`0x05` \| ±3.0G の振動検知<br>`0x06` \| ±3.5G の振動検知<br>`0x07` \| ±4.0G の振動検知<br>`0x08` \| ±4.5G の振動検知<br>`0x09` \| ±5.0G の振動検知<br>`0x0a` \| ±5.5G の振動検知<br>`0x0b` \| ±6.0G の振動検知<br>`0x0c` \| ±6.5G の振動検知<br>上記以外 \| ヒステリシス検知しません |

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
| SensorSetting | `0x3000` | SENS_READ_REQ<br>SENS_READ_RESP<br>SENS MODE<br>SAMPLING<br>HYSTERESIS H<br>HYSTERESIS L |
| DeviceInfo | `0x4000` | DEVICEID<br>FW_VERSION<br>HW_VERSION<br>BATTERY<br>DFU_TYPE<br>DFU_REQUEST<br>REGISTER |

#### 4-3-1. BraveGATEInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| BV DEVICEID | Read | `0x1001` | `0x00` | bvDeviceId [8byte] |
| BV COMPANYID | Read | `0x1002` | `0x00` | bvCompanyId[8byte] |
| BV SENSORID | Read | `0x1003` | `0x00` | bvSensorId [2byte] |

**<BraveGATEInfo Service の詳細>**

- **BV_DEVICEID**: BravePI メインボードとの通信に必要な DeviceID を Read できます。
- **BV_COMPANYID**: BravePI メインボードとの通信に必要な Company ID を Read できます。
- **BV_SENSORID**: BravePI メインボードとの通信に必要な SensorID を Read できます。

#### 4-3-2. DeviceSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| TIME ZONE | Read/Write | `0x2001` | `0x00` | timeZone[1byte] |
| BLE MODE | Read/Write | `0x2002` | `0x00` | bleMode[1byte] |
| TX POWER | Read/Write | `0x2003` | `0x00` | txPower [1byte] |
| ADV_INTERVAL | Read/Write | `0x2004` | `0x00` | advInterval [2byte] |
| UPLINK INTERVAL | Read/Write | `0x2005` | `0x00` | uplinkInterval [4byte] |

**<DeviceSettingInfo Service の詳細>**

- **TIME_ZONE**: タイムゾーンを設定します。
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00` | 日本時間 |
  | `0x01` | UTC |
  | 上記以外 | 日本時間 |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

- **BLE_MODE**: Bluetooth 通信モードの設定情報を以下に示します。
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00` | Long Range |
  | `0x01` | Legacy |
  | 上記以外 | LongRange |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

- **TX_POWER**: Bluetooth 通信モードの設定情報を以下に示します。
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

- **ADV_INTERVAL**: Advertise を発信する間隔を設定します。
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

- **UPLINK_INTERVAL**: Sensor 情報データを Uplink する間隔を設定する。
  
  **<計測モードが「瞬時値モード」の場合>**
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00000001` | 5秒以下の場合、5秒周期に Sensor 情報データを Uplink します。 |
  | : | |
  | `0x00000005` | 5秒周期に Sensor 情報データを Uplink します |
  | : | : |
  | `0x00000E10` | 3600秒(1時間)周期に Sensor 情報データを Uplink します |
  | : | |
  | `0x00015180` | 86400秒(24時間)周期に Sensor 情報データを Uplink します。 |
  | 上記以外 | 60秒周期に Advertise を発信する設定になります。 |

  **<計測モードが「検知モード」の場合>**
  本設定は無視されます。

  **<計測モードが「サンプリングモード」の場合>**
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x0000003C` | 60秒周期に Sensor 情報データを Uplink します |
  | : | |
  | `0x00000E10` | 3600秒(1時間)周期に Sensor 情報データを Uplink します。 |
  | : | : |
  | `0x00015180` | 86400秒(24時間)周期に Sensor 情報データを Uplink します |
  | 上記以外 | 60秒周期に Advertise を発信する設定になります。 |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。
  ※エンディアンはリトルエンディアン。

#### 4-3-3. SensorSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| SENS_READ_REQ | Write | `0x3001` | `0x00` | sensorReq[1byte] |
| SENS READ RESP | Notify | `0x3002` | `0x00` | sensorValue[12byte] |
| SENS MODE | Read/Write | `0x3003` | `0x00` | sensorMode [1byte] |
| SAMPLING | Read/Write | `0x3004` | `0x00` | sampling [1byte] |
| HYSTERESIS H | Read/Write | `0x3005` | `0x00` | hysteresisHigh[4byte] |
| HYSTERESIS L | Read/Write | `0x3006` | `0x00` | hysteresisLow[4byte] |

**<SensorSettingInfo Service の詳細>**

- **SENS_READ_REQ**: `0x01` を write すると現在のセンサー情報取得開始します。

- **SENS_READ_RESP**: SENS_READ_REQ に対する応答で、現在の加速度センサー値を Notify します。
  | データ | サイズ | 説明 |
  | :--- | :--- | :--- |
  | X軸の重力加速度(mG) | 4 | float 型 |
  | Y軸の重力加速度(mG) | 4 | float 型 |
  | Z軸の重力加速度(mG) | 4 | float 型 |
  ※エンディアンはリトルエンディアン。

- **SENS_MODE**: Sensor 情報の扱いを設定する。
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00` | 瞬時値モード: Uplink タイミング時の現在の値を通知します |
  | `0x01` | 検知モード: ヒステリシス検知したことを通知します。 |
  | `0x02` | サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します |
  | 上記以外 | 瞬時値モード設定になります。 |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

- **SAMPLING**: 当該センサー情報を Read する周期を設定します。
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00` | 1Hz: 1000ms 周期にセンサー情報を Read します |
  | `0x01` | 2Hz: 500ms 周期にセンサー情報を Read します |
  | `0x02` | 5Hz: 200ms 周期にセンサー情報を Read します。 |
  | `0x03` | 10Hz: 100ms 周期にセンサー情報を Read します。 |
  | `0x04` | 20Hz: 50ms 周期にセンサー情報を Read します。 |
  | 上記以外 | 1Hz 設定になります。 |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。

- **HYSTERESIS_H**: High 側のヒステリシスを設定します。
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00` | ±0.5G の振動検知 |
  | `0x01` | ±1.0G の振動検知 |
  | `0x02` | ±1.5G の振動検知 |
  | `0x03` | ±2.0G の振動検知 |
  | `0x04` | ±2.5G の振動検知 |
  | `0x05` | ±3.0G の振動検知 |
  | `0x06` | ±3.5G の振動検知 |
  | `0x07` | ±4.0G の振動検知 |
  | `0x08` | ±4.5G の振動検知 |
  | `0x09` | ±5.0G の振動検知 |
  | `0x0a` | ±5.5G の振動検知 |
  | `0x0b` | ±6.0G の振動検知 |
  | `0x0c` | ±6.5G の振動検知 |
  | 上記以外 | ヒステリシス検知しません |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。
  ※エンディアンはリトルエンディアン。

- **HYSTERESIS_L**: Low 側のヒステリシスを設定します。
  | 設定値 | 説明 |
  | :--- | :--- |
  | `0x00` | ±0.5G の振動検知 |
  | `0x01` | ±1.0G の振動検知 |
  | `0x02` | ±1.5G の振動検知 |
  | `0x03` | ±2.0G の振動検知 |
  | `0x04` | ±2.5G の振動検知 |
  | `0x05` | ±3.0G の振動検知 |
  | `0x06` | ±3.5G の振動検知 |
  | `0x07` | ±4.0G の振動検知 |
  | `0x08` | ±4.5G の振動検知 |
  | `0x09` | ±5.0G の振動検知 |
  | `0x0a` | ±5.5G の振動検知 |
  | `0x0b` | ±6.0G の振動検知 |
  | `0x0c` | ±6.5G の振動検知 |
  | 上記以外 | ヒステリシス検知しません |
  ※設定後、DeviceInfo/REGISTER を実行することで設定が反映されます。
  ※エンディアンはリトルエンディアン。

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

- **DEVICEID**: Nordic のチップのユニークなIDを読み出せます。
- **FW_VERSION**: 本製品のファームウェアバージョンを読み出せます。例: Ver1.2.9 の場合は、`[0x01, 0x02, 0x09]` で通知されます。
- **HW_VERSION**: 本製品のHWバージョンを読み出せます。例: Ver1.2.9 の場合は、`[0x01, 0x02, 0x09]` で通知されます。
- **BATTERY**: 本製品の現在のバッテリーレベル(%)を読み出せます。
- **DFU_TYPE**: 固定で `0x01` が読み出されます。
- **DFU_REQUEST**: `0x01` を Write すると、Bluetooth 切断し、DFU モードに移行します。
- **REGISTER**: `0x66a781` を write すると変更された変更されて全ての情報を保存し、変更した設定を有効にします。

---

## 5. 動作フロー

[画像: 動作フローチャート]

- POWER ON
- NFCTag 検知 (YES) -> NFC 要求処理実行 -> POWER OFF 中
- NFCTag 検知 (NO) -> POWER OFF 中
- POWER OFF 中 (YES) -> (ループして NFCTag 検知へ)
- POWER OFF 中 (NO) -> Config モード中
- Config モード中 (YES) -> Config モード中動作 -> (ループして NFCTag 検知へ)
- Config モード中 (NO) -> センサー Read タイミング
- センサー Read タイミング (YES) -> センサー情報 Read 実行 -> (ループして NFCTag 検知へ)
- センサー Read タイミング (NO) -> Uplink タイミング
- Uplink タイミング (YES) -> Uplink 実行 -> (ループして NFCTag 検知へ)
- Uplink タイミング (NO) -> Downlink 受信
- Downlink 受信 -> Downlink 受信処理実行 -> (ループして NFCTag 検知へ)

---

## 6. Uplink データ仕様

BravePI メインボードから通知される情報ついて以下に示す。

### 6-1. Sensor 情報

SensorID: `0x0106`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| DataLength | 2 | Data 部分のデータ長 | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0106` | |
| RSSI | 1 | Bluetooth 電波強度 | |
| Flag | 1 | `0x00`:継続データなし | |

**Data 領域**

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Battery Level | 1 | バッテリーレベル(%) | |
| sampleNum | 2 | サンプル数 | |
| acceleData[0] | | | |
| - X軸の重力加速度(mG) | 4 | X軸の重力加速度(mG) | float 型 |
| - Y軸の重力加速度(mG) | 4 | Y軸の重力加速度(mG) | float 型 |
| - Z軸の重力加速度(mG) | 4 | Z軸の重力加速度(mG) | float 型 |
| : | : | : | |
| acceleData[n] | | | |
| - X軸の重力加速度(mG) | 4 | X軸の重力加速度(mG) | float 型 |
| - Y軸の重力加速度(mG) | 4 | Y軸の重力加速度(mG) | float 型 |
| - Z軸の重力加速度(mG) | 4 | Z軸の重力加速度(mG) | float 型 |

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
| SensorID | 2 | `0x0107` 固定 | |
| FW Version | 3 | 本製品のファームウェアバージョン | Ver1.2.9 の場合は、`[0x01,0x02,0x09]` |
| TimeZone | 1 | タイムゾーン設定 | |
| BLE Mode | 1 | Bluetooth 通信モードの設定情報 | |
| Tx Power | 1 | Bluetooth 通信の送信電波出力 | |
| Advertise Interval | 2 | Advertise を発信する間隔 | |
| Sensor Uplink Interval | 4 | Sensor 情報データを Uplink する間隔 | |
| Sensor Read Mode | 1 | 計測モード | |
| Sampling | 1 | サンプリング周期 | |
| HysteresisHigh | 4 | ヒステリシス(High) | |
| HysteresisLow | 4 | ヒステリシス(Low) | |

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
| SensorID | 2 | `0x0107` | |
| CMD | 1 | `0x00` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| Data | | なし | |

※エンディアンはリトルエンディアンになります。データ作成時はリトルエンディアンで作成して下さい。

### 7-2. パラメータ情報設定要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00`固定 | |
| DataLength | 2 | `0x0014` | |
| DeviceID | 8 | 対象の DeviceID | |
| SensorID | 2 | `0x0000` | |
| CMD | 1 | `0x05` | |
| Flag | 1 | `0x00` | |
| **Data 部** | | | |
| SensorID | 2 | `0x0107` | |
| TimeZone | 1 | タイムゾーン設定 | |
| Tx Power | 1 | Bluetooth 通信の送信電波出力 | |
| Advertise Interval | 2 | Advertise を発信する間隔 | |
| Sensor Uplink Interval | 4 | Sensor 情報データを Uplink する間隔 | |
| Sensor Read Mode | 1 | 計測モード | |
| Sampling | 1 | サンプリング周期 | |
| HysteresisHigh | 4 | ヒステリシス(High) | |
| HysteresisLow | 4 | ヒステリシス(Low) | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-3. パラメータ情報取得要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| Type | 1 | `0x00` 固定 | |
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
| Type | 1 | `0x00`固定 | |
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

BravePI トランスミッター(CR123A) 使用時の代表的な設定におけるおおよその電池持ちを以下に示します。

**<Bluetooth 通信モード: Legacy の場合>**

| パラメータ設定情報 | | | | | 電池持ち |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **計測モード** | **サンプリング周期** | **TxPower** | **Uplink Interval** | **Advertise Interval** | **(日)** |
| 瞬時値モード | | 0dBm | 5秒 | 100ms | 54 |
| | | | 10秒 | 100ms | 76 |
| | | | | 1000ms | 102 |
| | | | 60秒 | 100ms | 111 |
| | | | | 1000ms | 248 |
| 検知モード | 1Hz | 0dBm | 60秒 | 100ms | 101 |
| | | | | 1000ms | 206 |
| サンプリングモード | 10Hz | 0dBm | 60秒 | 100ms | 62 |
| | | | | 1000ms | 80 |
| | 20Hz | 0dBm | 60秒 | 100ms | 44 |
| | | | | 1000ms | 48 |

**<Bluetooth 通信モード: Long Range の場合>**

| パラメータ設定情報 | | | | | 電池持ち |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **計測モード** | **サンプリング周期** | **TxPower** | **Uplink Interval** | **Advertise Interval** | **(日)** |
| 瞬時値モード | | 0dBm | 5秒 | 100ms | 15 |
| | | | 10秒 | 100ms | 23 |
| | | | | 1000ms | 31 |
| | | | 60秒 | 100ms | 37 |
| | | | | 1000ms | 111 |
| 検知モード | 1Hz | 0dBm | 60秒 | 100ms | 35 |
| | | | | 1000ms | 88 |
| サンプリングモード | 10Hz | 0dBm | 60秒 | 100ms | 22 |
| | | | | 1000ms | 30 |
| | 20Hz | 0dBm | 60秒 | 100ms | 15 |
| | | | | 1000ms | 17 |

---

## 9. 製品到着から使用開始までの流れ

### 9-1. BravePI トランスミッターの設定

BravePI トランスミッター側の設定手順について以下に示します。

1. トランスミッターからセンサーを外した状態にする。
2. トランスミッターに電池又はUSB給電する。
3. 専用の iPhone アプリを起動する。
4. iPhone アプリから加速度センサー用の「DFU」を実行する。
5. iPhone アプリから加速度センサー用の「パラメータ設定」を実行する。
6. トランスミッターに加速度センサーを取り付ける。
7. iPhone アプリからトランスミッターに電源ON(再起動)操作を行う。

次に BravePI トランスミッターと BravePI メインボードの紐付けを実行して下さい。

### 9-2. BravePI トランスミッターと BravePI メインボードの紐付け

BravePI トランスミッターと BravePI メインボードの紐付け手順について以下に示します。

1. 専用の iPhone アプリを起動する。
2. iPhone アプリから「ペアリング設定」を実行する。

以上で設定は終了です。

---

## 10. 商標について

- Bluetooth® とワードマークおよびロゴは、Bluetooth SIG INC が所有する登録商標です。
- 株式会社 Braveridge はこれら商標を使用する許可を受けています。その他のロゴマーク及び商号は各所有者に帰属します。

## 11. Revision 管理

| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023/10/16 | Ver1.0.0 | 初版 |
| 1.1 | 2023/11/10 | Ver1.0.2 | Uplink Interval の最小時間変更 |

※上記、製品仕様や機能、デザインは変更となる可能性がございます。あらかじめご了承ください。

---

**Braveridge**

Braveridgeとその製品に関する詳しい情報は、弊社Webサイトで御確認ください。
[https://www.braveridge.com/](https://www.braveridge.com/)

- **株式会社Braveridge 本社**
  〒819-0373 福岡県福岡市西区周船寺3-27-2
  (Tel): 092-834-5789 / (Fax): 092-807-7718

- **株式会社Braveridge 糸島工場**
  〒819-1122 福岡県糸島市東1999-19
  - Apple MFi Manufacture ライセンス認定工場(ライトニングコネクタ製品工場)