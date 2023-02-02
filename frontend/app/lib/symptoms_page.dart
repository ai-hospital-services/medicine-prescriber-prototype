import 'package:flutter/material.dart';
import 'package:multiple_search_selection/multiple_search_selection.dart';
import 'data.dart';
import 'config.dart';

class SymptomsPage extends StatefulWidget {
  final Future<List<SubjectiveSymptom>> getSubjectiveSymptomList;
  final Future<List<AssociatedSymptom>> getAssociatedSymptomList;
  final Future<List<Investigation>> getInvestigationList;
  final Future<List<Gender>> getGenderList;
  final Future<List<AgeGroup>> getAgeGroupList;
  final Function predictProvisionalDiagnosis;
  final Function getAdviseList;

  const SymptomsPage(
      {super.key,
      required this.getSubjectiveSymptomList,
      required this.getAssociatedSymptomList,
      required this.getInvestigationList,
      required this.getGenderList,
      required this.getAgeGroupList,
      required this.predictProvisionalDiagnosis,
      required this.getAdviseList});

  @override
  State<StatefulWidget> createState() => _SymptomsPageState();
}

class _SymptomsPageState extends State<SymptomsPage> {
  List<SubjectiveSymptom>? _subjectiveSymptomList;
  List<SubjectiveSymptom>? _selectedSubjectiveSymptomList;
  List<AssociatedSymptom>? _associatedSymptomList;
  List<AssociatedSymptom>? _selectedAssociatedSymptomList;
  List<Investigation>? _investigationsDoneList;
  List<Investigation>? _selectedInvestigationsDoneList;
  Gender? _selectedGender;
  AgeGroup? _selectedAgeGroup;
  bool _isPredictCauseButtonActive = false;
  Future<List<PredictedProvisionalDiagnosis>>?
      _predictedProvisionalDiagnosisList;
  bool _isReadAdviseButtonActive = false;
  int _selectedProvisionalDiagnosisIndex = -1;
  String? _selectedProvisionalDiagnosis;
  Future<List<ProvisionalDiagnosisAdvise>>? _adviseList;

