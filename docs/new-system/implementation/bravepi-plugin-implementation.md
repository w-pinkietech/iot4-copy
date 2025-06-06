# BravePIプラグイン詳細実装

## 概要

BravePI/JIGを疎結合アーキテクチャに統合するための具体的なプラグイン実装を詳述します。既存のBravePI/JIG資産を活用しながら、ベンダー中立的なフレームワークに適合させる設計です。

## BravePIプラグイン実装

### 1. **基本プラグイン構造**

```python
# plugins/bravepi_plugin.py
from typing import Dict, List, Any, Optional
from common.interfaces.device_interface import (
    DeviceDriverInterface, DeviceCapability, SensorReading
)
from plugins.base_plugin import DevicePluginBase
import asyncio
import serial
import struct
import json
from datetime import datetime

class BravePIPlugin(DevicePluginBase):
    """BravePI専用プラグイン実装"""
    
    VERSION = "1.0.0"
    VENDOR = "Fukuoka Industrial Technology Center"
    DESCRIPTION = "BravePI IoT Hub Driver with BLE and GPIO support"
    
    # BravePIプロトコル定義
    PROTOCOL_FRAME = {
        'protocol': 1,    # プロトコルバージョン
        'type': 1,        # メッセージタイプ
        'length': 2,      # データ長
        'timestamp': 4,   # タイムスタンプ
        'device_id': 8,   # デバイスID
        'data': 'variable' # センサーデータ
    }
    
    MESSAGE_TYPES = {
        0x00: "general_data",
        0x01: "downlink_response", 
        0x02: "jig_information",
        0x03: "dfu",
        0xFF: "error_response"
    }
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.serial_connection = None
        self.connected_sensors: Dict[str, Dict] = {}
        self.last_readings: Dict[str, SensorReading] = {}
        
    def get_capabilities(self) -> DeviceCapability:
        return DeviceCapability(
            device_type="sensor_hub",
            communication="serial",
            sensor_types=[
                "temperature", "humidity", "pressure", 
                "digital_input", "digital_output", "acceleration"
            ],
            max_sensors=16,  # BravePI最大センサー数
            supports_commands=True,
            supports_configuration=True
        )
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """BravePIの初期化"""
        try:
            self.serial_port = config.get("serial_port", "/dev/ttyAMA0")
            self.baud_rate = config.get("baud_rate", 38400)
            self.timeout = config.get("timeout", 1.0)
            
            # シリアル接続の確立
            self.serial_connection = serial.Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            
            self.logger.info(f"BravePI connected to {self.serial_port}")
            
            # センサー自動発見
            await self._discover_connected_sensors()
            
            return True
            
        except Exception as e:
            self.logger.error(f"BravePI initialization failed: {e}")
            return False
    
    async def discover_sensors(self) -> List[Dict[str, str]]:
        """接続されたBLEセンサーとGPIOの自動発見"""
        return await self._discover_connected_sensors()
    
    async def _discover_connected_sensors(self) -> List[Dict[str, str]]:
        """BravePI固有のセンサー発見処理"""
        discovered_sensors = []
        
        try:
            # BravePIにセンサー列挙コマンドを送信
            enumerate_command = self._build_command_frame(0x02, b"ENUM_SENSORS")
            self.serial_connection.write(enumerate_command)
            
            # 応答を待機・解析
            response_data = await self._read_serial_response()
            
            for sensor_info in self._parse_sensor_enumeration(response_data):
                sensor_config = {
                    "id": sensor_info["device_id"],
                    "name": sensor_info.get("name", f"Sensor_{sensor_info['device_id']}"),
                    "type": self._determine_sensor_type(sensor_info),
                    "access_type": sensor_info["access_type"],  # 0=BLE, 1=GPIO
                    "metadata": {
                        "rssi": sensor_info.get("rssi"),
                        "battery": sensor_info.get("battery_level")
                    }
                }
                
                self.connected_sensors[sensor_config["id"]] = sensor_config
                discovered_sensors.append(sensor_config)
            
            self.logger.info(f"Discovered {len(discovered_sensors)} sensors on BravePI")
            return discovered_sensors
            
        except Exception as e:
            self.logger.error(f"Sensor discovery failed: {e}")
            return []
    
    async def read_sensors(self) -> List[SensorReading]:
        """全センサーからのデータ読み取り"""
        readings = []
        
        try:
            # BravePIからの生データ読み取り
            raw_frames = await self._read_all_sensor_data()
            
            for frame in raw_frames:
                reading = self._convert_frame_to_reading(frame)
                if reading:
                    readings.append(reading)
                    self.last_readings[reading.sensor_id] = reading
            
            return readings
            
        except Exception as e:
            self.logger.error(f"Failed to read sensors: {e}")
            return []
    
    async def _read_all_sensor_data(self) -> List[Dict]:
        """BravePIプロトコルに基づく全センサーデータ読み取り"""
        frames = []
        
        # データ要求コマンドを送信
        read_command = self._build_command_frame(0x00, b"READ_ALL")
        self.serial_connection.write(read_command)
        
        # 複数フレームの受信処理
        timeout_count = 0
        max_timeout = 10
        
        while timeout_count < max_timeout:
            try:
                frame_data = await self._read_serial_response()
                if frame_data:
                    parsed_frame = self._parse_protocol_frame(frame_data)
                    if parsed_frame:
                        frames.append(parsed_frame)
                        timeout_count = 0  # データ受信でタイムアウトリセット
                else:
                    timeout_count += 1
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.warning(f"Frame read error: {e}")
                timeout_count += 1
        
        return frames
    
    def _parse_protocol_frame(self, raw_data: bytes) -> Optional[Dict]:
        """BravePIプロトコルフレームの解析"""
        try:
            if len(raw_data) < 16:  # 最小フレームサイズ
                return None
            
            # フレームヘッダー解析
            protocol = struct.unpack('B', raw_data[0:1])[0]
            msg_type = struct.unpack('B', raw_data[1:2])[0]
            length = struct.unpack('<H', raw_data[2:4])[0]
            timestamp = struct.unpack('<I', raw_data[4:8])[0]
            device_id = raw_data[8:16].decode('utf-8').rstrip('\\x00')
            
            # データ部分の抽出
            data_start = 16
            data_end = data_start + length
            sensor_data = raw_data[data_start:data_end]
            
            return {
                "protocol": protocol,
                "type": msg_type,
                "length": length,
                "timestamp": timestamp,
                "device_id": device_id,
                "data": sensor_data
            }
            
        except Exception as e:
            self.logger.error(f"Frame parsing error: {e}")
            return None
    
    def _convert_frame_to_reading(self, frame: Dict) -> Optional[SensorReading]:
        """プロトコルフレームを標準SensorReadingに変換"""
        try:
            device_id = frame["device_id"]
            sensor_config = self.connected_sensors.get(device_id)
            
            if not sensor_config:
                self.logger.warning(f"Unknown sensor: {device_id}")
                return None
            
            # センサータイプ別のデータ解析
            sensor_type = sensor_config["type"]
            raw_value = self._extract_sensor_value(frame["data"], sensor_type)
            
            # 標準化されたSensorReadingオブジェクトを作成
            reading = SensorReading(
                sensor_id=device_id,
                sensor_type=sensor_type,
                value=raw_value["value"],
                unit=raw_value["unit"],
                timestamp=datetime.fromtimestamp(frame["timestamp"]).isoformat(),
                quality=self._calculate_quality(frame, sensor_config),
                metadata=self._extract_metadata(frame, sensor_config)
            )
            
            return reading
            
        except Exception as e:
            self.logger.error(f"Reading conversion error: {e}")
            return None
    
    def _extract_sensor_value(self, data: bytes, sensor_type: str) -> Dict:
        """センサータイプ別の値抽出"""
        try:
            if sensor_type == "temperature":
                # 温度センサー（float, 4バイト）
                temp_celsius = struct.unpack('<f', data[0:4])[0]
                return {"value": round(temp_celsius, 2), "unit": "celsius"}
            
            elif sensor_type == "humidity":
                # 湿度センサー（float, 4バイト）
                humidity_percent = struct.unpack('<f', data[0:4])[0]
                return {"value": round(humidity_percent, 1), "unit": "percent"}
            
            elif sensor_type == "pressure":
                # 圧力センサー（float, 4バイト）
                pressure_pa = struct.unpack('<f', data[0:4])[0]
                return {"value": round(pressure_pa, 1), "unit": "pascal"}
            
            elif sensor_type == "digital_input":
                # デジタル入力（boolean, 1バイト）
                digital_state = struct.unpack('B', data[0:1])[0]
                return {"value": bool(digital_state), "unit": "boolean"}
            
            elif sensor_type == "acceleration":
                # 加速度センサー（X,Y,Z float, 12バイト）
                x, y, z = struct.unpack('<fff', data[0:12])
                return {
                    "value": [round(x, 3), round(y, 3), round(z, 3)],
                    "unit": "g"
                }
            
            else:
                # 未知のセンサータイプ
                return {"value": data.hex(), "unit": "raw"}
                
        except Exception as e:
            self.logger.error(f"Value extraction error for {sensor_type}: {e}")
            return {"value": None, "unit": "error"}
    
    def _calculate_quality(self, frame: Dict, sensor_config: Dict) -> float:
        """センサー品質指標の計算"""
        quality = 1.0
        
        # BLEセンサーの場合、RSSI基づく品質判定
        if sensor_config["access_type"] == 0:  # BLE
            rssi = sensor_config["metadata"].get("rssi")
            if rssi:
                # RSSI -40〜-80の範囲で品質を計算
                if rssi >= -40:
                    quality = 1.0
                elif rssi <= -80:
                    quality = 0.1
                else:
                    quality = 1.0 - (abs(rssi) - 40) / 40 * 0.9
        
        # バッテリーレベルでの品質減算
        battery = sensor_config["metadata"].get("battery")
        if battery and battery < 20:  # 20%以下
            quality *= 0.5
        
        return max(0.0, min(1.0, quality))
    
    def _extract_metadata(self, frame: Dict, sensor_config: Dict) -> Dict[str, Any]:
        """メタデータの抽出"""
        metadata = {}
        
        # BLE固有のメタデータ
        if sensor_config["access_type"] == 0:  # BLE
            metadata.update({
                "rssi": sensor_config["metadata"].get("rssi"),
                "battery_level": sensor_config["metadata"].get("battery"),
                "connection_type": "bluetooth_le"
            })
        else:  # GPIO
            metadata.update({
                "connection_type": "gpio",
                "gpio_pin": sensor_config.get("gpio_pin")
            })
        
        # プロトコル情報
        metadata.update({
            "protocol": "bravepi",
            "protocol_version": frame["protocol"],
            "message_type": self.MESSAGE_TYPES.get(frame["type"], "unknown")
        })
        
        return metadata
    
    async def send_command(self, command: Dict[str, Any]) -> bool:
        """BravePIへのコマンド送信"""
        try:
            command_type = command.get("type")
            target_sensor = command.get("sensor_id")
            parameters = command.get("parameters", {})
            
            if command_type == "gpio_output":
                return await self._send_gpio_command(target_sensor, parameters)
            elif command_type == "calibration":
                return await self._send_calibration_command(target_sensor, parameters)
            elif command_type == "sleep_wake":
                return await self._send_power_command(target_sensor, parameters)
            else:
                self.logger.warning(f"Unknown command type: {command_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Command sending failed: {e}")
            return False
    
    async def _send_gpio_command(self, sensor_id: str, params: Dict) -> bool:
        """GPIO出力コマンドの送信"""
        try:
            pin_number = params.get("pin", 0)
            state = params.get("state", False)
            
            # GPIO制御コマンドフレームの構築
            gpio_data = struct.pack('<BB', pin_number, int(state))
            command_frame = self._build_command_frame(0x01, gpio_data, sensor_id)
            
            self.serial_connection.write(command_frame)
            
            # 応答確認
            response = await self._read_serial_response(timeout=2.0)
            return self._validate_command_response(response)
            
        except Exception as e:
            self.logger.error(f"GPIO command failed: {e}")
            return False
    
    def _build_command_frame(self, cmd_type: int, data: bytes, device_id: str = "") -> bytes:
        """BravePIコマンドフレームの構築"""
        protocol = 1
        length = len(data)
        timestamp = int(datetime.now().timestamp())
        device_id_bytes = device_id.ljust(8, '\\x00')[:8].encode('utf-8')
        
        frame = struct.pack('<BBH', protocol, cmd_type, length)
        frame += struct.pack('<I', timestamp)
        frame += device_id_bytes
        frame += data
        
        return frame
    
    async def health_check(self) -> Dict[str, Any]:
        """BravePI健全性チェック"""
        health_status = {
            "status": "healthy",
            "connection": "connected",
            "sensor_count": len(self.connected_sensors),
            "last_communication": None,
            "errors": []
        }
        
        try:
            # 通信テスト
            test_command = self._build_command_frame(0x00, b"PING")
            self.serial_connection.write(test_command)
            
            response = await self._read_serial_response(timeout=5.0)
            if response:
                health_status["last_communication"] = datetime.now().isoformat()
            else:
                health_status["status"] = "warning"
                health_status["errors"].append("No response to ping command")
            
            # センサー状態チェック
            offline_sensors = []
            for sensor_id, config in self.connected_sensors.items():
                if sensor_id not in self.last_readings:
                    offline_sensors.append(sensor_id)
            
            if offline_sensors:
                health_status["status"] = "degraded"
                health_status["errors"].append(f"Offline sensors: {offline_sensors}")
            
        except Exception as e:
            health_status["status"] = "error"
            health_status["connection"] = "disconnected"
            health_status["errors"].append(str(e))
        
        return health_status
    
    async def _read_serial_response(self, timeout: float = 1.0) -> Optional[bytes]:
        """シリアル応答の非同期読み取り"""
        try:
            # タイムアウト付きで応答を待機
            start_time = asyncio.get_event_loop().time()
            response_data = b""
            
            while (asyncio.get_event_loop().time() - start_time) < timeout:
                if self.serial_connection.in_waiting > 0:
                    chunk = self.serial_connection.read(self.serial_connection.in_waiting)
                    response_data += chunk
                    
                    # フレーム完了チェック（最小フレームサイズ）
                    if len(response_data) >= 16:
                        return response_data
                
                await asyncio.sleep(0.01)  # CPU負荷軽減
            
            return response_data if response_data else None
            
        except Exception as e:
            self.logger.error(f"Serial read error: {e}")
            return None
```

