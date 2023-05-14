import 'package:objectid/objectid.dart';

enum LoggedInState {
  notLoggedIn,
  gotAuthorisationCode,
  gotAccessToken,
  gotUserProfile,
  loggedIn
}

enum UserType {
  doctor,
  nurse,
  pharamacist,
  internalStaff,
  notAvailable,
}

extension StringExtensions on UserType {
  String get description {
    switch (this) {
      case UserType.doctor:
        return "Doctor";
      case UserType.nurse:
        return "Nurse";
      case UserType.pharamacist:
        return "Pharmacist";
      case UserType.internalStaff:
        return "Internal Staff";
      case UserType.notAvailable:
        return "Not Available";
      default:
        return "Not Available";
    }
  }
}

extension UserTypeExtensions on UserType {
  static UserType fromDescription(String? description) {
    switch (description) {
      case "Doctor":
        return UserType.doctor;
      case "Nurse":
        return UserType.nurse;
      case "Pharmacist":
        return UserType.pharamacist;
      case "Internal Staff":
        return UserType.internalStaff;
      case "Not Available":
        return UserType.notAvailable;
      default:
        return UserType.notAvailable;
    }
  }

  static Map<UserType, String> getDescriptionsMap() {
    Map<UserType, String> descriptionsMap = {};
    for (UserType userType in UserType.values) {
      descriptionsMap[userType] = userType.description;
    }
    return descriptionsMap;
  }
}

class UserProfile {
  final ObjectId id;
  final String emailAddress;
  final String loginSub;
  UserType userType;
  String? name;
  final String? pictureURL;
  String? profileURL;
  String? remarks;
  final DateTime lastLoggedIn;

  bool get isComplete {
    if (id.toString().isNotEmpty &&
        emailAddress.isNotEmpty &&
        loginSub.isNotEmpty &&
        userType != UserType.notAvailable &&
        name != null &&
        name!.isNotEmpty &&
        profileURL != null &&
        profileURL!.isNotEmpty &&
        lastLoggedIn.toString().isNotEmpty) {
      return true;
    }
    return false;
  }

  UserProfile get copy {
    return UserProfile(
      id: id,
      emailAddress: emailAddress,
      loginSub: loginSub,
      userType: userType,
      name: name,
      pictureURL: pictureURL,
      profileURL: profileURL,
      remarks: remarks,
      lastLoggedIn: lastLoggedIn,
    );
  }

  UserProfile({
    required this.id,
    required this.emailAddress,
    required this.loginSub,
    required this.userType,
    required this.name,
    required this.pictureURL,
    required this.profileURL,
    required this.remarks,
    required this.lastLoggedIn,
  });

  UserProfile.fromJson(Map<String, dynamic> json)
      : id = ObjectId.fromHexString(json["_id"]),
        emailAddress = json["email_address"],
        loginSub = json["login_sub"],
        userType = UserTypeExtensions.fromDescription(json["user_type"]),
        name = json["name"],
        pictureURL = json["picture_url"],
        profileURL = json["profile_url"],
        remarks = json["remarks"],
        lastLoggedIn = DateTime.parse(json["last_logged_in"]);
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
