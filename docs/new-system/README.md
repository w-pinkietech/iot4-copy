# 新システム（Python/FastAPI）

## 概要

本ディレクトリには、新しく設計されたPython/FastAPIベースのIoTシステムに関するドキュメントを格納しています。

## システム概要

- **メインプラットフォーム**: Python + FastAPI + Streamlit
- **ハードウェア**: 既存のBravePI/JIGを継続利用
- **データベース**: SQLite (エッジ) + InfluxDB (時系列)
- **通信**: MQTT + REST API
- **アーキテクチャ**: 3層分散構成（Edge/Collection/Application）

## ドキュメント構成

### 要件定義
- [`requirements/requirements-definition.md`](requirements/requirements-definition.md) - システム要件定義書

### アーキテクチャ
- [`architecture/overview.md`](architecture/overview.md) - 新システム全体アーキテクチャ
- [`architecture/data-transformation-architecture.md`](architecture/data-transformation-architecture.md) - データ変換アーキテクチャ
- [`architecture/system-overview-diagrams.md`](architecture/system-overview-diagrams.md) - システム概要図解
- [`architecture/plugin-design.md`](architecture/plugin-design.md) - プラグイン設計アーキテクチャ
- [`architecture/sensor-drivers.md`](architecture/sensor-drivers.md) - センサードライバー設計

### 実装ガイド
- [`implementation/python-gateway-guide.md`](implementation/python-gateway-guide.md) - Python Gateway実装ガイド
- [`implementation/database-design.md`](implementation/database-design.md) - データベース設計
- [`implementation/bravepi-plugin-implementation.md`](implementation/bravepi-plugin-implementation.md) - BravePI プラグイン実装

### 運用・設計・リファレンス
- [`operations/`](operations/) - インストール・運用手順
- [`design/`](design/) - 設計プロセスとレビュー
- [`reference/`](reference/) - 技術リファレンス

## 現行システムとの違い

| 項目 | 現行システム | 新システム |
|------|-------------|------------|
| メインプラットフォーム | Node-RED | Python/FastAPI |
| エッジDB | MariaDB | SQLite |
| UI | Node-RED Dashboard | Streamlit |
| 設定管理 | GUI中心 | コード中心 |
| 保守性 | ビジュアル | テキスト・AI支援 |