class Part {
  const Part({
    required this.id,
    required this.title,
    required this.brand,
    required this.model,
    required this.generation,
    required this.price,
    required this.currency,
    required this.address,
    required this.image,
  });

  final int id;
  final String title;
  final String brand;
  final String model;
  final String generation;
  final num? price;
  final String currency;
  final String address;
  final String? image;

  factory Part.fromJson(Map<String, dynamic> json) {
    return Part(
      id: json['id'] as int,
      title: json['title'] as String? ?? 'Без названия',
      brand: json['brand'] as String? ?? '',
      model: json['model'] as String? ?? '',
      generation: json['generation'] as String? ?? '',
      price: json['price'] as num?,
      currency: json['currency'] as String? ?? 'USD',
      address: json['address'] as String? ?? 'Склад уточняется',
      image: json['main_image'] as String?,
    );
  }
}
