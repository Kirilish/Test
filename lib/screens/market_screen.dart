import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../core/providers.dart';
import '../models/part.dart';

class MarketScreen extends ConsumerStatefulWidget {
  const MarketScreen({super.key});

  @override
  ConsumerState<MarketScreen> createState() => _MarketScreenState();
}

class _MarketScreenState extends ConsumerState<MarketScreen> {
  final TextEditingController _search = TextEditingController();
  String? _sort;

  @override
  Widget build(BuildContext context) {
    final car = ref.watch(currentCarProvider);
    final asyncMatched = ref.watch(matchedPartsProvider);
    final asyncNew = ref.watch(searchPartsProvider(<String, dynamic>{
      'search': _search.text.isEmpty ? null : _search.text,
      'brand': car.brand,
      'model': car.model,
      'generation': car.generation,
      'sort': _sort,
      'withPhoto': true,
    }));

    return Scaffold(
      appBar: AppBar(title: const Text('Магазин Zapshop')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: <Widget>[
          TextField(
            controller: _search,
            decoration: InputDecoration(
              hintText: 'Поиск по названию/OEM',
              suffixIcon: IconButton(
                icon: const Icon(Icons.search),
                onPressed: () => setState(() {}),
              ),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onSubmitted: (_) => setState(() {}),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: <Widget>[
              ChoiceChip(label: const Text('Новые'), selected: _sort == 'new', onSelected: (_) => setState(() => _sort = 'new')),
              ChoiceChip(label: const Text('Дешевле'), selected: _sort == 'price_asc', onSelected: (_) => setState(() => _sort = 'price_asc')),
              ChoiceChip(label: const Text('Дороже'), selected: _sort == 'price_desc', onSelected: (_) => setState(() => _sort = 'price_desc')),
            ],
          ),
          const SizedBox(height: 12),
          Text('Запчасти под мой автомобиль: ${car.brand} ${car.model} ${car.year}'),
          asyncMatched.when(
            data: (items) => _partsList(context, items),
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Text('Ошибка: $e'),
          ),
          const SizedBox(height: 12),
          const Text('Новые поступления'),
          asyncNew.when(
            data: (items) => _partsList(context, items),
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Text('Ошибка: $e'),
          ),
        ],
      ),
    );
  }

  Widget _partsList(BuildContext context, List<Part> items) {
    if (items.isEmpty) {
      return Card(
        child: ListTile(
          title: const Text('Сейчас нет подходящих деталей в наличии.'),
          subtitle: const Text('Вы можете оставить заявку на подбор.'),
          trailing: TextButton(onPressed: () => context.go('/requests'), child: const Text('Оставить заявку')),
        ),
      );
    }
    return Column(
      children: items.take(8).map((Part part) {
        final isFav = ref.watch(favoritesProvider).contains(part.id);
        return Card(
          child: ListTile(
            title: Text(part.title, maxLines: 2, overflow: TextOverflow.ellipsis),
            subtitle: Text('${part.price ?? 'Цена по запросу'} ${part.currency}\n${part.address}\nНужно проверить VIN/OEM'),
            isThreeLine: true,
            onTap: () => context.go('/market/part/${part.id}'),
            trailing: IconButton(
              icon: Icon(isFav ? Icons.favorite : Icons.favorite_border),
              onPressed: () => ref.read(favoritesProvider.notifier).toggle(part.id),
            ),
          ),
        );
      }).toList(),
    );
  }
}
