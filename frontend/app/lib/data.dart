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
    return subjectiveSymptomList;
  }

  Future<List<ObjectiveSymptom>> getObjectiveSymptomList() async {
    final response = await Lib.httpGet(
        url: "$_backendAPIURL/read-all-objective-symptoms",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final objectiveSymptomList = <ObjectiveSymptom>[
      ...jsonList.map((item) => ObjectiveSymptom.fromJson(item))
    ];
    return objectiveSymptomList;
  }

  Future<List<Gender>> getGenderList() async {
    return await Future.value(Gender.values);
  }

  Future<List<Etiology>> getEtiologyList() async {
    final response = await Lib.httpGet(
        url: "$_backendAPIURL/read-all-etiologies", accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final etiologyList = <Etiology>[
      ...jsonList.map((item) => Etiology.fromJson(item))
    ];
    return etiologyList;
  }

  Future<List<PredictedCause>> predictCause(
      List<SubjectiveSymptom> subjectiveSymptomList,
      List<ObjectiveSymptom> objectiveSymptomList,
      Gender gender) async {
    final Map<String, String> body = {
      "subjective_symptoms":
          subjectiveSymptomList.map((item) => item.symptom).join(";"),
      "objective_symptoms":
          objectiveSymptomList.map((item) => item.symptom).join(";"),
      "gender": gender.name,
    };
    final response = await Lib.httpPost(
        url: "$_backendAPIURL/predict-cause",
        body: body,
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final predictedCauseList = <PredictedCause>[
      ...jsonList.map((item) => PredictedCause.fromJson(item))
    ];
    return predictedCauseList;
  }

  List<PredictedCauseWithEtiology> mapPredictCauseWithEtiology(
      List<PredictedCause> predictedCauseList,
      List<SubjectiveSymptom> subjectiveSymptomList,
      List<Etiology> etiologyList) {
    final result = <PredictedCauseWithEtiology>[
      ...predictedCauseList.map((item) {
        var split = item.cause.split("|");
        return PredictedCauseWithEtiology(
            split[0],
            split[1],
            item.probability,
            etiologyList
                .firstWhere((e) =>
                    e.cause == split[1] &&
                    subjectiveSymptomList
                            .firstWhere((s) => e.subjectiveSymptomId == s.id)
                            .symptom ==
                        split[0])
                .etiology);
      })
    ];
    return result;
  }

  Future<List<Drug>> getDrugList(ObjectId etiologyId) async {
    final response = await Lib.httpGet(
        url: "$_backendAPIURL/read-drugs/$etiologyId",
        accessToken: _accessToken);
    final jsonList = jsonDecode(response) as List<dynamic>;
    final drugList = <Drug>[...jsonList.map((item) => Drug.fromJson(item))];
    return drugList;
  }
}

class SubjectiveSymptom {
  final ObjectId id;
  final String symptom;

  SubjectiveSymptom.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        symptom = json["symptom"];
}

class ObjectiveSymptom {
  final ObjectId id;
  final ObjectId subjectiveSymptomId;
  final String symptom;

  ObjectiveSymptom.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        subjectiveSymptomId =
            ObjectId.fromHexString(json["subjective_symptom_id"]),
        symptom = json["symptom"];
}

enum Gender { female, male }

class Etiology {
  final ObjectId id;
  final ObjectId subjectiveSymptomId;
  final String cause;
  final String etiology;

  Etiology.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        subjectiveSymptomId =
            ObjectId.fromHexString(json["subjective_symptom_id"]),
        cause = json["cause"],
        etiology = json["etiology"];
}

class PredictedCause {
  final String cause;
  final double probability;

  PredictedCause.fromJson(List<dynamic> json)
      : cause = json[0],
        probability = json[1];
}

class PredictedCauseWithEtiology {
  final String subjectiveSymptom;
  final String cause;
  final double probability;
  final String etiology;

  PredictedCauseWithEtiology(
      this.subjectiveSymptom, this.cause, this.probability, this.etiology);
}

class Drug {
  final ObjectId id;
  final ObjectId etiologyId;
  final String drugCategory;
  final String drugUse;
  final String modeOfAction;
  final String dose;

  Drug.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        etiologyId = ObjectId.fromHexString(json["etiology_id"]),
        drugCategory = json["drug_category"],
        drugUse = json["drug_use"],
        modeOfAction = json["mode_of_action"],
        dose = json["dose"];
}
