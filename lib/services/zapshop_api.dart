import 'package:dio/dio.dart';

import '../models/part.dart';
import '../models/request_payload.dart';

class ZapshopApi {
  ZapshopApi()
      : _dio = Dio(
          BaseOptions(
            baseUrl: 'https://zapshop.by/wp-json/pmm/v1',
            connectTimeout: const Duration(seconds: 10),
            receiveTimeout: const Duration(seconds: 15),
          ),
        );

  final Dio _dio;

  Future<List<Part>> getParts({
    String? search,
    String? brand,
    String? model,
    String? generation,
    String? partName,
    String? oem,
    num? minPrice,
    num? maxPrice,
    bool withPhoto = false,
    String? sort,
    int page = 1,
    int perPage = 20,
  }) async {
    final Response<dynamic> response = await _dio.get<dynamic>(
      '/parts',
      queryParameters: <String, dynamic>{
        'search': search,
        'brand': brand,
        'model': model,
        'generation': generation,
        'part_name': partName,
        'oem': oem,
        'min_price': minPrice,
        'max_price': maxPrice,
        'with_photo': withPhoto ? 1 : null,
        'sort': sort,
        'page': page,
        'per_page': perPage,
      }..removeWhere((String key, dynamic value) => value == null),
    );

    final List<dynamic> items =
        (response.data as Map<String, dynamic>)['items'] as List<dynamic>? ??
            <dynamic>[];
    return items
        .whereType<Map<String, dynamic>>()
        .map(Part.fromJson)
        .toList(growable: false);
  }

  Future<List<Part>> matchCar({
    required String brand,
    required String model,
    required String generation,
    int page = 1,
    int perPage = 20,
  }) async {
    final Response<dynamic> response = await _dio.get<dynamic>(
      '/parts/match-car',
      queryParameters: <String, dynamic>{
        'brand': brand,
        'model': model,
        'generation': generation,
        'page': page,
        'per_page': perPage,
      },
    );

    final List<dynamic> items =
        (response.data as Map<String, dynamic>)['items'] as List<dynamic>? ??
            <dynamic>[];
    return items
        .whereType<Map<String, dynamic>>()
        .map(Part.fromJson)
        .toList(growable: false);
  }

  Future<Map<String, dynamic>> getFilters() async {
    final Response<dynamic> response = await _dio.get<dynamic>('/filters');
    return response.data as Map<String, dynamic>;
  }

  Future<Part> getPartDetails(int id) async {
    final Response<dynamic> response = await _dio.get<dynamic>('/parts/$id');
    return Part.fromJson(response.data as Map<String, dynamic>);
  }

  Future<String> checkFitment({
    required int partId,
    required String brand,
    required String model,
    required String generation,
  }) async {
    final Response<dynamic> response = await _dio.get<dynamic>(
      '/parts/$partId/check-fitment',
      queryParameters: <String, dynamic>{
        'brand': brand,
        'model': model,
        'generation': generation,
      },
    );
    final Map<String, dynamic> json = response.data as Map<String, dynamic>;
    return json['status'] as String? ?? 'Нужно проверить VIN/OEM';
  }

  Future<void> createRequest(RequestPayload payload) async {
    await _dio.post<dynamic>('/requests', data: payload.toJson());
  }
}
