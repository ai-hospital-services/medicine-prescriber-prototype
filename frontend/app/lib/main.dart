import 'package:flutter/material.dart';
import 'symptoms_to_diagnosis/archive.dart';
import 'user/login.dart';
import 'util/config.dart';
import 'util/data.dart';
import 'util/types.dart';
import 'util/util.dart';

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
  late LoggedInState _loggedInState;

  @override
  void initState() {
    super.initState();
    _data = Data();
    _loggedInState = _data.getLoggedInState();
    Util.setLoginInvalidState = _setLoginInvalidState;
  }

  void _setLoginInvalidState() {
    setState(() {
      _data.resetUserLogin();
    });
  }

  void _resetLoggedInState() {
    setState(() {
      _loggedInState = _data.getLoggedInState();
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AI-HOSPITAL.SERVICES",
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: (_loggedInState != LoggedInState.loggedIn)
          ?
          // if user is not logged in
          Login(
              getLoggedInState: _data.getLoggedInState,
              resetUserLogin: _data.resetUserLogin,
              getAuthorisationCode: _data.getAuthorisationCode,
              getAccessToken: _data.getAccessToken,
              getUserProfile: _data.getUserProfile,
              readCachedUserProfile: _data.readCachedUserProfile,
              saveUserProfile: _data.saveUserProfile,
              onCompletion: _resetLoggedInState,
            )
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
