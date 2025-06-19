# IoT導入支援キット Ver.4.1 - 現行システム

## 🏠 システム概要

**IoT導入支援キット Ver.4.1** は、Raspberry Pi + Node-REDベースの産業用IoTセンサー監視・制御プラットフォームです。福岡県工業技術センター提供システムとして、16種類のセンサータイプ、複数通信プロトコル、リアルタイムデータ処理を統合提供します。

### ⚡ 主要特徴
- **1017個のNode-REDノード**による高度な制御システム
- **16種類のセンサータイプ**対応（基本8種 + JIG拡張5種 + その他3種）
- **5層通信プロトコル**（I2C/GPIO/UART/BLE/HTTP/MQTT）
- **デュアルデータベース**設計（MariaDB + InfluxDB）
- **リアルタイム処理**（<100ms応答、最大10Hz取得）

### 🎯 対象ユーザー
- **初心者・導入検討者**: システムの価値と概要理解
- **運用管理者**: システム導入と日常運用
- **開発者・技術者**: 技術理解と拡張開発
- **システム統合者**: 深い技術理解と他システム統合

## 📚 ドキュメント構成

```
docs/current-system/
├── 📋 plan.md                    # ドキュメント構造化計画
├── 📖 overview/                  # システム概要（初心者向け）
├── 📊 specifications/            # 技術仕様（開発者向け）
├── ⚙️ implementation/            # 実装詳細（上級者向け）
├── 🔧 operations/               # 運用ガイド（運用者向け）
├── 🔬 analysis/                 # 技術分析（既存）
├── 🌐 api/                      # API仕様（既存）
├── 🏗️ architecture/             # アーキテクチャ設計（既存）
└── 📚 reference/                # リファレンス（既存）
```

## 🎪 ユーザー別クイックスタート

### 👶 **初めてのユーザー・導入検討者**
1. [📋 システム概要](overview/system-summary.md) - システムの価値と全体像
2. [🎯 機能と利点](overview/features-benefits.md) - ビジネス価値
3. [🚀 クイックスタート](overview/quick-start.md) - 基本的な使い方

### 🔧 **運用管理者・システム管理者**  
1. [📦 インストールガイド](operations/deployment-guide.md) - 環境構築手順
2. [📊 監視ガイド](operations/monitoring-guide.md) - システム監視方法
3. [🛠️ 保守ガイド](operations/maintenance-guide.md) - 日常保守

### 👨‍💻 **開発者・技術者**
1. [📖 技術仕様](specifications/technical-specs.md) - システム技術仕様
2. [🔌 センサー仕様](specifications/sensor-types.md) - 16種センサー詳細
3. [🌐 REST API](../api/rest-api.md) - API仕様

### 🏭 **システム統合者・上級技術者**
1. [⚙️ Node-RED実装](implementation/node-red-system.md) - 内部実装詳細
2. [🏗️ データアーキテクチャ](implementation/data-architecture.md) - DB設計
3. [🔬 技術分析](analysis/technical-analysis.md) - 包括的分析

## ⚡ クイックアクセス

### 基本情報
- **Node-REDエディター**: http://localhost:1880
- **ダッシュボード**: http://localhost:1880/ui  
- **REST API**: http://localhost:1880/api/v2

### データベース接続
- **MariaDB**: 127.0.0.1:3306 (iotkit/iotkit-password)
- **InfluxDB**: 127.0.0.1:8086 (fitc/iotkit)

### 基本コマンド
```bash
# システム起動
cd docker && docker-compose up -d

# システム停止  
cd docker && docker-compose down

# I2Cデバイス確認
sudo i2cdetect -y 1

# MQTTメッセージ監視
mosquitto_sub -h localhost -t "#" -v
```

## 📊 システム性能指標

| 項目 | 仕様 | 用途 |
|------|------|------|
| **センサー対応** | 16種類 | 産業用途全般 |
| **データレート** | 1-10Hz | リアルタイム監視 |
| **応答時間** | <100ms | ダッシュボード更新 |
| **同時接続** | 最大100センサー | 大規模システム |
| **データ保持** | 90日間 | InfluxDB自動管理 |

## 🔄 新システムへの移行

現行システムから**Python/FastAPI**ベースの新システムへの移行が計画されています：

- [新システム概要](../new-system/README.md)
- [移行戦略](../new-system/architecture/system-overview-diagrams.md)
- [設計レビュー](../new-system/design/design-review-checklist.md)

---

## 📋 文書メタデータ

**最終更新**: 2025年6月19日  
**システムバージョン**: Ver.4.1.0-Raspi4  
**文書構造**: リファクタリング済み（[plan.md](plan.md)参照）  
**問い合わせ**: GitHub Issues