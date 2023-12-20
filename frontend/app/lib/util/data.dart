import 'dart:convert';
import 'package:oauth2_client/oauth2_client.dart';
import 'package:tuple/tuple.dart';
import 'package:yaml/yaml.dart';
import 'config.dart';
import 'types.dart';
import 'util.dart';

class Data {
  late final String _backendAPIURL;

  late String? _authorisationCode;
  late String? _accessToken;
  late UserProfile? _userProfile;

  late final String _stateValue;
  late final OAuth2Client _oauth2Client;

  Data()
      : _backendAPIURL = Config.map["backendAPIURL"],
        _authorisationCode = null,
        _accessToken = null,
        _userProfile = null,
        _stateValue = "STATE_VALUE",
        _oauth2Client = OAuth2Client(
            authorizeUrl: Config.map["authoriseURL"],
            tokenUrl: "",
            redirectUri: Config.map["redirectURL"],
            customUriScheme: "");

  // region: user

  LoggedInState getLoggedInState() {
    if (_userProfile != null) {
      if (_userProfile!.isComplete) {
        return LoggedInState.loggedIn;
      } else {
        return LoggedInState.gotUserProfile;
      }
    } else if (_accessToken != null && _accessToken!.isNotEmpty) {
      return LoggedInState.gotAccessToken;
    } else if (_authorisationCode != null && _authorisationCode!.isNotEmpty) {
      return LoggedInState.gotAuthorisationCode;
    }
    return LoggedInState.notLoggedIn;
  }

  void resetUserLogin() {
    _authorisationCode = null;
    _accessToken = null;
    _userProfile = null;
  }

  Future<Tuple2<bool, String?>> getAuthorisationCode() async {
    bool success;
    String? error;
    try {
      final response = await _oauth2Client.requestAuthorization(
          clientId: Config.map["clientID"],
          scopes: <String>[...(Config.map["scopes"] as YamlList)],
          state: _stateValue,
          customParams: {"audience": Config.map["audience"]});
      if (response.code == null || response.code!.isEmpty) {
        error = "User login failure: no authorisation code in response";
        success = false;
        _setAuthorisationCode(null);
      } else {
        error = null;
        success = true;
        _setAuthorisationCode(response.code!);
      }
    } catch (e) {
      error = "User login failure: $e";
      success = false;
      _setAuthorisationCode(null);
    }
    return Tuple2(success, error);
  }

  _setAuthorisationCode(String? authorisationCode) {
    _authorisationCode = authorisationCode;
    _accessToken = null;
    _userProfile = null;
  }

  Future<Tuple2<bool, String?>> getAccessToken() async {
    bool success;
    String? error;
    try {
      final response = await Util.httpGet(
          url: "$_backendAPIURL/get-access-token/$_authorisationCode");
      if (response.startsWith("Error")) {
        error = "User login failure: $response";
        success = false;
      } else {
        final decodedResponse = jsonDecode(response) as Map;
        if (decodedResponse["access_token"] == null ||
            (decodedResponse["access_token"] as String).isEmpty) {
          error = "User login failure: no access token in response";
          success = false;
          _setAccessToken(null);
        } else {
          error = null;
          success = true;
          _setAccessToken(decodedResponse["access_token"] as String);
        }
      }
    } catch (e) {
      error = "User login failure: $e";
      success = false;
      _setAccessToken(null);
    }
    return Tuple2(success, error);
  }

  _setAccessToken(String? accessToken) {
    _accessToken = accessToken;
    if (accessToken == null) {
      _userProfile = null;
    }
  }

  UserProfile? readCachedUserProfile() {
    return _userProfile != null ? _userProfile!.copy : null;
  }

  Future<Tuple2<bool, String?>> getUserProfile() async {
    bool success;
    String? error;
    try {
      final response = await Util.httpGet(
          url: "$_backendAPIURL/get-user-profile", accessToken: _accessToken);
      if (response.startsWith("Error")) {
        error = "Get user profile failure: $response";
        success = false;
      } else {
        if (response.isEmpty) {
          error = "Get user profile failure: no email address in response";
          success = false;
        } else {
          final json = jsonDecode(response) as Map<String, dynamic>;
          final userProfile = UserProfile.fromJson(json);
          if (userProfile.emailAddress.isEmpty) {
            error = "Get user profile failure: no email address in response";
            success = false;
            _setUserProfile(null);
          } else {
            error = null;
            success = true;
            _setUserProfile(userProfile);
          }
        }
      }
    } catch (e) {
      error = "Get user profile failure: $e";
      success = false;
      _setUserProfile(null);
    }
    return Tuple2(success, error);
  }

