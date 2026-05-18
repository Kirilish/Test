import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../core/providers.dart';
import '../services/zapshop_api.dart';

class PartDetailsScreen extends ConsumerStatefulWidget {
  const PartDetailsScreen({required this.partId, super.key});

  final int partId;

  @override
  ConsumerState<PartDetailsScreen> createState() => _PartDetailsScreenState();
}

class _PartDetailsScreenState extends ConsumerState<PartDetailsScreen> {
  String _fitment = 'Нужно проверить VIN/OEM';

  Future<void> _checkFitment() async {
    final car = ref.read(currentCarProvider);
    final api = ref.read(apiProvider);
    final status = await api.checkFitment(
      partId: widget.partId,
      brand: car.brand,
      model: car.model,
      generation: car.generation,
    );
    setState(() => _fitment = status);
  }

  @override
  Widget build(BuildContext context) {
    final part = ref.watch(partDetailsProvider(widget.partId));
    return Scaffold(
      appBar: AppBar(title: const Text('Карточка товара')),
      body: part.when(
        data: (item) => ListView(
          padding: const EdgeInsets.all(16),
          children: <Widget>[
            Text(item.title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text('Цена: ${item.price ?? 'Цена по запросу'} ${item.currency}'),
            Text('Марка/модель/поколение: ${item.brand} ${item.model} ${item.generation}'),
            Text('Адрес/склад: ${item.address}'),
            const SizedBox(height: 12),
            const Text('Совместимость', style: TextStyle(fontWeight: FontWeight.bold)),
            Text(_fitment),
            const Text('Перед покупкой обязательно сверим совместимость по VIN/OEM, комплектации и фото старой детали.'),
            const SizedBox(height: 16),
            FilledButton(onPressed: _checkFitment, child: const Text('Проверить совместимость')),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: <Widget>[
                FilledButton(onPressed: () {}, child: const Text('Купить / Оформить заказ')),
                OutlinedButton(onPressed: () {}, child: const Text('Оставить заявку')),
                OutlinedButton(onPressed: () {}, child: const Text('Спросить AI')),
                OutlinedButton(onPressed: () {}, child: const Text('Позвонить')),
                OutlinedButton(onPressed: () {}, child: const Text('Написать в Telegram')),
                OutlinedButton(onPressed: () {}, child: const Text('Открыть на сайте')),
              ],
            ),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Ошибка: $e')),
      ),
    );
  }
}
