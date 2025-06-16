**公式仕様書**: [ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (接点出力センサー版)](https://drive.google.com/file/d/1t0C6AN2X27W4xw-IGD0meg2y4P2k_Kb5/view)

# 目次

  - [1 製品概要](https://www.google.com/search?q=%231-%E8%A3%BD%E5%93%81%E6%A6%82%E8%A6%81)
  - [2 機能概要](https://www.google.com/search?q=%232-%E6%A9%9F%E8%83%BD%E6%A6%82%E8%A6%81)
      - [2-1 Sensor データ取得機能](https://www.google.com/search?q=%232-1-sensor-%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
      - [2-2 LED 表示機能](https://www.google.com/search?q=%232-2-led-%E8%A1%A8%E7%A4%BA%E6%A9%9F%E8%83%BD)
      - [2-3 Bluetooth通信機能](https://www.google.com/search?q=%232-3-bluetooth%E9%80%9A%E4%BF%A1%E6%A9%9F%E8%83%BD)
      - [2-4 NFCTag 通信機能](https://www.google.com/search?q=%232-4-nfctag-%E9%80%9A%E4%BF%A1%E6%A9%9F%E8%83%BD)
      - [2-5 パラメータ変更/取得機能](https://www.google.com/search?q=%232-5-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%A4%89%E6%9B%B4%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
      - [2-6 DFU 機能](https://www.google.com/search?q=%232-6-dfu-%E6%A9%9F%E8%83%BD)
  - [3 パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)
  - [4 Config モード時 Bluetooth通信仕様](https://www.google.com/search?q=%234-config-%E3%83%A2%E3%83%BC%E3%83%89%E6%99%82-bluetooth%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98)
      - [4-1 基本情報](https://www.google.com/search?q=%234-1-%E5%9F%BA%E6%9C%AC%E6%83%85%E5%A0%B1)
      - [4-2 Advertise/Scan Response Packet](https://www.google.com/search?q=%234-2-advertisescan-response-packet)
      - [4-3 Service](https://www.google.com/search?q=%234-3-service)
  - [5 動作フロー](https://www.google.com/search?q=%235-%E5%8B%95%E4%BD%9C%E3%83%95%E3%83%AD%E3%83%BC)
  - [6 Uplink データ仕様](https://www.google.com/search?q=%236-uplink-%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98)
      - [6-1 Sensor 情報](https://www.google.com/search?q=%236-1-sensor-%E6%83%85%E5%A0%B1)
      - [6-2 パラメータ情報](https://www.google.com/search?q=%236-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)
  - [7 Downlink データ仕様](https://www.google.com/search?q=%237-downlink-%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98)
      - [7-1 即時 Uplink 要求](https://www.google.com/search?q=%237-1-%E5%8D%B3%E6%99%82-uplink-%E8%A6%81%E6%B1%82)
      - [7-2 パラメータ情報設定要求](https://www.google.com/search?q=%237-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1%E8%A8%AD%E5%AE%9A%E8%A6%81%E6%B1%82)
      - [7-3 パラメータ情報取得要求](https://www.google.com/search?q=%237-3-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1%E5%8F%96%E5%BE%97%E8%A6%81%E6%B1%82)
      - [7-4 接点出力要求](https://www.google.com/search?q=%237-4-%E6%8E%A5%E7%82%B9%E5%87%BA%E5%8A%9B%E8%A6%81%E6%B1%82)
      - [7-5 デバイス Config 移行要求](https://www.google.com/search?q=%237-5-%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9-config-%E7%A7%BB%E8%A1%8C%E8%A6%81%E6%B1%82)
      - [7-6 デバイス再起動要求](https://www.google.com/search?q=%237-6-%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9%E5%86%8D%E8%B5%B7%E5%8B%95%E8%A6%81%E6%B1%82)
  - [8 電池駆動時の各設定における電池持ち](https://www.google.com/search?q=%238-%E9%9B%BB%E6%B1%A0%E9%A7%86%E5%8B%95%E6%99%82%E3%81%AE%E5%90%84%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E9%9B%BB%E6%B1%A0%E6%8C%81%E3%81%A1)
  - [9 製品到着から使用開始までの流れ](https://www.google.com/search?q=%239-%E8%A3%BD%E5%93%81%E5%88%B0%E7%9D%80%E3%81%8B%E3%82%89%E4%BD%BF%E7%94%A8%E9%96%8B%E5%A7%8B%E3%81%BE%E3%81%A7%E3%81%AE%E6%B5%81%E3%82%8C)
      - [9-1 BravePI トランスミッターの設定](https://www.google.com/search?q=%239-1-bravepi-%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B9%E3%83%9F%E3%83%83%E3%82%BF%E3%83%BC%E3%81%AE%E8%A8%AD%E5%AE%9A)
      - [9-2 BravePI トランスミッターと BravePI メインボードの紐付け](https://www.google.com/search?q=%239-2-bravepi-%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B9%E3%83%9F%E3%83%83%E3%82%BF%E3%83%BC%E3%81%A8-bravepi-%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%E7%B4%90%E4%BB%98%E3%81%91)
  - [8 Revision 管理](https://www.google.com/search?q=%238-revision-%E7%AE%A1%E7%90%86)

-----

# 1 製品概要

[cite\_start]本仕様書は、BravePI トランスミッターに接点出力センサーボードを接続した際に使用するファームウェア(以降、本製品とする)のソフトウェア仕様を記載したものです。 [cite: 8]

[cite\_start]本仕様書は、対象とするハードウェアを以下に示します。 [cite: 8]

[cite\_start]\<BravePI トランスミッター\> [cite: 8]

| 製品名 | 型番 |
| :--- | :--- |
| BravePI トランスミッター (CR123A) | `BVPTB-01` |
| BravePI トランスミッター (USB) | `BVPTU-01` |

[cite\_start]\<BravePI センサーボード\> [cite: 10]

| 製品名 | 型番 |
| :--- | :--- |
| BravePI 接点出力センサーボード | `BVPSO-01` |

[cite\_start]BravePI トランスミッターは、取得した接点出力センサーの値をペアリングされた BravePI メインボードに通知します。 [cite: 12]

[cite\_start][画像: BravePI トランスミッターとBravePI メインボードのBluetooth通信を示す図] [cite: 12]

-----

# 2 機能概要

## 2-1 Sensor データ取得機能

[cite\_start]本製品は、接続した接点出力センサーに接続された機器に接点出力することができます。 [cite: 13]

| 項目 | 説明 |
| :--- | :--- |
| 接点出力情報 | `OFF(0)`/`ON(1)` |
| 接点出力時間 | `出力維持(0)`/`出力時間(1ms~65535ms)` |

## 2-2 LED 表示機能

[cite\_start]本製品は、本製品の状態をLEDで表示します。 [cite: 17]

| 優先 | 状態 | 赤 | LED 緑 | 青 | 備考 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 高 | LowBattery 状態 | 点滅 | | | 1秒点灯、3秒消灯を繰り返す |
| 1 | Config モード | | 点滅 | | 1秒点灯、3秒消灯を繰り返す |
| | PowerON | - | | 点灯 | 2 秒点灯 |
| | PowerOFF | 点灯 | | - | 2秒点灯 |
| 低 | 上記以外(通常動作中) | | | | 無灯 |

## 2-3 Bluetooth通信機能

[cite\_start]本製品は接続されたセンサー基板から取得されたセンサー情報を `Bleutooth` 通信で BravePI メインボードに通知します。また、BravePI メインボード経由で本製品に対して設定や指示等を `Downlink` することも可能です。 [cite: 17]

### 2-3-1 Uplink

[cite\_start]以下の情報を `Uplink` することができます。 [cite: 17]

| Uplink 情報 | Uplink タイミング |
| :--- | :--- |
| 接点出力状態データ | 即時 `Uplink` 要求された場合 |
| パラメータ情報 | `Downlink` でパラメータ情報取得要求された場合 |

### 2-3-2 Downlink

[cite\_start]以下の指示を`Downlink` することができます。 [cite: 19]

| Downlink 情報 | 動作概要 |
| :--- | :--- |
| 即時 `Uplink` 要求 | 現在のセンサー情報の `Uplink` 要求します。 |
| パラメータ情報設定要求 | 本製品のパラメータ情報を設定します。 |
| パラメータ情報取得要求 | 本製品のパラメータ情報の `Uplink` 要求します。 |
| デバイス `Config` 移行 | 本製品を `Config` モードに移行します。 |
| デバイス再起動 | 本製品を再起動します。 |

## 2-4 NFCTag 通信機能

[cite\_start]本製品は `NFCTag` を有しており、専用スマホアプリより各種設定や情報取得することができます。 [cite: 22]
[cite\_start]以下が `NFCTag` 機能で専用スマホアプリより行える操作になります。 [cite: 22]

| 項目 | 動作概要 | 備考 |
| :--- | :--- | :--- |
| デバイス再起動 | 本製品を再起動する。 | |
| 電源ON 要求 | 本製品を電源OFFから復帰する。 | |
| 電源OFF 要求 | 本製品を電源OFFにする (`NFCTag` のみ有効) | 電源OFF状態の場合は、本要求は 無視されます。 |
| `Config` モード移行要求 | 本製品を `Config` モードに移行します。 | 電源OFF状態の場合は、本要求は 無視されます。 |

## 2-5 パラメータ変更/取得機能

[cite\_start]本製品のパラメータ情報の変更/取得することができます。 [cite: 24]

### 2-5-1 パラメータ変更方法について

[cite\_start]本製品のパラメータ情報の変更は以下の方法で行えます。 [cite: 24]

  - [cite\_start]BravePI メインボードからパラメータ情報を `Downlink` することで変更することができます。 [cite: 24]
  - [cite\_start]本製品を `Config` モードにすることで、`Bleutooth`経由で変更することができます。 [cite: 24]

### 2-5-2 パラメータ取得方法について

[cite\_start]本製品のパラメータ情報の設定は以下の方法で行えます。 [cite: 24]

  - [cite\_start]BravePI メインボードからパラメータ取得要求を `Downlink` することでパラメータ情報を `Uplink` します。 [cite: 24]
  - [cite\_start]本製品を `Config` モードにすることで、`Bleutooth`経由で取得することができます。 [cite: 24]

### 2-5-3 変更可能なパラメータについて

[cite\_start]本製品の変更/取得可能なパラメータに関しては「[3 パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)」を参照下さい。 [cite: 24]

## 2-6 DFU 機能

[cite\_start]専用スマホアプリを使用することで、本製品のファームウェアの書き換えができます。 [cite: 24]
[cite\_start]本製品のファームウェアの書き換えは、専用スマホアプリ以外からは行えません。 [cite: 24]

-----

# 3 パラメータ情報

[cite\_start]本製品のパラメータを以下に示します。 [cite: 25]

| パラメータ項目 | 設定情報 |
| :--- | :--- |
| `DeviceID` | BravePI メインボードと通信する為に必要な、`DeviceID`. |
| `SensorID` | BravePI メインボードと通信する為に必要な、`SensorID` |
| タイムゾーン設定 | タイムゾーン設定に関する設定情報を以下に示します |
| | **設定値** **説明** |
| | `0x00` 日本時間 |
| | `0x01` `UTC` |
| | 上記以外 日本時間 |
| `BLE Mode` | `Bluetooth` 通信モードの設定情報を以下に示します。 |
| | **設定値** **説明** |
| | `0x00` `LongRange` |
| | `0x01` `Legacy` |
| | 上記以外 `Long Range` |
| `Tx Power` | `Bluetooth` 通信の送信電波出力の設定情報を以下に示します。 |
| | **設定値** **説明** |
| | `0x00` `±0dBm` |
| | `0x01` `+4dBm` |
| | `0x02` `-4dBm` |
| | `0x03` `-8dBm` |
| | `0x04` `-12dBm` |
| | `0x05` `-16dBm` |
| | `0x06` `-20dBm` |
| | `0x07` `-40dBm` |
| | `0x08` `+8dBm` |
| | 上記以外 `±0dBm` |
| `Advertise Interval` | `Advertise` を発信する間隔設定情報を以下に示します。 |
| | **設定値** **説明** |
| | `0x0064` `100ms` 周期に `Advertise` を発信します。 |
| | : : |
| | `0x03E8` `1000ms` 周期に`Advertise`を発信します。 |
| | : : |
| | `0x2710` `10000ms` 周期に`Advertise` を発信します。 |
| | 上記以外 `1000ms` 周期に`Advertise` を発信する設定になります。 |
| `Sensor Uplink Interval` | `Sensor` 情報データを `Uplink` する間隔を設定する。本設定は無視されます。 |

-----

# 4 Config モード時 Bluetooth通信仕様

[cite\_start]`Config` モード時用の`Bluetooth` 通信プロファイル仕様を以下に示します。 [cite: 29]

## 4-1 基本情報

| 項目 | 値 |
| :--- | :--- |
| `Advertising Interval` | `1000ms` |
| `Min Connection Interval` | `20ms` |
| `Max Connection Interval` | `40ms` |
| `Slave Latency` | `0` |
| `Supervision Timeout` | `6000ms` |

## 4-2 Advertise/Scan Response Packet

[cite\_start]\<Advertise データ\> [cite: 31]

| Index | Data | Description | Comment |
| :--- | :--- | :--- | :--- |
| 0 | `0x02` | Length | |
| 1 | `0x01` | Advertising Field Type | `FLAGS` |
| 2 | `0x06` | Flag type | `LE ONLY GENERAL DISCOVER MODE` |
| 3 | `0x11` | Length | |
| 4 | `0x07` | Advertising Field Type | `Complete List of 128-bit Service Class UUIDS` |
| 5-20 | 右記 | `Service UUID` | `57791000-a129-4d7f-93a6-87f82b59f6a4` |
| 21 | `0x06` | Length | |
| 22 | `0x09` | Advertising Field Type | `Complete Local Name` |
| 23-28 | 右記 | `Local Name` | `BvPiTm` |

[cite\_start]\<ScanResponse データ\> [cite: 33]
[cite\_start]なし [cite: 33]

## 4-3 Service

`677eXXXX-79f2-4584-91f9-098db93d0781`
[cite\_start]以下の `Service`/`Characteristic` の`UUID`は上記 `UUID` の `XXXX` (Alias)の部分に各`Service`/`Characteristic` の `Alias` を設定した値になります。 [cite: 34]

| Service Name | Alias | Characteristic Name |
| :--- | :--- | :--- |
| `BraveGATEInfo` | `0x1000` | `BV DEVICEID`\<br\>`BV COMPANYID`\<br\>`BV SENSORID` |
| `DeviceSetting` | `0x2000` | `TIME ZONE`\<br\>`BLE MODE`\<br\>`TX POWER`\<br\>`ADV INTERVAL`\<br\>`UPLINK INTERVAL` |
| `SensorSetting` | `0x3000` | `SENS_READ_REQ`\<br\>`SENS_READ_RESP`\<br\>`SENS CONTACT OUT` |
| `DeviceInfo` | `0x4000` | `DEVICEID`\<br\>`FW VERSION`\<br\>`HW_VERSION`\<br\>`BATTERY`\<br\>`DFU_TYPE`\<br\>`DFU_REQUEST`\<br\>`REGISTER` |

### 4-3-1 BraveGATEInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `BV DEVICEID` | Read | `0x1001` | `0x00` | `bvDeviceId [8byte]` |
| `BV COMPANYID` | Read | `0x1002` | `0x00` | `bvCompanyId[8byte]` |
| `BV SENSORID` | Read | `0x1003` | `0x00` | `bvSensorId [2byte]` |

[cite\_start]\<BraveGATEInfo Service の詳細\> [cite: 38]

  - [cite\_start]`BV_DEVICEID`: BravePI メインボードとの通信に必要な `DeviceID` を Read できます。 [cite: 38]
  - [cite\_start]`BV_COMPANYID`: BravePI メインボードとの通信に必要な `CompanyID` を Read できます。 [cite: 38]
  - [cite\_start]`BV_SENSORID`: BravePI メインボードとの通信に必要な `SensorID`をRead できます。 [cite: 38]

### 4-3-2 DeviceSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `TIME ZONE` | Read/Write | `0x2001` | `0x00` | `timeZone[1byte]` |
| `BLE MODE` | Read/Write | `0x2002` | `0x00` | `bleMode[1byte]` |
| `TX POWER` | Read/Write | `0x2003` | `0x00` | `txPower[1byte]` |
| `ADV_INTERVAL` | Read/Write | `0x2004` | `0x00` | `advInterval [2byte]` |
| `UPLINK INTERVAL` | Read/Write | `0x2005` | `0x00` | `uplinkInterval [4byte]` |

[cite\_start]\<DeviceSettingInfo Service の詳細\> [cite: 41]

  - [cite\_start]`TIME_ZONE`: タイムゾーンを設定します。 [cite: 41]

| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | 日本時間 |
| `0x01` | `UTC` |
| 上記以外 | 日本時間 |

[cite\_start]※設定後、`DeviceInfo`/`REGISTER` を実行することで設定が反映されます。 [cite: 43]

  - [cite\_start]`BLE_MODE`: `Bluetooth` 通信モードの設定情報を以下に示します。 [cite: 43]

| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | `Long Range` |
| `0x01` | `Legacy` |
| 上記以外 | `LongRange` |

[cite\_start]※設定後、`DeviceInfo`/`REGISTER` を実行することで設定が反映されます。 [cite: 45]

  - [cite\_start]`TX_POWER`: `Bluetooth` 通信モードの設定情報を以下に示します。 [cite: 45]

| 設定値 | 説明 |
| :--- | :--- |
| `0x00` | `±0dBm` |
| `0x01` | `+4dBm` |
| `0x02` | `-4dBm` |
| `0x03` | `-8dBm` |
| `0x04` | `-12dBm` |
| `0x05` | `-16dBm` |
| `0x06` | `-20dBm` |
| `0x07` | `-40dBm` |
| `0x08` | `+8dBm` |
| 上記以外 | `±0dBm` |

[cite\_start]※設定後、`DeviceInfo`/`REGISTER` を実行することで設定が反映されます。 [cite: 47]

  - [cite\_start]`ADV_INTERVAL`: `Advertise` を発信する間隔を設定します。 [cite: 50]

| 設定値 | 説明 |
| :--- | :--- |
| `0x0064` | `100ms` 周期に `Advertise` を発信します。 |
| : | : |
| `0x03E8` | `10000ms` 周期に `Advertise` を発信します。 |
| : | : |
| `0x2710` | `10000ms` 周期に`Advertise` を発信します。 |
| 上記以外 | `1000ms` 周期に`Advertise` を発信する設定になります。 |

[cite\_start]※設定後、`DeviceInfo`/`REGISTER` を実行することで設定が反映されます。 [cite: 50]
[cite\_start]※エンディアンはリトルエンディアン。 [cite: 50]

  - [cite\_start]`UPLINK_INTERVAL`: `Sensor` 情報データを `Uplink` する間隔を設定する。本設定は無視されます。 [cite: 50]

### 4-3-3 SensorSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `SENS_READ_REQ` | Write | `0x3001` | `0x00` | `sensnorReq[1byte]` |
| `SENS READ RESP` | Notify | `0x3002` | `0x00` | `sensnorValue[1byte]` |
| `SENS CONTACT _OUT` | Write | `0x3003` | `0x00` | `sensnorOutput[1byte]` |
| | | | `0x01` | `sensnorOutTime[2byte]` |

[cite\_start]\<SensorSettingInfo Service の詳細\> [cite: 53]

  - [cite\_start]`SENS_READ_REQ`: `0x01`を`write` すると現在のセンサー情報取得開始します。 [cite: 53]
  - [cite\_start]`SENS_READ_RESP`: `SENS_READ_REQ` に対する応答で、現在の接点状態を`Notify` します。 [cite: 53]

| 接点状態 | 値 |
| :--- | :--- |
| `OFF` | `0x00` |
| `ON` | `0x01` |

  - [cite\_start]`SENS_CONTACT_OUT`: 接点出力を開始します。 [cite: 55]

| 項目 | サイズ | 説明 |
| :--- | :--- | :--- |
| 接点出力情報 | 1 | `OFF(0)`/`ON(1)` |
| 接点出力時間 | 2 | `出力維持(0)`/`出力時間(1ms~65535ms)` |

[cite\_start]※エンディアンはリトルエンディアン。 [cite: 57]

### 4-3-4 DeviceInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `DEVICEID` | Read | `0x4001` | `0x00` | `nordicDeviceId[8byte]` |
| `FW VERSION` | Read | `0x4002` | `0x00` | `fwVersion [3byte]` |
| `HW VERSION` | Read | `0x4003` | `0x00` | `hwVersion[3byte]` |
| `BATTERY` | Read | `0x4004` | `0x00` | `battery Level [1byte]` |
| `DFU TYPE` | Read | `0x4005` | `0x00` | `dfuType[1byte]` |
| `DFU_REQUEST` | Write | `0x4006` | `0x00` | `dfuRequest[1byte]` |
| `REGISTER` | Write | `0x4007` | `0x00` | `register[3byte]` |

[cite\_start]\<DeviceInfo Service の詳細\> [cite: 60]

  - [cite\_start]`DEVICEID`: `Nordic` のチップのユニークなIDを読み出せます。 [cite: 60]
  - [cite\_start]`FW_VERSION`: 本製品のFWバージョンを読み出せます。例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]` で通知されます。 [cite: 60]
  - [cite\_start]`HW_VERSION`: 本製品のHW バージョンを読み出せます。例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。 [cite: 60]
  - [cite\_start]`BATTERY`: 本製品の現在のバッテリーレベル(%)を読み出せます。 [cite: 60]
  - [cite\_start]`DFU_TYPE`: 固定で `0x01` が読み出されます。 [cite: 60]
  - [cite\_start]`DFU_REQUEST`: `0x01`を `Write` すると、`Bluetooth` 切断し、`DFU` モードに移行します。 [cite: 60]
  - [cite\_start]`REGISTER`: `0x66a781` を `write` すると変更された変更されて全ての情報を保存し、変更した設定を有効にします。 [cite: 60]

-----

# 5 動作フロー

[cite\_start][画像: 動作フローチャート。POWER ONから始まり、NFCTag検知、POWER OFF中、Configモード中、センサーReadタイミング、Uplinkタイミング、Downlink受信の各状態と処理を示す。] [cite: 61]

-----

# 6 Uplink データ仕様

[cite\_start]BravePI メインボードから通知される情報ついて以下に示す。 [cite: 62]

## 6-1 Sensor 情報

[cite\_start]`SensorID`: `0x0102` [cite: 62]

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0102` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | `0x00`:継続データなし | |
| Data 領域 | | | |
| `Battery Level` | 1 | バッテリーレベル(%) | |
| `sampleNum` | 2 | サンプル数 | |
| `Status` | 4 | 現在の接点状態 | `OFF(0)`/`ON(1)` |

[cite\_start]※エンディアンはリトルエンディアンになります。 [cite: 64]

## 6-2 パラメータ情報

`SensorID`: `0x0000`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | Data 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | `0x00`:継続データなし | |
| Data 領域 | | | |
| `SensorID` | 2 | `0x0102` 固定 | |
| `FW Version` | 3 | 本製品のFWバージョン | `Ver1.2.9`の場合は、`[0x01,0x02,0x09]` |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `BLE Mode` | 1 | `Bluetooth` 通信モードの設定情報 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | 必ず0が設定される |

[cite\_start]※エンディアンはリトルエンディアンになります。 [cite: 64]

-----

# 7 Downlink データ仕様

[cite\_start]BravePI メインボードから送信する情報ついて以下に示す。 [cite: 65]

## 7-1 即時 Uplink 要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0102` | |
| `CMD` | 1 | `0x00` | |
| `Flag` | 1 | `0x00` | |
| Data 部 | | | |
| `Data` | | なし | |

[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 67]

## 7-2 パラメータ情報設定要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0006` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x05` | |
| `Flag` | 1 | `0x00` | |
| Data 部 | | | |
| `SensorID` | 2 | `0x0101` | |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |

[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 69]

## 7-3 パラメータ情報取得要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00`固定 | |
| `DataLength` | 2 | `0x0001` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x0D` | |
| `Flag` | 1 | `0x00` | |
| Data 部 | | | |
| `Data` | 1 | `0x00` | |

[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 72]

## 7-4 接点出力要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0003` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0102` | |
| `CMD` | 1 | `0x11` | |
| `Flag` | 1 | `0x00` | |
| Data 部 | | | |
| `Signal Mode` | 1 | 接点出力情報 | |
| `Signal Out Time` | 2 | 接点出力時間(ms) | |

[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 74]

## 7-5 デバイス Config 移行要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0xFC` | |
| `Flag` | 1 | `0x00` | |
| Data 部 | | | |
| `Data` | | なし | |

[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 76]

## 7-6 デバイス再起動要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00`固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0xFD` | |
| `Flag` | 1 | `0x00` | |
| Data 部 | | | |
| `Data` | | なし | |

[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 79]

-----

# 8 電池駆動時の各設定における電池持ち

[cite\_start]本製品を電池駆動させた場合の代表的な設定におけるおおよその電池持ちを以下に示します。 [cite: 80]
[cite\_start]\<`Bluetooth` モード: `Legacy` の場合\> [cite: 80]

| 計測モード | パラメータ設定情報 | 接点状態 | 電池持ち (日) |
| :--- | :--- | :--- | :--- |
| | `TxPower` | `Advertise Interval` | |
| 検知モード | `0dBm` | `100ms` | ON 出力状態 | 7 |
| | | | OFF 出力状態 | 175 |
| | | `1000ms` | ON 出力状態 | 7 |
| | | | OFF 出力状態 | 1050 |

[cite\_start]\<`Bluetooth` モード: `Long Range` の場合\> [cite: 82]

| 計測モード | パラメータ設定情報 | 接点状態 | 電池持ち (日) |
| :--- | :--- | :--- | :--- |
| | `TxPower` | `Advertise Interval` | |
| 検知モード | `0dBm` | `100ms` | ON 出力状態 | 5 |
| | | | OFF 出力状態 | 45 |
| | | `1000ms` | ON 出力状態 | 6 |
| | | | OFF 出力状態 | 385 |

-----

# 9 製品到着から使用開始までの流れ

## 9-1 BravePI トランスミッターの設定

[cite\_start]BravePI トランスミッター側の設定手順について以下に示します。 [cite: 85]

1.  [cite\_start]トランスミッターからセンサーを外した状態にする。 [cite: 85]
2.  [cite\_start]トランスミッターに電池又はUSB給電する。 [cite: 85]
3.  [cite\_start]専用の iPhone アプリを起動する。 [cite: 85]
4.  [cite\_start]iPhone アプリから接点出力センサー用の「ファームウェア書き込み」を実行する。 [cite: 85]
5.  [cite\_start]iPhone アプリから接点出力センサー用の「パラメータ設定」を実行する。 [cite: 85]
6.  [cite\_start]トランスミッターに接点出力センサーを取り付ける。 [cite: 85]
7.  [cite\_start]iPhone アプリからトランスミッターに電源ON(再起動)操作を行う。 [cite: 85]
    [cite\_start]次に BravePI トランスミッターと BravePI メインボードの紐付けを実行して下さい。 [cite: 85]

## 9-2 BravePI トランスミッターと BravePI メインボードの紐付け

[cite\_start]BravePI トランスミッターと BravePI メインボードの紐付け手順について以下に示します。 [cite: 85]

1.  [cite\_start]専用のiPhone アプリを起動する。 [cite: 85]
2.  [cite\_start]iPhone アプリから「ペアリング」を実行する。 [cite: 85]
    [cite\_start]以上で設定は終了です。 [cite: 85]

-----

# 8 Revision 管理

| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023/11/28 | `Ver1.0.0` | 初版 |

[cite\_start]※上記、製品仕様や機能、デザインは変更となる可能性がございます。あらかじめご了承ください。 [cite: 88]

**Braveridge**
Braveridgeとその製品に関する詳しい情報は、弊社Webサイトで御確認ください。
[cite\_start]https://www.braveridge.com/ [cite: 88]

  - 株式会社Braveridge 本社
    〒819-0373 福岡県福岡市西区周船寺3-27-2
    [cite\_start](https://www.google.com/search?q=Tel): 092-834-5789 / (Fax): 092-807-7718 [cite: 88]

  - 株式会社Braveridge 糸島工場
    〒819-1122 福岡県糸島市東1999-19

      - [cite\_start]Apple MFi Manufacture ライセンス認定工場(ライトニングコネクタ製品工場) [cite: 88]