  void _setOutputState() {
    _isPredictCauseButtonActive = _selectedSubjectiveSymptomList != null &&
        _selectedAssociatedSymptomList != null &&
        _selectedAssociatedSymptomList!.isNotEmpty &&
        _selectedGender != null &&
        _selectedAgeGroup != null;
    _predictedProvisionalDiagnosisList = null;
    _isReadAdviseButtonActive = false;
    _selectedProvisionalDiagnosisIndex = -1;
    _selectedProvisionalDiagnosis = null;
    _adviseList = null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Predict Provisional Diagnosis from Symptoms"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Row(
              children: [
                const Text("Select subjective symptoms: ",
                    style: TextStyle(fontWeight: FontWeight.bold)),
                FutureBuilder(
                  future: widget.getSubjectiveSymptomList,
                  builder: (context, snapshot) {
                    switch (snapshot.connectionState) {
                      case ConnectionState.waiting:
                        return const CircularProgressIndicator();
                      case ConnectionState.done:
                      default:
                        if (snapshot.hasData) {
                          return Expanded(
                              child: MultipleSearchSelection<SubjectiveSymptom>(
                            showedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.lightBlue),
                            pickedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.lightBlue),
                            fieldToCheck: (item) => item.symptom,
                            fuzzySearch: FuzzySearch.jaro,
                            items: () {
                              _subjectiveSymptomList =
                                  (snapshot.data as List<SubjectiveSymptom>);
                              return _subjectiveSymptomList!;
                            }(),
                            itemBuilder: (item, _) => Text(item.symptom),
                            itemsVisibility: ShowedItemsVisibility.alwaysOn,
                            maximumShowItemsHeight: 100,
                            onPickedChange: (items) {
                              setState(() {
                                _selectedSubjectiveSymptomList = items;
                                _setOutputState();
                              });
                            },
                            pickedItemBuilder: (item) =>
                                Text("${item.symptom};"),
                          ));
                        } else if (snapshot.hasError) {
                          return Text("Error: ${snapshot.error}");
                        } else {
                          return const SizedBox.shrink();
                        }
                    }
                  },
                ),
              ],
            ),
            const Divider(
              height: 20,
              thickness: 2,
              indent: 0,
              endIndent: 0,
              color: Colors.black,
            ),
            Row(
              children: [
                const Text("Select associated symptoms: ",
                    style: TextStyle(fontWeight: FontWeight.bold)),
                FutureBuilder(
                  key: _selectedSubjectiveSymptomList == null
                      ? widget.key
                      : ValueKey(_selectedSubjectiveSymptomList!
                          .map((item) => item.symptom)
                          .join(";")),
                  future: widget.getAssociatedSymptomList,
                  builder: (context, snapshot) {
                    switch (snapshot.connectionState) {
                      case ConnectionState.waiting:
                        return const CircularProgressIndicator();
                      case ConnectionState.done:
                      default:
                        if (snapshot.hasData) {
                          return Expanded(
                              child: MultipleSearchSelection<AssociatedSymptom>(
                            showedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.lime),
                            pickedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.lime),
                            fieldToCheck: (item) => item.symptom,
                            fuzzySearch: FuzzySearch.jaro,
                            items: () {
                              if (_selectedSubjectiveSymptomList != null) {
                                List<AssociatedSymptom> items = (snapshot.data
                                        as List<AssociatedSymptom>)
                                    .where((o) =>
                                        _selectedSubjectiveSymptomList!.any(
                                            (s) =>
                                                s.id == o.subjectiveSymptomId))
                                    .toList();
                                final Set set = {};
                                items.retainWhere(
                                    (element) => set.add(element.symptom));
                                if (items.map((e) => e.symptom).join(";") !=
                                    _associatedSymptomList!
                                        .map((e) => e.symptom)
                                        .join(";")) {
                                  _associatedSymptomList = items;
                                }
                              } else {
                                _associatedSymptomList = [];
                              }
                              return _associatedSymptomList!;
                            }(),
                            itemBuilder: (item, _) => Text(item.symptom),
                            itemsVisibility: ShowedItemsVisibility.alwaysOn,
                            maximumShowItemsHeight: 100,
                            onPickedChange: (items) {
                              setState(() {
                                _selectedAssociatedSymptomList = items;
                                _setOutputState();
                              });
                            },
                            pickedItemBuilder: (item) =>
                                Text("${item.symptom};"),
                          ));
                        } else if (snapshot.hasError) {
                          return Text("Error: ${snapshot.error}");
                        } else {
                          return const SizedBox.shrink();
                        }
                    }
                  },
                ),
              ],
            ),
            const Divider(
              height: 20,
              thickness: 2,
              indent: 0,
              endIndent: 0,
              color: Colors.black,
            ),
            Row(
              children: [
                const Text("Select investigations done: ",
                    style: TextStyle(fontWeight: FontWeight.bold)),
                FutureBuilder(
                  future: widget.getInvestigationList,
                  builder: (context, snapshot) {
                    switch (snapshot.connectionState) {
                      case ConnectionState.waiting:
                        return const CircularProgressIndicator();
                      case ConnectionState.done:
                      default:
                        if (snapshot.hasData) {
                          return Expanded(
                              child: MultipleSearchSelection<Investigation>(
                            showedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.grey),
                            pickedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.grey),
                            fieldToCheck: (item) => item.name,
                            fuzzySearch: FuzzySearch.jaro,
                            items: () {
                              _investigationsDoneList =
                                  (snapshot.data as List<Investigation>);
                              return _investigationsDoneList!;
                            }(),
                            itemBuilder: (item, _) => Text(item.name),
                            itemsVisibility: ShowedItemsVisibility.alwaysOn,
                            maximumShowItemsHeight: 100,
                            onPickedChange: (items) {
                              setState(() {
                                _selectedInvestigationsDoneList = items;
                                _setOutputState();
                              });
                            },
                            pickedItemBuilder: (item) => Text("${item.name};"),
                          ));
                        } else if (snapshot.hasError) {
                          return Text("Error: ${snapshot.error}");
                        } else {
                          return const SizedBox.shrink();
                        }
                    }
                  },
                ),
              ],
            ),
            const Divider(
              height: 20,
              thickness: 2,
              indent: 0,
              endIndent: 0,
              color: Colors.black,
            ),
            Row(children: [
              const Text("Select gender: ",
                  style: TextStyle(fontWeight: FontWeight.bold)),
              FutureBuilder(
                future: widget.getGenderList,
                builder: (context, snapshot) {
                  switch (snapshot.connectionState) {
                    case ConnectionState.waiting:
                      return const CircularProgressIndicator();
                    case ConnectionState.done:
                    default:
                      if (snapshot.hasData) {
                        return DropdownButton<Gender>(
                          value: _selectedGender,
                          items: (snapshot.data as List<Gender>)
                              .map<DropdownMenuItem<Gender>>(
                                (Gender value) => DropdownMenuItem<Gender>(
                                  value: value,
                                  child: Text(value.name),
                                ),
                              )
                              .toList(),
                          onChanged: (Gender? newValue) {
                            if (_selectedGender != newValue) {
                              setState(() {
                                _selectedGender = newValue;
                                _setOutputState();
                              });
                            }
                          },
                        );
                      } else if (snapshot.hasError) {
                        return Text("Error: ${snapshot.error}");
                      } else {
                        return const SizedBox.shrink();
                      }
                  }
                },
              ),
            ]),
            const Divider(
              height: 20,
              thickness: 2,
              indent: 0,
              endIndent: 0,
              color: Colors.black,
            ),
            Row(children: [
              const Text("Select age group: ",
                  style: TextStyle(fontWeight: FontWeight.bold)),
              FutureBuilder(
                future: widget.getAgeGroupList,
                builder: (context, snapshot) {
                  switch (snapshot.connectionState) {
                    case ConnectionState.waiting:
                      return const CircularProgressIndicator();
                    case ConnectionState.done:
                    default:
                      if (snapshot.hasData) {
                        return DropdownButton<AgeGroup>(
                          value: _selectedAgeGroup,
                          items: (snapshot.data as List<AgeGroup>)
                              .map<DropdownMenuItem<AgeGroup>>(
                                (AgeGroup value) => DropdownMenuItem<AgeGroup>(
                                  value: value,
                                  child: Text(value.age),
                                ),
                              )
                              .toList(),
                          onChanged: (AgeGroup? newValue) {
                            if (_selectedAgeGroup != newValue) {
                              setState(() {
                                _selectedAgeGroup = newValue;
                                _setOutputState();
                              });
                            }
                          },
                        );
                      } else if (snapshot.hasError) {
                        return Text("Error: ${snapshot.error}");
                      } else {
                        return const SizedBox.shrink();
                      }
                  }
                },
              ),
            ]),
            const Divider(
              height: 20,
              thickness: 2,
              indent: 0,
              endIndent: 0,
              color: Colors.black,
            ),
            Row(
              children: [
                ElevatedButton(
                  onPressed: _isPredictCauseButtonActive
                      ? () async {
                          setState(() {
                            _predictedProvisionalDiagnosisList = () async {
                              return widget.predictProvisionalDiagnosis(
                                      _selectedSubjectiveSymptomList,
                                      _selectedAssociatedSymptomList,
                                      _selectedInvestigationsDoneList,
                                      _selectedGender,
                                      _selectedAgeGroup)
                                  as Future<
                                      List<PredictedProvisionalDiagnosis>>;
                            }();
                          });
                        }
                      : null,
                  style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue[400]),
                  child: const Text("Predict Provisional Diagnosis",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                )
              ],
            ),
            Row(
              children: [
                FutureBuilder(
                  key: _predictedProvisionalDiagnosisList == null
                      ? widget.key
                      : ValueKey(
                          """${_selectedSubjectiveSymptomList!.map((item) => item.symptom).join(";")};
                          ${_selectedAssociatedSymptomList!.map((item) => item.symptom).join(";")};
                          ${_selectedInvestigationsDoneList!.map((item) => item.name).join(";")};
                          ${_selectedGender!.name};
                          ${_selectedAgeGroup!.age}"""),
                  future: _predictedProvisionalDiagnosisList,
                  builder: (context, snapshot) {
                    switch (snapshot.connectionState) {
                      case ConnectionState.waiting:
                        return const CircularProgressIndicator();
                      case ConnectionState.done:
                      default:
                        if (snapshot.hasData) {
                          return Expanded(
                              child: SingleChildScrollView(
                            scrollDirection: Axis.horizontal,
                            child: DataTable(
                              columns: () {
                                return [
                                  const DataColumn(
                                      label: Text("Probability %")),
                                  const DataColumn(
                                      label: Text("Provisional Diagnosis")),
                                ];
                              }(),
                              rows: () {
                                List<PredictedProvisionalDiagnosis>
                                    predictedProvisionalDiagnosisList =
                                    (snapshot.data
                                        as List<PredictedProvisionalDiagnosis>);
                                List<DataRow> result = [];
                                for (int i = 0;
                                    i <
                                        predictedProvisionalDiagnosisList
                                            .length;
                                    i++) {
                                  result.add(DataRow(
                                      selected:
                                          _selectedProvisionalDiagnosisIndex ==
                                              i,
                                      onSelectChanged: (value) {
                                        setState(() {
                                          _selectedProvisionalDiagnosisIndex =
                                              i;
                                          _selectedProvisionalDiagnosis =
                                              predictedProvisionalDiagnosisList[
                                                      i]
                                                  .provisionalDiagnosis;
                                          _isReadAdviseButtonActive = true;
                                          _adviseList = null;
                                        });
                                      },
                                      cells: [
                                        DataCell(Text(
                                            predictedProvisionalDiagnosisList[i]
                                                .probability
                                                .toString())),
                                        DataCell(Text(
                                            predictedProvisionalDiagnosisList[i]
                                                .provisionalDiagnosis
                                                .split(Config
                                                    .map["symptomsSeparator"])
                                                .join(" -> "))),
                                      ]));
                                }
                                return result;
                              }(),
                            ),
                          ));
                        } else if (snapshot.hasError) {
                          return Text("Error: ${snapshot.error}");
                        } else {
                          return const SizedBox.shrink();
                        }
                    }
                  },
                ),
              ],
            ),
            const Divider(
              height: 20,
              thickness: 2,
              indent: 0,
              endIndent: 0,
              color: Colors.black,
            ),
            Row(
              children: [
                ElevatedButton(
                  onPressed: _isReadAdviseButtonActive
                      ? () async {
                          setState(() {
                            _adviseList = () async {
                              return widget.getAdviseList(
                                      _selectedProvisionalDiagnosis!)
                                  as Future<List<ProvisionalDiagnosisAdvise>>;
                            }();
                          });
                        }
                      : null,
                  style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red[300]),
                  child: const Text("Read Advise",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                )
              ],
            ),
            Row(
              children: [
                FutureBuilder(
                  key: _selectedProvisionalDiagnosis == null
                      ? widget.key
                      : ValueKey(_selectedProvisionalDiagnosis),
                  future: _adviseList,
                  builder: (context, snapshot) {
                    switch (snapshot.connectionState) {
                      case ConnectionState.waiting:
                        return const CircularProgressIndicator();
                      case ConnectionState.done:
                      default:
                        if (snapshot.hasData) {
                          return Expanded(
                              child: SingleChildScrollView(
                            scrollDirection: Axis.horizontal,
                            child: DataTable(
                              columns: () {
                                return [
                                  const DataColumn(
                                      label: Text("Advised Investigations")),
                                  const DataColumn(label: Text("Mangement")),
                                  const DataColumn(
                                      label: Text("Surgical Management")),
                                ];
                              }(),
                              rows: () {
                                List<ProvisionalDiagnosisAdvise> adviseList =
                                    (snapshot.data
                                        as List<ProvisionalDiagnosisAdvise>);
                                List<DataRow> result = [];
                                for (var advise in adviseList) {
                                  result.add(DataRow(cells: [
                                    DataCell(
                                        Text(advise.advisedInvestigations)),
                                    DataCell(SizedBox(
                                        width: 220,
                                        child: Text(advise.management))),
                                    DataCell(SizedBox(
                                        width: 375,
                                        child:
                                            Text(advise.surgicalManagement))),
                                  ]));
                                }
                                return result;
                              }(),
                            ),
                          ));
                        } else if (snapshot.hasError) {
                          return Text("Error: ${snapshot.error}");
                        } else {
                          return const SizedBox.shrink();
                        }
                    }
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
