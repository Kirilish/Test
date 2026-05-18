import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Профиль пользователя')),
      body: ListView(
        children: const <Widget>[
          ListTile(title: Text('Имя'), subtitle: Text('Иван')),
          ListTile(title: Text('Телефон'), subtitle: Text('+375...')),
          ListTile(title: Text('Telegram'), subtitle: Text('@user')),
          ListTile(title: Text('Подписка'), subtitle: Text('Базовый тариф')),
        ],
      ),
    );
  }
}
