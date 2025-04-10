import json

# Input and output file paths
input_file = 'consumer_protection_chunks.json'
output_file = 'consumer_protection_chunks_fixed.json'

# Read the newline-delimited JSON objects
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Convert each line into a JSON object
json_objects = [json.loads(line.strip()) for line in lines if line.strip()]

# Write the objects as a valid JSON array
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(json_objects, f, indent=2, ensure_ascii=False)

print(f"✅ Fixed JSON saved to: {output_file}")
