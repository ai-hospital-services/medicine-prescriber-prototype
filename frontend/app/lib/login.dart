import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:yaml/yaml.dart';
import 'package:tuple/tuple.dart';
import 'package:oauth2_client/oauth2_client.dart';
import 'config.dart';
import 'lib.dart';

class Login extends StatefulWidget {
  late final String _backendAPIURL;
  final Function? _setValidLoginState;

  Login({super.key, required setValidLoginState})
      : _backendAPIURL = Config.map["backendAPIURL"],
        _setValidLoginState = setValidLoginState;

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  late final OAuth2Client _oauth2Client;
  late final String _stateValue;
  late String _authorisationCode;
  late String _authorisationCodeError;
  late String _accessCode;
  late String _accessCodeError;

  @override
  void initState() {
    super.initState();
    _oauth2Client = OAuth2Client(
        authorizeUrl: Config.map["authoriseURL"],
        tokenUrl: "",
        redirectUri: Config.map["redirectURL"],
        customUriScheme: "");
    _stateValue = "STATE_VALUE";
    _authorisationCode = "";
    _authorisationCodeError = "";
    _accessCode = "";
    _accessCodeError = "";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Login to application"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: (_authorisationCode.isEmpty)
            ?
            // First step is to get authorisation code
            Column(
                children: <Widget>[
                  ElevatedButton(
                    onPressed: () async {
                      final response = await _getAuthorisationCode();
                      final success = response.item1;
                      final result = response.item2;
                      setState(() {
                        if (success) {
                          _authorisationCode = result;
                          _authorisationCodeError = "";
                        } else {
                          _authorisationCode = "";
                          _authorisationCodeError = result;
                        }
                      });
                    },
                    style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue[400]),
                    child: const Text("Initiate Login",
                        style: TextStyle(fontWeight: FontWeight.bold)),
                  ),
                  if (_authorisationCodeError.isNotEmpty)
                    Text("User login failure: $_authorisationCodeError"),
                ],
              )
            :
            // Second step is to get access token from backend api call
            FutureBuilder(
                future: _getAccessToken(),
                builder: (context, snapshot) {
                  switch (snapshot.connectionState) {
                    case ConnectionState.waiting:
                      return const CircularProgressIndicator();
                    case ConnectionState.done:
                    default:
                      if (snapshot.hasData) {
                        final response = snapshot.data as Tuple2<bool, String>;
                        final success = response.item1;
                        final result = response.item2;
                        if (success) {
                          _accessCode = result;
                          _accessCodeError = "";
                          _runAfterSuccessfulLogin();
                          return Row(
                            children: const <Widget>[
                              Text("User login successful ..."),
                              CircularProgressIndicator(),
                            ],
                          );
                        } else {
                          _accessCode = "";
                          _accessCodeError = result;
                          return Text(result);
                        }
                      } else if (snapshot.hasError) {
                        return Text("Error: ${snapshot.error}");
                      } else {
                        return const SizedBox.shrink();
                      }
                  }
                },
              ),
      ),
    );
  }

  Future<Tuple2<bool, String>> _getAuthorisationCode() async {
    bool success;
    String result;
    try {
      final response = await _oauth2Client.requestAuthorization(
          clientId: Config.map["clientID"],
          scopes: <String>[...(Config.map["scopes"] as YamlList)],
          state: _stateValue,
          customParams: {"audience": Config.map["audience"]});
      if (response.code == null || response.code!.isEmpty) {
        result = "User login failure: no authorisation code in response";
        success = false;
      } else {
        result = response.code!;
        success = true;
      }
    } catch (e) {
      result = "User login failure: $e";
      success = false;
    }
    return Tuple2(success, result);
  }

  Future<Tuple2<bool, String>> _getAccessToken() async {
    bool success;
    String result;
    try {
      final response = await Lib.httpGet(
          url: "${widget._backendAPIURL}/get-access-token/$_authorisationCode");
      final decodedResponse = jsonDecode(response) as Map;
      if (decodedResponse["access_token"] == null ||
          (decodedResponse["access_token"] as String).isEmpty) {
        result = "User login failure: no access token in response";
        success = false;
      } else {
        result = decodedResponse["access_token"] as String;
        success = true;
      }
    } catch (e) {
      result = "User login failure: $e";
      success = false;
    }
    return Tuple2(success, result);
  }

  static Future<bool> validateAccessToken(String accessToken) async {
    bool success;
    try {
      final assertedClaims = (Config.map["scopes"] as YamlList).join(" ");
      await Lib.httpGet(
          url:
              "${Config.map["backendAPIURL"]}/validate-access-token/$assertedClaims",
          accessToken: accessToken);
      success = true;
    } catch (e) {
      success = false;
    }
    return success;
  }

  Future<void> _runAfterSuccessfulLogin() async {
    if (_accessCode.isNotEmpty &&
        _accessCodeError.isEmpty &&
        _authorisationCode.isNotEmpty &&
        _authorisationCodeError.isEmpty) {
      await Future.delayed(const Duration(seconds: 3));
      if (widget._setValidLoginState != null) {
        widget._setValidLoginState!(accessToken: _accessCode);
      }
    }
  }
}
