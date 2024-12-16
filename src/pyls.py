
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