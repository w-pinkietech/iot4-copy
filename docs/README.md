# IoT導入支援キット Ver.4.1 ドキュメント

## 概要

本ドキュメントは、Node-REDベースの現行IoTシステムから、Python/FastAPIベースの新システムへの移行プロジェクトに関する包括的なドキュメントセットです。

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

## ドキュメント再構築について

このプロジェクトでは、ドキュメントの整理と再構築を実施しています：

- **シンプルな構造**: 現行システムと新システムの2つに集約
- **関連情報の統合**: 運用、設計、リファレンス情報を各システム配下に整理
- **ナビゲーション改善**: 階層的な構造で情報アクセスを改善

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