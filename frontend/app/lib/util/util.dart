import 'package:http/http.dart' as http;
import 'package:yaml/yaml.dart';
import 'config.dart';

class Util {
  static Function? setLoginInvalidState;

  static Future<String> httpGet(
      {required String url, String? accessToken}) async {
    var headers = {
      "Accept": "application/json",
      "Access-Control-Allow-Origin": "*"
    };
    if (accessToken != null && accessToken.isNotEmpty) {
      headers.addAll({"Authorization": "Bearer $accessToken"});
    }

    final response = await http.get(Uri.parse(url), headers: headers);
    if (response.statusCode == 200) {
      return response.body;
    } else if (response.statusCode == 401 && setLoginInvalidState != null) {
      setLoginInvalidState!();
    }
    throw Exception(
        "Error calling api with status code: ${response.statusCode}");
  }

  static Future<String> httpPut(
      {required String url,
      required Map<String, String> body,
      String? accessToken}) async {
    var headers = {
      "Accept": "application/json",
      "Access-Control-Allow-Origin": "*"
    };
    if (accessToken != null && accessToken.isNotEmpty) {
      headers.addAll({"Authorization": "Bearer $accessToken"});
    }

    final response =
        await http.put(Uri.parse(url), headers: headers, body: body);
    if (response.statusCode == 200) {
      return response.body;
    } else if (response.statusCode == 401 && setLoginInvalidState != null) {
      setLoginInvalidState!();
    }
    throw Exception(
        "Error calling api with status code: ${response.statusCode}");
  }

  static Future<String> httpPost(
      {required String url,
      required Map<String, String> body,
      String? accessToken}) async {
    var headers = {
      "Accept": "application/json",
      "Access-Control-Allow-Origin": "*"
    };
    if (accessToken != null && accessToken.isNotEmpty) {
      headers.addAll({"Authorization": "Bearer $accessToken"});
    }

    final response =
        await http.post(Uri.parse(url), headers: headers, body: body);
    if (response.statusCode == 200) {
      return response.body;
    } else if (response.statusCode == 401 && setLoginInvalidState != null) {
      setLoginInvalidState!();
    }
    throw Exception(
        "Error calling api with status code: ${response.statusCode}");
  }

  static Future<bool> validateAccessToken(String accessToken) async {
    bool success;
    try {
      final assertedClaims = (Config.map["scopes"] as YamlList).join(" ");
      await httpGet(
          url:
              "${Config.map["backendAPIURL"]}/validate-access-token/$assertedClaims",
          accessToken: accessToken);
      success = true;
    } catch (e) {
      success = false;
    }
    return success;
  }
}
