import datetime

def print_top_level(json_file, print_hidden):
    result = ""
    if "contents" in json_file:
        for item in json_file["contents"]:
            if not print_hidden:
                if item["name"][0] != ".":
                    result = result + " " + item["name"]
            else:
                result = result + " " + item["name"]
    print(result)

def print_top_level_vertically_with_info(json_file, print_hidden, reverse):
    result = ""
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
                    result = result + item["permissions"] + " " + str(item["size"]) + " " + my_date + " " +item["name"] + "\n"
            else:
                result = result + item["permissions"] + " " + str(item["size"]) + " " + my_date + " " +item["name"] + "\n"
    print(result)