# 移行前分析手順書

## 概要

Node-REDベースのIoTシステムを別のアーキテクチャに移行する前に実施すべき包括的な分析手順を説明します。

## 事前分析チェックリスト

### 1. システム構成分析

#### 1.1 Node-REDフロー分析
```bash
# flows.json の構造分析
jq '.[] | select(.type=="tab") | {id: .id, label: .label}' flows.json > tabs_analysis.json

# 使用ノード統計
jq '[.[] | select(.type != "tab" and .type != "subflow") | .type] | group_by(.) | map({type: .[0], count: length})' flows.json > node_statistics.json

# カスタム関数の抽出
jq '.[] | select(.type=="function") | {id: .id, name: .name, func: .func}' flows.json > custom_functions.json
```

#### 1.2 依存関係マッピング
```bash
# Node-REDモジュール依存関係
jq '.dependencies' package.json > nodered_dependencies.json

# Pythonライブラリ依存関係
find python -name "*.py" -exec grep -H "import\|from" {} \; > python_dependencies.txt

# システムライブラリ使用状況
grep -r "subprocess\|os\|sys" python/ > system_dependencies.txt
```

### 2. データフロー分析

#### 2.1 データ処理パターン
- Function ノードの処理ロジック
- Change ノードの変換ルール
- Switch ノードの条件分岐
- Join/Split ノードのデータ集約

#### 2.2 外部連携分析
- HTTP API エンドポイント
- MQTT トピック構造
- データベース接続設定
- メール通知設定

### 3. パフォーマンス測定

#### 3.1 ベンチマーク測定
```bash
# CPU/メモリ使用量測定
top -p $(pgrep node-red) -n 100 > performance_baseline.txt

# ネットワーク利用状況
netstat -i > network_baseline.txt

# ディスク使用量
du -sh /path/to/node-red > disk_usage.txt
```

#### 3.2 レスポンス時間測定
```bash
# API レスポンス時間
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:1880/api/v2/device"

# ダッシュボード表示時間
lighthouse http://localhost:1880/ui/ --output=json > dashboard_performance.json
```

### 4. セキュリティ監査

#### 4.1 脆弱性スキャン
- 使用ライブラリの脆弱性チェック
- ネットワークポート開放状況
- 認証・認可機能の確認

#### 4.2 データ保護状況
- 機密データの取り扱い
- 通信暗号化状況
- アクセスログ記録状況

## 分析結果の文書化

### 分析レポートテンプレート
[analysis-report-template.md](../assets/templates/analysis-report-template.md)を参照

### 移行要件定義
分析結果をもとに移行要件を定義し、[移行計画書](./step-by-step-guide.md)に反映する。

## 関連資料
- [システムアーキテクチャ概要](../architecture/overview.md)
- [Node-REDフロー技術仕様](../technical/node-red-flows.md)
- [移行リスク評価](./risk-management.md)