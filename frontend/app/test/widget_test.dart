// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';
import 'package:app/main.dart';

void main() {
  testWidgets('All widgets render test', (WidgetTester tester) async {
    await tester.pumpWidget(const App());

    expect(find.text("Predict Etiology from Symptoms"), findsOneWidget);
    expect(find.text("Select subjective symptoms: "), findsOneWidget);
    expect(find.text("Select objective symptoms: "), findsOneWidget);
    expect(find.text("Select gender: "), findsOneWidget);
    expect(find.text("Predict Cause"), findsOneWidget);
    expect(find.text("Read Drug"), findsOneWidget);
    await tester.pump();

    // await tester.tap(find.textContaining("Vomiting;", findRichText: true));
    // await tester.pump();
    // await tester
    //     .tap(find.textContaining("Feeling nausea;", findRichText: true));
    // await tester.pump();
    // await tester.tap(find.textContaining("Female", findRichText: true));
    // await tester.pump();
    // await tester.tap(find.textContaining("Predict Cause", findRichText: true));
    // await tester.pump();

    // expect(find.text("miscellaneous"), findsOneWidget);
  });
}
