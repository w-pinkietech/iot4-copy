# IoT導入支援キット Ver.4.1 ドキュメント

## 概要

IoT導入支援キット Ver.4.1は、福岡県工業技術センター（FITC）が開発した産業用IoTデータ収集・可視化システムです。本ドキュメントは、Node-REDベースの現行IoTシステムから、Python/FastAPIベースの新システムへの移行プロジェクトに関する包括的なドキュメントセットです。

### システムの特徴
- **Raspberry Pi 4上で動作**: 省電力・低コストな産業用IoTプラットフォーム
- **13種類の産業用センサーサポート**: 多様な通信プロトコル（I2C、GPIO、シリアル、BLE、HTTP、MQTT）に対応
- **リアルタイム可視化**: Node-REDダッシュボードによる直感的なデータ表示
- **時系列データ管理**: InfluxDBによる効率的なセンサーデータ保存（90日間保持）
- **REST API提供**: 外部システムとの連携が容易

## ドキュメント構造

### 🔧 [現行システム](current-system/)
Node-RED + BravePI/JIG + MariaDB/InfluxDBで構成される現在のシステム

- **[アーキテクチャ](current-system/architecture/)**: システム全体設計、BravePI/JIG統合詳細
- **[技術分析](current-system/analysis/)**: 性能分析、課題分析
- **[API仕様](current-system/api/)**: 既存エンドポイント仕様
- **[リファレンス](current-system/reference/)**: ハードウェア/ソフトウェア仕様

### 🚀 [新システム](new-system/)
Python/FastAPI + Streamlit + Grafanaで構成される新しいシステム

- **[アーキテクチャ](new-system/architecture/)**: 3層分散アーキテクチャ設計
- **[実装詳細](new-system/implementation/)**: SQLite設計、MQTT仕様、セキュリティ
- **[API仕様](new-system/api/)**: REST API、メッセージフォーマット
- **[運用](new-system/operations/)**: インストール、保守、セキュリティ
- **[設計プロセス](new-system/design/)**: 設計レビュー、研究、プロトタイプ
- **[リファレンス](new-system/reference/)**: ハードウェア/ソフトウェア仕様

## クイックスタート

### 現行システムを理解したい方
1. [現行システム概要](current-system/README.md)
2. [BravePI/JIG統合アーキテクチャ](current-system/architecture/bravepi-bravejig-integration.md)
3. [技術分析](current-system/analysis/technical-analysis.md)

### 新システム設計を確認したい方
1. [新システム概要](new-system/README.md)
2. [アーキテクチャ概要](new-system/architecture/overview.md)
3. [センサードライバー設計](new-system/architecture/sensor-drivers.md)

### 新システムへの移行を検討したい方
1. [設計レビューチェックリスト](new-system/design/design-review-checklist.md)
2. [疎結合設計の研究](new-system/design/loose-coupling-research.md)

### システムを構築・運用したい方
1. [インストール手順](new-system/operations/installation-procedures.md)
2. [運用ガイド](new-system/operations/README.md)

## 開発・運用ガイド

### 実行環境
- **Node.js**: v20.19.1
- **Python**: 3.11.2
- **npm**: 10.8.2
- **OS**: Raspbian OS (Debian 11 Bullseye)
- **ハードウェア**: Raspberry Pi 4B (4GB RAM推奨)

### システムの起動と管理
```bash
# 初期設定（Raspberry Pi）
./desktop/first.sh

# サービスの起動
cd docker && docker-compose up -d

# サービスの停止
cd docker && docker-compose down

# サービス状態確認
docker-compose ps

# ログの確認
docker-compose logs mariadb
docker-compose logs influxdb
```

### 開発用コマンド
```bash
# Node-REDをセーフモードで実行
node-red --safe --userDir ./.node-red-dev

# I2Cデバイスの確認
sudo i2cdetect -y 1

# MQTTメッセージの監視
mosquitto_sub -h localhost -t "#" -v

# Node-REDログの表示
sudo journalctl -u node-red -f
```

