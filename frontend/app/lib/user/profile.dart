import 'package:flutter/material.dart';
import '../util/types.dart';

class Profile extends StatefulWidget {
  final UserProfile _userProfile;
  final Function _saveUserProfile;
  final Function _onCompletion;

  const Profile({
    super.key,
    required userProfile,
    required saveUserProfile,
    required onCompletion,
  })  : _userProfile = userProfile,
        _saveUserProfile = saveUserProfile,
        _onCompletion = onCompletion;

  @override
  State<Profile> createState() => _SignUpState();
}

class _SignUpState extends State<Profile> {
  late String? _name;
  late final TextEditingController _nameEditingController;
  late UserType _userType;
  late final TextEditingController _userTypeEditingController;
  late String? _profileURL;
  late final TextEditingController _profileURLEditingController;
  late String? _error;

  @override
  void initState() {
    super.initState();
    _name = widget._userProfile.name;
    _nameEditingController = TextEditingController(text: _name);
    _userType = widget._userProfile.userType;
    _userTypeEditingController =
        TextEditingController(text: _userType.description);
    _profileURL = widget._userProfile.profileURL;
    _profileURLEditingController = TextEditingController(text: _profileURL);
    _error = null;
  }

  @override
  void dispose() {
    _nameEditingController.dispose();
    _userTypeEditingController.dispose();
    _profileURLEditingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: _nameEditingController,
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  label: const Text(
                    "Enter your full name ...",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  suffixIcon: _nameEditingController.text !=
                          (widget._userProfile.name ?? "")
                      ? IconButton(
                          onPressed: () {
                            setState(() {
                              _name = widget._userProfile.name;
                              _nameEditingController.text = (_name ?? "");
                            });
                          },
                          icon: const Icon(Icons.undo),
                        )
                      : null,
                ),
                onChanged: (value) {
                  setState(() {
                    _name = value.trim();
                  });
                },
              ),
            ),
          ],
        ),
        const SizedBox(
          width: 0,
          height: 25,
        ),
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: TextEditingController(
                    text: widget._userProfile.emailAddress),
                readOnly: true,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  label: Text(
                    "Your email address (read only) ...",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(
          width: 0,
          height: 25,
        ),
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: _userTypeEditingController,
                readOnly: true,
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  label: const Text(
                    "Your profile type ...",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  suffixIcon: _userTypeEditingController.text !=
                          widget._userProfile.userType.description
                      ? IconButton(
                          icon: const Icon(Icons.undo),
                          onPressed: () {
                            setState(() {
                              _userType = widget._userProfile.userType;
                              _userTypeEditingController.text =
                                  _userType.description;
                            });
                          },
                        )
                      : null,
                ),
                onTap: () {
                  showDialog(
                    context: context,
                    builder: (BuildContext context) {
                      return AlertDialog(
                        content: DropdownButton(
                          items: getProfileTypeMenuItems(),
                          value: _userType,
                          onChanged: (value) {
                            setState(() {
                              _userType = value;
                              _userTypeEditingController.text =
                                  _userType.description;
                              Navigator.of(context).pop();
                            });
                          },
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
        const SizedBox(
          width: 0,
          height: 25,
        ),
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: _profileURLEditingController,
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  label: const Text(
                    "Enter your profile link like - https://www.practo.com/bhopal/doctor/<name> ...",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  suffixIcon: _profileURLEditingController.text !=
                          (widget._userProfile.profileURL ?? "")
                      ? IconButton(
                          icon: const Icon(Icons.undo),
                          onPressed: () {
                            setState(() {
                              _profileURL = widget._userProfile.profileURL;
                              _profileURLEditingController.text =
                                  (_profileURL ?? "");
                            });
                          },
                        )
                      : null,
                ),
                onChanged: (value) {
                  setState(() {
                    _profileURL = value.trim();
                  });
                },
              ),
            ),
          ],
        ),
        const SizedBox(
          width: 0,
          height: 25,
        ),
        Row(
          children: [
            ElevatedButton(
              onPressed: () async {
                widget._userProfile.name = _name;
                widget._userProfile.userType = _userType;
                widget._userProfile.profileURL = _profileURL;
                final response =
                    await widget._saveUserProfile(widget._userProfile);
                final success = response.item1;
                final error = response.item2;
                setState(() {
                  if (success) {
                    _error = null;
                    widget._onCompletion();
                  } else {
                    _error = error;
                  }
                });
              },
              style:
                  ElevatedButton.styleFrom(backgroundColor: Colors.blue[400]),
              child: const Text("Save Profile",
                  style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
        (_error != null && _error!.isNotEmpty)
            ? Row(
                children: [
                  Text(
                    "$_error!",
                    style: const TextStyle(
                      color: Colors.red,
                    ),
                  ),
                ],
              )
            : const SizedBox.shrink()
      ],
    );
  }

  List<DropdownMenuItem> getProfileTypeMenuItems() {
    List<DropdownMenuItem> result = List.empty(growable: true);
    for (var item in UserTypeExtensions.getDescriptionsMap().entries) {
      result.add(DropdownMenuItem(
        value: item.key,
        child: Text(item.value),
      ));
    }
    return result;
  }
}
