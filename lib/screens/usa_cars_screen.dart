import 'package:flutter/material.dart';

class UsaCarsScreen extends StatelessWidget {
  const UsaCarsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Авто из США')),
      body: ListView(
        children: const <Widget>[
          ListTile(title: Text('Проверка VIN'), subtitle: Text('История, комплектация, риск')), 
          ListTile(title: Text('Памятка по подбору деталей'), subtitle: Text('Сверка OEM и разъемов')), 
        ],
      ),
    );
  }
}