### システムアクセスポイント
- **Node-REDエディター**: http://localhost:1880
- **ダッシュボード**: http://localhost:1880/ui
- **API**: http://localhost:1880/api/v2

### データベース接続情報
#### MariaDB（設定・メタデータ）
- ホスト: 127.0.0.1:3306
- データベース: iotkit
- ユーザー: iotkit
- パスワード: iotkit-password

#### InfluxDB（時系列データ）
- ホスト: 127.0.0.1:8086
- 組織: fitc
- バケット: iotkit
- トークン: influxdb-iotkit-secret-token
- 保持期間: 90日

### サポートセンサー（13種類）
- デジタルI/O（接点入出力）
- アナログセンサー（ADC、電圧/電流）
- 環境センサー（温度、湿度、気圧、照度）
- 物理センサー（距離、加速度、差圧）
- 高温センサー（熱電対）
- カスタムセンサー用拡張スロット

### 通信プロトコル
- **I2C**: 主要なセンサー通信バス
- **GPIO**: デジタル入出力
- **シリアル/UART**: /dev/ttyAMA0、/dev/ttyACM0-9（38400ボー）
- **BLE**: Bluetooth Low Energyセンサーサポート
- **HTTP/MQTT**: ネットワークベースのセンサー通信

## プロジェクト状況

### 完了済み ✅
- 現行システムの技術分析
- 新システムアーキテクチャ設計
- センサードライバー設計
- SQLite実装設計
- 設計レビューチェックリスト作成
- BravePI/JIG統合アーキテクチャ分析

### 進行中 🔄
- ドキュメント体系の再構築
- 複雑処理（FFT解析等）の実装方法検討

### 今後の予定 📅
- 実装フェーズの開始
- パイロット運用
- 段階的移行の実行

## Node-REDフロー構成

現行システムは9つのメインフロータブで構成されています：

1. **PI・JIG・I2C・GPIO**: ハードウェアインターフェース制御
2. **ダッシュボード**: リアルタイム可視化ダッシュボード
3. **デバイス登録**: デバイスライフサイクル管理
4. **センサーログ**: 時系列データ管理
5. **BLEトランスミッター**: Bluetooth Low Energy管理
6. **ルーター**: ネットワークルーティング
7. **モジュール**: 拡張モジュール
8. **設定**: システム設定
9. **その他**: ユーティリティ機能

## APIエンドポイント

### デバイス管理
```
GET    /api/v2/device              # 全デバイスの取得
GET    /api/v2/device/:deviceId    # 特定デバイスの取得
POST   /api/v2/device              # 新規デバイスの登録
DELETE /api/v2/device/:deviceId    # デバイスの削除
```

### センサーデータ
```
GET    /api/v2/device/:deviceId/sensor/value  # センサー値の取得
POST   /api/v2/device/:deviceId/sensor/value  # センサーデータの送信
```

## ドキュメント再構築について

このプロジェクトでは、ドキュメントの整理と再構築を実施しています：

- **シンプルな構造**: 現行システムと新システムの2つに集約
- **関連情報の統合**: 運用、設計、リファレンス情報を各システム配下に整理
- **ナビゲーション改善**: 階層的な構造で情報アクセスを改善

## 開発上の注意事項

1. **Node-REDフローは日本語名を使用**: 明確性のため日本語での命名を推奨
2. **コミットメッセージ規約**: feat、fix、docs、style、refactor、test、choreを使用
3. **ローカルネットワーク展開**: セキュリティ上、インターネット公開は想定していません
4. **手動テスト中心**: 自動テストインフラは整備中

## 貢献

このドキュメントの改善提案や追加情報があれば、以下の方法で貢献できます：

1. **Issue作成**: 不明点や改善提案をGitHub Issueで報告
2. **Pull Request**: ドキュメントの修正・追加
3. **レビュー参加**: 設計レビューへの参加

## ライセンス

Copyright (c) 2023 Fukuoka Industrial Technology Center

Licensed under the Apache License, Version 2.0

## 連絡先

プロジェクトに関する質問は、GitHubのIssueまたはディスカッションをご利用ください。