# ドキュメント再構築計画

## 現状の課題

- 13個のMarkdownファイル、総計6317行
- アーキテクチャドキュメントが散在
- 現状分析と新設計が混在
- 読み手（開発者/運用者/利害関係者）別の整理が不十分

## 新しいディレクトリ構造

```
docs/
├── README.md                           # ドキュメント全体のインデックス
├── current-system/                     # 現行システム（Node-RED）
│   ├── README.md                      # 現行システム概要
│   ├── architecture/
│   │   ├── overview.md                # システム全体概要
│   │   ├── bravepi-bravejig-integration.md  # BravePI/JIG統合
│   │   ├── node-red-flows.md          # Node-REDフロー解析
│   │   └── data-flow.md               # データフロー詳細
│   ├── analysis/
│   │   ├── technical-analysis.md      # 技術分析
│   │   ├── performance-analysis.md    # パフォーマンス分析
│   │   └── challenges.md              # 課題分析
│   └── api/
│       └── node-red-endpoints.md      # 既存API仕様
│
├── new-system/                         # 新システム（Python/FastAPI）
│   ├── README.md                      # 新システム概要
│   ├── architecture/
│   │   ├── overview.md                # 新アーキテクチャ概要
│   │   ├── edge-gateway.md            # エッジゲートウェイ層
│   │   ├── collection-layer.md        # データ収集層
│   │   ├── application-layer.md       # アプリケーション層
│   │   └── sensor-drivers.md          # センサードライバー
│   ├── implementation/
│   │   ├── database-design.md         # SQLite実装詳細
│   │   ├── mqtt-protocol.md           # MQTT仕様
│   │   ├── bravepi-integration.md     # BravePI統合設計
│   │   └── security.md                # セキュリティ設計
│   └── api/
│       ├── rest-api.md                # REST API仕様
│       └── message-formats.md         # メッセージフォーマット
│
├── migration/                          # 移行計画
│   ├── README.md                      # 移行概要
│   ├── strategy/
│   │   ├── overview.md                # 移行戦略
│   │   ├── phase-planning.md          # フェーズ計画
│   │   ├── risk-assessment.md         # リスク評価
│   │   └── rollback-plan.md           # ロールバック計画
│   ├── procedures/
│   │   ├── data-migration.md          # データ移行手順
│   │   ├── testing-procedures.md      # テスト手順
│   │   └── deployment.md              # デプロイメント手順
│   └── validation/
│       ├── compatibility-testing.md   # 互換性テスト
│       └── performance-validation.md  # 性能検証
│
├── operations/                         # 運用ドキュメント
│   ├── README.md                      # 運用概要
│   ├── installation/
│   │   ├── requirements.md            # システム要件
│   │   ├── edge-gateway-setup.md      # エッジゲートウェイ構築
│   │   └── server-setup.md            # サーバー構築
│   ├── maintenance/
│   │   ├── monitoring.md              # 監視方法
│   │   ├── backup-restore.md          # バックアップ・リストア
│   │   ├── troubleshooting.md         # トラブルシューティング
│   │   └── firmware-updates.md        # ファームウェア更新
│   └── security/
│       ├── access-control.md          # アクセス制御
│       └── security-procedures.md     # セキュリティ手順
│
├── design/                             # 設計プロセス
│   ├── README.md                      # 設計プロセス概要
│   ├── reviews/
│   │   ├── design-review-checklist.md # 設計レビューチェックリスト
│   │   ├── review-2024-01.md          # レビュー記録
│   │   └── decisions.md               # 設計決定記録
│   ├── research/
│   │   ├── technology-evaluation.md   # 技術評価
│   │   └── alternatives-analysis.md   # 代替案分析
│   └── prototypes/
│       └── proof-of-concept.md        # PoC結果
│
├── reference/                          # リファレンス
│   ├── README.md                      # リファレンス概要
│   ├── hardware/
│   │   ├── bravepi-specs.md           # BravePI仕様
│   │   ├── bravejig-specs.md          # BraveJIG仕様
│   │   └── sensor-catalog.md          # センサーカタログ
│   ├── software/
│   │   ├── dependencies.md            # 依存関係一覧
│   │   └── configuration-reference.md # 設定リファレンス
│   └── glossary.md                    # 用語集
│
└── assets/                             # 共通アセット
    ├── diagrams/                       # 図表
    ├── images/                         # 画像
    ├── templates/                      # テンプレート
    └── styleguide.md                   # スタイルガイド
```

## 移行手順

### Phase 1: ディレクトリ構造作成
1. 新しいディレクトリ構造を作成
2. 各ディレクトリにREADME.mdを配置
3. ドキュメント間のナビゲーション整備

### Phase 2: 既存ドキュメントの分類・移動
1. 現行システム関連の移動
2. 新システム設計の整理
3. 移行計画の独立化

### Phase 3: 新規ドキュメント作成
1. BravePI/JIG統合の詳細化
2. 現行システムの完全な技術分析
3. 運用ドキュメントの充実

### Phase 4: 品質向上
1. ドキュメント間のリンク整備
2. 図表の統一
3. スタイルガイドの適用

## 利点

1. **目的別整理**: 現状分析、新設計、移行、運用が明確に分離
2. **読み手別対応**: 開発者、運用者、マネージャー向けに最適化
3. **メンテナンス性**: 各ドキュメントの責務が明確
4. **拡張性**: 新しいトピックの追加が容易
5. **ナビゲーション**: 階層的な構造で情報へのアクセスが改善