# デバッグログ

## 記録ルール

以下の条件を満たす問題は、このファイルに記録してください：
- 解決に30分以上要した問題
- 再発の可能性が高い問題
- チーム全体で共有すべき知見
- 将来の類似問題の参考になる解決過程

## 記録フォーマット

```markdown
## [YYYY-MM-DD] 問題の概要

**症状**: エラーメッセージや異常動作の詳細
**環境**: OS, Python, Node.js, ブラウザバージョンなど
**再現手順**: 具体的な操作手順（できるだけ詳細に）
**試行錯誤**: 試した方法とその結果
**最終解決方法**: 確実に動作する解決手順
**根本原因**: 問題の本質的な原因
**予防策**: 同じ問題を避けるための対策
**参考資料**: 役に立ったドキュメントやリンク
```

---

## デバッグ記録例

### [2024-06-20] I2C通信でのPermission Deniedエラー

**症状**: 
```
PermissionError: [Errno 13] Permission denied: '/dev/i2c-1'
```

**環境**: 
- OS: Raspberry Pi OS (Debian 11)
- Python: 3.11.2
- 使用ライブラリ: smbus2

**再現手順**:
1. Python環境でI2Cセンサーへのアクセスを試行
2. `sensor.read()`を実行
3. Permission Deniedエラーが発生

**試行錯誤**:
- ❌ `sudo`でPythonスクリプト実行 → 仮想環境が認識されない
- ❌ `/dev/i2c-1`のパーミッション変更 → 再起動後に元に戻る
- ✅ i2cグループへのユーザー追加 → 恒久的に解決

**最終解決方法**:
```bash
# i2cグループにユーザーを追加
sudo usermod -a -G i2c $USER

# 再ログインまたは再起動
sudo reboot

# 確認
groups $USER | grep i2c
```

**根本原因**: 
Raspberry PiのI2Cデバイスファイルはi2cグループに属しており、一般ユーザーはデフォルトでこのグループに属していない。

**予防策**: 
新しい開発環境構築時のチェックリストにi2cグループ追加を含める。

**参考資料**: 
- [Raspberry Pi I2C Setup Guide](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

---

## 一時的なデバッグファイルの管理

### sessions/ ディレクトリ
セッション別のデバッグログ（作業中の問題調査）
- ファイル名形式: `debug-YYYY-MM-DD-HHMMSS.md`
- 解決後は適宜 `archive/` に移動

### temp-logs/ ディレクトリ
作業中の一時ファイル（エラーログ、設定ファイルのバックアップなど）
- 定期的にクリーンアップが必要

### archive/ ディレクトリ
解決済み問題の保管
- 重要な知見は本ファイル（debug-log.md）に統合
- 詳細な調査過程を保管

## よくある問題の早見表

### I2C関連
- **Permission Denied**: i2cグループに追加
- **Device not found**: `i2cdetect -y 1`で確認
- **Communication error**: 配線、電源確認

### MQTT関連
- **Connection refused**: Mosquittoサービス確認
- **Topic not received**: QoS設定確認
- **SSL/TLS error**: 証明書パス確認

### データベース関連
- **Connection timeout**: サービス状態確認
- **Access denied**: ユーザー権限確認
- **Database locked**: 他プロセスの確認

### Python/FastAPI関連
- **Import error**: 仮想環境とパッケージ確認
- **Port already in use**: `netstat`でポート確認
- **Module not found**: PYTHONPATH確認

---

**注意**: 
このファイルは重要な知見の蓄積のためのものです。一時的な作業ログや個人的なメモは `debug/` ディレクトリ以下をご利用ください。