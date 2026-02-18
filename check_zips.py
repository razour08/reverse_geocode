
import zipfile
import sys

files = ["cities1000.zip", "alternateNames.zip"]
for f in files:
    try:
        with zipfile.ZipFile(f, 'r') as z:
            ret = z.testzip()
            if ret is not None:
                print(f"File {f} is corrupt. First bad file: {ret}")
                sys.exit(1)
            else:
                print(f"File {f} is valid.")
    except Exception as e:
        print(f"File {f} is invalid or missing: {e}")
        sys.exit(1)
print("All files valid.")
