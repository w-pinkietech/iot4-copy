# BravePI ソフトウェア仕様書

このディレクトリには、BravePI システムのソフトウェア仕様書が含まれています。

## 概要

BravePI システムは、メインボードとトランスミッターから構成されるIoTプラットフォームです。トランスミッターは様々なセンサーボードを接続し、Bluetooth通信でメインボードにデータを送信します。

## ドキュメント一覧

### BravePI メインボード
- [BravePI メインボード ソフトウェア仕様書](bravepi-mainboard-specification.md)

### BravePI トランスミッター センサー別仕様書

1. **[加速度センサー版](bravepi-transmitter-accelerometer-specification.md)**
   - 3軸加速度センサーによる振動・傾き検知
   - ADXL362センサー搭載

2. **[ADCセンサー版](bravepi-transmitter-adc-specification.md)**
   - アナログ信号のデジタル変換
   - MCP3427センサー搭載
   - 2チャンネル対応

3. **[接点入力センサー版](bravepi-transmitter-contact-input-specification.md)**
   - ドライ/ウェット接点入力対応
   - 接点状態の変化検知

4. **[接点出力センサー版](bravepi-transmitter-contact-output-specification.md)**
   - 外部機器への接点出力制御
   - 出力時間制御機能

5. **[差圧センサー版](bravepi-transmitter-differential-pressure-specification.md)**
   - 差圧測定機能
   - SDP810-500Paセンサー搭載

6. **[測距センサー版](bravepi-transmitter-distance-sensor-specification.md)**
   - レーザー測距機能
   - VL53L1センサー搭載
   - 測定範囲: 40～1300mm

7. **[照度センサー版](bravepi-transmitter-illuminance-specification.md)**
   - 環境光測定機能
   - RPR-0521RSセンサー搭載

8. **[熱電対センサー版](bravepi-transmitter-thermocouple-specification.md)**
   - 温度測定機能
   - MCP9600センサー搭載
   - 測定範囲: -300～2000℃

## 共通機能

すべてのトランスミッターには以下の共通機能があります：

- **Bluetooth通信機能**: Long Range/Legacy対応
- **NFCTag機能**: 設定・情報取得
- **LED表示機能**: 動作状態表示
- **バッテリー駆動**: CR123A電池またはUSB給電
- **DFU機能**: ファームウェアアップデート

## 関連リンク

- [ハードウェア仕様書](../hardware/)
- [BravePI 公式サイト](https://www.braveridge.com/)