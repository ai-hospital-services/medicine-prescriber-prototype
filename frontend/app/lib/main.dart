import 'package:flutter/material.dart';
import 'config.dart';
import 'lib.dart';
import 'data.dart';
import 'login.dart';
import 'symptoms_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Config().initDone;
  runApp(const App());
}

class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => _AppState();
}

class _AppState extends State<App> {
  late final Data _data;
  late bool _loginFlag;

  @override
  void initState() {
    super.initState();
    Lib.setInvalidLoginState = _setInvalidLoginState;
    _data = Data();
    _loginFlag = false;
  }

  void _setValidLoginState({required String accessToken}) {
    if (accessToken.isEmpty) return;
    _data.set(accessToken: accessToken);
    setState(() {
      _loginFlag = true;
    });
  }

  void _setInvalidLoginState() {
    _data.set(accessToken: null);
    setState(() {
      _loginFlag = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AI-HOSPITAL.SERVICES",
      theme: ThemeData(primarySwatch: Colors.blue),
      home: (!_loginFlag)
          ?
          // if user is not logged in
          Login(setValidLoginState: _setValidLoginState)
          :
          // once user is logged in
          SymptomsPage(
              getSubjectiveSymptomList: _data.getSubjectiveSymptomList(),
              getAssociatedSymptomList: _data.getAssociatedSymptomList(),
              getInvestigationList: _data.getInvestigationList(),
              getGenderList: _data.getGenderList(),
              getAgeGroupList: _data.getAgeGroupList(),
              predictProvisionalDiagnosis: _data.predictProvisionalDiagnosis,
              getAdviseList: _data.getAdviseList,
            ),
    );
  }
}
