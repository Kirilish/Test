import 'package:flutter/material.dart';

import '../models/part.dart';

class PartTile extends StatelessWidget {
  const PartTile({
    required this.part,
    required this.onTap,
    super.key,
  });

  final Part part;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final String priceText = part.price == null
        ? 'Цена по запросу'
        : '${part.price} ${part.currency}';

    return Card(
      child: ListTile(
        onTap: onTap,
        leading: CircleAvatar(
          child: Text(part.brand.isEmpty ? '?' : part.brand[0]),
        ),
        title: Text(part.title, maxLines: 2, overflow: TextOverflow.ellipsis),
        subtitle: Text('$priceText\n${part.address}'),
        isThreeLine: true,
        trailing: const Icon(Icons.chevron_right),
      ),
    );
  }
}
