import 'package:flutter/material.dart';
import 'package:tuple/tuple.dart';
import 'package:circular_countdown/circular_countdown.dart';
import 'profile.dart';
import '../util/types.dart';

class Login extends StatefulWidget {
  final Function _getLoggedInState;
  final Function _resetUserLogin;
  final Function _getAuthorisationCode;
  final Function _getAccessToken;
  final Function _getUserProfile;
  final Function _readCachedUserProfile;
  final Function _saveUserProfile;
  final Function _onCompletion;

  const Login({
    super.key,
    required getLoggedInState,
    required resetUserLogin,
    required getAuthorisationCode,
    required getAccessToken,
    required getUserProfile,
    required readCachedUserProfile,
    required saveUserProfile,
    required onCompletion,
  })  : _getLoggedInState = getLoggedInState,
        _resetUserLogin = resetUserLogin,
        _getAuthorisationCode = getAuthorisationCode,
        _getAccessToken = getAccessToken,
        _getUserProfile = getUserProfile,
        _readCachedUserProfile = readCachedUserProfile,
        _saveUserProfile = saveUserProfile,
        _onCompletion = onCompletion;

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  late final int _errorCountdownSeconds;
  late final int _successCountdownSeconds;
  late LoggedInState _loggedInState;
  late String? _error;

  @override
  void initState() {
    super.initState();
    _errorCountdownSeconds = 5;
    _successCountdownSeconds = 1;
    _loggedInState = widget._getLoggedInState();
    _error = null;
  }

  void _resetLoggedInState() {
    setState(() {
      _loggedInState = widget._getLoggedInState();
      if (_loggedInState == LoggedInState.loggedIn) {
        widget._onCompletion();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_error != null && _error!.isNotEmpty) {
        () async {
          await Future.delayed(Duration(seconds: _errorCountdownSeconds), () {
            setState(() {
              _error = null;
              widget._resetUserLogin();
              _loggedInState = widget._getLoggedInState();
            });
          });
        }();
      } else if (_loggedInState != LoggedInState.gotUserProfile) {
        () async {
          await Future.delayed(
              Duration(
                  seconds: _loggedInState == LoggedInState.notLoggedIn
                      ? 0
                      : _successCountdownSeconds), () {
            _resetLoggedInState();
          });
        }();
      }
    });

    return Scaffold(
      appBar: AppBar(
        title: const Text("AI-HOSPITAL.SERVICES"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(
                  'assets/app_logo.png',
                  scale: 1.25,
                ),
              ],
            ),
            const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  "DIGITAL MEDICAL SERVICES POWERED BY AI",
                  style: TextStyle(
                    fontSize: 20,
                    fontFamily: "RobotoMono",
                    fontWeight: FontWeight.w300,
                  ),
                ),
              ],
            ),
            const SizedBox(
              width: 0,
              height: 25,
            ),
            (_error != null && _error!.isNotEmpty)
                ? Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        "${_error!} ...",
                        style: const TextStyle(
                          color: Colors.red,
                        ),
                      ),
                      getCountdown(isError: true),
                    ],
                  )
                : switch (_loggedInState) {
                    LoggedInState.notLoggedIn =>
                      // First step is to get authorisation code
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          ElevatedButton(
                            onPressed: () async {
                              final response =
                                  await widget._getAuthorisationCode();
                              final success = response.item1;
                              final error = response.item2;
                              if (!success) _error = error;
                            },
                            style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.blue[400]),
                            child: const Text("Login Here",
                                style: TextStyle(fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                    LoggedInState.gotAuthorisationCode =>
                      // Second step is to get access token from backend api call
                      FutureBuilder(
                        future: widget._getAccessToken(),
                        builder: (context, snapshot) {
                          switch (snapshot.connectionState) {
                            case ConnectionState.waiting:
                              return const CircularProgressIndicator();
                            case ConnectionState.done:
                            default:
                              if (snapshot.hasData) {
                                final response =
                                    snapshot.data as Tuple2<bool, String?>;
                                final success = response.item1;
                                final error = response.item2;
                                if (success) {
                                  return Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      const Text(
                                          "User login successful, getting user profile ..."),
                                      getCountdown(),
                                    ],
                                  );
                                } else {
                                  _error = error;
                                }
                              } else if (snapshot.hasError) {
                                _error =
                                    "User login failure: ${snapshot.error}";
                              }
                              return const Row(children: [
                                Text("Wait ..."),
                                CircularProgressIndicator(),
                              ]);
                          }
                        },
                      ),
                    LoggedInState.gotAccessToken =>
                      // Fourth step is to save user profile to backend api call
                      FutureBuilder(
                        future: widget._getUserProfile(),
                        builder: (context, snapshot) {
                          switch (snapshot.connectionState) {
                            case ConnectionState.waiting:
                              return const CircularProgressIndicator();
                            case ConnectionState.done:
                            default:
                              if (snapshot.hasData) {
                                final response =
                                    snapshot.data as Tuple2<bool, String?>;
                                final success = response.item1;
                                final error = response.item2;
                                if (success) {
                                  return Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      const Text(
                                          "Getting user profile successful ..."),
                                      getCountdown(),
                                    ],
                                  );
                                } else {
                                  _error = error;
                                }
                              } else if (snapshot.hasError) {
                                _error =
                                    "User login failure: ${snapshot.error}";
                              }
                              return const Row(children: [
                                Text("Wait ..."),
                                CircularProgressIndicator(),
                              ]);
                          }
                        },
                      ),
                    LoggedInState.gotUserProfile => Profile(
                        userProfile: widget._readCachedUserProfile(),
                        saveUserProfile: widget._saveUserProfile,
                        onCompletion: _resetLoggedInState,
                      ),
                    LoggedInState.loggedIn =>
                      const Text("User is already logged in!")
                  },
          ],
        ),
      ),
    );
  }

  Widget getCountdown({bool isError = false}) {
    if (isError) {
      return TimeCircularCountdown(
        unit: CountdownUnit.second,
        countdownTotal: _errorCountdownSeconds,
        strokeWidth: 10,
        gapFactor: 20,
        diameter: 50,
        countdownCurrentColor: Colors.lightBlue,
        countdownTotalColor: Colors.blue,
        countdownRemainingColor: Colors.grey,
        textStyle: const TextStyle(color: Colors.black),
      );
    } else {
      return const CircularProgressIndicator();
    }
  }
}
