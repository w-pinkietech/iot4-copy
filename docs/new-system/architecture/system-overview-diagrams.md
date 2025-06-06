# システム概要図解説明書

*BravePI/JIG疎結合化の全体像とGateway設計の視覚的理解*

## 文書概要

本文書は、IoT導入支援キット Ver.4.1 の BravePI/JIG ハードウェア依存を解消するための全体システム構成を図解で説明します。プログラムの詳細に入る前に、システム全体の概念・データの流れ・疎結合化のアプローチを視覚的に理解することを目的とします。

## 目次
1. [現状システムの問題点（図解）](#現状システムの問題点図解)
2. [疎結合化の全体戦略（図解）](#疎結合化の全体戦略図解)
3. [Gatewayによる解決アプローチ](#gatewayによる解決アプローチ)
4. [データフロー変化の比較](#データフロー変化の比較)
5. [段階的移行戦略](#段階的移行戦略)

## 現状システムの問題点（図解）

### 1. 密結合の現状アーキテクチャ

```mermaid
graph TB
    subgraph "現状：密結合システム"
        subgraph "ハードウェア層"
            BPI[BravePI Device]
            BJG[BraveJIG Device]
        end
        
        subgraph "通信層（密結合）"
            UART[UART 38400baud]
            USB[USB Serial]
        end
        
        subgraph "Node-RED処理層（1017ノード）"
            F1[Function Node 1<br/>BravePI解析]
            F2[Function Node 2<br/>温度センサー専用]
            F3[Function Node 3<br/>接点入力専用]
            F53[... Function Node 53<br/>プロトコル解析]
            
            H1[Hardware Node 1<br/>GPIO制御]
            H2[Hardware Node 2<br/>I2C制御]
            H380[... Hardware Node 380<br/>デバイス制御]
        end
        
        subgraph "データベース層"
            MARIADB[MariaDB<br/>BravePI専用テーブル]
            INFLUX[InfluxDB<br/>固定スキーマ]
        end
        
        subgraph "UI層"
            WEB[Web Dashboard<br/>ハードウェア固有UI]
        end
    end
    
    BPI -->|バイナリプロトコル| UART
    BJG -->|バイナリプロトコル| USB
    UART --> F1
    USB --> F1
    F1 --> F2
    F1 --> F3
    F2 --> F53
    F3 --> F53
    F53 --> H1
    H1 --> H2
    H2 --> H380
    H380 --> MARIADB
    MARIADB --> INFLUX
    INFLUX --> WEB
    
    style F1 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style F2 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style F3 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style F53 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style H1 fill:#ff8787,stroke:#fff,stroke-width:2px,color:#fff
    style H2 fill:#ff8787,stroke:#fff,stroke-width:2px,color:#fff
    style H380 fill:#ff8787,stroke:#fff,stroke-width:2px,color:#fff
```

### 2. 密結合による具体的問題

```mermaid
graph TB
    subgraph "問題1：ベンダーロックイン"
        A[新しいハードウェア追加要求]
        A --> B[全システム修正必要]
        B --> C[3-6ヶ月の開発期間]
        C --> D[高いコスト・リスク]
    end
    
    subgraph "問題2：保守性の悪化"
        E[センサータイプ追加]
        E --> F[53個のFunctionノード修正]
        F --> G[380個のHardwareノード修正]
        G --> H[データベーススキーマ変更]
        H --> I[UI表示ロジック修正]
    end
    
    subgraph "問題3：テスト困難性"
        J[機能テスト実行]
        J --> K[実機必須]
        K --> L[環境構築困難]
        L --> M[デバッグ複雑化]
    end
    
    style B fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style G fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style H fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style I fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style K fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style L fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
```

## 疎結合化の全体戦略（図解）

### 1. 目標アーキテクチャ：疎結合システム

```mermaid
graph TB
    subgraph "目標：疎結合システム"
        subgraph "多様なハードウェア層"
            BPI[BravePI]
            BJG[BraveJIG]
            ESP[ESP32]
            ARD[Arduino]
            OTH[その他IoTデバイス]
        end
        
        subgraph "Gateway抽象化層"
            GW[Universal Gateway<br/>🌟 新規実装]
            subgraph "Protocol Adapters"
                PA1[BravePI Adapter]
                PA2[ESP32 Adapter]
                PA3[MQTT Adapter]
            end
        end
        
        subgraph "統一API層"
            API[REST API<br/>統一インターフェース]
            WS[WebSocket<br/>リアルタイム配信]
        end
        
        subgraph "アプリケーション層"
            APP[統一アプリケーション<br/>ハードウェア非依存]
        end
        
        subgraph "データ層"
            DB[統一データベース<br/>ベンダー中立スキーマ]
        end
        
        subgraph "ユーザーインターフェース"
            UI[統一Dashboard<br/>ハードウェア非依存UI]
        end
    end
    
    BPI --> PA1
    BJG --> PA1
    ESP --> PA2
    ARD --> PA2
    OTH --> PA3
    
    PA1 --> GW
    PA2 --> GW
    PA3 --> GW
    
    GW --> API
    GW --> WS
    
    API --> APP
    WS --> APP
    
    APP --> DB
    DB --> UI
    
    style GW fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style API fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style APP fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style PA1 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style PA2 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style PA3 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
```

### 2. 疎結合化による効果

```mermaid
graph LR
    subgraph "Before：密結合"
        B1[新ハードウェア対応<br/>3-6ヶ月]
        B2[全システム影響<br/>高リスク]
        B3[実機テスト必須<br/>効率低下]
    end
    
    subgraph "After：疎結合"
        A1[新ハードウェア対応<br/>1-2週間]
        A2[プラグイン追加のみ<br/>低リスク]
        A3[モック・シミュレート<br/>高効率]
    end
    
    B1 -.->|90%短縮| A1
    B2 -.->|リスク最小化| A2
    B3 -.->|5倍効率化| A3
    
    style A1 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style A2 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style A3 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style B1 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style B2 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style B3 fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
```

## Gatewayによる解決アプローチ

### 1. Gateway のコアコンセプト

```mermaid
graph LR
    subgraph "入力：多様なプロトコル"
        INPUT1[BravePI<br/>バイナリプロトコル<br/>38400baud]
        INPUT2[ESP32<br/>WiFi JSON]
        INPUT3[Arduino<br/>Serial ASCII]
        INPUT4[MQTT Device<br/>JSON Message]
    end
    
    subgraph "Gateway：プロトコル変換"
        subgraph "Parser Layer"
            P1[BravePI Parser]
            P2[ESP32 Parser]
            P3[Arduino Parser]
            P4[MQTT Parser]
        end
        
        subgraph "Transformer Layer"
            T[Universal Transformer<br/>統一データ形式生成]
        end
        
        subgraph "Validator Layer"
            V[Data Validator<br/>品質・整合性チェック]
        end
    end
    
    subgraph "出力：統一JSON形式"
        OUTPUT["Universal JSON<br/>deviceId: xxx<br/>sensorType: temperature<br/>value: 25.5<br/>unit: ℃<br/>timestamp: 2025-06-06T10:30:00Z"]
    end
    
    INPUT1 --> P1
    INPUT2 --> P2
    INPUT3 --> P3
    INPUT4 --> P4
    
    P1 --> T
    P2 --> T
    P3 --> T
    P4 --> T
    
    T --> V
    V --> OUTPUT
    
    style T fill:#fab005,stroke:#000,stroke-width:2px,color:#000
    style V fill:#fab005,stroke:#000,stroke-width:2px,color:#000
    style OUTPUT fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
```

### 2. Gateway出力後の通信規格

```mermaid
graph TB
    subgraph "Gateway出力"
        GW_OUT[統一JSON形式<br/>Universal Sensor Data]
    end
    
    subgraph "通信規格・配信方式"
        REST[REST API<br/>HTTP/HTTPS]
        WS[WebSocket<br/>リアルタイム配信]
        MQTT_OUT[MQTT Publish<br/>Broker経由配信]
        SSE[Server-Sent Events<br/>HTTP長時間接続]
    end
    
    subgraph "受信システム・デバイス"
        WEB_APP[Webアプリケーション<br/>JavaScript/React]
        MOBILE[モバイルアプリ<br/>Android/iOS]
        OTHER_IOT[他社IoTプラットフォーム<br/>AWS IoT/Azure IoT]
        ANALYTICS[分析システム<br/>Machine Learning]
        STORAGE[時系列データベース<br/>InfluxDB/TimescaleDB]
        ALERT[アラートシステム<br/>Slack/Email通知]
    end
    
    GW_OUT --> REST
    GW_OUT --> WS
    GW_OUT --> MQTT_OUT
    GW_OUT --> SSE
    
    REST --> WEB_APP
    REST --> OTHER_IOT
    REST --> ANALYTICS
    
    WS --> WEB_APP
    WS --> MOBILE
    
    MQTT_OUT --> OTHER_IOT
    MQTT_OUT --> ANALYTICS
    MQTT_OUT --> ALERT
    
    SSE --> WEB_APP
    SSE --> STORAGE
    
    style GW_OUT fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style REST fill:#74c0fc,stroke:#000,stroke-width:2px,color:#000
    style WS fill:#74c0fc,stroke:#000,stroke-width:2px,color:#000
    style MQTT_OUT fill:#74c0fc,stroke:#000,stroke-width:2px,color:#000
    style SSE fill:#74c0fc,stroke:#000,stroke-width:2px,color:#000
```

#### 通信規格の詳細

| 通信方式 | プロトコル | 用途 | 特徴 |
|----------|-----------|------|------|
| **REST API** | HTTP/HTTPS | 一般的なWebアプリ連携 | • 同期通信<br/>• ポーリング可能<br/>• 標準的 |
| **WebSocket** | WS/WSS | リアルタイム配信 | • 双方向通信<br/>• 低レイテンシ<br/>• 常時接続 |
| **MQTT** | MQTT v3.1.1/v5.0 | IoTデバイス間通信 | • 軽量プロトコル<br/>• QoS対応<br/>• Pub/Sub |
| **Server-Sent Events** | HTTP | 一方向リアルタイム | • HTTP互換<br/>• 自動再接続<br/>• 簡単実装 |

#### 実装例

```yaml
# REST API エンドポイント
GET  /api/v1/sensors/latest        # 最新データ取得
POST /api/v1/sensors/{id}/config   # センサー設定
GET  /api/v1/devices               # デバイス一覧

# WebSocket エンドポイント  
WS   /ws/sensor-stream             # リアルタイムデータ配信
WS   /ws/device/{id}/control       # デバイス制御

# MQTT トピック
Topic: sensors/{deviceId}/{sensorType}/data    # データ配信
Topic: sensors/{deviceId}/config               # 設定配信
Topic: alerts/{deviceId}/{alertType}           # アラート配信

# Server-Sent Events
GET  /events/sensor-stream         # イベントストリーム
GET  /events/alerts                # アラートストリーム
```

### 3. BravePI専用プロトコル変換の詳細

```mermaid
graph TB
    subgraph "BravePI バイナリフレーム"
        FRAME["Protocol・Type・Length・Timestamp・Device#・Sensor・Payload<br/>1byte・1byte・2bytes・4bytes・8bytes・2bytes・n bytes"]
    end
    
    subgraph "Gateway 解析処理"
        PARSE[Frame Parser<br/>バイナリ解析]
        MAP[Sensor Type Mapping<br/>257→contact_input<br/>261→temperature<br/>289→illuminance_jig]
        EXTRACT[Value Extractor<br/>ペイロードからセンサー値抽出]
        CALIB[Calibration<br/>較正・単位変換]
    end
    
    subgraph "統一JSON出力"
        JSON["統一JSON形式<br/>deviceId: bravepi-12345678<br/>sensorType: temperature<br/>value: 25.5<br/>unit: ℃<br/>timestamp: 2025-06-06T10:30:00Z<br/>quality: good<br/>metadata: source=bravepi"]
    end
    
    FRAME --> PARSE
    PARSE --> MAP
    MAP --> EXTRACT
    EXTRACT --> CALIB
    CALIB --> JSON
    
    style PARSE fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style MAP fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style JSON fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
```

## データフロー変化の比較

### 1. 現状：BravePI依存データフロー

```mermaid
sequenceDiagram
    participant BravePI
    participant NodeRED as Node-RED<br/>(1017 nodes)
    participant MariaDB
    participant InfluxDB
    participant Dashboard
    
    BravePI->>NodeRED: バイナリプロトコル<br/>(38400baud)
    Note over NodeRED: 53個のFunctionノード<br/>でプロトコル解析
    NodeRED->>NodeRED: センサータイプ別処理<br/>(380個のHardwareノード)
    NodeRED->>MariaDB: BravePI専用テーブル<br/>への保存
    MariaDB->>InfluxDB: 時系列データ転送
    InfluxDB->>Dashboard: ハードウェア固有UI<br/>での表示
    
    Note over BravePI,Dashboard: 問題：全てがBravePI固有実装
```

### 2. 目標：Gateway経由データフロー

```mermaid
sequenceDiagram
    participant Multiple as 複数ハードウェア<br/>(BravePI/ESP32/Arduino...)
    participant Gateway as Python Gateway<br/>🌟 新規実装
    participant API as REST API<br/>(統一)
    participant Database as 統一Database<br/>(ベンダー中立)
    participant App as Application<br/>(ハードウェア非依存)
    
    Multiple->>Gateway: 各種プロトコル<br/>(Binary/JSON/MQTT...)
    Note over Gateway: プロトコル変換<br/>統一JSON生成
    Gateway->>API: 統一JSON形式<br/>{"deviceId":"xxx","sensorType":"temperature"...}
    API->>Database: ベンダー中立スキーマ<br/>での保存
    Database->>App: 統一API経由<br/>データ取得
    App->>App: ハードウェア非依存<br/>処理・表示
    
    Note over Multiple,App: 利点：新ハードウェアはGatewayプラグインのみ追加
```

### 3. 新ハードウェア追加時の比較

```mermaid
graph TB
    subgraph "現状：ESP32追加時の影響範囲"
        ESP32_OLD[ESP32デバイス]
        ESP32_OLD --> MODIFY1[53個のFunctionノード修正]
        ESP32_OLD --> MODIFY2[380個のHardwareノード修正]
        ESP32_OLD --> MODIFY3[データベーススキーマ変更]
        ESP32_OLD --> MODIFY4[UI表示ロジック修正]
        
        MODIFY1 --> IMPACT[全システム影響<br/>3-6ヶ月開発]
        MODIFY2 --> IMPACT
        MODIFY3 --> IMPACT
        MODIFY4 --> IMPACT
    end
    
    subgraph "目標：ESP32追加時の影響範囲"
        ESP32_NEW[ESP32デバイス]
        ESP32_NEW --> PLUGIN[ESP32プラグイン実装のみ<br/>1-2週間]
        PLUGIN --> NOIMACT[既存システム無影響<br/>即座に利用可能]
    end
    
    style IMPACT fill:#ff6b6b,stroke:#fff,stroke-width:2px,color:#fff
    style NOIMACT fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style PLUGIN fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
```

## 段階的移行戦略

### 1. 移行フェーズ概要

```mermaid
gantt
    title 疎結合化移行ロードマップ
    dateFormat  YYYY-MM-DD
    section Phase 1: Gateway構築
    Gateway基盤実装          :p1-1, 2025-06-06, 2025-08-31
    BravePIアダプター実装    :p1-2, 2025-07-01, 2025-08-31
    
    section Phase 2: 並行運用
    新旧システム並行稼働     :p2-1, 2025-08-01, 2025-11-30
    データ整合性検証        :p2-2, 2025-09-01, 2025-11-30
    
    section Phase 3: 段階移行
    センサータイプ別移行     :p3-1, 2025-10-01, 2025-12-31
    アプリケーション層移行   :p3-2, 2025-11-01, 2025-12-31
    
    section Phase 4: 完全移行
    旧システム廃止          :p4-1, 2026-01-01, 2026-02-28
    新機能追加              :p4-2, 2026-02-01, 2026-04-30
```

### 2. Phase 1: Gateway構築の詳細

```mermaid
graph TB
    subgraph "Week 1-4: 基盤開発"
        W1[Python環境構築<br/>FastAPI + Pydantic]
        W2[BravePIプロトコル解析器<br/>バイナリフレーム処理]
        W3[統一データモデル定義<br/>UniversalSensorData]
        W4[基本API実装<br/>REST + WebSocket]
    end
    
    subgraph "Week 5-8: 変換機能実装"
        W5[センサータイプマッピング<br/>257-264, 289-293対応]
        W6[データ品質評価<br/>エラーハンドリング]
        W7[WebSocket配信機能<br/>リアルタイムストリーミング]
        W8[統合テスト<br/>実機検証]
    end
    
    subgraph "Week 9-12: 最適化・配備"
        W9[性能最適化<br/>レスポンス時間改善]
        W10[Docker化<br/>マルチプラットフォーム対応]
        W11[監視・ログ機能<br/>運用準備]
        W12[ドキュメント整備<br/>引き継ぎ準備]
    end
    
    W1 --> W2 --> W3 --> W4
    W4 --> W5 --> W6 --> W7 --> W8
    W8 --> W9 --> W10 --> W11 --> W12
    
    style W4 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style W8 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style W12 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
```

### 3. Phase 2: 並行運用アーキテクチャ

```mermaid
graph TB
    subgraph "BravePIデバイス"
        BPI[BravePI/JIG Hardware]
    end
    
    subgraph "データ分岐"
        SPLIT[Data Splitter<br/>データ複製配信]
    end
    
    subgraph "既存システム（継続稼働）"
        OLD_NR[Node-RED<br/>既存1017ノード]
        OLD_DB[MariaDB/InfluxDB<br/>既存スキーマ]
        OLD_UI[既存Dashboard]
    end
    
    subgraph "新Gateway（検証）"
        NEW_GW[Python Gateway<br/>🌟 新実装]
        NEW_API[REST API]
        NEW_DB[統一Database]
        NEW_UI[新Dashboard]
    end
    
    subgraph "データ整合性検証"
        VALIDATOR[Data Validator<br/>新旧比較・差分検出]
    end
    
    BPI --> SPLIT
    SPLIT --> OLD_NR
    SPLIT --> NEW_GW
    
    OLD_NR --> OLD_DB --> OLD_UI
    NEW_GW --> NEW_API --> NEW_DB --> NEW_UI
    
    OLD_DB --> VALIDATOR
    NEW_DB --> VALIDATOR
    
    style NEW_GW fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style VALIDATOR fill:#fab005,stroke:#000,stroke-width:2px,color:#000
    style SPLIT fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
```

## 実装優先度とROI

### 1. 機能別優先度マトリックス

```mermaid
graph TB
    subgraph "高優先度・高ROI"
        HIGH1[BravePIプロトコル変換<br/>📊 ROI: 即座に効果]
        HIGH2[基本センサー対応<br/>📊 ROI: 保守性大幅改善]
        HIGH3[統一API実装<br/>📊 ROI: 将来拡張性確保]
    end
    
    subgraph "中優先度・中ROI"
        MID1[WebSocket配信<br/>📊 ROI: UI応答性向上]
        MID2[データ品質評価<br/>📊 ROI: 信頼性向上]
        MID3[Docker化<br/>📊 ROI: 運用効率化]
    end
    
    subgraph "低優先度・将来ROI"
        LOW1[新ハードウェア対応<br/>📊 ROI: 将来の拡張時]
        LOW2[高度分析機能<br/>📊 ROI: 付加価値向上]
        LOW3[セキュリティ強化<br/>📊 ROI: 長期運用安定性]
    end
    
    style HIGH1 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style HIGH2 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style HIGH3 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style MID1 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style MID2 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style MID3 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
```

### 2. 段階的ROI実現

```mermaid
graph LR
    subgraph "Month 1-2"
        M1[Gateway基盤完成<br/>💰 開発効率20%向上]
    end
    
    subgraph "Month 3-4"
        M2[BravePI完全対応<br/>💰 保守コスト40%削減]
    end
    
    subgraph "Month 5-6"
        M3[新ハードウェア追加可能<br/>💰 新規対応期間90%短縮]
    end
    
    subgraph "Month 7+"
        M4[完全疎結合達成<br/>💰 総合開発速度3倍向上]
    end
    
    M1 --> M2 --> M3 --> M4
    
    style M1 fill:#ffd43b,stroke:#000,stroke-width:2px,color:#000
    style M2 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style M3 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
    style M4 fill:#51cf66,stroke:#fff,stroke-width:2px,color:#000
```

---

## 文書メタデータ

**文書タイトル**: システム概要図解説明書  
**作成日付**: 2025年6月6日  
**対象読者**: システム設計者・開発者・プロジェクト関係者  
**目的**: 疎結合化戦略の視覚的理解・合意形成  
**前提知識**: IoTシステム基礎・現状システム概要  
**文書レベル**: 概要説明・戦略図解 (★★☆)