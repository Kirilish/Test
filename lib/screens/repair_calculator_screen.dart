import 'package:flutter/material.dart';

class RepairCalculatorScreen extends StatelessWidget {
  const RepairCalculatorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Калькулятор ремонта')),
      body: const Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text('MVP-заглушка калькулятора:'),
            Text('- Стоимость деталей'),
            Text('- Стоимость работ'),
            Text('- Итого по ремонту'),
          ],
        ),
      ),
    );
  }
}
