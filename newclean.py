# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

# %% [markdown]
# # Data files full clean

# %%
import os
import re

############## Read and Clean TXT files ############################
# os.makedirs("./cleandata");
if not os.path.exists("./cleandata"):
    os.makedirs("./cleandata")
content = os.listdir()
for item in content:
    # delete the text files and the urls files to clean the library
    # print(item)

    if item.find(".txt") > 0 and item != ".git":
        print(item)
        with open("./{}".format(item), "r") as f:
            lines = f.readlines()
        # if (os.path.exists("./cleandata/{}".format(item))):
        with open("./cleandata/{}".format(item), "w+") as f:

            for line in lines:
                if "10 Messungen" in line.strip("\n"):
                    line = line[line.find("Ch") :]
                    # print(newline)
                if (
                    "Ch" in line.strip("\n")
                    or "VR1:" in line.strip("\n")
                    or "VR2:" in line.strip("\n")
                ):
                    f.write(line.replace(";", " "))

# print(content)

# %% [markdown]
# # Extract the Data and convert it to Dataframes and Excel files

# %%
import xlwt

a = {}
lst = {}
if not os.path.exists("./outvr"):
    os.makedirs("./outvr")
content = os.listdir("./cleandata")
result = pd.DataFrame()
verhaeltnis = pd.DataFrame()
deltas = pd.DataFrame()
new_df = pd.DataFrame()
for x in content:
    if x.find(".txt") > 0 and x != ".git":
        # print(x)
        df = pd.read_csv(
            "./cleandata/{}".format(x),
            names=["channal", "min", "max", "x", "y"],
            sep="\s+",
            encoding="ISO-8859-1",
        )
        dx = df.drop(["x", "y"], axis=1)
        # .map(lambda x: x.lstrip("+-;").rstrip("aAbBcC;"))
        dx["min"] = dx["min"]
        # .map(lambda x: x.lstrip(";").rstrip(";"))
        dx["channal"] = dx["channal"]
        if 100 in dx.index:
            dx = dx.drop(100)
        dx["min"] = pd.to_numeric(dx["min"])
        dx["max"] = pd.to_numeric(dx["max"])
        dx["deltas"] = dx["max"] - dx["min"]
        # dx["name"]=x.strip('.txt')
        ########### Extract channals ######

        ch0 = dx[dx.channal == "Ch0:"]
        ch1 = dx[dx.channal == "Ch1:"]
        ch2 = dx[dx.channal == "Ch2:"]
        ch3 = dx[dx.channal == "Ch3:"]
        ch4 = dx[dx.channal == "Ch4:"]
        ch5 = dx[dx.channal == "Ch5:"]
        ch6 = dx[dx.channal == "Ch6:"]
        ch7 = dx[dx.channal == "Ch7:"]
        ch8 = dx[dx.channal == "Ch8:"]
        # print(ch0.head())
        ############ build the deltas #############
        delta0 = ch0["max"] - ch0["min"]
        lst["delta0"] = delta0
        delta1 = ch1["max"] - ch1["min"]
        lst["delta1"] = delta1
        delta2 = ch2["max"] - ch2["min"]
        lst["delta2"] = delta2
        delta3 = ch3["max"] - ch3["min"]
        lst["delta3"] = delta3
        delta4 = ch4["max"] - ch4["min"]
        lst["delta4"] = delta4
        delta5 = ch5["max"] - ch5["min"]
        lst["delta5"] = delta5
        delta6 = ch6["max"] - ch6["min"]
        lst["delta6"] = delta6
        delta7 = ch7["max"] - ch7["min"]
        lst["delta7"] = delta7
        delta8 = ch8["max"] - ch8["min"]
        lst["delta8"] = delta8
        # print(delta0.head())
        # format reset index

        df_new = pd.DataFrame.from_dict(lst)
        df_new = df_new.apply(lambda x: pd.Series(x.dropna().values))
        # print(df_new.head(3))
        dv1 = dx[dx.channal == "VR1:"]
        dv2 = dx[dx.channal == "VR2:"]

        # connect the name of Measurement
        dv1.index.name = x.strip(".txt")
        dv2.index.name = x.strip(".txt")
        dx.index.name = x.strip(".txt")
        df_new.index.name = x.strip(".txt")

        dx = dx.reset_index()
        # clean the verhältnis Tabelle
        dv1 = dv1.reset_index()
        dv1 = dv1.rename(columns={"min": "VR1"})
        dv1 = dv1.drop(columns={"max", "deltas"})

        dv2 = dv2.reset_index(drop=True)
        dv2 = dv2.rename(columns={"min": "VR2"})
        dv2 = dv2.drop(columns={"channal", "max", "deltas"})
        df_new = df_new.reset_index()

        if not (dx.empty):
            a[x.strip(".txt")] = dx
        dv1 = dv1.replace("VR1:", "VR:{}".format(x.strip(".txt")))
        # dv2 = dv2.replace("VR2:", "VR2:{}".format(x.strip(".txt")))
        rows = df_new.shape[0]
        # print(rows)
        for row in range(rows):
            df_new["name"] = x.strip(".txt")
        # drop empty Dataframes
        if not (dx.empty):

            ratio = pd.concat([dv1, dv2], axis=1)
            ratio_mean = ratio.mean(axis=0)
            ratio_std = ratio.std(axis=0)
            # drop the index Mean values
            ratio_mean = ratio_mean.drop(ratio_mean.index[0])
            ratio_std = ratio_std.drop(ratio_std.index[0])
            ratio_mean["channal"] = "mean"
            ratio_std["channal"] = "standard deviation"

            ratio = ratio.append([ratio_mean, ratio_std], ignore_index=True)
            ratio = ratio.drop(ratio.columns[0], axis=1)
            name = "./outvr/{}.xlsx".format(x.strip(".txt"))
            ratio.to_excel(name)

            # deltas = pd.concat([deltas, df_new], axis=1)

# print(ratio_std.head())
# ratio_mean.to_excel("test.xlsx")


# %%
