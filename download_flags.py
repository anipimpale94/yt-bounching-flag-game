
import os
import urllib.request
import glob

# Top 50 countries by internet users (approximate 2024 data)
flags = [
    "cn", "in", "us", "id", "br", "pk", "ng", "ru", "bd", "jp",
    "mx", "ph", "eg", "vn", "de", "tr", "ir", "gb", "th", "fr",
    "it", "za", "kr", "es", "ar", "co", "iq", "ca", "dz", "ma",
    "my", "pl", "cd", "sa", "mm", "uz", "ua", "pe", "au", "gh",
    "tw", "kz", "cl", "nl", "ro", "ve", "ao", "np", "ec", "sd"
]

base_url = "https://flagcdn.com/w160"
output_dir = "img/flags"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Clean up existing flags not in the list
print("Cleaning up old flags...")
for filepath in glob.glob(os.path.join(output_dir, "*.png")):
    filename = os.path.basename(filepath)
    code = filename.split(".")[0]
    if code not in flags:
        os.remove(filepath)
        # print(f"Removed {filename}")

print(f"Ensuring top {len(flags)} flags are present...")

for code in flags:
    if os.path.exists(f"{output_dir}/{code}.png"):
        continue
        
    url = f"{base_url}/{code}.png"
    try:
        urllib.request.urlretrieve(url, f"{output_dir}/{code}.png")
        print(f"Downloaded {code}.png")
    except Exception as e:
        print(f"Error downloading {code}.png: {e}")

print("Done.")
