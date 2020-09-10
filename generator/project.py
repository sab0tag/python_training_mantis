from model.project import Project
import random
import string
import os.path  # define path to the file
import jsonpickle
import getopt  # read the command line options
import sys  # get access to the command line options

# read the args from the command line
try:
    # "n:" amount of generated data;
    # "f:" file with generated data;
    # [hints]
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

# params analysis; set default values
n = 20
f = "data/groups.json"

for o, a in opts:
    if o == "-n":
        n = int(a) # convert amount of groups value to int
    elif o == "-f":
        f = a #


# gen random testdata
def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.ascii_lowercase + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Project(name="", status="", viewstatus="", description="")] + [
    Project(name=random_string("name", 10), status=random.choice(["development", "release"]), viewstatus=random.choice(["private", "public"]), description="desc" + str(random.randrange(100)))
    for i in range(n)
]

# define path to json file
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)  # get the current directory for file
# open it into a write mode
with open(file, "w") as out_file:
    jsonpickle.set_encoder_options("json", indent=2)
    out_file.write(jsonpickle.encode(testdata))
    # out_file.write(json.dumps(testdata, default=lambda x: x.__dict__, indent=2))  # func to convert object into a dict
