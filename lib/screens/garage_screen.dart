import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../core/providers.dart';

class GarageScreen extends ConsumerWidget {
  const GarageScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final car = ref.watch(currentCarProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Мой гараж')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: <Widget>[
          ListTile(title: Text(car.fullName), subtitle: Text('VIN: ${car.vin}\nПробег: ${car.mileage} км')),
          const Divider(),
          const ListTile(title: Text('Добавить ремонт'), subtitle: Text('Запишите замену масла, фильтров, тормозов и т.д.')),
          const ListTile(title: Text('Источник авто'), subtitle: Text('Авто из США: да')),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(onPressed: () {}, label: const Text('Добавить авто')),
    );
  }
}
