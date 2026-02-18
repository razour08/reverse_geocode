# -*- coding: utf-8 -*-
import sys
import io
import logging
import traceback

# Force stdout to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

import reverse_geocode

# Test coordinates
# Dubai, UAE
dubai = (25.2048, 55.2708)
# Paris, France
paris = (48.8566, 2.3522)
# Algiers, Algeria
algiers = (36.7525, 3.0420)

print("Starting search...")
try:
    results = reverse_geocode.search([dubai, paris, algiers])

    for coords, result in zip([dubai, paris, algiers], results):
        print(f"Coords: {coords} -> City: {result['city']}, Country: {result['country']}")
except Exception:
    traceback.print_exc()
