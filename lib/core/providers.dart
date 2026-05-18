import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/car.dart';
import '../models/part.dart';
import '../services/zapshop_api.dart';

final Provider<ZapshopApi> apiProvider = Provider<ZapshopApi>((Ref ref) {
  return ZapshopApi();
});

final StateProvider<Car> currentCarProvider = StateProvider<Car>((Ref ref) {
  return const Car(
    id: 1,
    brand: 'Kia',
    model: 'K5',
    generation: 'DL3',
    year: 2023,
    engine: '1.6 Turbo',
    mileage: 42000,
    vin: 'KNAG...',
  );
});

final FutureProvider<List<Part>> newPartsProvider = FutureProvider<List<Part>>(
  (Ref ref) => ref.read(apiProvider).getParts(sort: 'new', perPage: 20),
);

final FutureProvider<List<Part>> matchedPartsProvider =
    FutureProvider<List<Part>>((Ref ref) {
  final Car car = ref.watch(currentCarProvider);
  return ref
      .read(apiProvider)
      .matchCar(brand: car.brand, model: car.model, generation: car.generation);
});

final FutureProviderFamily<List<Part>, Map<String, dynamic>> searchPartsProvider =
    FutureProviderFamily<List<Part>, Map<String, dynamic>>(
  (Ref ref, Map<String, dynamic> filters) => ref.read(apiProvider).getParts(
        search: filters['search'] as String?,
        brand: filters['brand'] as String?,
        model: filters['model'] as String?,
        generation: filters['generation'] as String?,
        partName: filters['partName'] as String?,
        oem: filters['oem'] as String?,
        minPrice: filters['minPrice'] as num?,
        maxPrice: filters['maxPrice'] as num?,
        withPhoto: filters['withPhoto'] as bool? ?? false,
        sort: filters['sort'] as String?,
      ),
);

final FutureProviderFamily<Part, int> partDetailsProvider =
    FutureProviderFamily<Part, int>(
  (Ref ref, int id) => ref.read(apiProvider).getPartDetails(id),
);

final StateNotifierProvider<FavoritesNotifier, Set<int>> favoritesProvider =
    StateNotifierProvider<FavoritesNotifier, Set<int>>(
  (Ref ref) => FavoritesNotifier(),
);

class FavoritesNotifier extends StateNotifier<Set<int>> {
  FavoritesNotifier() : super(<int>{});

  void toggle(int id) {
    if (state.contains(id)) {
      state = <int>{...state}..remove(id);
      return;
    }
    state = <int>{...state, id};
  }
}
