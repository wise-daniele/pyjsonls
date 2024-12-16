import json
from src.pyls import print_top_level

if __name__ == '__main__':
    with open("./data/sample.json") as f:
        data = json.load(f)
    print_top_level(data, True)