  Future<Tuple2<bool, dynamic>> saveUserProfile(UserProfile userProfile) async {
    bool success;
    String? error;
    try {
      final Map<String, String> body = {
        "id": userProfile.id.hexString,
        "email_address": userProfile.emailAddress,
        "login_sub": userProfile.loginSub,
        "user_type": userProfile.userType.description,
        "name": userProfile.name == null ? "" : userProfile.name!.toString(),
        "picture_url": userProfile.pictureURL == null
            ? ""
            : userProfile.pictureURL!.toString(),
        "profile_url": userProfile.profileURL == null
            ? ""
            : userProfile.profileURL!.toString(),
        "remarks":
            userProfile.remarks == null ? "" : userProfile.remarks!.toString(),
        "last_logged_in": userProfile.lastLoggedIn.toString(),
      };
      final response = await Util.httpPut(
          url: "$_backendAPIURL/save-user-profile",
          body: body,
          accessToken: _accessToken);
      if (response.startsWith("Error")) {
        error = "Save user profile failure: $response";
        success = false;
        _setUserProfile(null);
      } else {
        error = null;
        success = true;
        _setUserProfile(userProfile);
      }
    } catch (e) {
      error = "Save user profile failure: $e";
      success = false;
      _setUserProfile(null);
    }
    return Tuple2(success, error);
  }

  _setUserProfile(UserProfile? userProfile) {
    _userProfile = userProfile;
  }

  // end region

  // region: symptoms to diagnosis

  Future<List<SubjectiveSymptom>> getSubjectiveSymptomList() async {
    final response = await Util.httpGet(
        url: "$_backendAPIURL/read-all-subjective-symptoms",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final subjectiveSymptomList = <SubjectiveSymptom>[
      ...jsonList.map((item) => SubjectiveSymptom.fromJson(item))
    ];
    subjectiveSymptomList.sort((a, b) => a.symptom.compareTo(b.symptom));
    return subjectiveSymptomList;
  }

  Future<List<AssociatedSymptom>> getAssociatedSymptomList() async {
    final response = await Util.httpGet(
        url: "$_backendAPIURL/read-all-associated-symptoms",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final associatedSymptomList = <AssociatedSymptom>[
      ...jsonList.map((item) => AssociatedSymptom.fromJson(item))
    ];
    associatedSymptomList.sort((a, b) => a.symptom.compareTo(b.symptom));
    return associatedSymptomList;
  }

  Future<List<Investigation>> getInvestigationList() async {
    final response = await Util.httpGet(
        url: "$_backendAPIURL/read-all-investigations",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final investigationList = <Investigation>[
      ...jsonList.map((item) => Investigation.fromJson(item))
    ];
    investigationList.sort((a, b) => a.name.compareTo(b.name));
    return investigationList;
  }

  Future<List<Gender>> getGenderList() async {
    final response = await Util.httpGet(
        url: "$_backendAPIURL/read-all-gender", accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final genderList = <Gender>[
      ...jsonList.map((item) => Gender.fromJson(item))
    ];
    return genderList;
  }

  Future<List<AgeGroup>> getAgeGroupList() async {
    final response = await Util.httpGet(
        url: "$_backendAPIURL/read-all-age-groups", accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final ageGroupList = <AgeGroup>[
      ...jsonList.map((item) => AgeGroup.fromJson(item))
    ];
    return ageGroupList;
  }

  Future<List<PredictedProvisionalDiagnosis>> predictProvisionalDiagnosis(
      List<SubjectiveSymptom> subjectiveSymptomList,
      List<AssociatedSymptom> associatedSymptomList,
      List<Investigation> investigationsDoneList,
      Gender gender,
      AgeGroup age) async {
    String separator = Config.map["symptomsSeparator"];
    final Map<String, String> body = {
      "subjective_symptoms":
          subjectiveSymptomList.map((item) => item.symptom).join(separator),
      "associated_symptoms":
          associatedSymptomList.map((item) => item.symptom).join(separator),
      "investigations_done":
          investigationsDoneList.map((item) => item.name).join(separator),
      "gender": gender.name,
      "age": age.age,
    };
    final response = await Util.httpPost(
        url: "$_backendAPIURL/predict-provisional-diagnosis",
        body: body,
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final predictedCauseList = <PredictedProvisionalDiagnosis>[
      ...jsonList.map((item) => PredictedProvisionalDiagnosis.fromJson(item))
    ];
    return predictedCauseList;
  }

  Future<List<ProvisionalDiagnosisAdvise>> getAdviseList(
      String provisionalDiagnosis) async {
    final response = await Util.httpGet(
        url:
            "$_backendAPIURL/read-advises?provisional_diagnosis=$provisionalDiagnosis",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final adviseList = <ProvisionalDiagnosisAdvise>[
      ...jsonList.map((item) => ProvisionalDiagnosisAdvise.fromJson(item))
    ];
    return adviseList;
  }

  // end region
}
