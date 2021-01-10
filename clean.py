import os
import re
import pandas as pd
# os.makedirs("./cleandata");
if not os.path.exists('./cleandata'):
    os.makedirs('./cleandata')
content = os.listdir()
for item in content:
    # delete the text files and the urls files to clean the library
    # print(item)

    if (item.find(".txt") > 0 and item != ".git"):
        print(item)
        with open("./{}".format(item), "r") as f:
            lines = f.readlines()
        # if (os.path.exists("./cleandata/{}".format(item))):
        with open("./cleandata/{}".format(item), "w+") as f:

            for line in lines:
                if "10 Messungen" in line.strip("\n"):
                    line = line[line.find("Ch"):]
                    # print(newline)
                # if (line.strip("\n") != "þStartfischer1 p33-6 hf8 fc6x 0.9km")
                if ("Ch" in line.strip("\n") or "V:" in line.strip("\n")):
                    f.write(line.replace(';', ''))
print("wer are done.... have fun!! KOMPASS-SENSOR")
content = os.listdir("./cleandata")
result=pd.DataFrame();
for x in content:
    if (x.find(".txt") > 0 and x != ".git"):
        print(x)
        df = pd.read_csv("./cleandata/{}".format(x),names=["channal", "min", "max", "x", "y"],sep="\s+",encoding="utf")
        dx = df.drop(["x", "y"], axis=1)
        dx["min"] = dx["min"]  # .map(lambda x: x.lstrip("+-;").rstrip("aAbBcC;"))
        dx["channal"] = dx["channal"]  # .map(lambda x: x.lstrip(";").rstrip(";"))
        if 100 in dx.index:
            dx = dx.drop(100)
        dx["min"] = pd.to_numeric(dx["min"])
        dx["max"] = pd.to_numeric(dx["max"])
        dx["deltas"] = dx["max"] - dx["min"]
        dx.index.name = x
        dx=dx.reset_index()
        #drop empty Dataframes
        if not (dx.empty):
            result=pd.concat([result,dx],axis=1)
print(result.head())
result.to_excel("result.xlsx")
