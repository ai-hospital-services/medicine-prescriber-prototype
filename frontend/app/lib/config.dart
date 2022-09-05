import 'package:flutter/services.dart';
import 'package:yaml/yaml.dart';

class Config {
  static dynamic map;

  Future<void> loadAsset() async {
    final configString = await rootBundle.loadString("assets/config.yaml");
    Config.map = loadYaml(configString);
  }
}
