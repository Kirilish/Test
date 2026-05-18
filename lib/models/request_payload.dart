class RequestPayload {
  const RequestPayload({
    required this.name,
    required this.phone,
    required this.vin,
    required this.brand,
    required this.model,
    required this.generation,
    required this.year,
    required this.engine,
    required this.partName,
    required this.comment,
  });

  final String name;
  final String phone;
  final String vin;
  final String brand;
  final String model;
  final String generation;
  final String year;
  final String engine;
  final String partName;
  final String comment;

  Map<String, dynamic> toJson() => <String, dynamic>{
        'name': name,
        'phone': phone,
        'vin': vin,
        'brand': brand,
        'model': model,
        'generation': generation,
        'year': year,
        'engine': engine,
        'part_name': partName,
        'comment': comment,
        'source': 'mobile_app',
      };
}