### 2. **BraveJIGプラグイン実装**

```python
# plugins/bravejig_plugin.py
class BraveJIGPlugin(DevicePluginBase):
    """BraveJIG専用プラグイン実装"""
    
    VERSION = "1.0.0"
    VENDOR = "Fukuoka Industrial Technology Center"
    DESCRIPTION = "BraveJIG USB Sensor Hub Driver with FFT support"
    
    def get_capabilities(self) -> DeviceCapability:
        return DeviceCapability(
            device_type="sensor_hub",
            communication="usb_serial",
            sensor_types=[
                "illuminance", "acceleration", "temperature", 
                "humidity", "pressure", "distance", "digital_input", "digital_output"
            ],
            max_sensors=8,  # BraveJIG最大センサー数
            supports_commands=True,
            supports_configuration=True
        )
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """BraveJIG初期化（複数USBポート対応）"""
        try:
            self.usb_ports = config.get("usb_ports", ["/dev/ttyACM0"])
            self.connections: Dict[str, serial.Serial] = {}
            
            # 複数USBポートへの接続
            for port in self.usb_ports:
                try:
                    connection = serial.Serial(
                        port=port,
                        baudrate=38400,
                        timeout=1.0
                    )
                    self.connections[port] = connection
                    self.logger.info(f"BraveJIG connected to {port}")
                except Exception as e:
                    self.logger.warning(f"Failed to connect to {port}: {e}")
            
            if not self.connections:
                raise Exception("No BraveJIG connections established")
            
            # 各ポートでセンサー発見
            await self._discover_all_jig_sensors()
            return True
            
        except Exception as e:
            self.logger.error(f"BraveJIG initialization failed: {e}")
            return False
    
    async def read_sensors(self) -> List[SensorReading]:
        """全BraveJIGポートからのデータ読み取り"""
        all_readings = []
        
        for port, connection in self.connections.items():
            try:
                port_readings = await self._read_jig_port_data(port, connection)
                all_readings.extend(port_readings)
            except Exception as e:
                self.logger.error(f"Failed to read from {port}: {e}")
        
        return all_readings
    
    async def _read_jig_port_data(self, port: str, connection: serial.Serial) -> List[SensorReading]:
        """単一BraveJIGポートからのデータ読み取り"""
        readings = []
        
        # BraveJIG固有のデータ要求プロトコル
        read_command = self._build_jig_command(0x00, b"READ_ALL")
        connection.write(read_command)
        
        # 応答データの解析
        response = await self._read_jig_response(connection)
        if response:
            parsed_data = self._parse_jig_response(response)
            
            for sensor_data in parsed_data:
                reading = self._convert_jig_data_to_reading(sensor_data, port)
                if reading:
                    readings.append(reading)
        
        return readings
```

