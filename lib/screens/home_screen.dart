import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../core/providers.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final car = ref.watch(currentCarProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Zapshop Garage')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: <Widget>[
          Text('Ваш автомобиль: ${car.fullName}', style: Theme.of(context).textTheme.titleMedium),
          Text('Пробег: ${car.mileage} км • Следующее ТО: через 3 000 км'),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: <Widget>[
              FilledButton(onPressed: () => context.go('/market'), child: const Text('Открыть магазин')),
              OutlinedButton(onPressed: () => context.go('/garage'), child: const Text('Мой гараж')),
              OutlinedButton(onPressed: () => context.go('/service-history'), child: const Text('История обслуживания')),
              OutlinedButton(onPressed: () => context.go('/reminders'), child: const Text('Напоминания')),
              OutlinedButton(onPressed: () => context.go('/ai'), child: const Text('Спросить AI')),
            ],
          ),
          const SizedBox(height: 20),
          const Text('Разделы приложения'),
          ...<Map<String, String>>[
            {'t': 'Подбор запчасти', 'r': '/market'},
            {'t': 'Заявки', 'r': '/requests'},
            {'t': 'Заказы', 'r': '/orders'},
            {'t': 'Калькулятор ремонта', 'r': '/calculator'},
            {'t': 'Авто из США', 'r': '/usa-cars'},
            {'t': 'Профиль пользователя', 'r': '/profile'},
          ].map((e) => Card(
                child: ListTile(
                  title: Text(e['t']!),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () => context.go(e['r']!),
                ),
              )),
        ],
      ),
    );
  }
}
