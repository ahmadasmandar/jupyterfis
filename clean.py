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
a={}
content = os.listdir("./cleandata")
result=pd.DataFrame()
verhaeltnis=pd.DataFrame()
for x in content:
    if (x.find(".txt") > 0 and x != ".git"):
        #print(x)
        df = pd.read_csv("./cleandata/{}".format(x),names=["channal", "min", "max", "x", "y"],sep="\s+",encoding="cp1258")
        dx = df.drop(["x", "y"], axis=1)
        dx["min"] = dx["min"]  # .map(lambda x: x.lstrip("+-;").rstrip("aAbBcC;"))
        dx["channal"] = dx["channal"]  # .map(lambda x: x.lstrip(";").rstrip(";"))
        if 100 in dx.index:
            dx = dx.drop(100)
        dx["min"] = pd.to_numeric(dx["min"])
        dx["max"] = pd.to_numeric(dx["max"])
        dx["deltas"] = dx["max"] - dx["min"]
        dv=dx[dx.channal == "V:"]
        dv.index.name=x.strip('.txt')
        dx.index.name = x.strip('.txt')
        dx=dx.reset_index()
        #dv=dv.drop(["min", "max","deltas"], axis=1)#.reset_index()
        dv=dv.reset_index()
        if not (dx.empty):
            a[x]=dv
        dv=dv.replace('V:', 'V:{}'.format(x.strip('.txt')))
        #drop empty Dataframes
        #print(dv.head())
        #dx.append(pd.Series(name='NameOfNewRow'))
        if not (dx.empty):
            result=pd.concat([result,dx.append(pd.Series(name='Verh..'))],axis=1)
            verhaeltnis=pd.concat([verhaeltnis,dv],axis=1)
            new_df=result.append(verhaeltnis)

#new_df=pd.concat([result,verhaeltnis])
#print(result.head())
result.to_excel("result.xlsx")
verhaeltnis=verhaeltnis.drop(["max","deltas"], axis=1)
verhaeltnis=verhaeltnis.rename(columns={"min": "V"})
verhaeltnis.head()
verhaeltnis.to_excel("verhaeltnis.xlsx")
new_df.to_excel("FullData.xlsx")
