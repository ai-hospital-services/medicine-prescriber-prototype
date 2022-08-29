import 'package:app/data.dart';
import 'package:flutter/material.dart';
import 'package:multiple_search_selection/multiple_search_selection.dart';
import 'package:change_case/change_case.dart';
import 'package:objectid/objectid.dart';

class SymptomsPage extends StatefulWidget {
  final Future<List<SubjectiveSymptom>> getSubjectiveSymptomList;
  final Future<List<ObjectiveSymptom>> getObjectiveSymptomList;
  final Future<List<Gender>> getGenderList;
  final Future<List<Etiology>> getEtiologyList;
  final Function predictCause;
  final Function mapPredictCauseWithEtiology;
  final Function getDrugList;

  const SymptomsPage(
      {super.key,
      required this.getSubjectiveSymptomList,
      required this.getObjectiveSymptomList,
      required this.getGenderList,
      required this.getEtiologyList,
      required this.predictCause,
      required this.mapPredictCauseWithEtiology,
      required this.getDrugList});

  @override
  State<StatefulWidget> createState() => _SymptomsPageState();
}

class _SymptomsPageState extends State<SymptomsPage> {
  List<SubjectiveSymptom>? _subjectiveSymptomList;
  List<SubjectiveSymptom>? _selectedSubjectiveSymptomList;
  List<ObjectiveSymptom>? _selectedObjectiveSymptomList;
  Gender? _selectedGender;
  bool _isPredictCauseButtonActive = false;
  List<Etiology>? _etiologyList;
  Future<List<PredictedCause>>? _predictedCauseList;
  bool _isReadDrugButtonActive = false;
  int _selectedEtiologyIndex = -1;
  ObjectId? _selectedEtiologyId;
  Future<List<Drug>>? _drugList;

  void _setOutputState() {
    _isPredictCauseButtonActive = _selectedSubjectiveSymptomList != null &&
        _selectedObjectiveSymptomList != null &&
        _selectedObjectiveSymptomList!.isNotEmpty &&
        _selectedGender != null;
    _predictedCauseList = null;
    _isReadDrugButtonActive = false;
    _selectedEtiologyIndex = -1;
    _selectedEtiologyId = null;
    _drugList = null;
  }

