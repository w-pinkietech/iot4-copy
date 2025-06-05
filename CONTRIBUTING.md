# 貢献ガイド

## 概要

IoT導入支援キット Ver.4.1への貢献を歓迎します。このガイドでは、効果的な貢献のための手順とガイドラインを説明します。

## 貢献の種類

### 🐛 バグ報告
- [Issue](../../issues/new?template=bug_report.md)を作成
- 再現手順・環境情報を詳細に記載
- ログ・スクリーンショットを添付

### 💡 機能要求
- [Feature Request](../../issues/new?template=feature_request.md)を作成
- 使用ケース・期待する動作を具体的に説明
- 実装の優先度・影響範囲を明記

### 📝 ドキュメント改善
- 誤字・脱字の修正
- 説明の追加・改善
- 新しいガイドの作成
- 翻訳・多言語対応

### 🔧 コード貢献
- バグ修正
- 新機能実装
- パフォーマンス改善
- テストコード追加

## 開発環境セットアップ

### 前提条件
- Raspberry Pi 4 Model B (推奨)
- Docker & Docker Compose
- Node.js 16.x以降
- Git

### セットアップ手順
```bash
# 1. リポジトリフォーク & クローン
git clone https://github.com/your-username/iot4-copy.git
cd iot4-copy

# 2. 開発環境構築
./desktop/first.sh

# 3. 開発用サービス起動
cd docker && docker-compose -f docker-compose.dev.yml up -d

# 4. Node-RED開発モード起動
node-red --safe --userDir ./.node-red-dev
```

## 開発ワークフロー

### 1. Issue作成・確認
- 作業前に関連Issueが存在するか確認
- 新機能の場合は事前にIssueで議論
- 作業内容・スコープを明確化

### 2. ブランチ作成
```bash
# mainブランチから作業ブランチ作成
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# または
git checkout -b fix/issue-number
git checkout -b docs/update-readme
```

### ブランチ命名規則
- `feature/機能名` - 新機能追加
- `fix/修正内容` - バグ修正
- `docs/ドキュメント名` - ドキュメント変更
- `refactor/対象` - リファクタリング
- `test/テスト内容` - テスト追加

### 3. 開発・テスト
```bash
# コード変更後のテスト実行
npm test

# リンターチェック
npm run lint

# ドキュメント生成
npm run docs

# 手動テスト
# http://localhost:1880 でNode-RED確認
# http://localhost:1880/ui でダッシュボード確認
```

### 4. コミット
```bash
# ステージング
git add .

# コミット（Conventional Commitsに従う）
git commit -m "feat: add temperature sensor support"
git commit -m "fix: resolve sensor connection timeout"
git commit -m "docs: update installation guide"
```

### コミットメッセージ規則
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Type:**
- `feat` - 新機能
- `fix` - バグ修正
- `docs` - ドキュメント
- `style` - フォーマット変更
- `refactor` - リファクタリング
- `test` - テスト追加
- `chore` - その他

**例:**
```
feat(sensors): add BLE device discovery

- Implement BLE scanning functionality
- Add device pairing interface
- Update dashboard with BLE status

Closes #123
```

### 5. プルリクエスト作成
- [PR template](../../compare)を使用
- 変更内容を明確に説明
- 関連Issueを参照
- スクリーンショット・デモ動画を添付（UI変更の場合）

## コーディング規約

### Node-RED フロー
- フロー名は日本語で分かりやすく記載
- ノードのコメントを適切に記載
- サブフローを活用して再利用性を高める
- エラーハンドリングを適切に実装

### Python (センサードライバー)
```python
# PEP 8に従う
import os
import sys
from typing import Optional, Dict, Any

class TemperatureSensor:
    """温度センサークラス
    
    Args:
        address: I2Cアドレス
        bus: I2Cバス番号
    """
    
    def __init__(self, address: int, bus: int = 1):
        self.address = address
        self.bus = bus
    
    def read_temperature(self) -> Optional[float]:
        """温度を読み取り
        
        Returns:
            温度値（摂氏）、エラー時はNone
        """
        try:
            # 実装
            return temperature
        except Exception as e:
            logger.error(f"Temperature read error: {e}")
            return None
```

