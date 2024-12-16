import datetime
import json
import argparse
from operator import itemgetter


def print_top_level(json_file, all=False):
    result = ""
    if "contents" in json_file:
        for item in json_file["contents"]:
            if not all:
                if item["name"][0] != ".":
                    result = result + " " + item["name"]
            else:
                result = result + " " + item["name"]
    print(result)

def print_top_level_vertically_with_info(json_file, all=False, reverse=False, time_sorted=False, filter=None):
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
            if not all:
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', '--all', action=argparse.BooleanOptionalAction,
                        help="Prints all top level files and directories", default=False)
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
        print_top_level(data, args.all)
    else:
        print_top_level_vertically_with_info(data, args.all, args.reverse, args.time, args.filter)