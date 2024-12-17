import datetime
import json
import argparse
from operator import itemgetter


def print_top_level(data, print_all=False, filter=None):
    result = ""
    if "contents" in data:
        for item in data["contents"]:
            if apply_filter(item, filter):
                continue
            if not print_all:
                if item["name"][0] != ".":
                    result = result + " " + item["name"]
            else:
                result = result + " " + item["name"]
    print(result)

def print_top_level_vertically_with_info(data, print_all=False, reverse=False, time_sorted=False, my_filter=None):
    my_list = list()
    if "contents" in data:
        if reverse:
            my_json_list = reversed(data["contents"])
        else:
            my_json_list = data["contents"]
        for item in my_json_list:
            if apply_filter(item, my_filter):
                continue
            date = datetime.datetime.fromtimestamp(item["time_modified"])
            month = date.strftime('%b')
            day = date.day
            hour = date.hour
            minute = date.minute
            my_date = str(month) + " " + str(day) + " " + str(hour) + ":" + str(minute)
            if not print_all:
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

def apply_filter(item, my_filter):
    if my_filter:
        if (my_filter == "dir" and "contents" not in item) or (my_filter == "file" and "contents" in item):
            return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', '--print_all', action=argparse.BooleanOptionalAction,
                        help="Prints all files and directories (only top level)", default=False)
    parser.add_argument('-l', '--vert', action=argparse.BooleanOptionalAction,
                        help="Prints the results vertically with additional information",
                        default=False)
    parser.add_argument('-r', '--reverse', action=argparse.BooleanOptionalAction,
                        help="Prints the results vertically with additional information in reverse"
                             " order with respect to the json list. If used with the '-t' argument,"
                             " prints the result in reverse order with respect to the modified time",
                        default=False)
    parser.add_argument('-t', '--time', action=argparse.BooleanOptionalAction,
                        help="Prints the results sorted by the modified time. If used with '-r' "
                             "argument, prints the result in reverse order with respect to the "
                             "modified time", default=False)
    parser.add_argument('--filter', type=str, choices=['dir', 'file'],
                        help="Filters the output according to a given option. The available options"
                             " are 'dir' and 'file'")
    args = parser.parse_args()

    print(args)
    with open("../data/sample.json") as f:
        data = json.load(f)

    if not args.vert:
        print_top_level(data, args.print_all, args.filter)
    else:
        print_top_level_vertically_with_info(data, args.print_all, args.reverse, args.time, args.filter)