### JavaScript (Node-RED関数)
```javascript
// Node-RED関数ノード内のコード
// JSDoc形式でコメント記載
/**
 * センサーデータを処理する
 * @param {Object} msg - メッセージオブジェクト
 * @returns {Object} 処理済みメッセージ
 */
function processSensorData(msg) {
    // 実装
    return msg;
}
```

### ドキュメント
- Markdownファイルは80文字で改行
- 見出しレベルを適切に設定
- コードブロックに言語指定
- 相互リンクを活用

## テスト

### 自動テスト
```bash
# 全テスト実行
npm test

# カバレッジ確認
npm run test:coverage

# 特定テスト実行
npm test -- --grep "sensor"
```

### 手動テスト
- [ ] Node-REDフローが正常動作する
- [ ] ダッシュボードが適切に表示される
- [ ] センサーデータが正しく取得される
- [ ] データベース保存が動作する
- [ ] アラート機能が動作する

### テストケース作成
```python
# tests/sensors/test_temperature.py
import pytest
from sensors.temperature import TemperatureSensor

class TestTemperatureSensor:
    def setup_method(self):
        self.sensor = TemperatureSensor(address=0x48)
    
    def test_read_temperature_success(self):
        temperature = self.sensor.read_temperature()
        assert temperature is not None
        assert -40 <= temperature <= 85
    
    def test_read_temperature_error_handling(self):
        # エラー条件のテスト
        pass
```

## ドキュメント貢献

### ドキュメント構造
```
docs/
├── architecture/    # システム設計
├── technical/      # 技術仕様
├── migration/      # 移行ガイド
├── guides/         # 運用ガイド
├── api/           # API仕様
└── assets/        # 画像・図表
```

### ドキュメント作成手順
1. [テンプレート](./docs/assets/templates/)を使用
2. 対象読者を明確にする
3. 具体例・コード例を含める
4. 関連ドキュメントへのリンクを設置
5. プレビューで確認

### 画像・図表
- Mermaid図を積極的に活用
- スクリーンショットは適切なサイズに調整
- 説明的なファイル名を使用

## レビュープロセス

### レビュー観点
- [ ] 機能が正しく動作する
- [ ] コード品質が適切
- [ ] テストが充分
- [ ] ドキュメントが更新されている
- [ ] 破壊的変更がないか
- [ ] セキュリティ問題がないか

### レビュー後の対応
- フィードバックに基づく修正
- 追加のテスト実装
- ドキュメント更新

## セキュリティ

### 脆弱性報告
- セキュリティ問題は公開Issueではなくメールで報告
- security@example.com に詳細を送信
- 責任ある開示原則に従う

### セキュリティ考慮事項
- 認証・認可の適切な実装
- 入力値検証の実装
- ログに機密情報を出力しない
- 依存関係の脆弱性チェック

## リリース

### リリースプロセス
1. 機能完成・テスト完了
2. ドキュメント更新
3. CHANGELOG.md更新
4. バージョンタグ作成
5. GitHub Release作成

### バージョニング
- Semantic Versioning (SemVer) を採用
- MAJOR.MINOR.PATCH形式
- 破壊的変更はMAJORバージョンアップ

## コミュニティ

### コミュニケーション
- GitHub Issues - バグ報告・機能要求
- GitHub Discussions - 質問・議論
- Slack - リアルタイム議論（内部）

### 行動規範
- 建設的なフィードバック
- 多様性の尊重
- 協力的な姿勢
- 技術的な議論に集中

## ヘルプ・サポート

### 質問・相談
- [GitHub Discussions](../../discussions) - 技術的質問
- [ドキュメント](./docs/) - 既存の情報確認
- [トラブルシューティング](./docs/guides/troubleshooting.md) - 問題解決

### 学習リソース
- [Node-RED公式ドキュメント](https://nodered.org/docs/)
- [Raspberry Pi公式ドキュメント](https://www.raspberrypi.org/documentation/)
- [IoT開発ベストプラクティス](https://example.com/iot-best-practices)

---

ご不明な点がございましたら、お気軽にお声がけください。皆様の貢献をお待ちしております！