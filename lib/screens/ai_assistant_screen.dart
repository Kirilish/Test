import 'package:flutter/material.dart';

class AiAssistantScreen extends StatefulWidget {
  const AiAssistantScreen({super.key});

  @override
  State<AiAssistantScreen> createState() => _AiAssistantScreenState();
}

class _AiAssistantScreenState extends State<AiAssistantScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<String> _messages = <String>[
    'AI: Для точного подбора укажите VIN, сторону детали, OEM и комплектацию.',
  ];

  void _send() {
    if (_controller.text.trim().isEmpty) return;
    setState(() {
      _messages.add('Вы: ${_controller.text}');
      _messages.add(
        'AI: По марке и модели деталь может подходить, но перед покупкой нужно проверить VIN/OEM, сторону, разъём и комплектацию. Могу показать варианты в магазине или создать заявку.',
      );
      _controller.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI-помощник')),
      body: Column(
        children: <Widget>[
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: _messages.length,
              itemBuilder: (_, i) => Card(child: Padding(padding: const EdgeInsets.all(12), child: Text(_messages[i]))),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: <Widget>[
                Expanded(child: TextField(controller: _controller, decoration: const InputDecoration(hintText: 'Нужна фара на Kia K5 2023'))),
                IconButton(onPressed: _send, icon: const Icon(Icons.send)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
