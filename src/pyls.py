import sys, datetime
import json
from operator import itemgetter

def print_top_level(json_file, print_hidden=False):
    result = ""
    if "contents" in json_file:
        for item in json_file["contents"]:
            if not print_hidden:
                if item["name"][0] != ".":
                    result = result + " " + item["name"]
            else:
                result = result + " " + item["name"]
    print(result)

def print_top_level_vertically_with_info(json_file, print_hidden=False, reverse=False, time_sorted=False):
    my_list = list()
    if "contents" in json_file:
        if reverse:
            my_json_list = reversed(json_file["contents"])
        else:
            my_json_list = json_file["contents"]
        for item in my_json_list:
            date = datetime.datetime.fromtimestamp(item["time_modified"])
            month = date.strftime('%b')
            day = date.day
            hour = date.hour
            minute = date.minute
            my_date = str(month) + " " + str(day) + " " + str(hour) + ":" + str(minute)
            if not print_hidden:
                if item["name"][0] != ".":
                    current_str = item["permissions"] + " " + str(item["size"]) + " " + my_date + " " +item["name"]
                    my_dict = {
                        "timestamp": item["time_modified"],
                        "info": current_str
                    }
                    my_list.append(my_dict)
            else:
                current_str = item["permissions"] + " " + str(item["size"]) + " " + my_date + " " +item["name"]
                my_dict = {
                    "timestamp": item["time_modified"],
                    "info": current_str
                }
                my_list.append(my_dict)
    if time_sorted:
        if reverse:
            my_list = sorted(my_list, key=itemgetter("timestamp"), reverse=True)
        else:
            my_list = sorted(my_list, key=itemgetter("timestamp"))
    for item in my_list:
        print(item["info"])

if __name__ == '__main__':
    print("Start")
    args = sys.argv
    with open("../data/sample.json") as f:
        data = json.load(f)
    print(args)
    if len(args) == 1:
        print_top_level(data)
    elif len(args) == 2 and '-A' in args:
        print_top_level(data, print_hidden=True)
    elif len(args) == 2 and '-l' in args:
        print_top_level_vertically_with_info(data)
    elif len(args) == 3 and '-l' in args and '-r' in args:
        print_top_level_vertically_with_info(data, reverse=True)
    elif len(args) == 3 and '-l' in args and '-t' in args:
        print_top_level_vertically_with_info(data, time_sorted=True)
    elif len(args) == 4 and '-l' in args and '-r' in args and '-t' in args:
        print_top_level_vertically_with_info(data, reverse=True, time_sorted=True)