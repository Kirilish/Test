import 'package:flutter/material.dart';

class RemindersScreen extends StatelessWidget {
  const RemindersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Напоминания')),
      body: ListView(
        children: const <Widget>[
          ListTile(title: Text('Пора заменить масло'), subtitle: Text('через 3 000 км')),
          ListTile(title: Text('Проверьте тормозные колодки'), subtitle: Text('через 1 месяц')),
          ListTile(title: Text('Не забудьте обновить пробег')),
        ],
      ),
    );
  }
}
