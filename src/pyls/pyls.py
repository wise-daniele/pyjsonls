import datetime
import json
import argparse
from operator import itemgetter

KILO = 1024
MEGA = KILO ** 2
GIGA = KILO ** 3
TERA = KILO ** 4


def print_top_level(json_data, print_all=False, my_filter=None):
    result = ""
    if "contents" in json_data:
        for item in json_data["contents"]:
            if apply_filter(item, my_filter):
                continue
            if not print_all:
                if item["name"][0] != ".":
                    result = result + " " + item["name"]
            else:
                result = result + " " + item["name"]
    print(result)

def print_top_level_vertically_with_info(json_data, print_all=False, reverse=False, time_sorted=False,
                                         my_filter=None):
    my_list = list()
    if "contents" in json_data:
        if reverse:
            contents_list = reversed(json_data["contents"])
        else:
            contents_list = json_data["contents"]
        my_list = get_list_to_print(contents_list, print_all, my_filter)
    if time_sorted:
        if reverse:
            my_list = sorted(my_list, key=itemgetter("timestamp"), reverse=True)
        else:
            my_list = sorted(my_list, key=itemgetter("timestamp"))
    for item in my_list:
        print(item["info"])

def print_path_info(my_json, print_all=False, reverse=False, time_sorted=False, my_filter=None, path=None):
    list_path = path.split("/")
    my_list = list()
    path_found = False
    for item in my_json["contents"]:
        if list_path[0] != item["name"]:
            continue
        else:
            if len(list_path) == 1 and "contents" in item:
                my_list = get_list_to_print(item["contents"], print_all, my_filter)#print content
            else:
                current_path = "./" + item["name"]
                my_list = recursive_print_path_info(item["contents"], list_path, current_path, print_all, reverse,
                                                    time_sorted, my_filter)
            path_found = True
            break
    if not path_found or not my_list:
        print("error: cannot access '" + path + "': No such file or directory")
    else:
        if time_sorted:
            if reverse:
                my_list = sorted(my_list, key=itemgetter("timestamp"), reverse=True)
            else:
                my_list = sorted(my_list, key=itemgetter("timestamp"))
        for item in my_list:
            print(item["info"])

def recursive_print_path_info(my_json_list, list_path, current_path, print_all=False, reverse=False, time_sorted=False,
                              my_filter=None):
    for item in my_json_list:
        if len(list_path) == 0:
            break
        if list_path[0] == item["name"]:
            if len(list_path) == 1:
                my_list = list()
                my_date = build_date(item["time_modified"])
                if "contents" in item:
                    my_list = get_list_to_print(item["contents"], print_all, my_filter)
                else:
                    current_path = current_path + "/" + list_path.pop(0)
                    my_list.append(build_item_for_list(item["permissions"], item["size"], my_date, item["name"],
                                                       item["time_modified"], current_path))
                return my_list
            else:
                current_path = current_path + "/" + list_path.pop(0)
                recursive_print_path_info(item["contents"], list_path, current_path, print_all, reverse, time_sorted,
                                          my_filter)
        else:
            list_path.pop(0)
            continue
    return None


def get_list_to_print(contents_list, print_all=False, my_filter=None, current_path=None):
    my_list = list()
    for item in contents_list:
        if apply_filter(item, my_filter):
            continue
        my_date = build_date(item["time_modified"])
        if not print_all:
            if item["name"][0] != ".":
                my_list.append(build_item_for_list(item["permissions"], item["size"], my_date, item["name"],
                                                   item["time_modified"]))
        else:
            my_list.append(build_item_for_list(item["permissions"], item["size"], my_date, item["name"],
                                               item["time_modified"]))
    return my_list

def build_item_for_list(permissions, size, date, name, time_modified, path=None):
    my_size = build_size(size)
    if path:
        current_str = permissions + " " + my_size + " " + date + " " + path
    else:
        current_str = permissions + " " + my_size + " " + date + " " + name
    my_dict = {
        "timestamp": time_modified,
        "info": current_str
    }
    return my_dict

def build_size(size):
    if size < KILO:
        return str(size)
    elif KILO <= size < MEGA:
        return '{0:.1f}K'.format(round(size / KILO, 1))
    elif MEGA <= size < GIGA:
        return '{0:.1f}M'.format(round(size / MEGA), 1)
    elif GIGA <= size < TERA:
        return '{0:.1f}G'.format(round(size / GIGA), 1)
    elif TERA <= size:
        return '{0:.1f}T'.format(round(size / TERA), 1)

def build_date(time_modified):
    date = datetime.datetime.fromtimestamp(time_modified)
    month = date.strftime('%b')
    day = date.day
    hour = date.hour
    minute = date.minute
    my_date = str(month) + " " + str(day) + " " + str(hour) + ":" + str(minute)
    return my_date

def apply_filter(item, my_filter):
    if my_filter:
        if (my_filter == "dir" and "contents" not in item) or (my_filter == "file" and "contents" in item):
            return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser("This program takes a json file containing the representation of a directory"
                                     " in nested structure, and prints out its content in the console in the style"
                                     " of ls (linux utility).")
    parser.add_argument('-A', '--print_all', action='store_true',
                        help="Prints all files and directories at the top level. If path argument is specified"
                             "prints all files and directories at the path sub level")
    parser.add_argument('-l', '--vert', action='store_true',
                        help="Prints the results vertically with additional information")
    parser.add_argument('-r', '--reverse', action='store_true',
                        help="Prints the results vertically with additional information in reverse"
                             " order with respect to the json list. If used with the '-t' argument,"
                             " prints the result in reverse order with respect to the modified time",
                        default=False)
    parser.add_argument('-t', '--time', action='store_true',
                        help="Prints the results sorted by the modified time. If used with '-r' "
                             "argument, prints the result in reverse order with respect to the "
                             "modified time")
    parser.add_argument('--filter', type=str, choices=['dir', 'file'],
                        help="Filters the output according to a given option. The available options"
                             " are 'dir' and 'file'")
    parser.add_argument('path', nargs='?',
                        help="Navigate the structure within the json and prints the file information"
                             " if the path represents a file, and the list of contents with their"
                             " relative information if the path is a directory", default=None)
    args = parser.parse_args()

    print(args)
    with open("../../data/sample.json") as f:
        json_data = json.load(f)

    if not args.vert:
        print_top_level(json_data, args.print_all, args.filter)
    else:
        if args.path:
            print_path_info(json_data, args.print_all, args.reverse, args.time, args.filter, args.path)
        else:
            print_top_level_vertically_with_info(json_data, args.print_all, args.reverse, args.time, args.filter)