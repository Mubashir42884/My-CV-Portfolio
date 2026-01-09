import json

# Placeholder logic. Update this with real scraping logic (e.g. SerpAPI) later.
data = [
  {
    "title": "Deep Learning Approaches for Medical Image Segmentation",
    "authors": "M. Mohsin, Co-Author A",
    "venue": "Journal of Medical Imaging",
    "year": 2024,
    "citations": 15,
    "url": "#"
  },
  {
    "title": "Trustworthy AI in Healthcare",
    "authors": "M. Mohsin, Co-Author B",
    "venue": "International Conference on AI",
    "year": 2023,
    "citations": 8,
    "url": "#"
  }
]

with open('public/scholar.json', 'w') as f:
    json.dump(data, f)
    print("Updated public/scholar.json")