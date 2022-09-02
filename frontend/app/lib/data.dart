import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:objectid/objectid.dart';

class Data {
  final String backendAPIURL;

  const Data({this.backendAPIURL = "http://localhost:8080"});

  Future<List<SubjectiveSymptom>> getSubjectiveSymptomList() async {
    final List<dynamic> jsonList =
        await _httpGet("$backendAPIURL/read-all-subjective-symptoms");
    List<SubjectiveSymptom> subjectiveSymptomList = [];
    for (var json in jsonList) {
      subjectiveSymptomList.add(SubjectiveSymptom.fromJson(json));
    }
    return subjectiveSymptomList;
  }

  Future<List<ObjectiveSymptom>> getObjectiveSymptomList() async {
    final List<dynamic> jsonList =
        await _httpGet("$backendAPIURL/read-all-objective-symptoms");
    List<ObjectiveSymptom> objectiveSymptomList = [];
    for (var json in jsonList) {
      objectiveSymptomList.add(ObjectiveSymptom.fromJson(json));
    }
    return objectiveSymptomList;
  }

  Future<List<Gender>> getGenderList() async {
    return await Future.value(Gender.values);
  }

  Future<List<Etiology>> getEtiologyList() async {
    final List<dynamic> jsonList =
        await _httpGet("$backendAPIURL/read-all-etiologies");
    List<Etiology> etiologyList = [];
    for (var json in jsonList) {
      etiologyList.add(Etiology.fromJson(json));
    }
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
    final List<dynamic> jsonList =
        await _httpPost("$backendAPIURL/predict-cause", body);
    List<PredictedCause> predictedCauseList = [];
    for (var json in jsonList) {
      predictedCauseList.add(PredictedCause.fromJson(json));
    }
    return predictedCauseList;
  }

  List<PredictedCauseWithEtiology> mapPredictCauseWithEtiology(
      List<PredictedCause> predictedCauseList,
      List<SubjectiveSymptom> subjectiveSymptomList,
      List<Etiology> etiologyList) {
    List<PredictedCauseWithEtiology> result = [];
    for (var predictedCause in predictedCauseList) {
      List<String> split = predictedCause.cause.split("|");
      result.add(PredictedCauseWithEtiology(
          split[0],
          split[1],
          predictedCause.probability,
          etiologyList
              .firstWhere((e) =>
                  e.cause == split[1] &&
                  subjectiveSymptomList
                          .firstWhere((s) => e.subjectiveSymptomId == s.id)
                          .symptom ==
                      split[0])
              .etiology));
    }
    return result;
  }

  Future<List<Drug>> getDrugList(ObjectId etiologyId) async {
    final List<dynamic> jsonList =
        await _httpGet("$backendAPIURL/read-drugs/$etiologyId");
    List<Drug> drugList = [];
    for (var json in jsonList) {
      drugList.add(Drug.fromJson(json));
    }
    return drugList;
  }

  Future<List<dynamic>> _httpGet(String url) async {
    final response = await http.get(Uri.parse(url), headers: {
      "Accept": "application/json",
      "Access-Control-Allow-Origin": "*"
    });
    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body) as List<dynamic>;
      return jsonList;
    } else {
      throw Exception(
          "Error calling backend api with status code: ${response.statusCode}");
    }
  }

  Future<List<dynamic>> _httpPost(String url, Map<String, String> body) async {
    final response = await http.post(Uri.parse(url),
        headers: {
          "Accept": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: body);
    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body) as List<dynamic>;
      return jsonList;
    } else {
      throw Exception(
          "Error calling backend api with status code: ${response.statusCode}");
    }
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
