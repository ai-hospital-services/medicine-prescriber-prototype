import 'package:flutter/material.dart';
import 'config.dart';
import 'data.dart';
import 'symptoms_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Config().loadAsset();
  runApp(App());
}

class App extends StatelessWidget {
  final Data _data;

  App({super.key}) : _data = Data();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AI-HOSPITAL.SERVICES",
      theme: ThemeData(primarySwatch: Colors.blue),
      home: SymptomsPage(
        getSubjectiveSymptomList: _data.getSubjectiveSymptomList(),
        getObjectiveSymptomList: _data.getObjectiveSymptomList(),
        getGenderList: _data.getGenderList(),
        getEtiologyList: _data.getEtiologyList(),
        predictCause: _data.predictCause,
        mapPredictCauseWithEtiology: _data.mapPredictCauseWithEtiology,
        getDrugList: _data.getDrugList,
      ),
    );
  }
}
