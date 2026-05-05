import json
from comparator import compare_entry
from report import generate_html


with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

results = []

for item in data:
    results.append(compare_entry(item))
    
results.sort(key=lambda x: x["score"])

generate_html(results)

print("Done. Check report.html file.")