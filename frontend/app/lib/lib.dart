import 'package:http/http.dart' as http;

class Lib {
  static Function? setInvalidLoginState;

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
    } else if (response.statusCode == 401 && setInvalidLoginState != null) {
      setInvalidLoginState!();
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
    } else if (response.statusCode == 401 && setInvalidLoginState != null) {
      setInvalidLoginState!();
    }
    throw Exception(
        "Error calling api with status code: ${response.statusCode}");
  }
}
