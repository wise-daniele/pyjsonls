# Pyls

This program takes a json file containing the representation of a directory in nested structure, and prints out its content in the console in the style of ls (linux utility).
(https://github.com/wise-daniele/pyls)

##### JSON file
The top level item of the json must represents a directory with the following elements:
* name: file or directory name
* time_modified: timestamp of the last modified time
* permissions: file's or directory's permission
* contents: list of the files and/or directories within the current directory

The sub elements of the top directory are represented the same way. If the item is a file then the element "contents" is not present.

##### Script Arguments:
* -A: Prints all files and directories at the top level. If path argument is specified prints all files and directories at the path sub level
* -l: Prints the results vertically with additional information
* -r: Prints the results vertically with additional information in reverse order with respect to the json list. If used with the '-t' argument, prints the result in reverse order with respect to the modified time
* -t: Prints the results sorted by the modified time. If used with '-r' argument, prints the result in reverse order with respect to the modified time
* filter='name': Filters the output according to a given option. The available options are 'dir' and 'file'
* optional path: Navigate the structure within the json and prints the file information (if the path represents a file) and the list of contents with their relative information (if the path is a directory)

##### Install Procedure (Linux)
* Open a terminal
* Run "python3 -m build <project_path>"
* Run "python3 -m pip install <project_path>"
* Add the following line to your ~/.bashrc file: "alias pyls=<path_to_binary>/pyls"
* Rename your json as 'sample.json'
* Place your json within the same directory where the executable is located

##### Run 
* Open a terminal
* Run the script together with arguments as specified above
