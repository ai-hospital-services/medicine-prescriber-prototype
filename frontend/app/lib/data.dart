import 'dart:convert';
import 'package:objectid/objectid.dart';
import 'config.dart';
import 'lib.dart';

class Data {
  late final String _backendAPIURL;
  String? _accessToken;

  Data() : _backendAPIURL = Config.map["backendAPIURL"];

  set({required String? accessToken}) {
    _accessToken = accessToken;
  }

  Future<List<SubjectiveSymptom>> getSubjectiveSymptomList() async {
    final response = await Lib.httpGet(
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
    final response = await Lib.httpGet(
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
    final response = await Lib.httpGet(
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
    final response = await Lib.httpGet(
        url: "$_backendAPIURL/read-all-gender", accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final genderList = <Gender>[
      ...jsonList.map((item) => Gender.fromJson(item))
    ];
    return genderList;
  }

  Future<List<AgeGroup>> getAgeGroupList() async {
    final response = await Lib.httpGet(
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
    final response = await Lib.httpPost(
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
    final response = await Lib.httpGet(
        url:
            "$_backendAPIURL/read-advises?provisional_diagnosis=$provisionalDiagnosis",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final adviseList = <ProvisionalDiagnosisAdvise>[
      ...jsonList.map((item) => ProvisionalDiagnosisAdvise.fromJson(item))
    ];
    return adviseList;
  }
}

class SubjectiveSymptom {
  final ObjectId id;
  final String symptom;

  SubjectiveSymptom.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        symptom = json["symptom"];
}

class AssociatedSymptom {
  final ObjectId id;
  final ObjectId subjectiveSymptomId;
  final String symptom;

  AssociatedSymptom.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        subjectiveSymptomId =
            ObjectId.fromHexString(json["subjective_symptom_id"]),
        symptom = json["symptom"];
}

class Investigation {
  final ObjectId id;
  final String name;

  Investigation.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        name = json["investigation"];
}

class Gender {
  final ObjectId id;
  final String name;

  Gender.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        name = json["gender"];
}

class AgeGroup {
  final ObjectId id;
  final String age;

  AgeGroup.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        age = json["age"];
}

class PredictedProvisionalDiagnosis {
  final double probability;
  final String provisionalDiagnosis;

  PredictedProvisionalDiagnosis.fromJson(List<dynamic> json)
      : probability = json[0],
        provisionalDiagnosis = json[1];
}

class ProvisionalDiagnosisAdvise {
  final String provisionalDiagnosis;
  final String advisedInvestigations;
  final String management;
  final String surgicalManagement;

  ProvisionalDiagnosisAdvise.fromJson(Map<String, dynamic> json)
      : provisionalDiagnosis = json["provisional_diagnosis"],
        advisedInvestigations = json["advised_investigations"],
        management = json["management"],
        surgicalManagement = json["surgical_management"];
}
