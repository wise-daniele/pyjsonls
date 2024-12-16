
def print_top_level(json_file):
    result = ""
    if "contents" in json_file:
        for item in json_file["contents"]:
            if item["name"][0] != ".":
                result = result + " " + item["name"]
    print(result)