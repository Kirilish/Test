import 'package:flutter/material.dart';

class OrdersScreen extends StatelessWidget {
  const OrdersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Заказы')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const <Widget>[
          ListTile(title: Text('Заказ #125'), subtitle: Text('Проверяем совместимость')),
          ListTile(title: Text('Заказ #118'), subtitle: Text('Ожидает подтверждения')),
          Card(
            child: Padding(
              padding: EdgeInsets.all(12),
              child: Text('Перед подтверждением заказа менеджер проверит совместимость детали по VIN/OEM.'),
            ),
          ),
        ],
      ),
    );
  }
}
