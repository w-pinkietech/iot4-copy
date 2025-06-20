# Current System ドキュメント技術的正確性検証ステータス

このファイルは、**Current System（現行システム）** の技術的正確性検証状態を一覧表示するダッシュボードです。New Systemは検証対象外です。

## 技術的正確性ステータス凡例

- `TECHNICALLY_VERIFIED`: 実環境で技術的正確性を確認済み・間違いなし
- `NEEDS_TECHNICAL_FIX`: 技術的間違いを発見・早急な修正が必要
- `PARTIAL_VERIFICATION`: 部分的に確認済み・残り部分は要検証
- `UNVERIFIED`: 技術的正確性未確認・検証作業未着手
- `HUMAN_TECHNICAL_REVIEW`: 技術専門家による判断が必要

## 技術的重要度凡例

- `CRITICAL`: 技術的間違いがあると致命的・システム停止や重大障害の原因
- `HIGH`: 技術的間違いがあると運用に直接影響・間違った設定や操作の原因
- `MEDIUM`: 技術的間違いがあると開発に影響・非効率や混乱の原因
- `LOW`: 技術的間違いがあっても影響は軽微・参考情報レベル

---

## Current System 技術的正確性検証対象ファイル

### 🚨 CRITICAL Priority - 技術的間違いがあると致命的

| ファイル | ステータス | 最終更新 | 関連Issue | 備考 |
|---------|-----------|----------|-----------|------|
| `current-system/specifications/technical-specs.md` | `UNVERIFIED` | - | - | **DB接続情報・ポート番号要確認** |
| `current-system/operations/deployment-guide.md` | `UNVERIFIED` | - | - | **システム起動・停止手順要確認** |

### 🔴 HIGH Priority - 技術的間違いがあると運用に直接影響

| ファイル | ステータス | 最終更新 | 関連Issue | 備考 |
|---------|-----------|----------|-----------|------|
| `current-system/overview/quick-start.md` | `UNVERIFIED` | - | - | 初期設定手順要確認 |
| `current-system/api/rest-api.md` | `UNVERIFIED` | - | - | **API仕様・エンドポイント要確認** |

### 📊 MEDIUM Priority - 開発・拡張影響

| ファイル | ステータス | 最終更新 | 関連Issue | 備考 |
|---------|-----------|----------|-----------|------|
| `current-system/architecture/system-overview.md` | `UNVERIFIED` | - | - | システム構成図要確認 |
| `current-system/architecture/node-red-flows.md` | `UNVERIFIED` | - | - | フロー仕様書要確認 |
| `current-system/api/rest-api.md` | `UNVERIFIED` | - | - | API仕様要確認 |
| `current-system/implementation/node-red-system.md` | `UNVERIFIED` | - | - | 実装詳細要確認 |
| `current-system/architecture/data-flow-analysis.md` | `UNVERIFIED` | - | - | データフロー要確認 |
| `current-system/architecture/bravepi-bravejig-integration.md` | `UNVERIFIED` | - | - | ハードウェア連携要確認 |
| `current-system/architecture/program-runtime-architecture.md` | `UNVERIFIED` | - | - | 実行時アーキテクチャ要確認 |

### 📖 LOW Priority - 参考情報

| ファイル | ステータス | 最終更新 | 関連Issue | 備考 |
|---------|-----------|----------|-----------|------|
| `current-system/overview/system-summary.md` | `UNVERIFIED` | - | - | 概要説明 |
| `current-system/overview/features-benefits.md` | `UNVERIFIED` | - | - | 特徴・利点説明 |
| `current-system/overview/architecture-diagram.md` | `UNVERIFIED` | - | - | アーキテクチャ図 |
| `current-system/analysis/technical-analysis.md` | `UNVERIFIED` | - | - | 技術分析資料 |
| `current-system/analysis/comprehensive-node-red-flows-analysis.md` | `UNVERIFIED` | - | - | フロー分析資料 |
| `current-system/analysis/sensor-data-samples.md` | `UNVERIFIED` | - | - | センサーデータサンプル |
| `current-system/analysis/coupling-analysis.md` | `UNVERIFIED` | - | - | 結合度分析 |

---

## Hardware Reference (Current System関連のみ)

### 🔴 HIGH Priority - 技術的間違いがあると運用に直接影響

| ファイル | ステータス | 最終更新 | 関連Issue | 備考 |
|---------|-----------|----------|-----------|------|
| `current-system/reference/software/bravepi-mainboard-specification.md` | `UNVERIFIED` | - | - | **メインボード仕様要確認** |
| `current-system/reference/software/bravepi-transmitter-illuminance-specification.md` | `UNVERIFIED` | - | - | 照度センサー仕様 |
| `current-system/reference/software/bravepi-transmitter-accelerometer-specification.md` | `UNVERIFIED` | - | - | 加速度センサー仕様 |
| `current-system/reference/software/bravepi-transmitter-contact-input-specification.md` | `UNVERIFIED` | - | - | 接点入力仕様 |
| `current-system/reference/software/bravepi-transmitter-contact-output-specification.md` | `UNVERIFIED` | - | - | 接点出力仕様 |
| `current-system/reference/software/bravepi-transmitter-thermocouple-specification.md` | `UNVERIFIED` | - | - | 熱電対仕様 |
| `current-system/reference/software/bravepi-transmitter-distance-sensor-specification.md` | `UNVERIFIED` | - | - | 距離センサー仕様 |
| `current-system/reference/software/bravepi-transmitter-differential-pressure-specification.md` | `UNVERIFIED` | - | - | 差圧センサー仕様 |
| `current-system/reference/software/bravepi-transmitter-adc-specification.md` | `UNVERIFIED` | - | - | ADC仕様 |

---

## Current System 技術的正確性検証サマリー

### 技術的正確性検証進捗状況
- **TECHNICALLY_VERIFIED**: 0 ファイル (0%)
- **NEEDS_TECHNICAL_FIX**: 0 ファイル (0%)
- **PARTIAL_VERIFICATION**: 0 ファイル (0%)
- **UNVERIFIED**: 25 ファイル (100%)
- **HUMAN_TECHNICAL_REVIEW**: 0 ファイル (0%)

### 技術的重要度別統計（Current Systemのみ）
- **CRITICAL Priority**: 2 ファイル (全て未検証)
- **HIGH Priority**: 13 ファイル (全て未検証)
- **MEDIUM Priority**: 7 ファイル (全て未検証)
- **LOW Priority**: 3 ファイル (全て未検証)

### 次の推奨アクション（技術的正確性重視）
1. **最優先**: CRITICAL Priority ファイルの技術的正確性確認
   - `technical-specs.md` (**DB接続情報・ポート番号**)
   - `deployment-guide.md` (**システム起動・停止手順**)

2. **第二優先**: HIGH Priority ファイルの技術的正確性確認
   - `quick-start.md` (初期設定手順)
   - `rest-api.md` (API仕様・エンドポイント)
   - Hardware Reference 各種仕様書

3. **Issue作成推奨**: 上記CRITICALファイルのIssue作成
4. **Draft PR準備**: 技術的正確性検証作業用のDraft PR作成準備

---

**最終更新**: 2025年6月20日  
**管理方針**: Git/Issue/PR中心の軽量管理  
**ルール詳細**: [document-fact-verification-rules.md](./document-fact-verification-rules.md)