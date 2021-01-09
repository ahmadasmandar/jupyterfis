import os
import re
#os.makedirs("./cleandata");
if not os.path.exists('./cleandata'):
    os.makedirs('./cleandata')
content=os.listdir()

for item in content:
    # delete the text files and the urls files to clean the library
    # print(item)
    if (item.find(".txt") > 0 ):
        print(item)
        with open("./{}".format(item),"r") as f:
            lines=f.readlines()
        #if (os.path.exists("./cleandata/{}".format(item))):
        with open("./cleandata/{}".format(item),"w+") as f:

            for line in lines:
                if "10 Messungen" in line.strip("\n"):
                    line= line[line.find("Ch"):]
                    #print(newline)
                # if (line.strip("\n") != "þStartfischer1 p33-6 hf8 fc6x 0.9km")
                if ("Ch" in line.strip("\n") or "V" in line.strip("\n") ):
                    f.write(line.replace(';',''))
print("wer are done.... have fun!! KOMPASS-SENSOR")