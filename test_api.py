import requests
import json
import os
import time

BASE_URL = "http://localhost:8000"

print("Testing Resume API...")

# Test health
response = requests.get(f"{BASE_URL}/health")
print(f"Health: {response.json()}")

# Create test file
test_filename = "test.doc"
with open(test_filename, "w") as f:
    f.write("Test resume content")

# Create candidate - open file inside the request to ensure it's closed
with open(test_filename, 'rb') as f:
    files = {'resume': (test_filename, f, 'application/msword')}
    data = {
        'full_name': 'Jane Smith',
        'dob': '1992-05-15',
        'contact_number': '+9876543210',
        'contact_address': '456 Oak Ave',
        'education_qualification': 'Master of CS',
        'graduation_year': '2014',
        'years_of_experience': '6',
        'skill_set': json.dumps(['Python', 'Django', 'PostgreSQL'])
    }
    
    response = requests.post(f"{BASE_URL}/api/candidates/", data=data, files=files)
    print(f"\nCreate: {response.status_code}")
    if response.status_code == 201:
        print(json.dumps(response.json(), indent=2))
        candidate_id = response.json()['id']
        
        # Get by ID
        time.sleep(1)  # Small delay
        response = requests.get(f"{BASE_URL}/api/candidates/{candidate_id}")
        print(f"\nGet by ID: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))

# Wait a bit before listing
time.sleep(1)

# List all
response = requests.get(f"{BASE_URL}/api/candidates/")
print(f"\nList all: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Total candidates: {data['total']}")
    for c in data['candidates']:
        print(f"  - {c['full_name']} (ID: {c['id']}): {c['skill_set']}")

# Clean up test file
try:
    if os.path.exists(test_filename):
        os.remove(test_filename)
        print(f"\n✅ Cleaned up: {test_filename}")
except PermissionError:
    print(f"\n⚠️ Could not delete {test_filename} - will retry")
    time.sleep(2)
    try:
        os.remove(test_filename)
        print(f"✅ Deleted on retry")
    except:
        print(f"❌ Still cannot delete - you may need to delete manually")