  @override
  Widget build(BuildContext context) {
    widget.getEtiologyList.then((value) => _etiologyList = value);
    return Scaffold(
      appBar: AppBar(
        title: const Text("Predict Etiology from Symptoms"),
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
                                const BoxDecoration(color: Colors.yellow),
                            pickedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.yellow),
                            fieldToCheck: (item) => item.symptom,
                            fuzzySearch: FuzzySearch.jaro,
                            items: () {
                              _subjectiveSymptomList =
                                  (snapshot.data as List<SubjectiveSymptom>);
                              return _subjectiveSymptomList!;
                            }(),
                            itemBuilder: (item) =>
                                Text(item.symptom.toSentenceCase()),
                            itemsVisibility: ShowedItemsVisibility.alwaysOn,
                            maximumShowItemsHeight: 100,
                            onPickedChange: (items) {
                              setState(() {
                                _selectedSubjectiveSymptomList = items;
                                _setOutputState();
                              });
                            },
                            pickedItemBuilder: (item) =>
                                Text("${item.symptom.toSentenceCase()};"),
                          ));
                        } else if (snapshot.hasError) {
                          return Text('Error: ${snapshot.error}');
                        } else {
                          return const Text("");
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
                const Text("Select objective symptoms: ",
                    style: TextStyle(fontWeight: FontWeight.bold)),
                FutureBuilder(
                  key: _selectedSubjectiveSymptomList == null
                      ? widget.key
                      : ValueKey(_selectedSubjectiveSymptomList!
                          .map((item) => item.symptom)
                          .join(";")),
                  future: widget.getObjectiveSymptomList,
                  builder: (context, snapshot) {
                    switch (snapshot.connectionState) {
                      case ConnectionState.waiting:
                        return const CircularProgressIndicator();
                      case ConnectionState.done:
                      default:
                        if (snapshot.hasData) {
                          return Expanded(
                              child: MultipleSearchSelection<ObjectiveSymptom>(
                            showedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.lime),
                            pickedItemsBoxDecoration:
                                const BoxDecoration(color: Colors.lime),
                            fieldToCheck: (item) => item.symptom,
                            fuzzySearch: FuzzySearch.jaro,
                            items: () {
                              List<ObjectiveSymptom> items = [];
                              if (_selectedSubjectiveSymptomList != null) {
                                items = (snapshot.data
                                        as List<ObjectiveSymptom>)
                                    .where((o) =>
                                        _selectedSubjectiveSymptomList!.any(
                                            (s) =>
                                                s.id == o.subjectiveSymptomId))
                                    .toList();
                              }
                              return items;
                            }(),
                            itemBuilder: (item) =>
                                Text(item.symptom.toSentenceCase()),
                            itemsVisibility: ShowedItemsVisibility.alwaysOn,
                            maximumShowItemsHeight: 100,
                            onPickedChange: (items) {
                              setState(() {
                                _selectedObjectiveSymptomList = items;
                                _setOutputState();
                              });
                            },
                            pickedItemBuilder: (item) =>
                                Text("${item.symptom.toSentenceCase()};"),
                          ));
                        } else if (snapshot.hasError) {
                          return Text('Error: ${snapshot.error}');
                        } else {
                          return const Text("");
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
                                    child: Text(value.name.toSentenceCase()),
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
                          return Text('Error: ${snapshot.error}');
                        } else {
                          return const Text("");
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
                  onPressed: _isPredictCauseButtonActive
                      ? () async {
                          setState(() {
                            _predictedCauseList = () async {
                              return widget.predictCause(
                                _selectedSubjectiveSymptomList,
                                _selectedObjectiveSymptomList,
                                _selectedGender,
                              ) as Future<List<PredictedCause>>;
                            }();
                          });
                        }
                      : null,
                  style: ElevatedButton.styleFrom(primary: Colors.blue[400]),
                  child: const Text("Predict Cause",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                )
              ],
            ),
            Row(
              children: [
                FutureBuilder(
                  key: _predictedCauseList == null
                      ? widget.key
                      : ValueKey(
                          """${_selectedObjectiveSymptomList!.map((item) => item.symptom).join(";")};
                          ${_selectedObjectiveSymptomList!.map((item) => item.symptom).join(";")};
                          ${_selectedGender!.name}"""),
                  future: _predictedCauseList,
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
                                      label: Text("Subjective symptom")),
                                  const DataColumn(label: Text("Cause")),
                                  const DataColumn(
                                      label: Text("Probability %")),
                                  const DataColumn(label: Text("Etiology")),
                                ];
                              }(),
                              rows: () {
                                List<PredictedCause> predictedCauseList =
                                    (snapshot.data as List<PredictedCause>);
                                List<PredictedCauseWithEtiology> mappedList =
                                    widget.mapPredictCauseWithEtiology(
                                        predictedCauseList,
                                        _subjectiveSymptomList,
                                        _etiologyList);
                                List<DataRow> result = [];
                                for (int i = 0; i < mappedList.length; i++) {
                                  result.add(DataRow(
                                      selected: _selectedEtiologyIndex == i,
                                      onSelectChanged: (value) {
                                        setState(() {
                                          _selectedEtiologyIndex = i;
                                          _selectedEtiologyId = _etiologyList
                                              ?.firstWhere((item) =>
                                                  item.etiology ==
                                                  mappedList[i].etiology)
                                              .id;
                                          _isReadDrugButtonActive = true;
                                          _drugList = null;
                                        });
                                      },
                                      cells: [
                                        DataCell(Text(
                                            mappedList[i].subjectiveSymptom)),
                                        DataCell(Text(mappedList[i].cause)),
                                        DataCell(Text(mappedList[i]
                                            .probability
                                            .toString())),
                                        DataCell(SizedBox(
                                            width: 700,
                                            child:
                                                Text(mappedList[i].etiology))),
                                      ]));
                                }
                                return result;
                              }(),
                            ),
                          ));
                        } else if (snapshot.hasError) {
                          return Text('Error: ${snapshot.error}');
                        } else {
                          return const Text("");
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
                  onPressed: _isReadDrugButtonActive
                      ? () async {
                          setState(() {
                            _drugList = () async {
                              return widget.getDrugList(_selectedEtiologyId!)
                                  as Future<List<Drug>>;
                            }();
                          });
                        }
                      : null,
                  style: ElevatedButton.styleFrom(primary: Colors.red[300]),
                  child: const Text("Read Drug",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                )
              ],
            ),
            Row(
              children: [
                FutureBuilder(
                  key: _selectedEtiologyId == null
                      ? widget.key
                      : ValueKey(_selectedEtiologyId),
                  future: _drugList,
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
                                      label: Text("Drug category")),
                                  const DataColumn(label: Text("Drug use")),
                                  const DataColumn(
                                      label: Text("Mode of action")),
                                  const DataColumn(label: Text("Dose")),
                                ];
                              }(),
                              rows: () {
                                List<Drug> drugList =
                                    (snapshot.data as List<Drug>);
                                List<DataRow> result = [];
                                for (var drug in drugList) {
                                  result.add(DataRow(cells: [
                                    DataCell(Text(drug.drugCategory)),
                                    DataCell(SizedBox(
                                        width: 220, child: Text(drug.drugUse))),
                                    DataCell(SizedBox(
                                        width: 375,
                                        child: Text(drug.modeOfAction))),
                                    DataCell(SizedBox(
                                        width: 375, child: Text(drug.dose))),
                                  ]));
                                }
                                return result;
                              }(),
                            ),
                          ));
                        } else if (snapshot.hasError) {
                          return Text('Error: ${snapshot.error}');
                        } else {
                          return const Text("");
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