### 3. **プラグイン登録とテスト**

```python
# tests/test_bravepi_plugin.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from plugins.bravepi_plugin import BravePIPlugin

class TestBravePIPlugin:
    
    @pytest.fixture
    def plugin_config(self):
        return {
            "serial_port": "/dev/ttyAMA0",
            "baud_rate": 38400,
            "timeout": 1.0
        }
    
    @pytest.fixture  
    def bravepi_plugin(self, plugin_config):
        return BravePIPlugin(plugin_config)
    
    def test_get_capabilities(self, bravepi_plugin):
        """機能定義の確認"""
        capabilities = bravepi_plugin.get_capabilities()
        
        assert capabilities.device_type == "sensor_hub"
        assert capabilities.communication == "serial"
        assert "temperature" in capabilities.sensor_types
        assert capabilities.supports_commands is True
    
    @patch('serial.Serial')
    async def test_initialization(self, mock_serial, bravepi_plugin, plugin_config):
        """初期化テスト"""
        mock_connection = Mock()
        mock_serial.return_value = mock_connection
        
        success = await bravepi_plugin.initialize(plugin_config)
        
        assert success is True
        mock_serial.assert_called_once()
        assert bravepi_plugin.serial_connection == mock_connection
    
    async def test_sensor_discovery(self, bravepi_plugin):
        """センサー発見テスト"""
        # モックデータの準備
        with patch.object(bravepi_plugin, '_discover_connected_sensors') as mock_discover:
            mock_discover.return_value = [
                {"id": "ble_temp_001", "type": "temperature", "name": "温度センサー"},
                {"id": "gpio_input_001", "type": "digital_input", "name": "GPIO入力"}
            ]
            
            sensors = await bravepi_plugin.discover_sensors()
            
            assert len(sensors) == 2
            assert sensors[0]["type"] == "temperature"
            assert sensors[1]["type"] == "digital_input"
```

## 移行メリット

### 1. **既存資産の活用**
- BravePI/JIGハードウェアをそのまま利用
- 既存のプロトコル知識を活用
- 段階的な移行が可能

### 2. **標準化された統合**
- 他社製品と同じインターフェース
- 統一されたMQTTメッセージフォーマット
- 共通のUI/API

### 3. **将来への投資**
- 新デバイスの容易な追加
- ベンダーロックイン回避
- オープンエコシステム構築

この実装により、BravePI/JIGを疎結合アーキテクチャに統合し、他社製品との相互運用性を確保できます。