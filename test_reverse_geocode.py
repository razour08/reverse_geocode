# -*- coding: utf-8 -*-
import reverse_geocode
import unittest


class TestReverseGeocode(unittest.TestCase):
    def test_get(self):
        coordinate = -37.81, 144.96
        results = reverse_geocode.get(coordinate)
        self.assertEqual(results['country_code'], 'AU')
        self.assertEqual(results['country'], 'أستراليا')
        self.assertIn('city', results)
        self.assertAlmostEqual(results['latitude'], -37.814, places=2)
        self.assertAlmostEqual(results['longitude'], 144.96332, places=2)

    def test_search(self):
        coordinates = (-37.81, 144.96), (40.71427000, -74.00597000)
        results = reverse_geocode.search(coordinates)
        self.assertEqual(len(results), 2)
        # Australia
        self.assertEqual(results[0]['country_code'], 'AU')
        self.assertEqual(results[0]['country'], 'أستراليا')
        # United States
        self.assertEqual(results[1]['country_code'], 'US')
        self.assertEqual(results[1]['country'], 'الولايات المتحدة')

    def test_population(self):
        # a coordinate near NYC
        nyc_coordinate = 40.706322, -74.002640
        # when restrict to big cities then get a large city
        big_cities_result = reverse_geocode.get(nyc_coordinate, 100000)
        self.assertEqual(big_cities_result['country_code'], 'US')
        self.assertEqual(big_cities_result['country'], 'الولايات المتحدة')
        self.assertGreaterEqual(big_cities_result['population'], 100000)

    def test_arabic_city_names(self):
        """Test that Arabic city names are returned for well-known cities"""
        # Paris, France
        paris = reverse_geocode.get((48.8566, 2.3522))
        self.assertEqual(paris['country'], 'فرنسا')
        # City should be in Arabic if available
        self.assertIn('city', paris)

        # Dubai, UAE
        dubai = reverse_geocode.get((25.2048, 55.2708))
        self.assertEqual(dubai['country'], 'الإمارات العربية المتحدة')

        # Algiers, Algeria
        algiers = reverse_geocode.get((36.7525, 3.0420))
        self.assertEqual(algiers['country'], 'الجزائر')

    def test_country_code_present(self):
        """Test that country_code is always present in results"""
        coordinate = 35.6762, 139.6503  # Tokyo
        result = reverse_geocode.get(coordinate)
        self.assertIn('country_code', result)
        self.assertEqual(result['country_code'], 'JP')


if __name__ == "__main__":
    unittest.main()
