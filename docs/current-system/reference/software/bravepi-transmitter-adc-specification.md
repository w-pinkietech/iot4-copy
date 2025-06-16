**公式仕様書**: [ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (ADC センサー版)](https://drive.google.com/file/d/1sd4guzPmAeKje_iwyPTy7thZLyFEO8cf/view)

# ソフトウェア仕様書 BravePI トランスミッター専用 ファームウェア (ADC センサー版)

**REV 1.0**

**DESIGNED BY Braveridge Co., Ltd.**

-----

## 目次

  - [1 概要](https://www.google.com/search?q=%231-%E6%A6%82%E8%A6%81)
  - [2 機能概要](https://www.google.com/search?q=%232-%E6%A9%9F%E8%83%BD%E6%A6%82%E8%A6%81)
      - [2-1 Sensor データ取得機能](https://www.google.com/search?q=%232-1-sensor-%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
          - [2-1-1 計測モード](https://www.google.com/search?q=%232-1-1-%E8%A8%88%E6%B8%AC%E3%83%A2%E3%83%BC%E3%83%89)
      - [2-2 LED 表示機能](https://www.google.com/search?q=%232-2-led-%E8%A1%A8%E7%A4%BA%E6%A9%9F%E8%83%BD)
      - [2-3 Bluetooth 通信機能](https://www.google.com/search?q=%232-3-bluetooth-%E9%80%9A%E4%BF%A1%E6%A9%9F%E8%83%BD)
          - [2-3-1 Uplink](https://www.google.com/search?q=%232-3-1-uplink)
          - [2-3-2 Downlink](https://www.google.com/search?q=%232-3-2-downlink)
      - [2-4 NFCTag 通信機能](https://www.google.com/search?q=%232-4-nfctag-%E9%80%9A%E4%BF%A1%E6%A9%9F%E8%83%BD)
      - [2-5 パラメータ変更/取得機能](https://www.google.com/search?q=%232-5-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%A4%89%E6%9B%B4%E5%8F%96%E5%BE%97%E6%A9%9F%E8%83%BD)
          - [2-5-1 パラメータ変更方法について](https://www.google.com/search?q=%232-5-1-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%A4%89%E6%9B%B4%E6%96%B9%E6%B3%95%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
          - [2-5-2 パラメータ取得方法について](https://www.google.com/search?q=%232-5-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E6%96%B9%E6%B3%95%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
          - [2-5-3 変更可能なパラメータについて](https://www.google.com/search?q=%232-5-3-%E5%A4%89%E6%9B%B4%E5%8F%AF%E8%83%BD%E3%81%AA%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
      - [2-6 DFU 機能](https://www.google.com/search?q=%232-6-dfu-%E6%A9%9F%E8%83%BD)
  - [3 パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)
  - [4 Config モード時 Bluetooth 通信仕様](https://www.google.com/search?q=%234-config-%E3%83%A2%E3%83%BC%E3%83%89%E6%99%82-bluetooth-%E9%80%9A%E4%BF%A1%E4%BB%95%E6%A7%98)
      - [4-1 基本情報](https://www.google.com/search?q=%234-1-%E5%9F%BA%E6%9C%AC%E6%83%85%E5%A0%B1)
      - [4-2 Advertise/Scan Response Packet](https://www.google.com/search?q=%234-2-advertisescan-response-packet)
      - [4-3 Service](https://www.google.com/search?q=%234-3-service)
          - [4-3-1 BraveGATEInfo Service](https://www.google.com/search?q=%234-3-1-bravegateinfo-service)
          - [4-3-2 DeviceSettingInfo Service](https://www.google.com/search?q=%234-3-2-devicesettinginfo-service)
          - [4-3-3 SensorSettingInfo Service](https://www.google.com/search?q=%234-3-3-sensorsettinginfo-service)
          - [4-3-4 DeviceInfo Service](https://www.google.com/search?q=%234-3-4-deviceinfo-service)
  - [5 動作フロー](https://www.google.com/search?q=%235-%E5%8B%95%E4%BD%9C%E3%83%95%E3%83%AD%E3%83%BC)
  - [6 Uplink データ仕様](https://www.google.com/search?q=%236-uplink-%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98)
      - [6-1 Sensor 情報](https://www.google.com/search?q=%236-1-sensor-%E6%83%85%E5%A0%B1)
      - [6-2 パラメータ情報](https://www.google.com/search?q=%236-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)
  - [7 Downlink データ仕様](https://www.google.com/search?q=%237-downlink-%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98)
      - [7-1 即時 Uplink 要求](https://www.google.com/search?q=%237-1-%E5%8D%B3%E6%99%82-uplink-%E8%A6%81%E6%B1%82)
      - [7-2 パラメータ情報設定要求](https://www.google.com/search?q=%237-2-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1%E8%A8%AD%E5%AE%9A%E8%A6%81%E6%B1%82)
      - [7-3 パラメータ情報取得要求](https://www.google.com/search?q=%237-3-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1%E5%8F%96%E5%BE%97%E8%A6%81%E6%B1%82)
      - [7-4 デバイス Config 移行要求](https://www.google.com/search?q=%237-4-%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9-config-%E7%A7%BB%E8%A1%8C%E8%A6%81%E6%B1%82)
      - [7-5 デバイス再起動要求](https://www.google.com/search?q=%237-5-%E3%83%87%E3%83%90%E3%82%A4%E3%82%B9%E5%86%8D%E8%B5%B7%E5%8B%95%E8%A6%81%E6%B1%82)
  - [8 電池駆動時の各設定における電池持ち](https://www.google.com/search?q=%238-%E9%9B%BB%E6%B1%A0%E9%A7%86%E5%8B%95%E6%99%82%E3%81%AE%E5%90%84%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8B%E9%9B%BB%E6%B1%A0%E6%8C%81%E3%81%A1)
  - [9 製品到着から使用開始までの流れ](https://www.google.com/search?q=%239-%E8%A3%BD%E5%93%81%E5%88%B0%E7%9D%80%E3%81%8B%E3%82%89%E4%BD%BF%E7%94%A8%E9%96%8B%E5%A7%8B%E3%81%BE%E3%81%A7%E3%81%AE%E6%B5%81%E3%82%8C)
      - [9-1 BravePI トランスミッターの設定](https://www.google.com/search?q=%239-1-bravepi-%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B9%E3%83%9F%E3%83%83%E3%82%BF%E3%83%BC%E3%81%AE%E8%A8%AD%E5%AE%9A)
      - [9-2 BravePI トランスミッターと BravePI メインボードの紐付け](https://www.google.com/search?q=%239-2-bravepi-%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B9%E3%83%9F%E3%83%83%E3%82%BF%E3%83%BC%E3%81%A8-bravepi-%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9C%E3%83%BC%E3%83%89%E3%81%AE%E7%B4%90%E4%BB%98%E3%81%91)
  - [10 商標について](https://www.google.com/search?q=%2310-%E5%95%86%E6%A8%99%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)
  - [11 Revision 管理](https://www.google.com/search?q=%2311-revision-%E7%AE%A1%E7%90%86)

-----

[画像: BravePI メインボードとBravePI トランスミッターがBluetoothで接続されている図]

# 1 概要

本仕様書は、BravePI トランスミッターにADC センサーボードを接続した際に使用するファームウェア (以降、本製品とする) のソフトウェア仕様を記載したものです。

本仕様書は、対象とするハードウェアを以下に示します。

\<BravePI トランスミッター\>
| 製品名 | | 型番 |
| :--- | :--- | :--- |
| BravePI | トランスミッター (CR123A) | `BVPTB-01` |
| BravePI | トランスミッター (USB) | `BVPTU-01` |

\<BravePI センサーボード\>
| 製品名 | 型番 |
| :--- | :--- |
| BravePI ADC センサーボード | `BVPSA-01` |

BravePI トランスミッターは、取得したセンサーの値をペアリングされた BravePI メインボードに通知します。

[画像: BravePI メインボードとBravePI トランスミッターの通信イメージ図]

# 2 機能概要

## 2-1 Sensor データ取得機能

本製品は、接続した `ADC` センサーの値を送信することができます。

| センサーIC | センサーメーカー |
| :--- | :--- |
| `MCP3427` | Microchip |

### 2-1-1 計測モード

本製品は以下の計測モードで `ADC` センサーの情報を取得することができます。
| 測定モード | 説明 |
| :--- | :--- |
| 瞬時値モード | `Uplink` タイミング時に現在の値を取得し通知します。 |
| 検知モード | 定期的に値を取得し、ヒステリシス検知した場合に通知します。\<br\>ヒステリシスで指定された検知/復帰の設定範囲は以下になります。\<br\>設定 `CH` 項目\<br\>ヒステリシス (High) 1 `-2000mV~2000mV`\<br\>ヒステリシス (Low) `-2000mV~2000mV`\<br\>ヒステリシス (High) 2 `-2000mV~2000mV`\<br\>ヒステリシス (Low) `-2000mV~2000mV` |
| サンプリングモード | 指定したサンプリング周期でサンプリングした値を通知します。\<br\>サンプリングモード時の設定可能なサンプリング周期は以下とする。\<br\>項目 設定\<br\>サンプリング周期 `1Hz` `2Hz`\<br\>各サンプリングモード時の最大 `Uplink` 周期は以下になります\<br\>最大 `Uplink` 間隔 サンプリング周期\<br\>`10000秒` `1Hz`\<br\>`5000秒` `2Hz` |

## 2-2 LED 表示機能

本製品は、本製品の状態をLEDで表示します。
| 優先 | 状態 | LED | | 備考 |
| :--- | :--- | :--- | :--- | :--- |
| | | 赤 | 青 | |
| 高 | `LowBattery` 状態 | 点滅 | - | 1秒点灯、3秒消灯を繰り返す |
| | `Config` モード | | 点滅 | 1秒点灯、3秒消灯を繰り返す |
| 1 | `PowerON` | | 点灯 | 2秒点灯 |
| | `PowerOFF` | 点灯 | | 2秒点灯 |
| 低 | 上記以外(通常動作中) | | | 無灯 |

## 2-3 Bluetooth 通信機能

本製品は接続されたセンサー基板から取得されたセンサー情報を `Bleutooth` 通信で `BravePI` メインボードに通知します。また、`BravePI` メインボード経由で本製品に対して設定や指示等を `Downlink` することも可能です。

### 2-3-1 Uplink

以下の情報を `Uplink` することができます。
| Uplink 情報 | Uplink タイミング |
| :--- | :--- |
| センサーデータ | パラメータで指定された `Uplink` 間隔 |
| パラメータ情報 | `Downlink` でパラメータ情報取得要求された場合 |

### 2-3-2 Downlink

以下の指示を `Downlink` することができます。
| Downlink 情報 | 動作概要 |
| :--- | :--- |
| 即時 `Uplink` 要求 | 現在のセンサー情報の `Uplink` 要求します。 |
| パラメータ情報設定要求 | 本製品のパラメータ情報を設定します。 |
| パラメータ情報取得要求 | 本製品のパラメータ情報の `Uplink` 要求します |
| デバイス `Config` 移行 | 本製品を `Config` モードに移行します。 |
| デバイス再起動 | 本製品を再起動します |

## 2-4 NFCTag 通信機能

本製品は `NFCTag`を有しており、専用スマホアプリより各種設定や情報取得することができます。
以下が`NFCTag` 機能で専用スマホアプリより行える操作になります。
| 項目 | 動作概要 | 備考 |
| :--- | :--- | :--- |
| デバイス再起動 | 本製品を再起動する。 | |
| 電源ON 要求 | 本製品を電源OFF から復帰する | |
| 電源OFF 要求\<br\>(`NFCTag` のみ有効) | 本製品を電源OFFにする。 | 電源OFF状態の場合は、本要求は\<br\>無視されます。 |
| `Config` モード移行要求 | 本製品を `Config` モードに移行します。 | 電源OFF状態の場合は、本要求は\<br\>無視されます。 |

## 2-5 パラメータ変更/取得機能

本製品のパラメータ情報の変更/取得することができます。

### 2-5-1 パラメータ変更方法について

本製品のパラメータ情報の変更は以下の方法で行えます。
・`BravePI` メインボードからパラメータ情報を `Downlink` することで変更することができます。
・本製品を `Config` モードにすることで、`Bleutooth` 経由で変更することができます。

### 2-5-2 パラメータ取得方法について

本製品のパラメータ情報の設定は以下の方法で行えます。
・`BravePI` メインボードからパラメータ取得要求を `Downlink` することでパラメータ情報を `Uplink` します。
・本製品を `Config` モードにすることで、`Bleutooth` 経由で取得することができます。

### 2-5-3 変更可能なパラメータについて

本製品の変更/取得可能なパラメータに関しては「[3 パラメータ情報](https://www.google.com/search?q=%233-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E6%83%85%E5%A0%B1)」を参照下さい。

## 2-6 DFU 機能

専用スマホアプリを使用することで、本製品のファームウェアの書き換えができます。
本製品のファームウェアの書き換えは、専用スマホアプリ以外からは行えません。

# 3 パラメータ情報

本製品のパラメータを以下に示します。
| パラメータ項目 | 設定情報 |
| :--- | :--- |
| `DeviceID` | `BravePI` メインボードと通信する為に必要な、`DeviceID`. |
| `SensorID` | `BravePI` メインボードと通信する為に必要な、`SensorID` |
| タイムゾーン設定 | タイムゾーン設定に関する設定情報を以下に示します\<br\>設定値 説明\<br\>`0x00` 日本時間\<br\>`0x01` UTC\<br\>上記以外 日本時間 |
| `BLE Mode` | `Bluetooth` 通信モードの設定情報を以下に示します。\<br\>設定値 説明\<br\>`$0\times00$` `LongRange`\<br\>`0x01` `Legacy`\<br\>上記以外 `Long Range` |
| `Tx Power` | `Bluetooth` 通信の送信電波出力の設定情報を以下に示します\<br\>設定値 説明\<br\>`$0\times00$` `±0dBm`\<br\>`0x01` `+4dBm`\<br\>`0x02` `-4dBm`\<br\>`$0\times03$` `-8dBm`\<br\>`0x04` `-12dBm`\<br\>`$0\times05$` `-16dBm`\<br\>`$0\times06$` `-20dBm`\<br\>`0x07` `-40dBm`\<br\>`0x08` `+8dBm`\<br\>上記以外 `±0dBm` |
| `Advertise Interval` | Advertise を発信する間隔設定情報を以下に示します。\<br\>設定値 説明\<br\>`0x0064` `100ms` 周期に `Advertise` を発信します。\<br\>: :\<br\>`0x03E8` `1000ms` 周期に`Advertise`を発信します。\<br\>: :\<br\>`0x2710` `10000ms` 周期に`Advertise` を発信します。\<br\>上記以外 `1000ms` 周期に`Advertise` を発信する設定になります。 |
| `Sensor Uplink Interval` | `Sensor` 情報データを `Uplink` する間隔を設定する\<br\>\<計測モードが「瞬時値モード」の場合\>\<br\>設定値 説明\<br\>`0x00000001` 1 秒周期に `Sensor` 情報データを `Uplink` します。\<br\>: :\<br\>`0x00000E10` 3600秒(1H)周期に `Sensor` 情報データを `Uplink`します\<br\>: :\<br\>`0x00015180` 86400秒(24H)周期に `Sensor` 情報データを `Uplink` します。\<br\>上記以外 60 秒周期に `Sensor` 情報データを`Uplink` します\<br\>\<計測モードが「検知モード」の場合\>\<br\>本設定は無視されます。\<br\>\<計測モードが「サンプリングモード」の場合\>\<br\>設定値 説明\<br\>`0x0000003C` 60秒周期に `Sensor` 情報データを `Uplink` します\<br\>: :\<br\>`0x00000E10` 3600秒(1H)周期に `Sensor` 情報データを `Uplink` します。\<br\>: :\<br\>`0x00015180` 86400秒(24H)周期に `Sensor` 情報データを `Uplink` します。\<br\>上記以外 60 秒周期に `Sensor` 情報データを `Uplink` します。 |
| 計測モード | `Sensor` 情報の扱いを設定します。\<br\>設定値 説明\<br\>`0x00` 瞬時値モード: `Uplink` タイミング時の現在の値を通知します。\<br\>`0x01` 検知モード: ヒステリシス検知したことを通知します。\<br\>`0x02` サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します。\<br\>上記以外 瞬時値モードの設定になります。 |
| サンプリング周期 | 当該センサー情報を `Read` する周期を設定します。\<br\>設定値 説明\<br\>`0x00` `1Hz`: `1000ms` 周期にセンサー情報を `Read` します。\<br\>`0x01` `2Hz`: `500ms` 周期にセンサー情報を`Read`します。\<br\>上記以外 `1Hz` 設定になります。 |
| `CH1 Gain` | `CH1`の`Gain` を設定します。\<br\>設定値 説明\<br\>`$0\times00$` `×1`\<br\>`0x01` `x2`\<br\>`$0\times02$` `x4`\<br\>`$0\times03$` `x8`\<br\>上記以外 `×1`設定になります。 |
| `CH1 ヒステリシス(High)` | `CH1`の`High` 側のヒステリシスを設定します\<br\>設定値 説明\<br\>: `-2000mV`以下は`-2000mV` に丸められます。\<br\>`0xFFFFF830` `-2000mV`\<br\>: \<br\>`0xFFFFFFFF` `-1mV`\<br\>`0x00000000` `0mV`\<br\>`0x00000001` `1mV`\<br\>: \<br\>`0x000007B0` `2000mV`\<br\>: `2000mV`以上はは`2000mV` に丸められます。 |
| `CH1 ヒステリシス (Low)` | `CH1`の`Low` 側のヒステリシスを設定します。\<br\>設定値 説明\<br\>: `-2000mV`以下は`-2000mV`に丸められます。\<br\>`0xFFFFF830` `-2000mV`\<br\>: \<br\>`0xFFFFFFFF` `-1mV`\<br\>`0x00000000` `0mV`\<br\>`0x00000001` `1mV`\<br\>: \<br\>`0x000007B0` `2000mV`\<br\>: `2000mV`以上はは`2000mV` に丸められます。 |
| `CH2 Gain` | `CH2`の`Gain` を設定します。\<br\>設定値 説明\<br\>`0x00` `1`\<br\>`0x01` `x2`\<br\>`0x02` `x4`\<br\>`0x03` `x8`\<br\>上記以外 `×1`設定になります。 |
| `CH2 ヒステリシス(High)` | `CH2`の`High` 側のヒステリシスを設定します\<br\>設定値 説明\<br\>: `-2000mV`以下は`-2000mV` に丸められます。\<br\>`0xFFFFF830` `-2000mV`\<br\>: \<br\>`0xFFFFFFFF` `-1mV`\<br\>`0x00000000` `0mV`\<br\>`0x00000001` `1mV`\<br\>: \<br\>`0x000007B0` `2000mV`\<br\>: `2000mV`以上はは`2000mV` に丸められます。 |
| `CH2 ヒステリシス(Low)` | `CH2`の`Low` 側のヒステリシスを設定します。\<br\>設定値 説明\<br\>`0xFFFFF830` `-2000mV`以下は`-2000mV` に丸められます。\<br\>: `-2000mV`\<br\>`0xFFFFFFFF` `-1mV`\<br\>`0x00000000` `0mV`\<br\>`0x00000001` `1mV`\<br\>: \<br\>`0x000007B0` `2000mV`\<br\>: `2000mV`以上はは`2000mV` に丸められます。 |

# 4 Config モード時 Bluetooth 通信仕様

`Config` モード時用の`Bluetooth` 通信プロファイル仕様を以下に示します。

## 4-1 基本情報

| 項目 | 値 |
| :--- | :--- |
| `Advertising Interval` | `1000ms` |
| `Min Connection Interval` | `20ms` |
| `Max Connection Interval` | `40ms` |
| `Slave Latency` | `0` |
| `Supervision Timeout` | `6000ms` |

## 4-2 Advertise/Scan Response Packet

**\<Advertise データ\>**
| Index | Data | Description | Comment |
| :--- | :--- | :--- | :--- |
| 0 | `$0\times02$` | Length | |
| 1 | `$0\times01$` | Advertising Field Type | `FLAGS` |
| 2 | `$0\times06$` | Flag type | `LE ONLY GENERAL DISCOVER MODE` |
| 3 | `$0\times11$` | Length | |
| 4 | `0x07` | Advertising Field Type | `Complete List of 128-bit Service Class UUIDS` |
| 5-20 | 右記 | Service UUID | `57791000-a129-4d7f-93a6-87f82b59f6a4` |
| 21 | `0x06` | Length | |
| 22 | `0x09` | Advertising Field Type | `Complete Local Name` |
| 23-28 | 右記 | Local Name | `BvPiTm` |

**\<ScanResponse データ\>**
なし

## 4-3 Service

`677eXXXX-79f2-4584-91f9-098db93d0781`
以下の `Service`/`Characteristic` の`UUID`は上記 `UUID` の `XXXX` (Alias)の部分に各`Service`/`Characteristic` の `Alias` を設定した値になります。

| Service Name | Alias | Characteristic Name |
| :--- | :--- | :--- |
| `BraveGATEInfo` | `$0\times1000$` | `BV DEVICEID` |
| | | `BV COMPANYID` |
| | | `BV SENSORID` |
| `DeviceSetting` | `0x2000` | `TIME ZONE` `BLE MODE` |
| | | `TX POWER` `ADV INTERVAL` |
| | | `UPLINK INTERVAL` |
| `SensorSetting` | `0x3000` | `SENS_READ_REQ` |
| | | `SENS_READ_RESP` |
| | | `SENS MODE` |
| | | `SAMPLING` |
| | | `CH1 GAIN` |
| | | `CH2 GAIN` |
| | | `CH1 HYSTERESIS H` |
| | | `CH1 HYSTERESIS L` |
| | | `CH2 HYSTERESIS H` |
| | | `CH2 HYSTERESIS L` |
| `DeviceInfo` | `0x4000` | `DEVICEID` |
| | | `FW VERSION` |
| | | `HW_VERSION` |
| | | `BATTERY` |
| | | `DFU TYPE` |
| | | `DFU_REQUEST` |
| | | `REGISTER` |

### 4-3-1 BraveGATEInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `BV DEVICEID` | `Read` | `0x1001` | `$0\times00$` | `bvDeviceId` [8byte] |
| `BV COMPANYID` | `Read` | `$0\times1002$` | `$0\times00$` | `bvCompanyId` [8byte] |
| `BV SENSORID` | `Read` | `$0\times1003$` | `$0\times00$` | `bvSensorId` [2byte] |

**\<`BraveGATEInfo Service` の詳細\>**

  - **`BV_DEVICEID`**
    `BravePI` メインボードとの通信に必要な `DeviceID` を `Read` できます。
  - **`BV_COMPANYID`**
    `BravePI` メインボードとの通信に必要な `CompanyID`を `Read` できます。
  - **`BV_SENSORID`**
    `BravePI` メインボードとの通信に必要な `SensorID` を `Read` できます。

### 4-3-2 DeviceSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `TIME ZONE` | `Read/Write` | `$0\times2001$` | `$0\times00$` | `timeZone`[1byte] |
| `BLE MODE` | `Read/Write` | `$0\times2002$` | `$0\times00$` | `bleMode`[1byte] |
| `TX POWER` | `Read/Write` | `$0\times2003$` | `$0\times00$` | `txPower`[1byte] |
| `ADV_INTERVAL` | `Read/Write` | `$0\times2004$` | `$0\times00$` | `advInterval` [2byte] |
| `UPLINK INTERVAL` | `Read/Write` | `$0\times2005$` | `$0\times00$` | `uplinkInterval` [4byte] |

**\<`DeviceSettingInfo Service` の詳細\>**

  - **`TIME_ZONE`**
    タイムゾーンを設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | 日本時間 |
    | `$0\times01$` | `UTC` |
    | 上記以外 | 日本時間 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`BLE_MODE`**
    `Bluetooth` 通信モードの設定情報を以下に示します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | `Long Range` |
    | `$0\times01$` | `Legacy` |
    | 上記以外 | `LongRange` |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`TX_POWER`**
    `Bluetooth` 通信モードの設定情報を以下に示します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | `±0dBm` |
    | `$0\times01$` | `+4dBm` |
    | `$0\times02$` | `-4dBm` |
    | `$0\times03$` | `-8dBm` |
    | `$0\times04$` | `-12dBm` |
    | `$0\times05$` | `-16dBm` |
    | `$0\times06$` | `-20dBm` |
    | `$0\times07$` | `-40dBm` |
    | `$0\times08$` | `+8dBm` |
    | 上記以外 | `±0dBm` |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`ADV_INTERVAL`**
    `Advertise` を発信する間隔を設定します。
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

  - **`UPLINK_INTERVAL`**
    `Sensor` 情報データを `Uplink` する間隔を設定する。

    \<計測モードが「瞬時値モード」の場合\>
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x00000001` | 1秒周期に `Sensor` 情報データを `Uplink` します |
    | : | |
    | `0x00000E10` | 3600秒(1時間)周期に`Sensor` 情報データを `Uplink` します |
    | `0x00015180` | 86400秒(24時間)周期に`Sensor` 情報データを `Uplink` します。 |
    | 上記以外 | 60秒周期に `Sensor` 情報データを `Uplink` します。 |

    \<計測モードが「検知モード」の場合\>
    本設定は無視されます。

    \<計測モードが「サンプリングモード」の場合\>
    | 設定値 | 説明 |
    | :--- | :--- |
    | `0x0000003C` | 60秒周期に `Sensor` 情報データを `Uplink` します |
    | : | : |
    | `0x00000E10` | 3600秒(1時間)周期に`Sensor` 情報データを `Uplink` します |
    | : | : |
    | `0x00015180` | 86400秒(24時間)周期に`Sensor` 情報データを `Uplink` します。 |
    | 上記以外 | 60秒周期に `Sensor` 情報データを`Uplink` します。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

### 4-3-3 SensorSettingInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `SENS_READ_REQ` | `Write` | `$0\times3001$` | `$0\times00$` | `sensnorReq`[1byte] |
| `SENS READ RESP` | `Notify` | `$0\times3002$` | `$0\times00$` | `sensnorValue`[4byte] |
| `SENS MODE` | `Read/Write` | `$0\times3003$` | `$0\times00$` | `sensnorMode`[1byte] |
| `SAMPLING` | `Read/Write` | `$0\times3004$` | `$0\times00$` | `sampling`[1byte] |
| `CH1 GAIN` | `Read/Write` | `$0\times3005$` | `$0\times00$` | `ch1Gain`[1byte] |
| `CH2 GAIN` | `Read/Write` | `$0\times3006$` | `$0\times00$` | `ch2Gain` [1byte] |
| `CH1 HYSTERESIS H`| `Read/Write` | `$0\times3007$` | `$0\times00$` | `ch1HysteresisHigh` [4byte] |
| `CH1 HYSTERESIS L`| `Read/Write` | `$0\times3008$` | `$0\times00$` | `ch1HysteresisLow`[4byte] |
| `CH2 HYSTERESIS H`| `Read/Write` | `$0\times3009$` | `$0\times00$` | `ch2HysteresisHigh`[4byte] |
| `CH2 HYSTERESIS L`| `Read/Write` | `$0\times300A$` | `$0\times00$` | `ch2HysteresisLow`[4byte] |

**\<`SensorSettingInfo Service` の詳細\>**

  - **`SENS_READ_REQ`**
    `0x01`を `write` すると現在のセンサー情報取得開始します。

  - **`SENS_READ_RESP`**
    `SENS_READ_REQ` に対する応答で、現在の`CH1`/`CH2`の`AD`値を`Notify` します。
    | データ | サイズ | 説明 | |
    | :--- | :--- | :--- | :--- |
    | `CH1` 情報 | 2 | `AD` 情報(`mV`) | ※`signed short`型 |
    | `CH2` 情報 | 2 | `AD` 情報(`mV`) | ※`signed short` 型 |
    ※失敗時は、`0xFFFF`を返します。
    ※エンディアンはリトルエンディアン。

  - **`SENS_MODE`**
    `Sensor` 情報の扱いを設定する。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | 瞬時値モード: `Uplink` タイミング時の現在の値を通知します |
    | `0x01` | 検知モード: ヒステリシス検知したことを通知します |
    | `$0\times02$` | サンプリングモード: 指定したサンプリング周期でサンプリングした結果を通知します |
    | 上記以外 | 瞬時値モード設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`SAMPLING`**
    当該センサー情報を `Read` する周期を設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | `1Hz`: `1000ms` 周期にセンサー情報を `Read` します。 |
    | `$0\times01$` | `2Hz`: `500ms` 周期にセンサー情報を `Read` します。 |
    | `$0\times02$` | `5Hz`: `200ms` 周期にセンサー情報を `Read` します。 |
    | 上記以外 | `1Hz` 設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`CH1_GAIN`**
    `CH1`の`Gain` を設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | `x1` |
    | `0x01` | `x2` |
    | `$0\times02$` | `x3` |
    | `$0\times03$` | `x4` |
    | 上記以外 | `×1` 設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`CH2_GAIN`**
    `CH2`の`Gain` を設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | `$0\times00$` | `x1` |
    | `$0\times01$` | `x2` |
    | `$0\times02$` | `x3` |
    | `$0\times03$` | `x4` |
    | 上記以外 | `×1` 設定になります。 |
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。

  - **`CH1_HYSTERESIS_H`**
    `CH1`の`High` 側のヒステリシスを設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | : | `-2000mV`以下は`-2000mV` に丸められます |
    | `0xFFFFF830` | `-2000mV` |
    | : | : |
    | `0xFFFFFFFF` | `-1mV` |
    | `0x00000000` | `0mV` |
    | `0x00000001` | `1mV` |
    | : | : |
    | `0x000007B0` | `2000mV` |
    | : | `2000mV`以上はは`2000mV` に丸められます。 |
    ※`Low`\>=`High` の場合は当該`CH`のヒステリシスは無効となる。
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

  - **`CH1_HYSTERESIS_L`**
    `Low` 側のヒステリシスを設定します。(範囲:`-2000`\~`2000mV`)
    | 設定値 | 説明 |
    | :--- | :--- |
    | : | `-2000mV`以下は`-2000mV` に丸められます。 |
    | `0xFFFFF830` | `-2000mV` |
    | : | |
    | `0xFFFFFFFF` | `-1mV` |
    | `0x00000000` | `0mV` |
    | `0x00000001` | `1mV` |
    | : | : |
    | `0x000007B0` | `2000mV` |
    | : | `2000mV`以上はは`2000mV`に丸められます |
    ※`Low`\>=`High` の場合は当該`CH`のヒステリシスは無効となる。
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

  - **`CH2_HYSTERESIS_H`**
    `CH1`の`High` 側のヒステリシスを設定します。
    | 設定値 | 説明 |
    | :--- | :--- |
    | : | `-2000mV`以下は`-2000mV` に丸められます。 |
    | `0xFFFFF830` | `-2000mV` |
    | : | : |
    | `0xFFFFFFFF` | `-1mV` |
    | `0x00000000` | `0mV` |
    | `0x00000001` | `1mV` |
    | : | : |
    | `0x00000780` | `2000mV` |
    | : | `2000mV`以上はは`2000mV` に丸められます。 |
    ※`Low`\>=`High` の場合は当該`CH`のヒステリシスは無効となる。
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

  - **`CH2_HYSTERESIS_L`**
    `Low` 側のヒステリシスを設定します。(範囲:`-2000`\~`2000mV`)
    | 設定値 | 説明 |
    | :--- | :--- |
    | : | `-2000mV`以下は`-2000mV`に丸められます。 |
    | `0xFFFFF830` | `-2000mV` |
    | : | |
    | `0xFFFFFFFF` | `-1mV` |
    | `0x00000000` | `0mV` |
    | `0x00000001` | `1mV` |
    | : | |
    | `0x00000780` | `2000mV` |
    | : | `2000mV`以上はは`2000mV` に丸められます。 |
    ※`Low`\>=`High` の場合は当該`CH`のヒステリシスは無効となる。
    ※設定後、`DeviceInfo/REGISTER` を実行することで設定が反映されます。
    ※エンディアンはリトルエンディアン。

### 4-3-4 DeviceInfo Service

| Characteristic Name | Property | Alias | Address | Data |
| :--- | :--- | :--- | :--- | :--- |
| `DEVICEID` | `Read` | `$0\times4001$` | `$0\times00$` | `nordicDeviceId` [8byte] |
| `FW VERSION` | `Read` | `$0\times4002$` | `$0\times00$` | `fwVersion` [3byte] |
| `HW VERSION` | `Read` | `$0\times4003$` | `$0\times00$` | `hwVersion` [3byte] |
| `BATTERY` | `Read` | `$0\times4004$` | `$0\times00$` | `batteryLevel` [1byte] |
| `DFU TYPE` | `Read` | `$0\times4005$` | `$0\times00$` | `dfuType`[1byte] |
| `DFU_REQUEST` | `Write` | `$0\times4006$` | `$0\times00$` | `dfuRequest`[1byte] |
| `REGISTER` | `Write` | `$0\times4007$` | `$0\times00$` | `register`[3byte] |

**\<`DeviceInfo Service` の詳細\>**

  - **`DEVICEID`**
    `Nordic` のチップのユニークなIDを読み出せます。
  - **`FW_VERSION`**
    本製品のファームウェアバージョンを読み出せます。
    例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。
  - **`HW_VERSION`**
    本製品のHWバージョンを読み出せます。
    例: `Ver1.2.9`の場合は、 `[0x01, 0x02, 0x09]`で通知されます。
  - **`BATTERY`**
    本製品の現在のバッテリーレベル(%)を読み出せます。
  - **`DFU_TYPE`**
    固定で `0x01` が読み出されます。
  - **`DFU_REQUEST`**
    `0x01` を `Write` すると、`Bleutooth` 切断し、`DFU` モードに移行します。
  - **`REGISTER`**
    `0x66a781` を `write` すると変更された変更されて全ての情報を保存し、変更した設定を有効にします。

# 5 動作フロー

[画像: 動作フローチャート。POWER ONから始まり、NFCTag検知、POWER OFF中、Configモード中、センサーReadタイミング、Uplinkタイミング、Downlink受信の各状態を確認し、それぞれ対応する処理を実行するループ構造。]

# 6 Uplink データ仕様

`BravePI` メインボードから通知される情報ついて以下に示す。

## 6-1 Sensor 情報

`SensorID`: `0x0103`

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0103` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | 継続データ有無 | |
| **Data 領域** | | | |
| `Battery Level` | 1 | バッテリーレベル(%) | |
| `sampleNum` | 2 | サンプル数 | |
| `AdcData[0]` | 2 | `CH1` `ADC` 情報 | `signed short` 型 |
| | 2 | `CH2` `ADC` 情報 | `signed short`型 |
| : | : | : | |
| `AdcData[n]` | 2 | `CH1` `ADC` 情報 | `signed short` 型 |
| | 2 | `CH2` `ADC` 情報 | `signed short` 型 |

※エンディアンはリトルエンディアンになります。

## 6-2 パラメータ情報

`SensorID`: `0x0000`
| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `DataLength` | 2 | `Data` 部分のデータ長 | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `RSSI` | 1 | `Bluetooth` 電波強度 | |
| `Flag` | 1 | `0x00`:継続データなし | |
| **Data 領域** | | | |
| `SensorID` | 2 | `0x0103` 固定 | |
| `FW Version` | 3 | 本製品のファームウェアバージョン | `Ver1.2.9`の場合は、`[0x01,0x02,0x09]` |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `BLE Mode` | 1 | `Bluetooth` 通信モードの設定情報 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | |
| `Sensor Read Mode` | 1 | 計測モード | |
| `Sampling` | 1 | サンプリング周期 | |
| `CH1 Gain` | 1 | `CH1 Gain` | |
| `CH2 Gain` | 1 | `CH2 Gain` | |
| `CH1_HysteresisHigh` | 4 | `CH1` ヒステリシス(`High`) | |
| `CH1_HysteresisLow` | 4 | `CH1` ヒステリシス(`Low`) | |
| `CH2_HysteresisHigh` | 4 | `CH2` ヒステリシス(`High`) | |
| `CH2_HysteresisLow` | 4 | `CH2` ヒステリシス(`Low`) | |

※エンディアンはリトルエンディアンになります。

# 7 Downlink データ仕様

`BravePI` メインボードから送信する情報ついて以下に示す。

## 7-1 即時 Uplink 要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x0000` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0103` | |
| `CMD` | 1 | `0x00` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `Data` | | なし | |
※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

## 7-2 パラメータ情報設定要求

| 項目 | サイズ(Byte) | 説明 | 備考 |
| :--- | :--- | :--- | :--- |
| `Type` | 1 | `0x00` 固定 | |
| `DataLength` | 2 | `0x001E` | |
| `DeviceID` | 8 | 対象の `DeviceID` | |
| `SensorID` | 2 | `0x0000` | |
| `CMD` | 1 | `0x05` | |
| `Flag` | 1 | `0x00` | |
| **Data 部** | | | |
| `SensorID` | 2 | `0x0103` | |
| `TimeZone` | 1 | タイムゾーン設定 | |
| `Tx Power` | 1 | `Bluetooth` 通信の送信電波出力 | |
| `Advertise Interval` | 2 | `Advertise` を発信する間隔 | |
| `Sensor Uplink Interval` | 4 | `Sensor` 情報データを `Uplink` する間隔 | |
| `Sensor Read Mode` | 1 | 計測モード | |
| `Sampling` | 1 | サンプリング周期 | |
| `CH1 Gain` | 1 | `CH1 Gain` | |
| `CH2 Gain` | 1 | `CH2 Gain` | |
| `CH1_HysteresisHigh` | 4 | `CH1` ヒステリシス(`High`) | |
| `CH1_HysteresisLow` | 4 | `CH1` ヒステリシス(`Low`) | |
| `CH2_HysteresisHigh` | 4 | `CH2` ヒステリシス(`High`) | |
| `CH2_HysteresisLow` | 4 | `CH2` ヒステリシス(`Low`) | |

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

## 7-3 パラメータ情報取得要求

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

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

## 7-4 デバイス Config 移行要求

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

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

## 7-5 デバイス再起動要求

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

※エンディアンはリトルエンディアンになります。データ作成時がリトルエンディアンで作成して下さい。

# 8 電池駆動時の各設定における電池持ち

`BravePI` トランスミッター(`CR123A`) 使用時の代表的な設定におけるおおよその電池持ちを以下に示します。

**\<`Bluetooth` 通信モード: `Legacy` の場合\>**
| パラメータ設定情報 | | | | | 電池持ち |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **計測モード** | **サンプリング周期** | **`TxPower`** | **`Uplink Interval`** | **`Advertise Interval`** | **(日)** |
| 瞬時値モード | | `0dBm` | `1秒` | `100ms` | `72` |
| | | | `10秒` | `100ms` | `359` |
| | | | | `1000ms` | `593` |
| | | | `60秒` | `100ms` | `571` |
| | | | | `1000ms` | `1826` |
| 検知モード | `1Hz` | `0dBm` | `60秒` | `100ms` | `71` |
| サンプリングモード | | | | `1000ms` | `76` |
| | `2Hz` | `0dBm` | `60秒` | `100ms` | `37` |
| | | | | `1000ms` | `38` |

**\<`Bluetooth` 通信モード: `Long Range` の場合\>**
| パラメータ設定情報 | | | | | 電池持ち |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **計測モード** | **サンプリング周期** | **`TxPower`** | **`Uplink Interval`** | **`Advertise Interval`** | **(日)** |
| 瞬時値モード | | `0dBm` | `1秒` | `100ms` | `60` |
| | | | `10秒` | `100ms` | `132` |
| | | | | `1000ms` | `480` |
| | | | `60秒` | `100ms` | `181` |
| | | | | `1000ms` | `1020` |
| 検知モード | `1Hz` | `0dBm` | `60秒` | `100ms` | `53` |
| サンプリングモード | | | | `1000ms` | `67` |
| | `2Hz` | `0dBm` | `60秒` | `100ms` | `33` |
| | | | | `1000ms` | `36` |

# 9 製品到着から使用開始までの流れ

## 9-1 BravePI トランスミッターの設定

`BravePI` トランスミッター側の設定手順について以下に示します。

1.  トランスミッターからセンサーを外した状態にする。
2.  トランスミッターに電池又はUSB給電する。
3.  専用のiPhoneアプリを起動する。
4.  iPhone アプリから `ADC` センサー用の「`DFU`」を実行する。
5.  iPhone アプリから `ADC` センサー用の「パラメータ設定」を実行する。
6.  トランスミッターに`ADC` センサーを取り付ける。
7.  iPhone アプリからトランスミッターに電源ON(再起動)操作を行う。

次に `BravePI` トランスミッターと `BravePI` メインボードの紐付けを実行して下さい。

## 9-2 BravePI トランスミッターと BravePI メインボードの紐付け

`BravePI` トランスミッターと `BravePI` メインボードの紐付け手順について以下に示します。

1.  専用の iPhone アプリを起動する。
2.  iPhone アプリから「ペアリング設定」を実行する。

以上で設定は終了です。

# 10 商標について

・`Bluetooth`®とワードマークおよびロゴは、`Bluetooth SIG INC` が所有する登録商標です。
株式会社 `Braveridge` はこれら商標を使用する許可を受けています。その他のロゴマーク及び商号は各所有者に帰属します。

# 11 Revision 管理

| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023/11/29 | `Ver1.0.0` | 初版 |

※上記、製品仕様や機能、デザインは変更となる可能性がございます。あらかじめご了承ください。

-----

`Braveridge`とその製品に関する詳しい情報は、弊社Webサイトで御確認ください。
[https://www.braveridge.com/](https://www.braveridge.com/)

●株式会社Braveridge 本社
〒819-0373 福岡県福岡市西区周船寺3-27-2
(Tel): 092-834-5789 / (Fax): 092-807-7718

●株式会社Braveridge 糸島工場
〒819-1122 福岡県糸島市東1999-19
`Apple MFi Manufacture` ライセンス認定工場(ライトニングコネクタ製品工場)