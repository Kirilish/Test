import 'package:flutter/material.dart';

class ServiceHistoryScreen extends StatelessWidget {
  const ServiceHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('История обслуживания')),
      body: ListView(
        children: const <Widget>[
          ListTile(title: Text('Замена масла'), subtitle: Text('41 000 км • 2026-04-02 • 120 USD')),
          ListTile(title: Text('Колодки передние'), subtitle: Text('39 500 км • 2026-02-15 • 180 USD')),
        ],
      ),
    );
  }
}
