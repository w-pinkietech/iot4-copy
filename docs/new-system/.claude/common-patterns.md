# よく使用するパターン

## システム操作コマンド

### Docker環境の管理
```bash
# システム起動
cd docker && docker-compose up -d

# システム停止
cd docker && docker-compose down

# ログ確認
docker-compose logs -f [service-name]
```

### MQTT関連操作
```bash
# MQTTメッセージ監視（全トピック）
mosquitto_sub -h localhost -t "#" -v

# 特定トピックの監視
mosquitto_sub -h localhost -t "sensor/+/data" -v

# テストメッセージの送信
mosquitto_pub -h localhost -t "test/topic" -m "test message"
```

### I2Cデバイス確認
```bash
# I2Cデバイスの検出
sudo i2cdetect -y 1

# I2Cツールのインストール（必要に応じて）
sudo apt-get install i2c-tools
```

### ログ確認パターン
```bash
# Node-REDログ確認
sudo journalctl -u node-red -f

# システムログ確認
sudo journalctl -f

# アプリケーション固有ログ
tail -f /var/log/iotkit/app.log
```

## 開発支援コマンド

### Python/FastAPI開発
```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt

# FastAPIサーバーの起動（開発用）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# テストの実行
pytest tests/ -v
```

### データベース操作
```bash
# MariaDB接続
mysql -h 127.0.0.1 -P 3306 -u iotkit -p iotkit

# SQLiteファイルの確認
sqlite3 /path/to/database.db ".tables"

# InfluxDB CLI（必要に応じて）
influx -host 127.0.0.1 -port 8086
```

## Claude Code活用パターン

### 新機能開発の依頼
```
.claude/context.md と .claude/project-knowledge.md の制約条件を考慮して、
以下の要件で新しいセンサープラグインを実装してください：

- センサー: [センサー名] 
- 通信方式: I2C/UART/USB Serial
- データフォーマット: [期待する出力形式]
- プラグインアーキテクチャに従った実装
- 単体テストも含める
```

### デバッグ支援の依頼
```
.claude/project-improvements.md の過去の解決パターンを参考に、
以下のエラーを分析して解決策を提案してください：

エラーメッセージ: [具体的なエラー]
発生環境: Raspberry Pi 4, Python 3.11
再現手順: [手順を記載]
```

### アーキテクチャレビューの依頼
```
.claude/project-knowledge.md のアーキテクチャ原則に従って、
以下の設計をレビューしてください：

[設計内容を記載]

特に以下の観点でチェック：
- 疎結合性
- 拡張性
- パフォーマンス
- セキュリティ
```

## 定型的な実装テンプレート

### センサードライバーの基本構造
```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class SensorDriver(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def read(self) -> Dict[str, Any]:
        """センサーデータを読み取り"""
        pass
    
    @abstractmethod
    def configure(self, config: Dict[str, Any]) -> bool:
        """センサー設定の更新"""
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """設定の妥当性検証"""
        required_keys = self.get_required_config_keys()
        return all(key in config for key in required_keys)
```

### プラグインの基本構造
```python
from typing import Dict, Any, Optional
import logging

class ProtocolPlugin:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def parse(self, raw_data: bytes) -> Optional[Dict[str, Any]]:
        """生データの解析"""
        try:
            # プロトコル固有の解析処理
            return parsed_data
        except Exception as e:
            self.logger.error(f"Parse error: {e}")
            return None
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """データの妥当性検証"""
        # 検証ロジック
        return True
    
    def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """標準フォーマットへの変換"""
        # 変換ロジック
        return transformed_data
```

### FastAPI エンドポイントの基本構造
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

class SensorDataRequest(BaseModel):
    sensor_id: str
    data: Dict[str, Any]

class SensorDataResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

@app.post("/api/sensors/data", response_model=SensorDataResponse)
async def post_sensor_data(request: SensorDataRequest):
    try:
        # データ処理ロジック
        return SensorDataResponse(
            success=True,
            message="Data processed successfully",
            data=processed_data
        )
    except Exception as e:
        logger.error(f"Error processing sensor data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

## トラブルシューティングパターン

### よくある問題と解決策

#### I2C通信エラー
```bash
# 権限確認
sudo usermod -a -G i2c $USER
# 再ログインが必要

# I2Cデバイスの確認
ls -la /dev/i2c-*
```

#### MQTT接続エラー
```bash
# MQTTブローカーの状態確認
sudo systemctl status mosquitto

# ポートの確認
netstat -an | grep 1883
```

#### データベース接続エラー
```bash
# MariaDBサービス確認
sudo systemctl status mariadb

# 接続テスト
mysql -h 127.0.0.1 -P 3306 -u iotkit -p iotkit -e "SELECT 1;"
```

## 設定ファイルのテンプレート

### センサー設定（SQLite）
```sql
INSERT INTO sensors (
    sensor_id, sensor_type, i2c_address, 
    polling_interval, enabled, config_json
) VALUES (
    'temp_001', 'mcp9600', 0x67,
    1000, 1, '{"thermocouple_type": "K", "cold_junction_resolution": 0.25}'
);
```

### MQTT設定例
```json
{
    "broker": {
        "host": "localhost",
        "port": 1883,
        "keepalive": 60
    },
    "topics": {
        "sensor_data": "sensor/{sensor_id}/data",
        "sensor_status": "sensor/{sensor_id}/status",
        "commands": "command/{sensor_id}",
        "responses": "response/{sensor_id}"
    },
    "qos": 1,
    "retain": false
}
```