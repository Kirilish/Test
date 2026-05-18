class Car {
  const Car({
    required this.id,
    required this.brand,
    required this.model,
    required this.generation,
    required this.year,
    required this.engine,
    required this.mileage,
    required this.vin,
  });

  final int id;
  final String brand;
  final String model;
  final String generation;
  final int year;
  final String engine;
  final int mileage;
  final String vin;

  String get fullName => '$brand $model $year $engine';
}
