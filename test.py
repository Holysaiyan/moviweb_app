user = [
  {
    "id": 1,
    "name": "Alice",
    "movies": [
      {
        "id": 1,
        "name": "Inception",
        "director": "Christopher Nolan",
        "year": 2010,
        "rating": 8.8
      },
      {
        "id": 2,
        "name": "The Dark Knight",
        "director": "Christopher Nolan",
        "year": 2008,
        "rating": 9.0
      }
    ]
  },
  {
    "id": 2,
    "name": "Bob",
    "movies": []
  }
]


for u in user:
    for i in u['movies']:
        print(i['name'])
   