
print("Start import test")
try:
    import reverse_geocode
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
