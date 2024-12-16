import json
from src.pyls import print_top_level, print_top_level_vertically_with_info

if __name__ == '__main__':
    with open("./data/sample.json") as f:
        data = json.load(f)
    print_top_level(data, True)
    print()
    print_top_level_vertically_with_info(data)
    print()
    print_top_level_vertically_with_info(data, time_sorted=True)



