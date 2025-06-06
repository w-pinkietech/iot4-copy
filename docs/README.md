# IoT導入支援キット Ver.4.1 ドキュメント

## 概要

本ドキュメントは、Node-REDベースの現行IoTシステムから、Python/FastAPIベースの新システムへの移行プロジェクトに関する包括的なドキュメントセットです。

## ドキュメント構造

### 🔧 [現行システム](current-system/)
Node-RED + BravePI/JIG + MariaDB/InfluxDBで構成される現在のシステム

- **[アーキテクチャ](current-system/architecture/)**: システム全体設計、BravePI/JIG統合詳細
- **[技術分析](current-system/analysis/)**: 性能分析、課題分析
- **[API仕様](current-system/api/)**: 既存エンドポイント仕様

### 🚀 [新システム](new-system/)
Python/FastAPI + Streamlit + Grafanaで構成される新しいシステム

- **[アーキテクチャ](new-system/architecture/)**: 3層分散アーキテクチャ設計
- **[実装詳細](new-system/implementation/)**: SQLite設計、MQTT仕様、セキュリティ
- **[API仕様](new-system/api/)**: REST API、メッセージフォーマット

### 🔄 [移行計画](migration/)
現行システムから新システムへの移行戦略

- **[戦略](migration/strategy/)**: 移行方針、フェーズ計画、リスク評価
- **[手順](migration/procedures/)**: データ移行、テスト、デプロイメント
- **[検証](migration/validation/)**: 互換性テスト、性能検証

### ⚙️ [運用](operations/)
システムの構築、運用、保守に関するドキュメント

- **[インストール](operations/installation/)**: システム要件、構築手順
- **[保守](operations/maintenance/)**: 監視、バックアップ、トラブルシューティング
- **[セキュリティ](operations/security/)**: アクセス制御、セキュリティ手順

### 📋 [設計プロセス](design/)
設計検討プロセスと意思決定の記録

- **[レビュー](design/reviews/)**: 設計レビューチェックリスト、決定記録
- **[研究](design/research/)**: 技術評価、代替案分析
- **[プロトタイプ](design/prototypes/)**: PoC結果

### 📚 [リファレンス](reference/)
技術仕様、用語集などの参考資料

- **[ハードウェア](reference/hardware/)**: BravePI/JIG仕様、センサーカタログ
- **[ソフトウェア](reference/software/)**: 依存関係、設定リファレンス
- **[用語集](reference/glossary.md)**: 専門用語の定義

## クイックスタート

### 現行システムを理解したい方
1. [現行システム概要](current-system/README.md)
2. [BravePI/JIG統合アーキテクチャ](current-system/architecture/bravepi-bravejig-integration.md)
3. [技術分析](current-system/analysis/technical-analysis.md)

### 新システム設計を確認したい方
1. [新システム概要](new-system/README.md)
2. [アーキテクチャ概要](new-system/architecture/overview.md)
3. [センサードライバー設計](new-system/architecture/sensor-drivers.md)

### 移行を計画・実行したい方
1. [移行戦略](migration/strategy/overview.md)
2. [移行手順](migration/procedures/data-migration.md)
3. [設計レビューチェックリスト](design/reviews/design-review-checklist.md)

### システムを構築・運用したい方
1. [システム要件](operations/installation/requirements.md)
2. [構築手順](operations/installation/edge-gateway-setup.md)
3. [運用ガイド](operations/maintenance/monitoring.md)

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
- 移行戦略の策定
- 複雑処理（FFT解析等）の移行方法検討

### 今後の予定 📅
- 実装フェーズの開始
- パイロット運用
- 段階的移行の実行

## ドキュメント再構築について

このプロジェクトでは、ドキュメントの整理と再構築を実施しています：

- **目的別整理**: 現状分析、新設計、移行、運用を明確に分離
- **読み手別対応**: 開発者、運用者、マネージャー向けに最適化
- **ナビゲーション改善**: 階層的な構造で情報アクセスを改善

詳細は[再構築計画](REORGANIZATION_PLAN.md)をご覧ください。

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