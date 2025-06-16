かしこまりました。
ドキュメント内の連番の誤りを修正し、目次と見出しを更新しました。

-----

**公式仕様書**: [ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (差圧センサー版) REV 1.0](https://drive.google.com/file/d/14RFM6lgytNA1gYXiB19nxGmrZ4K_SWVb/view)

# ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (差圧センサー版)

**REV 1.0**

**DESIGNED BY Braveridge Co., Ltd.**

-----

## 目次

  - [1. 概要](https://www.google.com/search?q=%231-%E6%A6%82%E8%A6%81)
  - [2. 機能概要](https://www.google.com/search?q=%232-%E6%A9%9F%E8%83%BD%E6%A6%82%E8%A6%81)
      - [2-1. Sensor データ取得機能](https://www.google.com/search?q=%232-1-sensor-%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
          - [2-1-1. 計測モード](https://www.google.com/search?q=%232-1-1-%E8%A8%88%E6%B8%AC%E3%83%A2%E3%83%BC%E3%83%89)
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
  - [10. 商標について](https://www.google.com/search?q=%2310-%E5%95%86%E6%A8%99%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
  - [11. Revision 管理](https://www.google.com/search?q=%2311-revision-%E7%AE%A1%E7%90%86)

-----

## 1\. 概要

[cite\_start]本仕様書は、BravePI トランスミッターに差圧センサーボードを接続した際に使用するファームウェアのソフトウェア仕様を記載したものです。 [cite: 8]

[cite\_start]本仕様書は、対象とするハードウェアを以下に示します。 [cite: 8]

**\<BravePI トランスミッター\>**
| 製品名 | | 型番 |
| :--- | :--- | :--- |
| `BravePI` | トランスミッター (`CR123A`) | `BVPTB-01` |
| `BravePI` | トランスミッター (`USB`) | `BVPTU-01` |
[cite\_start][cite: 9]

**\<BravePI センサーボード\>**
| 製品名 | 型番 |
| :--- | :--- |
| `BravePI` 差圧センサーボード | `BVPSP-01` |
[cite\_start][cite: 11]

[cite\_start]`BravePI` トランスミッターは、取得したセンサーの値をペアリングされた `BravePI` メインボードに通知します。 [cite: 12]

[cite\_start][画像: BravePI トランスミッターがBluetoothとNFCでBravePI メインボードと通信する図] [cite: 12]

-----

## 2\. 機能概要

### 2-1. Sensor データ取得機能

[cite\_start]本製品は、接続した差圧センサーの値を送信することができます。 [cite: 13]

| センサーIC | センサーメーカー |
| :--- | :--- |
| `SDP810-500Pa` | `SENSIRION` |
[cite\_start][cite: 14]

#### 2-1-1. 計測モード

[cite\_start]本製品は以下の計測モードで差圧センサーの情報を取得することができます。 [cite: 15]

| 測定モード | 説明 |
| :--- | :--- |
| **瞬時値モード** | [cite\_start]`Uplink` タイミング時に現在の値を取得し通知します。 [cite: 16] |
| **検知モード** | [cite\_start]定期的に値を取得し、ヒステリシス検知した場合に通知します。 [cite: 16][cite\_start]\<br\>ヒステリシスで指定された検知/復帰の設定範囲は以下になります [cite: 16] |
| | **設定項目** |
| | ヒステリシス (High) | [cite\_start]`-500Pa`\~`500Pa` [cite: 16] |
| | ヒステリシス (Low) | [cite\_start]`-500Pa`\~`500Pa` [cite: 16] |
| **サンプリングモード** | [cite\_start]指定したサンプリング周期でサンプリングした値を通知します。 [cite: 16][cite\_start]\<br\>サンプリングモード時の設定可能なサンプリング周期は以下とする [cite: 16] |
| | **項目** | **設定** |
| | サンプリング周期 | [cite\_start]`1Hz` `2Hz` [cite: 16] |
| | [cite\_start]各サンプリングモード時の最大 `Uplink` 周期は以下になります。 [cite: 16] |
| | **サンプリング周期** | **最大 `Uplink` 間隔** |
| | `1Hz` | [cite\_start]`10000`秒 [cite: 16] |
| | `2Hz` | [cite\_start]`5000`秒 [cite: 16] |

### 2-2. LED 表示機能

[cite\_start]本製品は、本製品の状態をLEDで表示します。 [cite: 18]

| 優先 | 状態 | LED | | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| | | **赤** | **緑** | **青** |
| **高** | `LowBattery` 状態 | 点滅 | - | - | [cite\_start]1秒点灯、3秒消灯を繰り返す [cite: 19] |
| | `Config` モード | - | 点滅 | - | [cite\_start]1秒点灯、3秒消灯を繰り返す [cite: 19] |
| **1** | `PowerON` | - | 点灯 | - | [cite\_start]2秒点灯 [cite: 19] |
| | `PowerOFF` | 点灯 | - | - | [cite\_start]2秒点灯 [cite: 19] |
| **低** | 上記以外(通常動作中) | - | - | 無灯 | |
[cite\_start][cite: 19]

### 2-3. Bluetooth 通信機能

[cite\_start]本製品は接続されたセンサー基板から取得されたセンサー情報を `Bleutooth` 通信で `BravePI` メインボードに通知します。 [cite: 20] [cite\_start]また、`BravePI` メインボード経由で本製品に対して設定や指示等を `Downlink` することも可能です。 [cite: 20]

#### 2-3-1. Uplink

[cite\_start]以下の情報を `Uplink` することができます。 [cite: 20]

| `Uplink` 情報 | `Uplink` タイミング |
| :--- | :--- |
| センサーデータ | [cite\_start]パラメータで指定された `Uplink` 間隔 [cite: 21] |
| パラメータ情報 | [cite\_start]`Downlink` でパラメータ情報取得要求された場合 [cite: 21] |

#### 2-3-2. Downlink

[cite\_start]以下の指示を `Downlink` することができます。 [cite: 22]

| `Downlink` 情報 | 動作概要 |
| :--- | :--- |
| 即時 `Uplink` 要求 | [cite\_start]現在のセンサー情報の `Uplink` 要求します。 [cite: 23] |
| パラメータ情報設定要求 | [cite\_start]本製品のパラメータ情報を設定します。 [cite: 23] |
| パラメータ情報取得要求 | [cite\_start]本製品のパラメータ情報の `Uplink` 要求します [cite: 23] |
| デバイス `Config` 移行 | [cite\_start]本製品を `Config` モードに移行します。 [cite: 23] |
| デバイス再起動 | [cite\_start]本製品を再起動します [cite: 23] |

### 2-4. NFCTag 通信機能

[cite\_start]本製品は `NFCTag`を有しており、専用スマホアプリより各種設定や情報取得することができます。 [cite: 25]
[cite\_start]以下が`NFCTag` 機能で専用スマホアプリより行える操作になります。 [cite: 25]

| 項目 | 動作概要 | 備考 |
| :--- | :--- | :--- |
| デバイス再起動 | [cite\_start]本製品を再起動する。 [cite: 26] | |
| 電源ON 要求 | [cite\_start]本製品を電源OFF から復帰する [cite: 26] | |
| 電源OFF 要求\<br\>(`NFCTag` のみ有効) | [cite\_start]本製品を電源OFFにする。 [cite: 26] | [cite\_start]電源OFF状態の場合は、本要求は無視されます。 [cite: 26] |
| `Config` モード移行要求 | [cite\_start]本製品を `Config` モードに移行します。 [cite: 26] | [cite\_start]電源OFF状態の場合は、本要求は無視されます。 [cite: 26] |

### 2-5. パラメータ変更/取得機能

[cite\_start]本製品のパラメータ情報の変更/取得することができます。 [cite: 27]

#### 2-5-1. パラメータ変更方法について

[cite\_start]本製品のパラメータ情報の変更は以下の方法で行えます。 [cite: 27]

  - [cite\_start]`BravePI` メインボードからパラメータ情報を `Downlink` することで変更することができます。 [cite: 27]
  - [cite\_start]本製品を `Config` モードにすることで、`Bleutooth` 経由で変更することができます。 [cite: 27]

#### 2-5-2. パラメータ取得方法について

[cite\_start]本製品のパラメータ情報の設定は以下の方法で行えます。 [cite: 27]

  - [cite\_start]`BravePI` メインボードからパラメータ取得要求を `Downlink` することでパラメータ情報を `Uplink` します。 [cite: 27]
  - [cite\_start]本製品を `Config` モードにすることで、`Bleutooth` 経由で取得することができます。 [cite: 27]

#### 2-5-3. 変更可能なパラメータについて

[cite\_start]本製品の変更/取得可能なパラメータに関しては「[3 パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)」を参照下さい。 [cite: 27]

### 2-6. DFU 機能

[cite\_start]専用スマホアプリを使用することで、本製品のファームウェアの書き換えができます。 [cite: 27]
[cite\_start]本製品のファームウェアの書き換えは、専用スマホアプリ以外からは行えません。 [cite: 27]

-----

## 3\. パラメータ情報

[cite\_start]本製品のパラメータを以下に示します。 [cite: 28]
| パラメータ項目 | 設定情報 |
| :--- | :--- |
| `DeviceID` | [cite\_start]`BravePI` メインボードと通信する為に必要な、`DeviceID`. [cite: 29] |
| `SensorID` | [cite\_start]`BravePI` メインボードと通信する為に必要な、`SensorID` [cite: 29] |
| タイムゾーン設定 | [cite\_start]タイムゾーン設定に関する設定情報を以下に示します [cite: 29] |
| | **設定値** | **説明** |
| | `0x00` | [cite\_start]日本時間 [cite: 29] |
| | `0x01` | [cite\_start]UTC [cite: 29] |
| | 上記以外 | [cite\_start]日本時間 [cite: 29] |
| `BLE Mode` | [cite\_start]`Bluetooth` 通信モードの設定情報を以下に示します。 [cite: 29] |
| | **設定値** | **説明** |
| | `$0\times00$` | [cite\_start]`LongRange` [cite: 29] |
| | `0x01` | [cite\_start]`Legacy` [cite: 29] |
| | 上記以外 | [cite\_start]`Long Range` [cite: 29] |
| `Tx Power` | [cite\_start]`Bluetooth` 通信の送信電波出力の設定情報を以下に示します [cite: 29] |
| | **設定値** | **説明** |
| | `0x00` | [cite\_start]`±0dBm` [cite: 29] |
| | `0x01` | [cite\_start]`+4dBm` [cite: 29] |
| | `0x02` | [cite\_start]`-4dBm` [cite: 29] |
| | `$0\times03$` | [cite\_start]`-8dBm` [cite: 29] |
| | `0x04` | [cite\_start]`-12dBm` [cite: 29] |
| | `$0\times05$` | [cite\_start]`-16dBm` [cite: 29] |
| | `$0\times06$` | [cite\_start]`-20dBm` [cite: 29] |
| | `0x07` | [cite\_start]`-40dBm` [cite: 29] |
| | `0x08` | [cite\_start]`+8dBm` [cite: 29] |
| | 上記以外 | [cite\_start]`±0dBm` [cite: 29] |
| `Advertise Interval` | [cite\_start]`Advertise` を発信する間隔設定情報を以下に示します。 [cite: 29] |
| | **設定値** | **説明** |
| | `0x0064` | [cite\_start]`100ms` 周期に `Advertise` を発信します。 [cite: 29] |
| | : | : |
| | `0x03E8` | [cite\_start]`1000ms` 周期に`Advertise`を発信します。 [cite: 29] |
| | : | : |
| | `0x2710` | [cite\_start]`10000ms` 周期に`Advertise` を発信します。 [cite: 29] |
| | 上記以外 | [cite\_start]`1000ms` 周期に`Advertise` を発信する設定になります。 [cite: 29] |
| `Sensor Uplink Interval` | [cite\_start]`Sensor` 情報データを `Uplink` する間隔を設定する [cite: 31] |
| | [cite\_start]**\<計測モードが「瞬時値モード」の場合\>** [cite: 31] |
| | **設定値** | **説明** |
| | `0x00000001` | [cite\_start]`1` 秒周期に `Sensor` 情報データを `Uplink` します。 [cite: 31] |
| | : | : |
| | `0x00000E10` | [cite\_start]`3600`秒(1H)周期に `Sensor` 情報データを `Uplink`します [cite: 31] |
| | : | : |
| | `0x00015180` | [cite\_start]`86400`秒(24H)周期に `Sensor` 情報データを `Uplink` します。 [cite: 31] |
| | 上記以外 | [cite\_start]`60` 秒周期に `Sensor` 情報データを`Uplink` します [cite: 31] |
| | [cite\_start]**\<計測モードが「検知モード」の場合\>** [cite: 31] |
| | [cite\_start]本設定は無視されます。 [cite: 31] |
| | [cite\_start]**\<計測モードが「サンプリングモード」の場合\>** [cite: 31] |
| | **設定値** | **説明** |
| | `0x0000003C` | [cite\_start]`60`秒周期に `Sensor` 情報データを `Uplink` します [cite: 31] |
| | : | : |
| | `0x00000E10` | [cite\_start]`3600`秒(1H)周期に`Sensor` 情報データを `Uplink` します。 [cite: 31] |
| | : | : |
| | `0x00015180` | [cite\_start]`86400`秒(24H)周期に `Sensor` 情報データを `Uplink` します。 [cite: 31] |
| | 上記以外 | [cite\_start]`60` 秒周期に `Sensor` 情報データを `Uplink` します [cite: 31] |
| 計測モード | [cite\_start]`Sensor` 情報の扱いを設定します。 [cite: 31] |
| | **設定値** | **説明** |
| | `0x00` | [cite\_start]瞬時値モード: `Uplink` タイミング時の現在の値を通知します。 [cite: 31] |
| | `0x01` | [cite\_start]検知モード:ヒステリシス検知したことを通知します。 [cite: 31] |
| | `0x02` | [cite\_start]サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します。 [cite: 31] |
| | 上記以外 | [cite\_start]瞬時値モードの設定になります。 [cite: 31] |
| サンプリング周期 | [cite\_start]当該センサー情報を `Read` する周期を設定します。 [cite: 31] |
| | **設定値** | **説明** |
| | `0x00` | [cite\_start]`1Hz`: `1000ms` 周期にセンサー情報を `Read` します。 [cite: 31] |
| | `0x01` | [cite\_start]`2Hz`:`500ms` 周期にセンサー情報を`Read`します。 [cite: 31] |
| | 上記以外 | [cite\_start]`1Hz` 設定になります。 [cite: 31] |
| ヒステリシス(High) | [cite\_start]`High` 側のヒステリシスを設定します [cite: 34] |
| | **設定値** | **説明** |
| | : | [cite\_start]`-500Pa` 以下は`-500Pa` に丸められます。 [cite: 34] |
| | `0xFFFFFE0C` | [cite\_start]`-500mV` [cite: 34] |
| | : | |
| | `0xFFFFFFFF` | [cite\_start]`-1Pa` [cite: 34] |
| | `0x00000000` | [cite\_start]`OPa` [cite: 34] |
| | `0x00000001` | [cite\_start]`1Pa` [cite: 34] |
| | : | |
| | `0x000001F4` | [cite\_start]`500Pa` [cite: 34] |
| | : | [cite\_start]`500Pa` 以上はは`500Pa`に丸められます。 [cite: 34] |
| ヒステリシス(Low) | [cite\_start]`Low` 側のヒステリシスを設定します [cite: 34] |
| | **設定値** | **説明** |
| | : | [cite\_start]`-500Pa` 以下は`-500Pa` に丸められます。 [cite: 34] |
| | `0xFFFFFE0C` | [cite\_start]`-500Pa` [cite: 34] |
| | : | |
| | `0xFFFFFFFF` | [cite\_start]`-1Pa` [cite: 34] |
| | `0x00000000` | [cite\_start]`OPa` [cite: 34] |
| | `0x00000001` | [cite\_start]`1Pa` [cite: 34] |
| | : | |
| | `0x000001F4` | [cite\_start]`500Pa` [cite: 34] |
| | : | [cite\_start]`500Pa` 以上はは`500Pa` に丸められます。 [cite: 34] |

-----

## 4\. Config モード時 Bluetooth通信仕様

[cite\_start]`Config` モード時用の`Bluetooth` 通信プロファイル仕様を以下に示します。 [cite: 36]

### 4-1. 基本情報

| 項目 | 値 |
| :--- | :--- |
| `Advertising Interval` | [cite\_start]`1000ms` [cite: 37] |
| `Min Connection Interval` | [cite\_start]`20ms` [cite: 37] |
| `Max Connection Interval` | [cite\_start]`40ms` [cite: 37] |
| `Slave Latency` | [cite\_start]`0` [cite: 37] |
| `Supervision Timeout` | [cite\_start]`6000ms` [cite: 37] |

### 4-2. Advertise/Scan Response Packet

**\<Advertise データ\>**
| Index | Data | Description | Comment |
| :--- | :--- | :--- | :--- |
| 0 | `$0\times02$` | Length | |
| 1 | `$0\times01$` | Advertising Field Type | `FLAGS` |
| 2 | `$0\times06$` | Flag type | `LE ONLY GENERAL DISCOVER MODE` |
| 3 | `$0\times11$` | Length | |
| 4 | `$0\times07$` | Advertising Field Type | `Complete List of 128-bit Service Class UUIDS` |
| 5-20 | 右記 | `Service UUID` | `57791000-a129-4d7f-93a6-87f82b59f6a4` |
| 21 | `0x06` | Length | |
| 22 | `0x09` | Advertising Field Type | `Complete Local Name` |
| 23-28 | 右記 | `Local Name` | `BvPiTm` |
[cite\_start][cite: 39]

**\<ScanResponse データ\>**
[cite\_start]なし [cite: 40]

### 4-3. Service

`677eXXXX-79f2-4584-91f9-098db93d0781`
[cite\_start]以下の `Service`/`Characteristic` の`UUID`は上記 `UUID` の `XXXX` (Alias)の部分に各 `Service`/`Characteristic` の Alias を設定した値になります。 [cite: 41]

| Service Name | Alias | Characteristic Name |
| :--- | :--- | :--- |
| `BraveGATEInfo` | `$0\times1000$` | `BV DEVICEID` \<br\> `BV COMPANYID` \<br\> `BV SENSORID` |
| `DeviceSetting` | `0x2000` | `TIME ZONE` \<br\> `BLE MODE` \<br\> `TX POWER` \<br\> `ADV INTERVAL` \<br\> `UPLINK INTERVAL` |
| `SensorSetting` | `0x3000` | `SENS_READ_REQ` \<br\> `SENS_READ_RESP` \<br\> `SENS MODE` \<br\> `SAMPLING` \<br\> `HYSTERESIS H` \<br\> `HYSTERESIS L` |
| `DeviceInfo` | `0x4000` | `DEVICEID` \<br\> `FW_VERSION` \<br\> `HW_VERSION` \<br\> `BATTERY` \<br\> `DFU_TYPE` \<br\> `DFU_REQUEST` \<br\> `REGISTER` |
[cite\_start][cite: 42]

#### 4-3-1. BraveGATEInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `BV DEVICEID` | `Read` | `0x1001` | `$0\times00$` | `bvDeviceId` [8byte] |
| `BV COMPANYID` | `Read` | `$0\times1002$` | `$0\times00$` | `bvCompanyId` [8byte] |
| `BV SENSORID` | `Read` | `$0\times1003$` | `$0\times00$` | `bvSensorId` [2byte] |
[cite\_start][cite: 45]

**\<`BraveGATEInfo` Service の詳細\>**

  - **`BV_DEVICEID`**
    [cite\_start]`BravePI` メインボードとの通信に必要な `DeviceID` を `Read` できます。 [cite: 46]
  - **`BV_COMPANYID`**
    [cite\_start]`BravePI` メインボードとの通信に必要な `CompanyID`を `Read` できます。 [cite: 46]
  - **`BV_SENSORID`**
    [cite\_start]`BravePI` メインボードとの通信に必要な `SensorID` を `Read` できます。 [cite: 46]

#### 4-3-2. DeviceSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `TIME ZONE` | `Read/Write` | `$0\times2001$` | `$0\times00$` | `timeZone`[1byte] |
| `BLE MODE` | `Read/Write` | `$0\times2002$` | `$0\times00$` | `bleMode`[1byte] |
| `TX POWER` | `Read/Write` | `$0\times2003$` | `$0\times00$` | `txPower`[1byte] |
| `ADV_INTERVAL` | `Read/Write` | `$0\times2004$` | `$0\times00$` | `advInterval` [2byte] |
| `UPLINK INTERVAL` | `Read/Write` | `$0\times2005$` | `$0\times00$` | `uplinkInterval` [4byte] |
[cite\_start][cite: 48]

**\<`DeviceSettingInfo` Service の詳細\>**

  - **`TIME_ZONE`**
    [cite\_start]タイムゾーンを設定します。 [cite: 49]
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | [cite\_start]日本時間 [cite: 50] |
    | `$0\times01$` | [cite\_start]UTC [cite: 50] |
    | 上記以外 | [cite\_start]日本時間 [cite: 50] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 51]

  - **`BLE_MODE`**
    [cite\_start]`Bluetooth` 通信モードの設定情報を以下に示します。 [cite: 51]
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | [cite\_start]`LongRange` [cite: 52] |
    | `$0\times01$` | [cite\_start]`Legacy` [cite: 52] |
    | 上記以外 | [cite\_start]`LongRange` [cite: 52] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 53]

  - **`TX_POWER`**
    [cite\_start]`Bluetooth` 通信モードの設定情報を以下に示します。 [cite: 53]
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | [cite\_start]`±0dBm` [cite: 54] |
    | `$0\times01$` | [cite\_start]`+4dBm` [cite: 54] |
    | `$0\times02$` | [cite\_start]`-4dBm` [cite: 54] |
    | `$0\times03$` | [cite\_start]`-8dBm` [cite: 54] |
    | `$0\times04$` | [cite\_start]`-12dBm` [cite: 54] |
    | `$0\times05$` | [cite\_start]`-16dBm` [cite: 54] |
    | `$0\times06$` | [cite\_start]`-20dBm` [cite: 54] |
    | `$0\times07$` | [cite\_start]`-40dBm` [cite: 54] |
    | `$0\times08$` | [cite\_start]`+8dBm` [cite: 54] |
    | 上記以外 | [cite\_start]`±0dBm` [cite: 54] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 55]

  - **`ADV_INTERVAL`**
    [cite\_start]`Advertise` を発信する間隔を設定します。 [cite: 58]
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x0064` | [cite\_start]`100ms` 周期に `Advertise` を発信します。 [cite: 57] |
    | : | : |
    | `0x03E8` | [cite\_start]`10000ms` 周期に `Advertise` を発信します。 [cite: 57] |
    | : | : |
    | `0x2710` | [cite\_start]`10000ms` 周期に`Advertise` を発信します。 [cite: 57] |
    | 上記以外 | [cite\_start]`1000ms` 周期に`Advertise` を発信する設定になります。 [cite: 57] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 58]
    [cite\_start]※エンディアンはリトルエンディアン。 [cite: 58]

  - **`UPLINK_INTERVAL`**
    [cite\_start]`Sensor` 情報データを `Uplink` する間隔を設定する。 [cite: 58]
    **\<計測モードがが「瞬時値モード」の場合\>**
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00000001` | [cite\_start]`1`秒周期に `Sensor` 情報データを `Uplink` します [cite: 59] |
    | : | |
    | `0x00000E10` | [cite\_start]`3600`秒(1時間)周期に`Sensor` 情報データを `Uplink` します [cite: 59] |
    | `0x00015180` | [cite\_start]`86400`秒(24時間)周期に`Sensor` 情報データを `Uplink` します。 [cite: 59] |
    | 上記以外 | [cite\_start]`60`秒周期に `Sensor` 情報データを `Uplink` します。 [cite: 59] |

    **\<計測モードがが「検知モード」の場合\>**
    [cite\_start]本設定は無視されます。 [cite: 60]

    **\<計測モードがが「サンプリングモード」の場合\>**
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x0000003C` | [cite\_start]`60`秒周期に `Sensor` 情報データを `Uplink` します [cite: 61] |
    | : | : |
    | `0x00000E10` | [cite\_start]`3600`秒(1時間)周期に`Sensor` 情報データを `Uplink` します [cite: 61] |
    | : | : |
    | `0x00015180` | [cite\_start]`86400`秒(24時間)周期に`Sensor` 情報データを `Uplink` します。 [cite: 61] |
    | 上記以外 | [cite\_start]`60`秒周期に `Sensor` 情報データを`Uplink` します。 [cite: 61] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 62]
    [cite\_start]※エンディアンはリトルエンディアン。 [cite: 62]

#### 4-3-3. SensorSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `SENS_READ_REQ` | `Write` | `$0\times3001$` | `$0\times00$` | `sensnorReq`[1byte] |
| `SENS READ RESP` | `Notify` | `$0\times3002$` | `$0\times00$` | `sensnorValue`[4byte] |
| `SENS MODE` | `Read/Write` | `$0\times3003$` | `$0\times00$` | `sensnorMode` [1byte] |
| `SAMPLING` | `Read/Write` | `$0\times3004$` | `$0\times00$` | `sampling` [1byte] |
| `HYSTERESIS H` | `Read/Write` | `$0\times3005$` | `$0\times00$` | `hysteresisHigh`[4byte] |
| `HYSTERESIS L` | `Read/Write` | `$0\times3006$` | `$0\times00$` | `hysteresisLow`[4byte] |
[cite\_start][cite: 64]

**\<`SensorSettingInfo` Service の詳細\>**

  - **`SENS_READ_REQ`**
    [cite\_start]`0x01`を `write` すると現在のセンサー情報取得開始します。 [cite: 65]
  - **`SENS_READ_RESP`**
    [cite\_start]`SENS_READ_REQ` に対する応答で、現在の差圧センサー値(`Pa`)を `Notify` します。 [cite: 65]
    [cite\_start]※※データフォーマットは `float`型。 [cite: 65]
    [cite\_start]※エンディアンはリトルエンディアン。 [cite: 65]
  - **`SENS_MODE`**
    [cite\_start]`Sensor` 情報の扱いを設定する。 [cite: 65]
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | [cite\_start]瞬時値モード: `Uplink` タイミング時の現在の値を通知します [cite: 66] |
    | `$0\times01$` | [cite\_start]検知モード: ヒステリシス検知したことを通知します。 [cite: 66] |
    | `$0\times02$` | [cite\_start]サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します [cite: 66] |
    | 上記以外 | [cite\_start]瞬時値モード設定になります。 [cite: 66] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 67]
  - **`SAMPLING`**
    [cite\_start]当該センサー情報を `Read` する周期を設定します。 [cite: 67]
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | [cite\_start]`1Hz`: `1000ms` 周期にセンサー情報を`Read`します。 [cite: 68] |
    | `$0\times01$` | [cite\_start]`2Hz`:`500ms` 周期にセンサー情報を `Read` します。 [cite: 68] |
    | 上記以外 | [cite\_start]`1Hz` 設定になります。 [cite: 68] |
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 69]
  - **`HYSTERESIS_H`**
    [cite\_start]`High` 側のヒステリシスを設定します。(範囲:`-500Pa`\~`500Pa`) [cite: 70]
    | 設定値 | 説明 |
    | :--- | :--- |
    | : | [cite\_start]`-500Pa` 以下は`-500Pa`に丸められます。 [cite: 71] |
    | `0xFFFFFE0C` | [cite\_start]`-500Pa` [cite: 71] |
    | : | : |
    | `0xFFFFFFFF` | [cite\_start]`-1Pa` [cite: 71] |
    | `0x00000000` | [cite\_start]`OPa` [cite: 71] |
    | `0x00000001` | [cite\_start]`1Pa` [cite: 71] |
    | : | : |
    | `0x000001F4` | [cite\_start]`500Pa` [cite: 71] |
    | : | [cite\_start]`500Pa` 以上はは`500Pa` に丸められます。 [cite: 71] |
    [cite\_start]※`Low`\>=`High` の場合は当該CHのヒステリシスは無効となる。 [cite: 72]
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 72]
    [cite\_start]※エンディアンはリトルエンディアン。 [cite: 72]
  - **`HYSTERESIS_L`**
    [cite\_start]`Low` 側のヒステリシスを設定します。(範囲:`-500Pa`\~`500Pa`) [cite: 72]
    | 設定値 | 説明 |
    | :--- | :--- |
    | : | [cite\_start]`-500Pa` 以下は`-500Pa`に丸められます。 [cite: 73] |
    | `0xFFFFFE0C` | [cite\_start]`-500Pa` [cite: 73] |
    | : | : |
    | `0xFFFFFFFF` | [cite\_start]`-1Pa` [cite: 73] |
    | `0x00000000` | [cite\_start]`OPa` [cite: 73] |
    | `0x00000001` | [cite\_start]`1Pa` [cite: 73] |
    | : | : |
    | `0x000001F4` | [cite\_start]`500Pa` [cite: 73] |
    | : | [cite\_start]`500Pa` 以上はは`500Pa` に丸められます。 [cite: 73] |
    [cite\_start]※`Low`\>=`High` の場合は当該CHのヒステリシスは無効となる。 [cite: 74]
    [cite\_start]※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。 [cite: 74]
    [cite\_start]※エンディアンはリトルエンディアン。 [cite: 74]

#### 4-3-4. DeviceInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `DEVICEID` | `Read` | `$0\times4001$` | `$0\times00$` | `nordicDeviceId` [8byte] |
| `FW VERSION` | `Read` | `$0\times4002$` | `$0\times00$` | `fwVersion` [3byte] |
| `HW VERSION` | `Read` | `$0\times4003$` | `$0\times00$` | `hwVersion` [3byte] |
| `BATTERY` | `Read` | `$0\times4004$` | `$0\times00$` | `batteryLevel` [1byte] |
| `DFU TYPE` | `Read` | `$0\times4005$` | `$0\times00$` | `dfuType`[1byte] |
| `DFU_REQUEST` | `Write` | `$0\times4006$` | `$0\times00$` | `dfuRequest`[1byte] |
| `REGISTER` | `Write` | `$0\times4007$` | `$0\times00$` | `register`[3byte] |
[cite\_start][cite: 76]

**\<`DeviceInfo` Service の詳細\>**

  - **`DEVICEID`**
    [cite\_start]`Nordic` のチップのユニークなIDを読み出せます。 [cite: 77]
  - **`FW_VERSION`**
    [cite\_start]本製品のファームウェアバージョンを読み出せます。 [cite: 77]
    [cite\_start]例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。 [cite: 77]
  - **`HW_VERSION`**
    [cite\_start]本製品のHWバージョンを読み出せます。 [cite: 77]
    [cite\_start]例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。 [cite: 77]
  - **`BATTERY`**
    [cite\_start]本製品の現在のバッテリーレベル(%)を読み出せます。 [cite: 77]
  - **`DFU_TYPE`**
    [cite\_start]固定で `0x01` が読み出されます。 [cite: 77]
  - **`DFU_REQUEST`**
    [cite\_start]`0x01` を `Write` すると、`Bleutooth` 切断し、`DFU` モードに移行します。 [cite: 77]
  - **`REGISTER`**
    [cite\_start]`0x66a781` を `write` すると変更された変更されて全ての情報を保存し、変更した設定を有効にします。 [cite: 77]

-----

## 5\. 動作フロー

[cite\_start][画像: 動作フロー図] [cite: 78]

-----

## 6\. Uplink データ仕様

[cite\_start]`BravePI` メインボードから通知される情報ついて以下に示す。 [cite: 79]

### 6-1. Sensor 情報

[cite\_start]`SensorID`: `0x0107` [cite: 79]
| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0107` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | 継続データ有無 | |
| **Data 領域** | | | |
| `Battery Level` | 1 | バッテリーレベル(%) | |
| `sampleNum` | 2 | サンプル数 | |
| `DiffPaData[0]` | 4 | 差圧情報(`Pa`) | `float` 型 |
| : | : | : | |
| `DiffPaData[n]` | 4 | 差圧情報(`Pa`) | `float` 型 |
[cite\_start][cite: 80]
[cite\_start]※エンディアンはリトルエンディアンになります。 [cite: 81]

### 6-2. パラメータ情報

[cite\_start]`SensorID`: `0x0000` [cite: 82]
| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | `0x00`:継続データなし | |
| **Data 領域** | | | |
| `SensorID` | 2 | `0x0107` 固定 | |
| `FW Version` | 3 | 本製品のファームウェアバージョン | `Ver1.2.9`の場合は、`[0x01,0x02,0x09]` |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `BLE Mode` | 1 | `Bluetooth` 通信モードの設定情報 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval`| 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | |
| `Sensor Read Mode` | 1 | 計測モード | |
| `Sampling` | 1 | サンプリング周期 | |
| `HysteresisHigh` | 4 | ヒステリシス(`High`) | |
| `HysteresisLow` | 4 | ヒステリシス(`Low`) | |
[cite\_start][cite: 83]
[cite\_start]※エンディアンはリトルエンディアンになります。 [cite: 84]

-----

## 7\. Downlink データ仕様

[cite\_start]`BravePI` メインボードから送信する情報ついて以下に示す。 [cite: 85]

### 7-1. 即時 Uplink 要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0107` | |
| `CMD` | 1 | `0x00` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
[cite\_start][cite: 86]
[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 87]

### 7-2. パラメータ情報設定要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0014` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x05` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `SensorID` | 2 | `0x0107` | |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | |
| `Sensor Read Mode` | 1 | 計測モード | |
| `Sampling` | 1 | サンプリング周期 | |
| `HysteresisHigh` | 4 | ヒステリシス(`High`) | |
| `HysteresisLow` | 4 | ヒステリシス(`Low`) | |
[cite\_start][cite: 88]
[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 89]

### 7-3. パラメータ情報取得要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00`固定 | |
| `DataLength` | 2 | `0x0001` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x0D` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | 1 | `0x00` | |
[cite\_start][cite: 91]
[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 92]

### 7-4. デバイス Config 移行要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0xFC` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
[cite\_start][cite: 93]
[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 94]

### 7-5. デバイス再起動要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0xFD` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
[cite\_start][cite: 95]
[cite\_start]※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。 [cite: 96]

-----

## 8\. 電池駆動時の各設定における電池持ち

[cite\_start]`BravePI` トランスミッター(`CR123A`) 使用時の代表的な設定におけるおおよその電池持ちを以下に示します。 [cite: 97]

**\<`Bluetooth` 通信モード: `Legacy` の場合\>**
| パラメータ設定情報 | | | | | 電池持ち |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **計測モード** | **サンプリング周期** | **`TxPower`** | **`Uplink Interval`** | **`Advertise Interval`** | **(日)** |
| 瞬時値モード | | `0dBm` | `1`秒 | `100ms` | 164 |
| | | | `10`秒 | `100ms` | 465 |
| | | | | `1000ms` | 1159 |
| | | | `60`秒 | `100ms` | 568 |
| | | | | `1000ms` | 2160 |
| 検知モード | `1Hz` | `0dBm` | `60`秒 | `100ms` | 156 |
| サンプリングモード | | | | `1000ms` | 205 |
| | `2Hz` | `0dBm` | `60`秒 | `100ms` | 93 |
| | | | | `1000ms` | 102 |
[cite\_start][cite: 98]

**\<`Bluetooth` 通信モード: `Long Range` の場合\>**
| パラメータ設定情報 | | | | | 電池持ち |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **計測モード** | **サンプリング周期** | **`TxPower`** | **`Uplink Interval`** | **`Advertise Interval`** | **(日)** |
| 瞬時値モード | | `0dBm` | `1`秒 | `100ms` | 108 |
| | | | `10`秒 | `100ms` | 173 |
| | | | | `1000ms` | 819 |
| | | | `60`秒 | `100ms` | 181 |
| | | | | `1000ms` | 1175 |
| 検知モード | `1Hz` | `0dBm` | `60`秒 | `100ms` | 93 |
| サンプリングモード | | | | `1000ms` | 155 |
| | `2Hz` | `0dBm` | `60`秒 | `100ms` | 67 |
| | | | | `1000ms` | 92 |
[cite\_start][cite: 100]

-----

## 9\. 製品到着から使用開始までの流れ

### 9-1. BravePI トランスミッターの設定

[cite\_start]`BravePI` トランスミッター側の設定手順について以下に示します。 [cite: 102]

1.  [cite\_start]トランスミッターからセンサーを外した状態にする。 [cite: 102]
2.  [cite\_start]トランスミッターに電池又はUSB給電する。 [cite: 102]
3.  [cite\_start]専用のiPhoneアプリを起動する。 [cite: 102]
4.  [cite\_start]iPhone アプリから差圧センサー用の「`DFU`」を実行する。 [cite: 102]
5.  [cite\_start]iPhone アプリから差圧センサー用の「パラメータ設定」を実行する。 [cite: 102]
6.  [cite\_start]トランスミッターに差圧センサーを取り付ける。 [cite: 102]
7.  [cite\_start]iPhone アプリからトランスミッターに電源ON(再起動)操作を行う。 [cite: 102]

[cite\_start]次に`BravePI` トランスミッターと `BravePI` メインボードの紐付けを実行して下さい。 [cite: 102]

### 9-2. BravePI トランスミッターと BravePI メインボードの紐付け

[cite\_start]`BravePI` トランスミッターと `BravePI` メインボードの紐付け手順について以下に示します。 [cite: 102]

1.  [cite\_start]専用の iPhone アプリを起動する。 [cite: 102]
2.  [cite\_start]iPhone アプリから「ペアリング設定」を実行する。 [cite: 102]

[cite\_start]以上で設定は終了です。 [cite: 102]

-----

## 10\. 商標について

  - [cite\_start]`Bluetooth®`とワードマークおよびロゴは、`Bluetooth SIG INC` が所有する登録商標です。 [cite: 103]
    [cite\_start]株式会社 `Braveridge` はこれら商標を使用する許可を受けています。 [cite: 103] [cite\_start]その他のロゴマーク及び商号は各所有者に帰属します。 [cite: 103]

## 11\. Revision 管理

| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2024/01/25 | `Ver1.0.1` | 初版 |
[cite\_start][cite: 104]

[cite\_start]※上記、製品仕様や機能、デザインは変更となる可能性がございます。 [cite: 105] [cite\_start]あらかじめご了承ください。 [cite: 105]

[cite\_start]`Braveridge`とその製品に関する詳しい情報は、弊社Webサイトで御確認ください。 [cite: 105]
[cite\_start][https://www.braveridge.com/](https://www.braveridge.com/) [cite: 105]

  - **株式会社Braveridge 本社**
    [cite\_start]〒819-0373 福岡県福岡市西区周船寺3-27-2 [cite: 105]
    [cite\_start](https://www.google.com/search?q=Tel): 092-834-5789 / (Fax): 092-807-7718 [cite: 105]
  - **株式会社Braveridge 糸島工場**
    [cite\_start]〒819-1122 福岡県糸島市東1999-19 [cite: 105]
    [cite\_start]Apple `MFi` Manufacture ライセンス認定工場(ライトニングコネクタ製品工場) [cite: 105]