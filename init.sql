CREATE TABLE `sensor_types`(
  `sensor_type_id` INT NOT NULL PRIMARY KEY COMMENT 'センサー種別ID',
  `sensor_type_text` VARCHAR(255) NOT NULL COMMENT 'センサー種別名',
  `measurement` VARCHAR(63) NOT NULL UNIQUE COMMENT 'テーブル名'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'センサー種別テーブル';

CREATE TABLE `sensor_channels`(
  `sensor_channel_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'センサーチャンネルID',
  `sensor_type_id` INT NOT NULL COMMENT 'センサー種別ID',
  `channel` VARCHAR(31) NOT NULL COMMENT 'チャンネル',
  `channel_name` VARCHAR(63) NOT NULL COMMENT 'チャンネル名',
  `unit` VARCHAR(63) NOT NULL COMMENT '単位',
  `fraction` TINYINT UNSIGNED NOT NULL COMMENT '画面表示上の小数点以下の桁数',
  `hysteresis_min` FLOAT NOT NULL COMMENT 'ヒステリシス最小値',
  `hysteresis_max` FLOAT NOT NULL COMMENT 'ヒステリシス最大値',
  `hysteresis_step` FLOAT NOT NULL COMMENT 'ヒステリシスステップ',
  `hysteresis_default` FLOAT NOT NULL COMMENT 'ヒステリシスデフォルト値',
  `offset_range` FLOAT NOT NULL COMMENT 'オフセットレンジ',
  UNIQUE(`sensor_type_id`, `channel`, `channel_name`),
  FOREIGN KEY (`sensor_type_id`) REFERENCES `sensor_types`(`sensor_type_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'センサーチャンネルテーブル';

CREATE TABLE `devices`(
  `device_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'デバイスID',
  `device_name` VARCHAR(255) NOT NULL UNIQUE COMMENT 'デバイス名',
  `sensor_type_id` INT NOT NULL COMMENT 'センサー種別ID',
  `access_type` TINYINT NOT NULL COMMENT '通信区分',
  `is_save_data` BOOLEAN DEFAULT TRUE NOT NULL COMMENT 'データ保存の可否',
  `is_save_count` BOOLEAN DEFAULT FALSE NOT NULL COMMENT 'カウント保存の可否',
  INDEX(`device_name`),
  FOREIGN KEY (`sensor_type_id`) REFERENCES `sensor_types`(`sensor_type_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'デバイステーブル';

CREATE TABLE `ble_device_configs` (
  `ble_device_config_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'BLEデバイス設定ID',
  `device_number` BIGINT NOT NULL UNIQUE COMMENT 'デバイスID',
  `timezone` BOOLEAN DEFAULT FALSE NOT NULL COMMENT 'タイムゾーン',
  `ble_mode` BOOLEAN DEFAULT FALSE NOT NULL COMMENT 'Bluetooth通信モード',
  `tx_power` TINYINT DEFAULT 0 NOT NULL COMMENT '送信電波出力',
  `advertise_interval` SMALLINT DEFAULT 1000 NOT NULL COMMENT 'Advertise発信間隔[ms]',
  `uplink_interval` INT DEFAULT 60 NOT NULL COMMENT 'Uplink間隔[s]',
  `measurement_mode` TINYINT DEFAULT 0 NOT NULL COMMENT '計測モード',
  `sampling_interval` TINYINT DEFAULT 0 NOT NULL COMMENT 'サンプリング周期',
  `device_id` INT NOT NULL UNIQUE COMMENT 'デバイスID',
  INDEX(`device_number`),
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'BLEデバイス設定テーブル';

CREATE TABLE `usb_device_configs` (
  `usb_device_config_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'USBデバイス設定ID',
  `device_number` BIGINT NOT NULL UNIQUE COMMENT 'デバイスID',
  `advertise_interval` SMALLINT DEFAULT 1000 NOT NULL COMMENT 'Advertise発信間隔[ms]',
  `uplink_interval` INT DEFAULT 60 NOT NULL COMMENT 'Uplink間隔[s]',
  `device_id` INT NOT NULL UNIQUE COMMENT 'デバイスID',
  INDEX(`device_number`),
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'USBデバイス設定テーブル';

CREATE TABLE `i2c_device_configs` (
  `i2c_device_config_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'I2Cデバイス設定ID',
  `address` SMALLINT NOT NULL UNIQUE COMMENT 'I2Cアドレス',
  `output_interval` INT DEFAULT 1000 NOT NULL COMMENT '出力間隔[ms]',
  `device_id` INT NOT NULL UNIQUE COMMENT 'デバイスID',
  INDEX(`address`),
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'I2Cデバイス設定テーブル';

CREATE TABLE `gpio_device_configs` (
  `gpio_device_config_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'GPIOデバイス設定ID',
  `gpio_index` TINYINT NOT NULL UNIQUE COMMENT 'GPIOピン番号インデックス',
  `device_id` INT NOT NULL UNIQUE COMMENT 'デバイスID',
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'GPIOデバイス設定テーブル';

CREATE TABLE `http_device_configs` (
  `http_device_config_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'HTTPデバイス設定ID',
  `http_sensor_name` VARCHAR (255) NOT NULL UNIQUE COMMENT 'HTTPセンサー名',
  `device_id` INT NOT NULL UNIQUE COMMENT 'デバイスID',
  INDEX(`http_sensor_name`),
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'HTTPデバイス設定テーブル';

CREATE TABLE `mqtt_brokers` (
  `mqtt_broker_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'MQTTブローカー設定ID',
  `broker` VARCHAR (255) NOT NULL COMMENT 'ブローカーホスト',
  `port` SMALLINT UNSIGNED NOT NULL COMMENT 'ポート番号',
  `username` VARCHAR (255) COMMENT 'ユーザー',
  `password` VARCHAR (255) COMMENT 'パスワード'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'MQTTブローカー設定テーブル';

CREATE TABLE `mqtt_topics` (
  `mqtt_topic_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'MQTTトピックID',
  `topic` VARCHAR (255) NOT NULL COMMENT 'トピック',
  `retain` BOOLEAN NOT NULL COMMENT '保持',
  `qos` TINYINT NOT NULL COMMENT 'QoS',
  `mqtt_broker_id` INT NOT NULL COMMENT 'MQTTブローカー設定ID',
  UNIQUE(`topic`, `mqtt_broker_id`),
  FOREIGN KEY (`mqtt_broker_id`) REFERENCES `mqtt_brokers`(`mqtt_broker_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'MQTTトピックテーブル';

CREATE TABLE `mail_servers` (
  `mail_server_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'メールサーバー設定ID',
  `smtp_host` VARCHAR(255) NOT NULL COMMENT 'SMTPホスト',
  `smtp_port` SMALLINT UNSIGNED DEFAULT 25 NOT NULL COMMENT 'SMTPポート',
  `from` VARCHAR(255) NOT NULL COMMENT '送信元アドレス',
  `user` VARCHAR(255) COMMENT 'ユーザー',
  `password` VARCHAR(255) COMMENT 'パスワード',
  `secure` BOOLEAN DEFAULT FALSE NOT NULL COMMENT '安全な接続を使用する',
  `tls` BOOLEAN DEFAULT FALSE NOT NULL COMMENT 'TLSチェックサーバー証明書'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'メールサーバー設定テーブル';

CREATE TABLE `mail_addresses`(
  `mail_address_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'メールアドレス設定テーブル',
  `to` VARCHAR(255) NOT NULL COMMENT '送信先アドレス',
  `mail_server_id` INT NOT NULL COMMENT 'メールサーバー設定ID',
  UNIQUE(`to`, `mail_server_id`),
  FOREIGN KEY (`mail_server_id`) REFERENCES `mail_servers`(`mail_server_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'メールアドレス設定テーブル';

CREATE TABLE `sensors` (
  `sensor_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'センサーID',
  `channel` VARCHAR(31) NOT NULL COMMENT 'チャンネル',
  `count` INT DEFAULT 0 NOT NULL COMMENT 'カウント',
  `take_photo` BOOLEAN DEFAULT FALSE NOT NULL COMMENT '写真撮影',
  `toggle` BOOLEAN DEFAULT FALSE NOT NULL COMMENT '反転',
  `extra_mqtt` JSON DEFAULT '{}' NOT NULL COMMENT 'MQTT追加送信情報',
  `hysteresis_high` FLOAT NOT NULL COMMENT 'ヒステリシスHigh',
  `hysteresis_low` FLOAT NOT NULL COMMENT 'ヒステリシスLow',
  `debounce_high` FLOAT UNSIGNED DEFAULT 0 NOT NULL COMMENT 'デバウンスHigh',
  `debounce_low` FLOAT UNSIGNED DEFAULT 0 NOT NULL COMMENT 'デバウンスLow',
  `offset` FLOAT DEFAULT 0 NOT NULL COMMENT 'オフセット',
  `device_id` INT NOT NULL COMMENT 'デバイスID',
  UNIQUE(`device_id`, `channel`),
  FOREIGN KEY (`device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'センサーテーブル';

CREATE TABLE `sensor_mqtt_pivots`(
  `sensor_mqtt_pivot_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'センサーMQTT交差ID',
  `sensor_id` INT NOT NULL COMMENT 'センサーID',
  `mqtt_topic_id` INT NOT NULL COMMENT 'MQTTトピックID',
  UNIQUE(`sensor_id`, `mqtt_topic_id`),
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE,
  FOREIGN KEY (`mqtt_topic_id`) REFERENCES `mqtt_topics`(`mqtt_topic_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'センサーMQTT交差テーブル';

CREATE TABLE `sensor_mail_pivots`(
  `sensor_mail_pivot_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'センサーメール交差ID',
  `sensor_id` INT NOT NULL COMMENT 'センサーID',
  `mail_address_id` INT NOT NULL COMMENT 'メールアドレスID',
  UNIQUE(`sensor_id`, `mail_address_id`),
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE,
  FOREIGN KEY (`mail_address_id`) REFERENCES `mail_addresses`(`mail_address_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'センサーメール交差テーブル';

CREATE TABLE `sensor_gpio_output_pivots` (
  `sensor_gpio_output_pivot_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'センサーGPIO出力交差ID',
  `sensor_id` INT NOT NULL COMMENT 'センサーID',
  `gpio_output_device_id` INT COMMENT 'GPIO出力デバイスID',
  UNIQUE(`sensor_id`, `gpio_output_device_id`),
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE,
  FOREIGN KEY (`gpio_output_device_id`) REFERENCES `devices`(`device_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'センサーGPIO出力交差テーブル';

CREATE TABLE `gpio_inputs` (
  `gpio_input_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'GPIO入力設定ID',
  `chattering` SMALLINT UNSIGNED DEFAULT 0 NOT NULL COMMENT 'チャタリング時間[ms]',
  `sensor_id` INT NOT NULL UNIQUE COMMENT 'センサーID',
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'GPIO入力設定テーブル';

CREATE TABLE `gpio_outputs` (
  `gpio_output_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'GPIO出力設定ID',
  `init_state` BOOLEAN DEFAULT FALSE NOT NULL COMMENT '初期出力',
  `signal_out_time` SMALLINT UNSIGNED DEFAULT 0 NOT NULL COMMENT '接点出力時間[ms]',
  `sensor_id` INT NOT NULL UNIQUE COMMENT 'センサーID',
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'GPIO出力設定テーブル';

CREATE TABLE `temperatures` (
  `temperature_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '温度センサー設定ID',
  `thermocouple_type` TINYINT DEFAULT 0 NOT NULL COMMENT '熱電対タイプ',
  `sensor_id` INT NOT NULL UNIQUE COMMENT 'センサーID',
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '温度センサー設定テーブル';

CREATE TABLE `adcs` (
  `adc_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'ADCセンサー設定ID',
  `gain` TINYINT DEFAULT 0 NOT NULL COMMENT 'ゲイン',
  `magnification` FLOAT DEFAULT 1 NOT NULL COMMENT '表示倍率',
  `display_name`  VARCHAR(63) DEFAULT '' NOT NULL COMMENT '表示名',
  `display_unit` VARCHAR(63) DEFAULT '' NOT NULL COMMENT '表示単位',
  `sensor_id` INT NOT NULL UNIQUE COMMENT 'センサーID',
  FOREIGN KEY (`sensor_id`) REFERENCES `sensors`(`sensor_id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'ADCセンサー設定テーブル';

ALTER DATABASE iotkit CHARACTER SET utf8mb4;

INSERT INTO
  `mqtt_brokers`(`broker`, `port`, `username`, `password`)
VALUES
  ('localhost', 1883, 'iotkit', 'iotkit');

INSERT INTO
  `mail_servers`(`smtp_host`, `smtp_port`, `from`)
VALUES
  ('localhost', 25, '"IoT導入支援キット"<iotkit@fitc.pref.fukuoka.jp>');

INSERT INTO
  `sensor_types`(`sensor_type_id`, `sensor_type_text`, `measurement`)
VALUES
  (257, '接点入力', 'gpio_input'),
  (258, '接点出力', 'gpio_output'),
  (259, 'ADC', 'voltage'),
  (260, '測距', 'distance'),
  (261, '熱電対', 'temperature'),
  (262, '加速度', 'acceleration'),
  (263, '差圧', 'pressure'),
  (264, '照度', 'illuminance'),
  (289, '照度', 'illuminance_jig'),
  (290, '加速度', 'acceleration_jig'),
  (291, '温湿度', 'environment_jig'),
  (292, '気圧', 'atmospheric_jig'),
  (293, '測距', 'distance_jig');

INSERT INTO
  `sensor_channels`(`sensor_type_id`, `channel`, `channel_name`, `unit`, `fraction`,
  `hysteresis_min`,`hysteresis_max`, `hysteresis_step`, `hysteresis_default`, `offset_range`)
VALUES
  (257, '', '', '', 0, 0.5, 0.5, 0, 0.5, 0),
  (258, '', '', '', 0, 0.5, 0.5, 0, 0.5, 0),
  (259, 'CH1', '電圧', 'mV', 0, -2000, 2000, 10, 100, 500),
  (259, 'CH2', '電圧', 'mV', 0, -2000, 2000, 10, 100, 500),
  (260, '', '距離', 'mm', 0, 0, 2000, 10, 500, 500),
  (261, '', '温度', '℃', 1, -50, 2000, 1, 20, 10),
  (262, 'X', '加速度', 'G', 1, -6.5, 6.5, 0.5, 0, 2),
  (262, 'Y', '加速度', 'G', 1, -6.5, 6.5, 0.5, 0, 2),
  (262, 'Z', '加速度', 'G', 1, -6.5, 6.5, 0.5, 0, 2),
  (262, 'COMP', '加速度', 'G', 1, 0, 6.5, 0.5, 0, 2),
  (263, '', '差圧', 'Pa', 1, -500, 500, 10, 0, 100),
  (264, '', '照度', 'lux', 0, 40, 83865, 100, 500, 500),
  (289, '', '照度', 'lux', 0, 40, 83865, 100, 500, 500),
  (290, 'X', '加速度', 'G', 1, -6.5, 6.5, 0.5, 0, 2),
  (290, 'Y', '加速度', 'G', 1, -6.5, 6.5, 0.5, 0, 2),
  (290, 'Z', '加速度', 'G', 1, -6.5, 6.5, 0.5, 0, 2),
  (290, 'COMP', '加速度', 'G', 1, 0, 6.5, 0.5, 0, 2),
  (291, '温度', '温度', '℃', 1, -40, 125, 1, 20, 10),
  (291, '湿度', '湿度', '%', 1, 0, 100, 1, 20, 10),
  (292, '', '気圧', 'hPa', 0, 260, 1260, 10, 1000, 20),
  (293, '', '距離', 'mm', 0, 40, 1300, 10, 500, 500);