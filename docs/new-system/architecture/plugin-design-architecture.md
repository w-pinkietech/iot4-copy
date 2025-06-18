# Plugin Design and Architecture

This document consolidates key design patterns, examples, and implementations for creating a vendor-neutral plugin architecture for IoT systems.

## Table of Contents

1. [SOLID Principles Examples](#solid-principles-examples)
2. [TypeScript Interface Definitions](#typescript-interface-definitions)
3. [Python Plugin Architecture](#python-plugin-architecture)
4. [Vendor Plugin Implementations](#vendor-plugin-implementations)
5. [Config-Based Device Management](#config-based-device-management)
6. [Project Structure](#project-structure)

## SOLID Principles Examples

### Single Responsibility Principle (SRP)

```typescript
// ❌ Poor Design: Multiple Responsibilities
class BravePISensor {
  readValue() { /* センサー読み取り */ }
  parseProtocol() { /* プロトコル解析 */ }
  validateData() { /* データ検証 */ }
  saveToDatabase() { /* DB保存 */ }
}

// ✅ Good Design: Single Responsibility
class Sensor {
  readValue(): Promise<SensorValue> { /* センサー読み取りのみ */ }
}

class ProtocolParser {
  parse(buffer: Buffer): ParsedData { /* プロトコル解析のみ */ }
}

class DataValidator {
  validate(data: any): ValidationResult { /* データ検証のみ */ }
}
```

### Open/Closed Principle (OCP)

```typescript
// Open for extension, closed for modification
abstract class SensorDriver {
  abstract readValue(): Promise<SensorValue>;
  abstract configure(config: SensorConfig): void;
  
  // Common functionality (closed for modification)
  protected logAccess(): void { /* ログ記録 */ }
  protected validateConfig(config: SensorConfig): boolean { /* 設定検証 */ }
}

// New hardware extends without modifying existing code
class ESP32SensorDriver extends SensorDriver {
  readValue(): Promise<SensorValue> { /* ESP32固有実装 */ }
  configure(config: SensorConfig): void { /* ESP32固有設定 */ }
}
```

### Dependency Inversion Principle (DIP)

```typescript
// ❌ Poor Design: Depends on concrete class
class SensorManager {
  private bravePI = new BravePIDevice(); // Concrete class dependency
  
  readSensor() {
    return this.bravePI.readData(); // BravePI-specific method
  }
}

// ✅ Good Design: Depends on abstraction
interface HardwareDevice {
  readData(): Promise<any>;
}

class SensorManager {
  constructor(private device: HardwareDevice) {} // Depends on abstraction
  
  readSensor() {
    return this.device.readData(); // Standard interface
  }
}
```

## TypeScript Interface Definitions

### Hardware Abstraction Layer Interfaces

```typescript
// Unified hardware interface
interface HardwareDevice {
  // Metadata
  getDeviceInfo(): DeviceInfo;
  getCapabilities(): DeviceCapabilities;
  
  // Lifecycle
  initialize(config: DeviceConfig): Promise<void>;
  shutdown(): Promise<void>;
  reset(): Promise<void>;
  
  // Sensor operations
  createSensor(type: SensorType, config: SensorConfig): Promise<Sensor>;
  destroySensor(sensor: Sensor): Promise<void>;
  listSensors(): Promise<Sensor[]>;
  
  // Configuration management
  getConfiguration(): Promise<DeviceConfig>;
  updateConfiguration(config: Partial<DeviceConfig>): Promise<void>;
  
  // Diagnostics & monitoring
  getHealthStatus(): Promise<HealthStatus>;
  runDiagnostics(): Promise<DiagnosticsResult>;
}

// Device information structure
interface DeviceInfo {
  id: string;
  name: string;
  manufacturer: string;
  model: string;
  firmwareVersion: string;
  hardwareVersion: string;
  supportedProtocols: Protocol[];
}

// Device capabilities definition
interface DeviceCapabilities {
  maxSensors: number;
  supportedSensorTypes: SensorType[];
  communicationMethods: CommunicationMethod[];
  powerManagement: PowerCapabilities;
  dataRates: DataRateCapabilities;
}
```

### Unified Protocol Interface

```typescript
// Unified protocol interface
interface ProtocolAdapter {
  getProtocolInfo(): ProtocolInfo;
  
  // Connection management
  connect(endpoint: string, options?: ConnectionOptions): Promise<Connection>;
  disconnect(connection: Connection): Promise<void>;
  
  // Data transmission
  send(connection: Connection, data: any): Promise<void>;
  receive(connection: Connection): Promise<any>;
  
  // Protocol-specific processing
  encodeMessage(message: Message): Buffer;
  decodeMessage(buffer: Buffer): Message;
  validateMessage(message: Message): ValidationResult;
}
```

### Plugin System Interfaces

```typescript
// Plugin metadata
interface PluginManifest {
  name: string;
  version: string;
  description: string;
  author: string;
  
  // Dependencies
  dependencies: PluginDependency[];
  platforms: Platform[];
  nodeVersion: string;
  
  // Capabilities
  capabilities: PluginCapability[];
  entryPoint: string;
  configSchema: JSONSchema;
}

// Base plugin interface
interface Plugin {
  // Metadata
  getName(): string;
  getVersion(): string;
  getDescription(): string;
  
  // Lifecycle
  initialize(context: PluginContext): Promise<void>;
  shutdown(): Promise<void>;
  
  // Functionality
  getCapabilities(): PluginCapability[];
  handleRequest(request: PluginRequest): Promise<PluginResponse>;
}

// Plugin context
interface PluginContext {
  // System services
  getLogger(): Logger;
  getEventBus(): EventBus;
  getConfigManager(): ConfigManager;
  getDataAccess(): DataAccess;
  
  // Inter-plugin communication
  callPlugin(pluginName: string, method: string, params: any): Promise<any>;
  subscribeEvent(eventType: string, handler: EventHandler): void;
  publishEvent(event: PluginEvent): void;
}
```

### Sensor Interfaces

```typescript
// Base sensor interface
interface Sensor {
  // Identification
  getId(): string;
  getType(): SensorType;
  getDeviceId(): string;
  
  // Data reading
  readValue(): Promise<SensorValue>;
  readRawValue(): Promise<number>;
  
  // Configuration
  configure(config: SensorConfig): Promise<void>;
  getConfiguration(): Promise<SensorConfig>;
  
  // Lifecycle
  initialize(): Promise<void>;
  shutdown(): Promise<void>;
  
  // Health monitoring
  getStatus(): Promise<SensorStatus>;
  isHealthy(): Promise<boolean>;
  
  // Events
  on(event: SensorEvent, callback: EventCallback): void;
  off(event: SensorEvent, callback: EventCallback): void;
}

// Sensor value structure
interface SensorValue {
  value: number;
  unit: string;
  timestamp: Date;
  quality: DataQuality;
  metadata?: Record<string, any>;
}

// Sensor configuration structure
interface SensorConfig {
  // Measurement settings
  measurementInterval: number;
  samplingRate: number;
  
  // Calibration settings
  calibration: {
    enabled: boolean;
    scale: number;
    offset: number;
    polynomialCoefficients?: number[];
  };
  
  // Threshold settings
  thresholds: {
    min: number;
    max: number;
    hysteresisHigh?: number;
    hysteresisLow?: number;
  };
  
  // Filter settings
  filtering: {
    enabled: boolean;
    type: FilterType;
    parameters: Record<string, any>;
  };
  
  // Alert settings
  alertRules: {
    enabled: boolean;
    conditions: AlertCondition[];
    actions: AlertAction[];
  };
}
```

## Python Plugin Architecture

### Base Plugin Interface

```python
# common/interfaces/device_interface.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class DeviceCapability:
    """Device capability definition"""
    device_type: str           # "sensor_hub", "plc", "gateway"
    communication: str         # "serial", "ethernet", "mqtt", "modbus"
    sensor_types: List[str]    # ["temperature", "pressure", "acceleration"]
    max_sensors: int          # Maximum number of sensors
    supports_commands: bool   # Command support
    supports_configuration: bool  # Configuration change support

@dataclass 
class SensorReading:
    """Standardized sensor reading value"""
    sensor_id: str
    sensor_type: str          # "temperature", "pressure", etc.
    value: Any               # Measurement value (single or list)
    unit: str                # Unit
    timestamp: str           # ISO8601 format
    quality: float           # Quality indicator (0.0-1.0)
    metadata: Dict[str, Any] # Additional info (RSSI, Battery, etc.)

class DeviceDriverInterface(ABC):
    """Common interface for all device drivers"""
    
    @abstractmethod
    def get_capabilities(self) -> DeviceCapability:
        """Get device capabilities"""
        pass
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize device"""
        pass
    
    @abstractmethod
    async def discover_sensors(self) -> List[Dict[str, str]]:
        """Auto-discover connected sensors"""
        pass
    
    @abstractmethod
    async def read_sensors(self) -> List[SensorReading]:
        """Read data from all sensors"""
        pass
    
    @abstractmethod
    async def send_command(self, command: Dict[str, Any]) -> bool:
        """Send command to device"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check device health"""
        pass
```

### Base Plugin Class

```python
# plugins/base_plugin.py
class DevicePluginBase(DeviceDriverInterface):
    """Base class for plugins"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"plugin.{self.__class__.__name__}")
    
    def get_plugin_info(self) -> Dict[str, str]:
        """Plugin information"""
        return {
            "name": self.__class__.__name__,
            "version": getattr(self, "VERSION", "unknown"),
            "vendor": getattr(self, "VENDOR", "unknown"),
            "description": getattr(self, "DESCRIPTION", "")
        }
```

## Vendor Plugin Implementations

### BravePI Plugin Implementation

```python
# plugins/bravepi_plugin.py
class BravePIPlugin(DevicePluginBase):
    """BravePI-specific plugin"""
    
    VERSION = "1.0.0"
    VENDOR = "Fukuoka Industrial Technology Center"
    DESCRIPTION = "BravePI IoT Hub Driver"
    
    def get_capabilities(self) -> DeviceCapability:
        return DeviceCapability(
            device_type="sensor_hub",
            communication="serial",
            sensor_types=["temperature", "humidity", "digital_input", "digital_output"],
            max_sensors=16,
            supports_commands=True,
            supports_configuration=True
        )
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        try:
            self.serial_port = config["serial_port"]
            self.baud_rate = config.get("baud_rate", 38400)
            self.protocol_handler = BravePIProtocolHandler(
                self.serial_port, self.baud_rate
            )
            await self.protocol_handler.connect()
            return True
        except Exception as e:
            self.logger.error(f"BravePI initialization failed: {e}")
            return False
    
    async def discover_sensors(self) -> List[Dict[str, str]]:
        # BravePI-specific sensor discovery logic
        return await self.protocol_handler.enumerate_sensors()
    
    async def read_sensors(self) -> List[SensorReading]:
        # BravePI-specific data reading logic
        raw_data = await self.protocol_handler.read_all()
        return [self._convert_to_standard_reading(data) for data in raw_data]
```

### OMRON PLC Plugin Implementation

```python
# plugins/omron_plugin.py  
class OMRONFinsPlugin(DevicePluginBase):
    """OMRON PLC FINS communication plugin"""
    
    VERSION = "1.0.0"
    VENDOR = "OMRON"
    DESCRIPTION = "OMRON PLC FINS Protocol Driver"
    
    def get_capabilities(self) -> DeviceCapability:
        return DeviceCapability(
            device_type="plc",
            communication="ethernet", 
            sensor_types=["pressure", "temperature", "flow", "digital_input"],
            max_sensors=1000,
            supports_commands=True,
            supports_configuration=False
        )
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        try:
            from omron_fins import FinsClient  # External library
            self.client = FinsClient(
                config["ip_address"], 
                config["port"],
                config.get("unit_address", 0)
            )
            await self.client.connect()
            return True
        except Exception as e:
            self.logger.error(f"OMRON FINS initialization failed: {e}")
            return False
```

### Generic MQTT Plugin Implementation

```python
# plugins/mqtt_generic_plugin.py
class MQTTGenericPlugin(DevicePluginBase):
    """Generic MQTT device plugin"""
    
    VERSION = "1.0.0"
    VENDOR = "Generic"
    DESCRIPTION = "Generic MQTT Device Driver"
    
    def get_capabilities(self) -> DeviceCapability:
        return DeviceCapability(
            device_type="mqtt_gateway",
            communication="mqtt",
            sensor_types=["any"],  # Any sensor type
            max_sensors=1000,
            supports_commands=True,
            supports_configuration=True
        )
```

## Config-Based Device Management

### Device Configuration YAML

```yaml
# config/devices.yml - Device configuration example
devices:
  - name: "factory_line_1_hub"
    driver: "bravepi"
    config:
      serial_port: "/dev/ttyAMA0"
      baud_rate: 38400
      protocol_version: "1.0"
    sensors:
      - id: "temp_001"
        type: "temperature"
        name: "Factory Temperature"
        thresholds:
          high: 30.0
          low: 10.0
  
  - name: "precision_measurement"
    driver: "bravejig" 
    config:
      usb_ports: ["/dev/ttyACM0", "/dev/ttyACM1"]
      protocol_version: "2.0"
    sensors:
      - id: "accel_001"
        type: "acceleration"
        name: "Vibration Sensor"
        fft_enabled: true
  
  - name: "omron_plc_station"
    driver: "omron_fins"
    config:
      ip_address: "192.168.1.100"
      port: 9600
      unit_address: 0
    sensors:
      - id: "pressure_001"
        type: "pressure"
        name: "Hydraulic Pressure"
        address: "D100"
  
  - name: "keyence_vision"
    driver: "keyence_ethernet"
    config:
      ip_address: "192.168.1.101"
      port: 8500
    sensors:
      - id: "vision_001"
        type: "quality_check"
        name: "Quality Inspection"
  
  - name: "mqtt_generic_device"
    driver: "mqtt_generic"
    config:
      broker: "192.168.1.200"
      topics:
        - "factory/sensors/+/data"
    sensors:
      - id: "ext_temp_001"
        type: "temperature"
        name: "External Temperature"
```

## Project Structure

### Recommended Directory Layout

```
new-iot-platform/
├── packages/
│   ├── core/                    # Core libraries
│   │   ├── src/
│   │   │   ├── domain/         # Domain models
│   │   │   ├── infrastructure/ # Infrastructure layer
│   │   │   └── application/    # Application services
│   │   └── tests/
│   │
│   ├── plugins/                 # Hardware plugins
│   │   ├── bravepi/            # BravePI plugin
│   │   ├── esp32/              # ESP32 plugin
│   │   └── mock/               # Mock for testing
│   │
│   ├── api/                    # REST API
│   │   ├── src/
│   │   │   ├── controllers/    # API controllers
│   │   │   ├── services/       # Business logic
│   │   │   └── middleware/     # Middleware
│   │   └── tests/
│   │
│   ├── web-ui/                 # Web dashboard
│   │   ├── src/
│   │   │   ├── components/     # UI components
│   │   │   ├── pages/          # Page components
│   │   │   └── services/       # Frontend services
│   │   └── tests/
│   │
│   └── cli/                    # CLI tools
│       ├── src/
│       │   ├── commands/       # CLI commands
│       │   └── utils/          # Utilities
│       └── tests/
│
├── tools/                      # Development tools
│   ├── scripts/                # Build/deploy scripts
│   ├── docker/                 # Docker configuration
│   └── docs/                   # Technical documentation
│
├── examples/                   # Samples & tutorials
│   ├── basic-setup/            # Basic setup
│   ├── custom-plugin/          # Custom plugin
│   └── integration/            # Integration examples
│
└── tests/                      # Integration tests
    ├── e2e/                    # E2E tests
    ├── integration/            # Integration tests
    └── performance/            # Performance tests
```

## Summary

This document consolidates the essential design patterns and implementation examples for creating a vendor-neutral plugin architecture. The key principles include:

1. **SOLID Design Principles**: Ensuring maintainable and extensible code
2. **Strong Type Definitions**: Using TypeScript interfaces for clear contracts
3. **Flexible Plugin System**: Supporting multiple vendors through a common interface
4. **Configuration-Driven**: YAML-based device management for easy deployment
5. **Clear Project Structure**: Organized layout for scalable development

This architecture enables seamless integration of various IoT devices from different vendors while maintaining a clean, maintainable codebase.