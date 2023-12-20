import 'package:flutter/services.dart';
import 'package:yaml/yaml.dart';

class Config {
  static late final dynamic map;
  late final Future _initDone;

  Config() {
    _initDone = _init();
  }

  Future get initDone => _initDone;

  Future _init() async {
    final configString = await rootBundle.loadString("assets/config.yaml");
    Config.map = loadYaml(configString);
  }
}
