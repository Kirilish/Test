import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../screens/ai_assistant_screen.dart';
import '../screens/garage_screen.dart';
import '../screens/home_screen.dart';
import '../screens/market_screen.dart';
import '../screens/orders_screen.dart';
import '../screens/part_details_screen.dart';
import '../screens/profile_screen.dart';
import '../screens/reminders_screen.dart';
import '../screens/repair_calculator_screen.dart';
import '../screens/requests_screen.dart';
import '../screens/service_history_screen.dart';
import '../screens/usa_cars_screen.dart';

class ZapshopGarageApp extends StatelessWidget {
  const ZapshopGarageApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Zapshop Garage',
      theme: ThemeData(colorSchemeSeed: const Color(0xFF0B7CE8), useMaterial3: true),
      routerConfig: _router,
    );
  }
}

final GoRouter _router = GoRouter(
  routes: <RouteBase>[
    GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    GoRoute(path: '/garage', builder: (_, __) => const GarageScreen()),
    GoRoute(path: '/service-history', builder: (_, __) => const ServiceHistoryScreen()),
    GoRoute(path: '/reminders', builder: (_, __) => const RemindersScreen()),
    GoRoute(path: '/ai', builder: (_, __) => const AiAssistantScreen()),
    GoRoute(
      path: '/market',
      builder: (_, __) => const MarketScreen(),
      routes: <RouteBase>[
        GoRoute(
          path: 'part/:id',
          builder: (_, GoRouterState state) =>
              PartDetailsScreen(partId: int.parse(state.pathParameters['id']!)),
        ),
      ],
    ),
    GoRoute(path: '/requests', builder: (_, __) => const RequestsScreen()),
    GoRoute(path: '/orders', builder: (_, __) => const OrdersScreen()),
    GoRoute(path: '/calculator', builder: (_, __) => const RepairCalculatorScreen()),
    GoRoute(path: '/usa-cars', builder: (_, __) => const UsaCarsScreen()),
    GoRoute(path: '/profile', builder: (_, __) => const ProfileScreen()),
  ],
);
