import os.path
har = 0
count = 18
while count <= 20:
    dat = open("data/order/order_"+str(count)+"122019.txt", "r")
    kon = dat.readline()
    while kon:
        kon = kon.replace("\n", "")
        data = kon.split(" ")
        name = "filter_firza/"+data[0]+".txt"
        name2 = "filter_firza/trans/"+data[0]+".txt"
        if os.path.isfile(name):
            re = open(name, "r")
            lines = re.readlines()
            las = lines[len(lines)-1]
            las = las.split(" ")
            if las[0] == "2":
                if data[1] == "1":
                    unt = int(data[6])-int(las[1])
                    hal = open(name2, "a")
                    hal.write(str(unt)+"\n")
                    hal.close()
            re.close()
        ol = open(name, "a")
        if data[1] == "1":
            har = data[6]
        elif data[1] == "2":
            har = data[7]
        ol.write(data[1]+" "+str(har)+"\n")
        ol.close()
        kon = dat.readline()
    count = count+1
    dat.close()
