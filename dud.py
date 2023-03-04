import random
"""for x in range(1, 50):
  print(round((4 * (x ** 3)) / 5))"""
pos = {"Common": 40, "Rare": 45, "Epic": 13, "Legendary": 2}
items = {
    "개량한복": {
        "rarity": "Common",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "술 잔": {
        "rarity": "Common",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "국자": {
        "rarity": "Common",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "저고리": {
        "rarity": "Rare",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "깃털 머리띠": {
        "rarity": "Rare",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "솥뚜껑": {
        "rarity": "Rare",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "이빨": {
        "rarity": "Epic",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "비녀": {
        "rarity": "Epic",
        "image": "https://i.imgur.com/NHBALeB.png",
    },
        "줄무늬 그것": {
        "rarity": "Epic",
        "image" : "https://i.imgur.com/NHBALeB.png",
    },
        "알 수 없는 용액": {
        "rarity": "Legendary", #침
        "image" : "https://i.imgur.com/NHBALeB.png", 
    }
}

#a=random.choice(list(items.keys()))
rarity = random.choices(list(pos.keys()), weights=list(pos.values()), k=1)[0]
item = random.choice([k for k, v in items.items() if v["rarity"] == rarity])
print(item)