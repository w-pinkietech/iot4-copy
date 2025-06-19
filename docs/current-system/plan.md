# 現行システムドキュメント リファクタリング計画

## 📋 概要

現在の606行のREADME.mdを、ユーザー目的別・学習段階別に分割し、使いやすいドキュメント構造に再編成する計画です。

## 🎯 現在の課題

### 構造上の問題
- **巨大すぎるREADME**: 606行で情報が混在
- **ナビゲーション困難**: 目的の情報へのアクセスが困難
- **学習レベル混在**: 初心者向けと上級者向け情報が混在
- **保守性の問題**: 大きなファイルでの変更管理が困難

### ユーザビリティの問題
- 初心者が概要を把握しにくい
- 技術者が詳細仕様を見つけにくい
- 運用者が運用情報にアクセスしにくい
- 検索性が低い

## 🏗️ 新しいディレクトリ構造

```
docs/current-system/
├── README.md                     # 🏠 簡潔な概要とナビゲーション（100行以内）
├── plan.md                       # 📋 このリファクタリング計画書
├── overview/                     # 📖 システム概要（初心者・導入検討者向け）
│   ├── system-summary.md         # エグゼクティブサマリー
│   ├── architecture-diagram.md   # アーキテクチャ図と基本説明
│   ├── features-benefits.md      # 機能と利点
│   └── quick-start.md            # クイックスタート手順
├── specifications/               # 📊 技術仕様（開発者・技術者向け）
│   ├── technical-specs.md        # 詳細技術仕様
│   ├── sensor-types.md          # 16種センサー詳細仕様
│   ├── communication-protocols.md # 通信プロトコル詳細
│   ├── performance-metrics.md    # 性能指標・ベンチマーク
│   └── database-schema.md       # データベース設計
├── implementation/               # ⚙️ 実装詳細（上級開発者向け）
│   ├── node-red-system.md       # Node-RED実装分析
│   ├── data-architecture.md     # データアーキテクチャ詳細
│   ├── industrial-algorithms.md # 産業制御アルゴリズム
│   └── binary-protocols.md      # バイナリ通信プロトコル
├── operations/                   # 🔧 運用ガイド（運用者向け）
│   ├── deployment-guide.md      # インストール・環境構築
│   ├── monitoring-guide.md      # システム監視・ログ管理
│   ├── maintenance-guide.md     # 保守・トラブルシューティング
│   └── backup-recovery.md       # バックアップ・復旧手順
├── analysis/                     # (既存) 技術分析
├── api/                         # (既存) API仕様
├── architecture/                # (既存) アーキテクチャ設計
└── reference/                   # (既存) リファレンス
```

## 👥 ユーザー別ナビゲーション設計

### 🎯 初めてのユーザー・導入検討者
```
README.md → overview/system-summary.md → overview/features-benefits.md → overview/quick-start.md
```
- **目的**: システムの価値と概要を理解
- **コンテンツ**: 非技術的な説明、ビジネス価値、導入効果

### 🔧 運用管理者・システム管理者
```
README.md → operations/deployment-guide.md → operations/monitoring-guide.md → specifications/performance-metrics.md
```
- **目的**: システムの導入と日常運用
- **コンテンツ**: インストール手順、運用手順、監視方法

### 👨‍💻 開発者・技術者
```
README.md → specifications/technical-specs.md → implementation/ → architecture/
```
- **目的**: システムの技術理解と拡張開発
- **コンテンツ**: 技術仕様、実装詳細、API仕様

### 🏭 システム統合者・上級技術者
```
README.md → specifications/ → implementation/ → analysis/ → reference/
```
- **目的**: 深い技術理解と他システムとの統合
- **コンテンツ**: 全技術詳細、分析結果、カスタマイズ情報

## 📝 コンテンツ移動計画

### Phase 1: 基本構造作成
- [ ] 新ディレクトリ作成
- [ ] 新README.md作成（簡潔版）
- [ ] overview/ディレクトリとコンテンツ作成

### Phase 2: 仕様・実装詳細分離
- [ ] specifications/ディレクトリ作成
- [ ] implementation/ディレクトリ作成
- [ ] 現README.mdから技術詳細を移動

### Phase 3: 運用ガイド作成
- [ ] operations/ディレクトリ作成
- [ ] 運用関連コンテンツの集約・整理

### Phase 4: 最終調整・検証
- [ ] 相互リンクの整備
- [ ] 重複コンテンツの削除
- [ ] ナビゲーション検証

## 📊 リファクタリング指標

### 目標指標
- **README.md**: 606行 → 100行以内
- **平均ファイルサイズ**: 150-200行
- **ナビゲーション深度**: 最大3クリックで目的情報にアクセス
- **重複率**: 現在の推定30% → 5%以下

### 品質指標
- **情報完全性**: 現在の情報量を維持
- **アクセス性**: ユーザータイプ別の明確な導線
- **保守性**: ファイル分割による更新効率化
- **検索性**: ファイル名・見出しによる直感的発見

## 🔗 既存ドキュメント連携

### 保持する既存構造
- `analysis/` - 技術分析（そのまま保持）
- `api/` - API仕様（そのまま保持）
- `architecture/` - 詳細アーキテクチャ（そのまま保持）
- `reference/` - リファレンス（そのまま保持）

### 新構造との関係
- 新overview/ → 既存architecture/system-overview.md
- 新specifications/ → 既存README.mdの技術仕様部分
- 新implementation/ → 既存analysis/の実装詳細
- 新operations/ → 既存README.mdの運用部分

## ✅ 進捗管理

### 完了基準
- [ ] 全ユーザータイプが3クリック以内で目的情報にアクセス可能
- [ ] README.mdが100行以内で概要と導線を提供
- [ ] 各ファイルが単一責任で150-200行程度
- [ ] 重複コンテンツが5%以下
- [ ] 既存情報の欠損なし

### 品質チェック
- [ ] ユーザーナビゲーションテスト
- [ ] 情報完全性チェック
- [ ] リンク切れチェック
- [ ] 日本語品質チェック

## 📅 実装スケジュール

1. **Phase 1** (1-2時間): 基本構造とoverview作成
2. **Phase 2** (2-3時間): 技術仕様・実装詳細分離
3. **Phase 3** (1-2時間): 運用ガイド作成
4. **Phase 4** (1時間): 最終調整・品質チェック

**総予想時間**: 5-8時間

## 🎯 期待される効果

### ユーザー体験向上
- 初心者: システム理解時間50%短縮
- 運用者: 運用情報アクセス時間70%短縮  
- 開発者: 技術詳細発見時間60%短縮

### 保守性向上
- ドキュメント更新時間50%短縮
- 情報の整合性向上
- 新規コントリビューター参入障壁低下

---

**作成日**: 2025年6月19日  
**更新予定**: リファクタリング進捗に応じて随時更新