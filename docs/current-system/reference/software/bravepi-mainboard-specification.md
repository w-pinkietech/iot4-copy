
***

**公式仕様書**: [BravePI メインボード BVPMB-01 公式仕様書 (PDF)](https://drive.google.com/file/d/1yfrWPkb5cJCD_FizM9DuRC5_uimsXSmu/view)

---

**Braveridge**
# ソフトウェア仕様書
## BravePI メインボード BVPMB-01
### REV 1.2
DESIGNED BY Braveridge Co., Ltd.

---

## 内容(目次)

*   **[1 製品概要](#1-製品概要)**
*   **[2 機能概要](#2-機能概要)**
    *   [2-1 BraveRoute 通信機能](#2-1-braveroute-通信機能)
    *   [2-2 NFC Tag 機能](#2-2-nfc-tag-機能)
    *   [2-3 パラメータ変更/取得機能](#2-3-パラメータ変更取得機能)
    *   [2-4 DFU 機能](#2-4-dfu-機能)
*   **[3 パラメータ情報](#3-パラメータ情報)**
*   **[4 Config モード時 Bluetooth 通信仕様](#4-config-モード時-bluetooth-通信仕様)**
    *   [4-1 基本情報](#4-1-基本情報)
    *   [4-2 Advertise/ScanResponse Packet](#4-2-advertisescanresponse-packet)
    *   [4-3 Service](#4-3-service)
        *   [4-3-1 BraveGATE Info Service](#4-3-1-bravegate-info-service)
        *   [4-3-2 Device Setting Service](#4-3-2-device-setting-service)
        *   [4-3-3 Device Info Service](#4-3-3-device-info-service)
*   **[5 コマンド仕様](#5-コマンド仕様)**
    *   [5-1 UART 通信機能](#5-1-uart-通信機能)
    *   [5-2 Uplink コマンド](#5-2-uplink-コマンド)
    *   [5-3 Downlink コマンド](#5-3-downlink-コマンド)
        *   [5-3-1 エンドデバイス コマンド](#5-3-1-エンドデバイス-コマンド)
        *   [5-3-2 設定 コマンド](#5-3-2-設定-コマンド)
*   **[6 製品到着から使用開始までの流れ](#6-製品到着から使用開始までの流れ)**
*   **[7 Revision 管理](#7-revision-管理)**

---

## 1 製品概要
本製品は、BravePI トランスミッターとラズベリーパイとの通信を UART にて中継します。

[画像: BravePI メインボードとBravePI トランスミッターがBluetoothで通信する図]

---

## 2 機能概要

### 2-1 BraveRoute 通信機能
ラズベリーパイに接続することにより UART を介して、BravePI トランスミッターからの Uplink を取得することができます。また、BravePI トランスミッターに UART を介して、Downlink を行うことができます。
コマンドの詳細は「[5 コマンド仕様](#5-コマンド仕様)」を参照ください。

### 2-2 NFC Tag 機能
本製品は NFCTag を有しており、専用スマホアプリ起動し、本製品にスマホを近づけることで以下の各種設定や情報取得することが出来ます。

| 項目 | 動作概要 |
| :--- | :--- |
| デバイス再起動要求 | 本製品を再起動します。 |
| Config モード移行要求 | 本製品を Config モードに移行します。 |
| Company ID 取得要求 | 本製品の Company ID を取得します。 |
| デバイス ID 紐づけ登録 | 本製品と紐づくデバイス ID を登録します。 |
| デバイス ID 紐づけ削除 | 本製品と紐づくデバイス ID を削除します。 |
| デバイス ID 紐づけ取得 | 本製品と紐づくデバイス ID を取得します。 |
| DFU モード移行要求 | 本製品を DFU モードに移行します。 |

### 2-3 パラメータ変更/取得機能
本製品のパラメータ情報は取得・変更することができます。
本製品の変更・取得可能なパラメータは以下の「[3 パラメータ情報](#3-パラメータ情報)」を参照ください。

本製品のパラメータの取得・変更方法は以下になります。
- 専用アプリの NFC 機能を使用
- Config モード時の BLE 機能を使用

### 2-4 DFU 機能
専用アプリを使用することで、本製品のFWを更新することができます。
本製品のFW の更新は、専用アプリ以外では行うことができません。

---

## 3 パラメータ情報
本製品のパラメータを以下に示します。

| パラメータ項目 | 設定情報 |
| :--- | :--- |
| Company ID | 本製品と通信を行うために必要な ID。<br>この ID が一致している BravePI トランスミッターと通信を行います。 |
| Filter Device ID | 本製品と通信を行うデバイスの Device ID。<br>16 個まで保存可能です。<br>登録された Device ID を持つ BravePI トランスミッターとのみ通信を行います。 |
| Bluetooth Mode | Bluetooth 通信モードの設定情報を以下に示します。<br>**設定値** \| **説明**<br>--- \| ---<br>`0x00` \| LongRange<br>`0x01` \| Legacy<br>上記以外 \| LongRange |

---

## 4 Config モード時 Bluetooth 通信仕様
Config モード時用の Bluetooth 通信プロファイル仕様を以下に示します。

### 4-1 基本情報
| 項目 | 値 |
| :--- | :--- |
| Advertising Interval | 100ms |
| Min Connection Interval | 50ms |
| Max Connection Interval | 70ms |
| Slave Latency | 0 |
| Supervision Timeout | 6000ms |

### 4-2 Advertise/ScanResponse Packet

**<Advertise データ>**

| Index | Data | Description | Comment |
| :--- | :--- | :--- | :--- |
| 0 | `0x02` | Length | |
| 1 | `0x01` | Advertising Field Type | FLAGS |
| 2 | `0x06` | Flag type | LE ONLY GENERAL DISCOVER MODE |
| 3 | `0x11` | Length | |
| 4 | `0x07` | Advertising Field Type | Complete List of 128-bit Service Class UUIDs |
| 5 - 20 | 右記 | Service UUID | 57791000-a129-4d7f-93a6-87f82b59f6a4 |
| 21 | `0x06` | Length | |
| 22 | `0x09` | Advertising Field Type | Complete Local Name |
| 23 - 29 | 右記 | Local Name | BPBConf |

**<ScanResponse データ>**
なし

### 4-3 Service
`5779xxxx-a129-4d7f-93a6-87f82b59f6a4`
以下の Service/Characteristic の UUID は上記 UUID の XXXX(Alias)の部分に各 Service/Characteristic の Alias を設定した値になります。

| Service Name | Alias | Characteristic Name |
| :--- | :--- | :--- |
| BraveGATE Info | `0x1100` | COMPANY_ID<br>CLEAR_FILTER<br>SET_FILTER<br>REQ_NOTIFY_FILTER<br>NOTIFY_FILTER<br>BV_CODE |
| Device Setting | `0x1200` | BLE_MODE |
| DeviceInfo | `0x1300` | DEVICE_ID<br>FW_VERSION<br>DFU_REQUEST<br>REGISTER |

#### 4-3-1 BraveGATE Info Service
| Characteristic Name | Property | Alias | Size | Description |
| :--- | :--- | :--- | :--- | :--- |
| COMPANY_ID | Write/Read | `0x1101` | 6 | Company ID を変更・取得を行います。 |
| CLEAR_FILTER | Write | `0x1102` | 1 | `0x2F` を送信することで、本製品と通信する全てのデバイスの Device ID 登録を消去します。 |
| SET_FILTER | Write | `0x1103` | 9 | インデックスを指定して、本製品と通信するデバイスの Device ID を登録します。 |
| REQ_NOTIFY_FILTER | Write | `0x1104` | 1 | 本製品と通信するデバイスの Device ID の Notify を要求します。 |
| NOTIFY_FILTER | Notify | `0x1105` | 9 | REQ_NOTIFY_FILTER キャラクタリスティックで指定されたインデックスの Device ID を Notify します。 |
| BV_CODE | Write | `0x1106` | 4 | `0x2B7A6150` を送信することで、BraveGATE Info Service の BV_CODE 以外のキャラクタリスティックへの Write 操作を許可します。このコードを Write されるまでは Write しても反映されません。 |

**<BraveGATE Info Service の詳細>**
-   **SET_FILTER**
    インデックスを指定して、本製品と通信するデバイスの Device ID を登録します。データの並びは以下になります。

| Index | Name | Description |
| :--- | :--- | :--- |
| 0 | インデックス | 0 から 15 まで指定可能。それ以外は無視されます。 |
| 1 - 9 | Device ID | 本製品と通信するデバイスの Device ID |

#### 4-3-2 Device Setting Service
| Characteristic Name | Property | Alias | Size | Data |
| :--- | :--- | :--- | :--- | :--- |
| BLE_MODE | Read/Write | `0x1201` | 1 | BLE Central としてふるまう際の Bluetooth 通信モードの設定を行います。<br>0 : Long Range<br>1 : Legacy<br>上記以外 : Long Range |

#### 4-3-3 Device Info Service
| Characteristic Name | Property | Alias | Size | Description |
| :--- | :--- | :--- | :--- | :--- |
| DEVICE_ID | Read | `0x1301` | 8 | Nordic のユニーク ID を取得します。 |
| FW_VERSION | Read | `0x1302` | 3 | 現在の FW のバージョンを取得します。 |
| DFU_REQUEST | Write | `0x1303` | 1 | `0xE8` を送信することで DFU モードへ遷移します。 |
| REGISTER | Write | `0x1304` | 3 | `0x9C8AD2` を送信することで、上記パラメータを更新します。 |

---

## 5 コマンド仕様

### 5-1 UART 通信機能
本製品は、UART 通信にて以下のコマンドの送受信が可能です。

**<UART 設定>**
| | Setting Value |
| :--- | :--- |
| Baud Rate | 38400bps |
| Data | 8bit |
| Parity | None |
| Stop | 1bit |
| Flow Control | None |

### 5-2 Uplink コマンド
| Index | Name | Size | Description |
| :--- | :--- | :--- | :--- |
| 0 | Data Length | 2byte | Data 部分のサイズ |
| 2 | Device ID | 8byte | Uplink されたデバイスの Device ID |
| 10 | Sensor ID | 2byte | Uplink されたデータの Sensor ID |
| 12 | RSSI | 1byte | BLE 通信時の RSSI |
| 13 | Flag | 1byte | 0 : 後続なし<br>1 : 後続あり |
| 14~ | Data | n byte | |

BravePI トランスミッターから Uplink されるデータの詳細については、各 BravePI トランスミッターのソフトウェア仕様書を参照下さい。

### 5-3 Downlink コマンド

#### 5-3-1 エンドデバイス コマンド
| Index | Name | Size | Description |
| :--- | :--- | :--- | :--- |
| 0 | Type | 1byte | `0x00` 固定 |
| 1 | Data Length | 2byte | Data 部分のサイズ |
| 3 | Device ID | 8byte | コマンドを送信するデバイスの Device ID |
| 11 | Sensor ID | 2byte | コマンドの対象の Sensor ID |
| 13 | CMD | 1byte | Downlink 要求コマンド |
| 14 | Flag | 1byte | 0 : 後続なし<br>1 : 後続あり |
| 15~ | Data | n byte | |

Downlink データの詳細については、各 BravePI トランスミッターのソフトウェア仕様書を参照下さい。

#### 5-3-2 設定 コマンド
| Index | Name | Size | Description |
| :--- | :--- | :--- | :--- |
| 0 | Type | 1byte | `0x01` 固定 |
| 1 | CMD | 1byte | 0 : BLE スキャン停止<br>1 : BLE スキャン開始 |
| 2 | Local Time | 4byte | 日本時間 (UTC + 9 時間) |
| 6 | UTC | 4byte | UTC |

---

## 6 製品到着から使用開始までの流れ
以下の手順で BravePI メインボードと BravePI トランスミッターとの紐づけを行うことができます。
1.  BravePI メインボードとラズベリーパイを接続します。
2.  専用の iPhone アプリを起動します。
3.  専用アプリから「ペアリング設定」を実行します。
4.  専用アプリから BravePI トランスミッターの NFC をスキャンするように指示がでますので、iPhone をトランスミッターに近づけます。
5.  専用アプリから BravePI メインボードの NFC をスキャンするように指示がでますので、iPhone をメインボードに近づけます。

以上で設定は終了です。

---

## 7 Revision 管理
| Rev | Date | Firmware | 変更内容 |
| :--- | :--- | :--- | :--- |
| 1.0 | 2023/10/10 | Ver1.0.0 | 初版 |
| 1.1 | 2024/2/1 | Ver1.0.0 | **5-2 Uplink コマンド**<br>-> Uplink データ参照先についての記述追記<br>**5-3-1 エンドデバイス コマンド**<br>-> 表中に不要な情報があったので削除<br>-> Downlink データ参照先についての記述追記 |
| 1.2 | 2024/3/5 | Ver1.0.0 | **5-1 UART 通信機能**<br>-> Baud Rate の Setting Value 値誤り修正 |

※上記、製品仕様や機能、デザインは変更となる可能性がございます。あらかじめご了承ください。

---
**Braveridge**

Braveridge とその製品に関する詳しい情報は、弊社 Web サイトで御確認ください。
[https://www.braveridge.com](https://www.braveridge.com)

*   製品故障の場合はこちらまでご連絡をお願い致します。
    E-mail: support@braveridge.com (故障受付窓口)

*   **株式会社ブレイブリッジ (本社)**
    〒819-0373 福岡県福岡市西区周船寺 3-27-2
    (Tel): 092-834-5789 / (Fax): 092-807-7718

*   **ブレイブリッジグループカンパニー**
    *   ブレイブリッジ糸島工場
        〒819-1122 福岡県糸島市東 1999-19