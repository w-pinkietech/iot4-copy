# 現行システム（Node-RED + BravePI/JIG）

## 概要

本ディレクトリには、現在運用中のNode-REDベースのIoTシステムに関するドキュメントを格納しています。

## システム概要

- **メインプラットフォーム**: Node-RED
- **ハードウェア**: Raspberry Pi 4 + BravePI + BraveJIG
- **データベース**: MariaDB + InfluxDB
- **センサー**: 7種類のI2Cセンサー + BLE/GPIO
- **通信**: MQTT + Serial + I2C

## ドキュメント構成

### アーキテクチャ
- [`architecture/overview.md`](architecture/overview.md) - システム全体アーキテクチャ
- [`architecture/bravepi-bravejig-integration.md`](architecture/bravepi-bravejig-integration.md) - BravePI/JIG統合詳細
- [`architecture/node-red-flows.md`](architecture/node-red-flows.md) - Node-REDフロー解析
- [`architecture/data-flow.md`](architecture/data-flow.md) - データフロー詳細

### 技術分析
- [`analysis/technical-analysis.md`](analysis/technical-analysis.md) - 技術的な詳細分析
- [`analysis/performance-analysis.md`](analysis/performance-analysis.md) - パフォーマンス分析
- [`analysis/challenges.md`](analysis/challenges.md) - 現システムの課題

### API仕様
- [`api/node-red-endpoints.md`](api/node-red-endpoints.md) - 既存API仕様

## 関連ファイル

### システム構成ファイル
- `/home/kenta/pinkie/iot4-copy/.node-red/` - Node-RED設定
- `/home/kenta/pinkie/iot4-copy/.node-red/python/` - センサードライバー
- `/home/kenta/pinkie/iot4-copy/docker/` - Docker構成

### データベース
- MariaDB: センサー設定、しきい値、較正データ
- InfluxDB: 時系列センサーデータ