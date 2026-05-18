import 'package:flutter/material.dart';

class RequestsScreen extends StatelessWidget {
  const RequestsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Заявки на подбор')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: <Widget>[
          const ListTile(title: Text('Фара левая Kia K5'), subtitle: Text('В обработке')),
          const ListTile(title: Text('Бампер передний Kia K5'), subtitle: Text('Найдено 3 варианта')),
          const SizedBox(height: 16),
          FilledButton(onPressed: () {}, child: const Text('Оставить заявку на подбор')),
        ],
      ),
    );
  }
}
