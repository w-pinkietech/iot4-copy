**公式仕様書**: [ソフトウェア仕様書 Brave PI トランスミッター専用 ファームウェア (熱電対センサー版)](https://drive.google.com/file/d/13UhGmNtsrLN4Siob9l_rnWOBpDOwxtwD/view)

# ソフトウェア仕様書 Brave PI トランスミッター専用 ファームウェア (熱電対センサー版) REV 1.0

## 目次

  - [1. 概要](https://www.google.com/search?q=%231-%E6%A6%82%E8%A6%81)
  - [2. 機能概要](https://www.google.com/search?q=%232-%E6%A9%9F%E8%83%BD%E6%A6%82%E8%A6%81)
      - [2-1. Sensor データ取得機能](https://www.google.com/search?q=%232-1-sensor-%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
          - [2-1-2. 計測モード](https://www.google.com/search?q=%232-1-2-%E8%A8%88%E6%B8%AC%E3%83%A2%E3%83%BC%E3%83%89)
      - [2-2. LED 表示機能](https://www.google.com/search?q=%232-2-led-%E8%A1%A8%E7%A4%BA%E6%A9%9F%E8%83%BD)
      - [2-3. Bluetooth 通信機能](https://www.google.com/search?q=%232-3-bluetooth-%E9%80%9A%E4%BF%A1%E6%A9%9F%E8%83%BD)
          - [2-3-1. Uplink](https://www.google.com/search?q=%232-3-1-uplink)
          - [2-3-2. Downlink](https://www.google.com/search?q=%232-3-2-downlink)
      - [2-4. NFCTag 通信機能](https://www.google.com/search?q=%232-4-nfctag-%E9%80%9A%E4%BF%A1%E6%A9%9F%E8%83%BD)
      - [2-5. パラメータ変更/取得機能](https://www.google.com/search?q=%232-5-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%A4%89%E6%9B%B4%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
          - [2-5-1. パラメータ変更方法について](https://www.google.com/search?q=%232-5-1-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%A4%89%E6%9B%B4%E6%96%B9%E6%B3%95%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
          - [2-5-2. パラメータ取得方法について](https://www.google.com/search?q=%232-5-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
          - [2-5-3. 変更可能なパラメータについて](https://www.google.com/search?q=%232-5-3-%E5%A4%89%E6%9B%B4%E5%8F%AF%E8%83%BD%E3%81%AA%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
      - [2-6. DFU 機能](https://www.google.com/search?q=%232-6-dfu-%E6%A9%9F%E8%83%BD)
  - [3. パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)
  - [4. Config モード時 Bluetooth通信仕様](https://www.google.com/search?q=%234-config-%E3%83%A2%E3%83%BC%E3%83%89%E6%99%82-bluetooth%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98)
      - [4-1. 基本情報](https://www.google.com/search?q=%234-1-%E5%9F%BA%E6%9C%AC%E6%83%85%E5%A0%B1)
      - [4-2. Advertise/Scan Response Packet](https://www.google.com/search?q=%234-2-advertisescan-response-packet)
      - [4-3. Service](https://www.google.com/search?q=%234-3-service)
          - [4-3-1. BraveGATEInfo Service](https://www.google.com/search?q=%234-3-1-bravegateinfo-service)
          - [4-3-2. DeviceSettingInfo Service](https://www.google.com/search?q=%234-3-2-devicesettinginfo-service)
          - [4-3-3. SensorSettingInfo Service](https://www.google.com/search?q=%234-3-3-sensorsettinginfo-service)
          - [4-3-4. DeviceInfo Service](https://www.google.com/search?q=%234-3-4-deviceinfo-service)
  - [5. 動作フロー](https://www.google.com/search?q=%235-%E5%8B%95%E4%BD%9C%E3%83%95%E3%83%AD%E3%83%BC)
  - [6. Uplink データ仕様](https://www.google.com/search?q=%236-uplink-%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98)
      - [6-1. Sensor 情報](https://www.google.com/search?q=%236-1-sensor-%E6%83%85%E5%A0%B1)
      - [6-2. パラメータ情報](https://www.google.com/search?q=%236-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)
  - [7. Downlink データ仕様](https://www.google.com/search?q=%237-downlink-%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98)
      - [7-1. 即時 Uplink 要求](https://www.google.com/search?q=%237-1-%E5%8D%B3%E6%99%82-uplink-%E8%A6%81%E6%B1%82)
      - [7-2. パラメータ情報設定要求](https://www.google.com/search?q=%237-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1%E8%A8%AD%E5%AE%9A%E8%A6%81%E6%B1%82)
      - [7-3. パラメータ情報取得要求](https://www.google.com/search?q=%237-3-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1%E5%8F%96%E5%BE%97%E8%A6%81%E6%B1%82)
      - [7-4. デバイス Config 移行要求](https://www.google.com/search?q=%237-4-%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9-config-%E7%A7%BB%E8%A1%8C%E8%A6%81%E6%B1%82)
      - [7-5. デバイス再起動要求](https://www.google.com/search?q=%237-5-%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9%E5%86%8D%E8%B5%B7%E5%8B%95%E8%A6%81%E6%B1%82)
  - [8. 電池駆動時の各設定における電池持ち](https://www.google.com/search?q=%238-%E9%9B%BB%E6%B1%A0%E9%A7%86%E5%8B%95%E6%99%82%E3%81%AE%E5%90%84%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E9%9B%BB%E6%B1%A0%E6%8C%81%E3%81%A1)
  - [9. 製品到着から使用開始までの流れ](https://www.google.com/search?q=%239-%E8%A3%BD%E5%93%81%E5%88%B0%E7%9D%80%E3%81%8B%E3%82%89%E4%BD%BF%E7%94%A8%E9%96%8B%E5%A7%8B%E3%81%BE%E3%81%A7%E3%81%AE%E6%B5%81%E3%82%8C)
      - [9-1. BravePI トランスミッターの設定](https://www.google.com/search?q=%239-1-bravepi-%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B9%E3%83%9F%E3%83%83%E3%82%BF%E3%83%BC%E3%81%AE%E8%A8%AD%E5%AE%9A)
      - [9-2. BravePI トランスミッターと BravePI メインボードの紐付け](https://www.google.com/search?q=%239-2-bravepi-%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B9%E3%83%9F%E3%83%83%E3%82%BF%E3%83%BC%E3%81%A8-bravepi-%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%E7%B4%90%E4%BB%98%E3%81%91)
  - [8. 商標について](https://www.google.com/search?q=%238-%E5%95%86%E6%A8%99%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
  - [9. Revision 管理](https://www.google.com/search?q=%239-revision-%E7%AE%A1%E7%90%86)

-----

## 1 概要

本製品は、BravePI トランスミッターに熱電対センサーボードを接続した際に使用するファームウェア (以降、本製品とする) のソフトウェア仕様を記載したものです。

本仕様書は、対象とするハードウェアを以下に示します。

\<BravePI トランスミッター\>

| 製品名 | 型番 |
| :--- | :--- |
| `BravePI トランスミッター (CR123A)` | `BVPTB-01` |
| `BravePI トランスミッター (USB)` | `BVPTU-01` |

\<BravePI センサーボード\>

| 製品名 | | 型番 |
| :--- | :--- | :--- |
| `BravePI 熱電対センサー` | `ボード` | `BVPSTO-01` |
| `オメガコネク` | | |
| `BravePI 熱電対センサー` | `ボード` | `BVPSTP-01` |
| `プッシュコネクタ` | | |

`BravePI トランスミッター`は、取得した熱電対センサーの値をペアリングされた `BravePI メインボード`に通知します。

[画像: BravePIトランスミッター、NFC、Bluetooth、BravePIメインボードの連携を示す図]

-----

## 2 機能概要

### 2-1 Sensor データ取得機能

本製品は、接続した熱電対センサーの値を送信することができます。

| センサーIC | センサーメーカー |
| :--- | :--- |
| `MCP9600` | `MICROCHIP` |

### 2-1-2 計測モード

本製品は以下の計測モードで熱電対センサーの情報を取得することができます。

| 測定モード | 説明 |
| :--- | :--- |
| `瞬時値モード` | `Uplink` タイミング時に現在の値を取得し通知します。 |
| `検知モード` | 定期的に値を取得し、ヒステリシス検知した場合に通知します。 ヒステリシスで指定された検知/復帰の設定範囲は以下になります |
| | **設定項目** |
| | `ヒステリシス (High)` |
| | $-300\\sim2000^{\\circ}C$ |
| | `ヒステリシス (Low)` |
| | $-300\\sim2000^{\\circ}C$ |
| `サンプリングモード` | 指定したサンプリング周期でサンプリングした値を通知します |
| | サンプリングモード時の設定可能なサンプリング周期は以下とする |
| | **設定項目** |
| | `サンプリング周期` |
| | `1Hz` |
| | 各サンプリングモード時の最大 `Uplink` 周期は以下になります。 |
| | **サンプリング周期** | **最大 `Uplink` 間隔** |
| | `1Hz` | `10000秒` |

-----

### 2-2 LED 表示機能

本製品は、本製品の状態をLEDで表示します。

| 優先 | 状態 | LED | | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| | | **赤** | **緑** | **青** |
| 高 | `LowBattery` 状態 | 点滅 | - | - | 1秒点灯、3秒消灯を繰り返す |
| | `Config モード` | - | 点滅 | - | 1秒点灯、3秒消灯を繰り返す |
| 1 | `PowerON` | - | 点灯 | - | 2秒点灯 |
| | `PowerOFF` | 点灯 | - | - | 2秒点灯 |
| 低 | 上記以外(通常動作中) | - | - | 無灯 | |

### 2-3 Bluetooth 通信機能

本製品は接続されたセンサー基板から取得されたセンサー情報を `Bleutooth` 通信で `BravePI メインボード`に通知します。また、`BravePI メインボード`経由で本製品に対して設定や指示等を `Downlink` することも可能です。

#### 2-3-1 Uplink

以下の情報を `Uplink` することができます。

| Uplink 情報 | Uplink タイミング |
| :--- | :--- |
| センサーデータ | パラメータで指定された `Uplink` 間隔 |
| パラメータ情報 | `Downlink` でパラメータ情報取得要求された場合 |

#### 2-3-2 Downlink

以下の指示を `Downlink` することができます。

| Downlink 情報 | 動作概要 |
| :--- | :--- |
| 即時 `Uplink` 要求 | 現在のセンサー情報の `Uplink` 要求します。 |
| パラメータ情報設定要求 | 本製品のパラメータ情報を設定します。 |
| パラメータ情報取得要求 | 本製品のパラメータ情報の `Uplink` 要求します |
| デバイス `Config` 移行 | 本製品を `Config` モードに移行します。 |
| デバイス再起動 | 本製品を再起動します |

-----

### 2-4 NFCTag 通信機能

本製品は `NFCTag`を有しており、専用スマホアプリより各種設定や情報取得することができます。
以下が`NFCTag` 機能で専用スマホアプリより行える操作になります。

| 項目 | 動作概要 | 備考 |
| :--- | :--- | :--- |
| デバイス再起動 | 本製品を再起動する。 | |
| 電源ON 要求 | 本製品を電源OFF から復帰する | |
| 電源OFF 要求\<br\>(`NFCTag` のみ有効) | 本製品を電源OFFにする。 | 電源OFF状態の場合は、本要求は無視されます。 |
| `Config` モード移行要求 | 本製品を `Config` モードに移行します。 | 電源OFF状態の場合は、本要求は無視されます。 |

### 2-5 パラメータ変更/取得機能

本製品のパラメータ情報の変更/取得することができます。

#### 2-5-1 パラメータ変更方法について

本製品のパラメータ情報の変更は以下の方法で行えます。

  - `BravePI メインボード`からパラメータ情報を `Downlink` することで変更することができます。
  - 本製品を `Config` モードにすることで、`Bleutooth` 経由で変更することができます。

#### 2-5-2 パラメータ取得方法について

本製品のパラメータ情報の設定は以下の方法で行えます。

  - `BravePI メインボード`からパラメータ取得要求を `Downlink` することでパラメータ情報を `Uplink` します。
  - 本製品を `Config` モードにすることで、`Bleutooth` 経由で取得することができます。

#### 2-5-3 変更可能なパラメータについて

本製品の変更/取得可能なパラメータに関しては「[3 パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)」を参照下さい。

### 2-6 DFU 機能

専用スマホアプリを使用することで、本製品のファームウェアの書き換えができます。
本製品のファームウェアの書き換えは、専用スマホアプリ以外からは行えません。

-----

## 3 パラメータ情報

本製品のパラメータを以下に示します。

| パラメータ項目 | 設定情報 |
| :--- | :--- |
| `DeviceID` | `BravePI メインボード`と通信する為に必要な、`DeviceID`. |
| `SensorID` | `BravePI メインボード`と通信する為に必要な、`SensorID` |
| `タイムゾーン設定` | タイムゾーン設定に関する設定情報を以下に示します |
| | **設定値** | **説明** |
| | `0x00` | 日本時間 |
| | `0x01` | `UTC` |
| | 上記以外 | 日本時間 |
| `BLE Mode` | `Bluetooth` 通信モードの設定情報を以下に示します。 |
| | **設定値** | **説明** |
| | `0x00` | `LongRange` |
| | `0x01` | `Legacy` |
| | 上記以外 | `Long Range` |
| `Tx Power` | `Bluetooth` 通信の送信電波出力の設定情報を以下に示します |
| | **設定値** | **説明** |
| | `0x00` | `±0dBm` |
| | `0x01` | `+4dBm` |
| | `0x02` | `-4dBm` |
| | `0x03` | `-8dBm` |
| | `0x04` | `-12dBm` |
| | `0x05` | `-16dBm` |
| | `0x06` | `-20dBm` |
| | `0x07` | `-40dBm` |
| | `0x08` | `+8dBm` |
| | 上記以外 | `±0dBm` |
| `Advertise Interval` | `Advertise` を発信する間隔設定情報を以下に示します。 |
| | **設定値** | **説明** |
| | `0x0064` | `100ms` 周期に `Advertise` を発信します。 |
| | : | : |
| | `0x03E8` | `1000ms` 周期に`Advertise`を発信します。 |
| | : | : |
| | `0x2710` | `10000ms` 周期に`Advertise` を発信します。 |
| | 上記以外 | `1000ms` 周期に`Advertise` を発信する設定になります。 |

| | |
| :--- | :--- |
| `Sensor Uplink Interval` | `Sensor` 情報データを `Uplink` する間隔を設定する\<br\>\<計測モードが「`瞬時値モード`」の場合\> |
| | **設定値** | **説明** |
| | `0x00000001` | `1` 秒周期に `Sensor` 情報データを `Uplink` します。 |
| | : | : |
| | `0x00000E10` | `3600`秒(1H)周期に `Sensor` 情報データを `Uplink`します |
| | : | : |
| | `0x00015180` | `86400`秒(24H)周期に `Sensor` 情報データを `Uplink` します |
| | 上記以外 | `60` 秒周期に `Sensor` 情報データを`Uplink` します |
| | \<計測モードが「`検知モード`」の場合\>\<br\>本設定は無視されます。 |
| | \<計測モードが「`サンプリングモード`」の場合\> |
| | **設定値** | **説明** |
| | `0x00000001` | `1` 秒周期に `Sensor` 情報データを `Uplink` します。 |
| | : | : |
| | `0x00000E10` | `3600`秒(1H)周期に`Sensor` 情報データを `Uplink` します。 |
| | : | : |
| | `0x00015180` | `86400`秒(24H)周期に`Sensor` 情報データを `Uplink` します。 |
| | 上記以外 | `60` 秒周期に `Sensor` 情報データを `Uplink` します。 |
| `計測モード` | `Sensor` 情報の扱いを設定します |
| | **設定値** | **説明** |
| | `0x00` | `瞬時値モード`: `Uplink` タイミング時の現在の値を通知します。 |
| | `0x01` | `検知モード`: ヒステリシス検知したことを通知します |
| | `0x02` | `サンプリングモード`: 指定したサンプリング周期でサンプリングした結果を通知します。 |
| | 上記以外 | `瞬時値モード`の設定になります。 |
| `サンプリング周期` | 当該センサー情報を `Read` する周期を設定します。 |
| | **設定値** | **説明** |
| | `0x00` | `1Hz`:`1000ms` 周期にセンサー情報を `Read` します |
| | `0x01` | `2Hz`:`500ms` 周期にセンサー情報を `Read` します。 |
| | 上記以外 | `1Hz` 設定になります。 |

| | |
| :--- | :--- |
| 熱電対タイプ | 使用する熱電対タイプを設定します。 |
| | **設定値** | **説明** |
| | `0x00` | `K`型 |
| | `0x01` | `J`型 |
| | `0x02` | `T`型 |
| | `0x03` | `N`型 |
| | `0x04` | `S`型 |
| | `0x05` | `E`型 |
| | `0x06` | `B`型 |
| | `0x07` | `R`型 |
| | 上記以外 | `K`型設定になります。 |
| `ヒステリシス(High)` | `High` 側のヒステリシスを設定します。(範囲:-300 \~ 2000℃) |
| `ヒステリシス(Low)` | `Low` 側のヒステリシスを設定します。(範囲:-300\~2000℃) |

-----

## 4 Config モード時 Bluetooth通信仕様

`Config` モード時用の`Bluetooth` 通信プロファイル仕様を以下に示します。

### 4-1 基本情報

| 項目 | 値 |
| :--- | :--- |
| `Advertising Interval` | `1000ms` |
| `Min Connection Interval` | `20ms` |
| `Max Connection Interval` | `40ms` |
| `Slave Latency` | `0` |
| `Supervision Timeout` | `6000ms` |

### 4-2 Advertise/Scan Response Packet

**\<Advertise データ\>**

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
| 23-28| 右記 | `Local Name` | `BvPiTm` |

**\<ScanResponse データ\>**
なし

### 4-3 Service

`677eXXXX-79f2-4584-91f9-098db93d0781`
以下の `Service`/`Characteristic` の`UUID`は上記 `UUID` の `XXXX` (`Alias`)の部分に
各`Service`/`Characteristic` の `Alias` を設定した値になります。

| Service Name | Alias | Characteristic Name |
| :--- | :--- | :--- |
| `BraveGATEInfo` | `0x1000` | `BV DEVICEID` |
| | | `BV COMPANYID` |
| | | `BV SENSORID` |
| `DeviceSetting` | `0x2000` | `TIME ZONE` |
| | | `BLE MODE` |
| | | `TX POWER` |
| | | `ADV INTERVAL` |
| | | `UPLINK INTERVAL` |
| `SensorSetting` | `0x3000` | `SENS_READ_REQ` |
| | | `SENS_READ_RESP` |
| | | `SENS MODE` |
| | | `SAMPLING` |
| | | `HYSTERESIS H` |
| | | `HYSTERESIS L` |
| | | `LINE_TYPE` |
| `DeviceInfo` | `0x4000` | `DEVICEID` |
| | | `FW_VERSION` |
| | | `HW_VERSION` |
| | | `BATTERY` |
| | | `DFU_TYPE` |
| | | `DFU_REQUEST` |
| | | `REGISTER` |

#### 4-3-1 BraveGATEInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `BV DEVICEID` | `Read` | `0x1001` | `0x00` | `bvDeviceId [8byte]` |
| `BV COMPANYID` | `Read` | `0x1002` | `0x00` | `bvCompanyId [8byte]` |
| `BV SENSORID` | `Read` | `0x1003` | `0x00` | `bvSensorId[2byte]` |

**\<BraveGATEInfo Service の詳細\>**

  - **BV\_DEVICEID**: `BravePI メインボード`との通信に必要な `DeviceID` を `Read` できます。
  - **BV\_COMPANYID**: `BravePI メインボード`との通信に必要な `Company ID` を `Read` できます。
  - **BV\_SENSORID**: `BravePI メインボード`との通信に必要な `SensorID` を `Read` できます。

#### 4-3-2 DeviceSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `TIME ZONE` | `Read/Write` | `0x2001` | `0x00` | `timeZone[1byte]` |
| `BLE MODE` | `Read/Write` | `0x2002` | `0x00` | `bleMode[1byte]` |
| `TX POWER` | `Read/Write` | `0x2003` | `0x00` | `txPower [1byte]` |
| `ADV_INTERVAL` | `Read/Write` | `0x2004` | `0x00` | `advInterval [2byte]` |
| `UPLINK INTERVAL` | `Read/Write` | `0x2005` | `0x00` | `uplinkInterval [4byte]` |

**\<DeviceSettingInfo Service の詳細\>**

  - **TIME\_ZONE**: タイムゾーンを設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00` | 日本時間 |
    | `0x01` | `UTC` |
    | 上記以外 | 日本時間 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **BLE\_MODE**: `Bluetooth` 通信モードの設定情報を以下に示します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00` | `Long Range` |
    | `0x01` | `Legacy` |
    | 上記以外 | `LongRange` |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **TX\_POWER**: `Bluetooth` 通信モードの設定情報を以下に示します。
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
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **ADV\_INTERVAL**: `Advertise` を発信する間隔を設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x0064` | `100ms` 周期に `Advertise` を発信します。 |
    | : | : |
    | `0x03E8` | `1000ms` 周期に `Advertise` を発信します。 |
    | : | : |
    | `0x2710` | `10000ms` 周期に`Advertise` を発信します。 |
    | 上記以外 | `1000ms` 周期に`Advertise` を発信する設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

  - **UPLINK\_INTERVAL**: `Sensor` 情報データを `Uplink` する間隔を設定する。
    \<計測モードがが「`瞬時値モード`」の場合\>
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00000001` | `1`秒周期に `Sensor` 情報データを `Uplink` します |
    | : | |
    | `0x00000E10` | `3600`秒(1時間)周期に`Sensor` 情報データを `Uplink` します |
    | `0x00015180` | `86400`秒(24時間)周期に`Sensor` 情報データを `Uplink` します。 |
    | 上記以外 | `60`秒周期に `Sensor` 情報データを `Uplink` します。 |

    \<計測モードがが「`検知モード`」の場合\>
    本設定は無視されます。

    \<計測モードがが「`サンプリングモード`」の場合\>
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00000001` | `1`秒周期に `Sensor` 情報データを `Uplink` します |
    | : | : |
    | `0x00000E10` | `3600`秒(1時間)周期に`Sensor` 情報データを `Uplink` します |
    | : | : |
    | `0x00015180` | `86400`秒(24時間)周期に`Sensor` 情報データを `Uplink` します |
    | 上記以外 | `60`秒周期に `Sensor` 情報データを`Uplink` します。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

#### 4-3-3 SensorSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `SENS_READ_REQ` | `Write` | `0x3001` | `0x00` | `sensnorReq[1byte]` |
| `SENS READ RESP` | `Notify` | `0x3002` | `0x00` | `sensnorValue[4byte]` |
| `SENS MODE` | `Read/Write`| `0x3003` | `0x00` | `sensnorMode[1byte]` |
| `SAMPLING` | `Read/Write`| `0x3004` | `0x00` | `sampling [1byte]` |
| `HYSTERESIS H` | `Read/Write`| `0x3005` | `0x00` | `hysteresisHigh[4byte]`|
| `HYSTERESIS L` | `Read/Write`| `0x3006` | `0x00` | `hysteresisLow[4byte]` |
| `LINE TYPE` | `Read/Write`| `0x3007` | `0x00` | `lineType[1byte]` |

**\<SensorSettingInfo Service の詳細\>**

  - **SENS\_READ\_REQ**: `0x01`を`write` すると現在のセンサー情報取得開始します。

  - **SENS\_READ\_RESP**: `SENS_READ_REQ`に対する応答で、現在の照度センサー値(Lux)を `Notify` します。
    ※失敗時は、`0xFFFFFFFF` を返します。
    ※エンディアンはリトルエンディアン。

  - **SENS\_MODE**: `Sensor` 情報の扱いを設定する。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x0` | `瞬時値モード`: `Uplink` タイミング時の現在の値を通知します。 |
    | `0x01` | `検知モード`: ヒステリシス検知したことを通知します。 |
    | `0x02` | `サンプリングモード`: 指定したサンプリング周期でサンプリングした結果を通知します |
    | 上記以外 | `瞬時値モード`設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **SAMPLING**: 当該センサー情報を `Read` する周期を設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00` | `1Hz`: `1000ms` 周期にセンサー情報を `Read` します。 |
    | `0x01` | `2Hz`:`500ms` 周期にセンサー情報を `Read` します。 |
    | `0x02` | `5Hz`:`200ms` 周期にセンサー情報を`Read` します。 |
    | 上記以外 | `1Hz` 設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **HYSTERESIS\_H**: `High` 側のヒステリシスを設定します。(範囲:-300\~2000℃)
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

  - **HYSTERESIS\_L**: `Low` 側のヒステリシスを設定します。(範囲: $-300\\sim2000^{\\circ}C)$
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

  - **LINE\_TYPE**: 使用する熱電対タイプを設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00` | `K` 型 |
    | `0x01` | `J` 型 |
    | `0x02` | `T`型 |
    | `0x03` | `N`型 |
    | `0x04` | `S`型 |
    | `0x05` | `E`型 |
    | `0x06` | `B`型 |
    | `0x07` | `R`型 |
    | 上記以外 | `K`型設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

#### 4-3-4 DeviceInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `DEVICEID` | `Read` | `0x4001` | `0x00` | `nordicDeviceId[8byte]` |
| `FW VERSION` | `Read` | `0x4002` | `0x00` | `fwVersion [3byte]` |
| `HW VERSION` | `Read` | `0x4003` | `0x00` | `hwVersion [3byte]` |
| `BATTERY` | `Read` | `0x4004` | `0x00` | `batteryLevel [1byte]` |
| `DFU TYPE` | `Read` | `0x4005` | `0x00` | `dfuType[1byte]` |
| `DFU_REQUEST` | `Write`| `0x4006` | `0x00` | `dfuRequest[1byte]` |
| `REGISTER` | `Write`| `0x4007` | `0x00` | `register[3byte]` |

**\<DeviceInfo Service の詳細\>**

  - **DEVICEID**: `Nordic` のチップのユニークなIDを読み出せます。
  - **FW\_VERSION**: 本製品のファームウェアバージョンを読み出せます。
    例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。
  - **HW\_VERSION**: 本製品のHWバージョンを読み出せます。
    例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。
  - **BATTERY**: 本製品の現在のバッテリーレベル(%)を読み出せます。
  - **DFU\_TYPE**: 固定で `0x01` が読み出されます。
  - **DFU\_REQUEST**: `0x01`を `Write` すると、`Bleutooth` 切断し、`DFU`モードに移行します。
  - **REGISTER**: `0x66a781` を `write` すると変更された変更されて全ての情報を保存し、変更した設定を有効にします。

-----

## 5 動作フロー

[画像: 動作フローチャート]
`POWER ON` → `NFCTag検知` → (YES) → `NFC要求処理実行` → `POWER OFF中`
`NFCTag検知` → (NO) → `POWER OFF中`
`POWER OFF中` → (YES) → (ループ先頭へ)
`POWER OFF中` → (NO) → `Configモード中`
`Configモード中` → (YES) → `Configモード中動作` → (ループ先頭へ)
`Configモード中` → (NO) → `センサーReadタイミング`
`センサーReadタイミング` → (YES) → `センサー情報Read実行` → (ループ先頭へ)
`センサーReadタイミング` → (NO) → `Uplinkタイミング`
`Uplinkタイミング` → (YES) → `Uplink実行` → (ループ先頭へ)
`Uplinkタイミング` → (NO) → `Downlink受信`
`Downlink受信` → `Downlink受信処理実行` → (ループ先頭へ)

-----

## 6 Uplink データ仕様

`BravePI メインボード`から通知される情報ついて以下に示す。

### 6-1 Sensor 情報

`SensorID`: `0x0105`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0105` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | `0x00`:継続データなし | |
| **Data 領域** | | | |
| `Battery Level` | 1 | バッテリーレベル(%) | |
| `sampleNum` | 2 | サンプル数 | |
| `TempData[0]` | 4 | 温度情報 | `float` 型 |
| : | : | : | |
| `TempData[n]` | 4 | 温度情報 | `float` 型 |
※エンディアンはリトルエンディアンになります。

### 6-2 パラメータ情報

`SensorID`: `0x0000`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | `0x00`:継続データなし | |
| **Data 領域** | | | |
| `SensorID` | 2 | `0x0105` 固定 | |
| `FW Version` | 3 | 本製品のファームウェアバージョン | `Ver1.2.9`の場合は、`[0x01,0x02,0x09]` |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `BLE Mode` | 1 | `Bluetooth` 通信モードの設定情報 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | |
| `Sensor Read Mode` | 1 | 計測モード | |
| `Sampling` | 1 | サンプリング周期 | |
| `HysteresisHigh` | 4 | ヒステリシス(`High`) | |
| `HysteresisLow` | 4 | ヒステリシス(`Low`) | |
| `Line Type` | 1 | 熱電対タイプ | |
※エンディアンはリトルエンディアンになります。

-----

## 7 Downlink データ仕様

`BravePI メインボード`から送信する情報ついて以下に示す。

### 7-1 即時 Uplink 要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength`| 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0105` | |
| `CMD` | 1 | `0x00` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
※エンディアンはリトルエンディアンになります。データ作成時はリトルエンディアンで作成して下さい。

### 7-2 パラメータ情報設定要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength`| 2 | `0x0015` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x05` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `SensorID` | 2 | `0x0108` | |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | |
| `Sensor Read Mode` | 1 | 計測モード | |
| `Sampling` | 1 | サンプリング周期 | |
| `HysteresisHigh` | 4 | ヒステリシス(`High`) | |
| `HysteresisLow` | 4 | ヒステリシス(`Low`) | |
| `Line Typw` | 1 | 熱電対タイプ | |
※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-3 パラメータ情報取得要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00`固定 | |
| `DataLength`| 2 | `0x0001` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x0D` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | 1 | `0x00` | |
※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-4 デバイス Config 移行要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength`| 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0xFC` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

### 7-5 デバイス再起動要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength`| 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0xFD` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

-----

## 8 電池駆動時の各設定における電池持ち

`BravePI トランスミッター (CR123A)`使用時の代表的な設定におけるおおよその電池持ちを以下に示します。

**\<`Bluetooth` 通信モード: `Legacy` の場合\>**

| 計測モード | サンプリング周期 | パラメータ設定情報 | | | 電池持ち (日) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | **`Uplink Interval`** | **`TxPower`** | **`Advertise Interval`** | |
| `瞬時値モード` | | `1秒` | `0dBm` | `100ms` | 4 |
| | | `10秒` | | `100ms` | 33 |
| | | | | `1000ms`| 39 |
| | | `60秒` | | `100ms` | 102 |
| | | | | `1000ms`| 201 |
| `検知モード` | `1Hz` | `60秒` | `0dBm` | `100ms` | 40 |
| `サンプリングモード` | | | | `1000ms`| 41 |

**\<`Bluetooth` 通信モード: `Long Range` の場合\>**

| 計測モード | サンプリング周期 | パラメータ設定情報 | | | 電池持ち (日) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | **`TxPower`** | **`Uplink Interval`** | **`Advertise Interval`** | |
| `瞬時値モード` | | `0dBm` | `1秒` | `100ms` | 4 |
| | | | `10秒` | `100ms` | 23 |
| | | | | `1000ms`| 37 |
| | | | `60秒` | `100ms` | 41 |
| | | | | `1000ms`| 155 |
| `検知モード` | `1Hz` | `0dBm` | `60秒` | `100ms` | 3 |
| `サンプリングモード` | | | | `1000ms`| 3 |

-----

## 9 製品到着から使用開始までの流れ

### 9-1 BravePI トランスミッターの設定

`BravePI トランスミッター`側の設定手順について以下に示します。

1.  トランスミッターからセンサーを外した状態にする。
2.  トランスミッターに電池又はUSB給電する。
3.  専用のiPhoneアプリを起動する。
4.  iPhone アプリから熱電対センサー用の「`DFU`」を実行する。
5.  iPhone アプリから熱電対センサー用の「`パラメータ設定`」を実行する。
6.  トランスミッターに熱電対センサーを取り付ける。
7.  iPhone アプリからトランスミッターに電源ON(再起動)操作を行う。

次に `BravePI トランスミッター`と `BravePI メインボード`の紐付けを実行して下さい。

### 9-2 BravePI トランスミッターと BravePI メインボードの紐付け

`BravePI トランスミッター`と `BravePI メインボード`の紐付け手順について以下に示します。

1.  専用の iPhone アプリを起動する。
2.  iPhone アプリから「`ベアリング設定`」を実行する。

以上で設定は終了です。

-----

## 8 商標について

  - Bluetooth®とワードマークおよびロゴは、Bluetooth SIG INC が所有する登録商標です。
    株式会社 Braveridge はこれら商標を使用する許可を受けています。その他のロゴマーク及び商号は各所有者に帰属します。

## 9 Revision 管理

| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023/10/16 | Ver1.0.0 | 初版 |

※上記、製品仕様や機能、デザインは変更となる可能性がございます。あらかじめご了承ください。

Braveridgeとその製品に関する詳しい情報は、弊社Webサイトで御確認ください。
[https://www.braveridge.com/](https://www.braveridge.com/)

  - **株式会社Braveridge 本社**
    〒819-0373 福岡県福岡市西区周船寺3-27-2
    (Tel): 092-834-5789/ (Fax): 092-807-7718
  - **株式会社Braveridge 糸島工場**
    〒819-1122 福岡県糸島市東1999-19
      - Apple MFi Manufacture ライセンス認定工場(ライトニングコネクタ製品工場)