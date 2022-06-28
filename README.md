# OPSWAT Technical Assessment

![logo](https://static.opswat.com/uploads/images/brand_opswat.png)

This program was developed for completion of the OPSWAT Technical Assessment as part of consideration
for the Software Engineer position, Tampa FL. This program makes use of the OPSWAT Metadefender API
[metadefender.opswat.com](metadefender.opswat.com). The program calculates a hash of the given file, then performs a hash lookup
against existing files on [metadefender.opswat.com](metadefender.opswat.com). If the file exists, then the corresponding scan results
will be displayed and the program will terminate. If no hash match is found, then the given file will be uploaded via the OPSWAT
Metadefender API. Results will be repeatedly pulled using the resultant file ID while the file is still in queue to be scanned.

This program makes use of a SHA256 hash to perform the necessary hash lookup. This is done as SHA256 as it is one of the three hash types accepted by the API (MD5, SHA1, SHA256) and is generally considered to be the most secure of the three.

## Prerequisites

A Python version of 3.8.10 or later is required. The latest version of choice can be downloaded [here](https://www.python.org/downloads/). Alternatively, for a Linux environment, an example of how the latest Python version can be downloaded (update as necessary) is shown below:

```install
sudo apt install python3
sudo apt install python3.8
```

This program makes use of various modules that are required for proper execution:

- requests
- hashlib
- sys
- time
- json

These can installed, as necessary, using the [pip](https://pip.pypa.io/en/stable/) package manager via a command line interface,
such as a Linux terminal or bash.

Ex:

```pip
pip install hashlib
```

## Installation and Usage

This program can be run on a clean Ubuntu 20.04 VM or a Visual Studio 2022 Windows machine as required.

The initial installation steps can be as follows:

1. Clone the repository
2. Provide API key in APIKEY variable at top of program file.

```key
APIKEY = "" # API key
```

To run on a **Ubuntu** machine, the program can be run in the command line. The file to test can be passed in as an argument. An example can be seen below:

```python
python hash.py sample_file.txt
python3 hash.py sample_file.txt
```

Alternatively, the direct file path can be provided, such as if the file is not in the local directory:

```python
python hash.py /path/to/sample_file.txt
python3 hash.py /path/to/sample_file.txt
```

For a **Visual Studio 2022** environment, one can create a new project as follows:

1. Select "Create a new project" in the "Get started" menu upon startup.
2. Select "From Existing Python Code" and click Next.
3. Give a project name and the location of the program. Give a solution name and click Create.
4. In the "Welcome to the Create New Project From Existing Python Code Wizard", select the folder of the desired code and click Next.
5. Select a Python interpreter (latest version should suffice) and click Next.
6. Select where to save project and click Finish.

If not using the "Get Started" menu:

1. Go to File > New > Project From Existing Code
2. In "Welcome to the Create New Project From Existing Code Files Wizard, select the type of project (Visual Basic should suffice) and click Next.
3. Select the where files are and give a name to the project. The output type can remain as default (console application).

Alternatively, one can clone and download the program from Github directly:

1. Select "Clone a repo" in the "Get started" menu.
2. Enter the repository location URL (INSERT HERE).
3. Select desired file path and click Clone.
4. Double-click "Folder View" in Solution Explorer on the right-hand side of screen.
5. Select desired program to run/edit.
6. Ensure proper interpreter environment is selected in the drop-down menu above.
7. Follow steps above to create new project from existing code as necessary.

To add a file as argument in Visual Studio 2022:

1. Add file argument form Project > Properties > Debug tab > Script arguments.
2. You can also check the interpreter in the General tab > Interpreter.
3. Run and build file as necessary.

Feel free to modify these steps as necessary to fit your testing preferences.
