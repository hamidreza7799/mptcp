import statistics
import math
import re
import matplotlib.pyplot as plt
import argparse
import itertools
from mpl_toolkits.mplot3d import Axes3D

def getDataFromFile(fileAddress,mode=1):
    with open(fileAddress, 'r') as file:
        fileText = file.read()
    if mode == 3:
        indexes = [m.start() for m in re.finditer('MBytes', fileText)]
    else:
        indexes = [m.start() for m in re.finditer('Mbits/sec', fileText)]
    data = []
    for i in range(len(indexes)):
        data.append(float(fileText[indexes[i] - 6:indexes[i] - 1]))
    return data

def getAllDatas(folderName,NoFiles,mode=1):
    fileNames = []
    for i in range(NoFiles):
        fileNames.append("./" + folderName + "/" + "IPERF_" + str(i))
    first5seconds = []
    second5seconds = []
    third5seconds = []
    forth5seconds = []
    fifth5seconds = []
    sixth5seconds = []
    seventh5seconds = []
    eighth5seconds = []
    nineth5seconds = []
    tenth5seconds = []
    finalSeconds = []
    for i in range(len(fileNames)):
        data = getDataFromFile(fileNames[i],mode)
        first5seconds.append(data[0])
        second5seconds.append(data[1])
        third5seconds.append(data[2])
        forth5seconds.append(data[3])
        fifth5seconds.append(data[4])
        sixth5seconds.append(data[5])
        seventh5seconds.append(data[6])
        eighth5seconds.append(data[7])
        nineth5seconds.append(data[8])
        tenth5seconds.append(data[9])
        finalSeconds.append(data[10])
    return [first5seconds,second5seconds,third5seconds,forth5seconds,fifth5seconds,sixth5seconds,seventh5seconds,eighth5seconds,nineth5seconds,tenth5seconds,finalSeconds]

def calculateMeanData(folderName,bandwithArrays,transferArrays):
    with open("./" + folderName + "/" + "IPERF_MEAN" , 'w') as file:
        file.write("------------------------------------------------------------\nClient connecting to 10.1.0.1, TCP port 5001\nTCP window size: 86.2 KByte (default)\n------------------------------------------------------------\n[  3] local 10.0.0.1 port 54996 connected with 10.1.0.1 port 5001\n[ ID] Interval       Transfer     Bandwidth\n")
        for i in range(len(bandwithArrays)):
            transferMean = statistics.mean(transferArrays[i])
            bandwithMean = statistics.mean(bandwithArrays[i])
            if transferMean > 100:
                transferMean = round(transferMean)
            elif transferMean > 10 :
                transferMean = round(transferMean, 1)
            else:
                transferMean = round(transferMean, 2)
            if bandwithMean > 100:
                bandwithMean = round(bandwithMean)
            elif bandwithMean > 10:
                bandwithMean = round(bandwithMean, 1)
            else:
                bandwithMean = round(bandwithMean, 2)
            if i != 10:
                file.write("[  3] " + str(float(i*5)) + "-" + str(float((i+1)*5)) + " sec  " + str(transferMean) + " MBytes  " + str(bandwithMean) + " Mbits/sec\n")
            else:
                file.write("[  3] " + " 0.0" + "-" + "50.0" + " sec  " + str(transferMean) + " MBytes  " + str(bandwithMean) + " Mbits/sec\n")

def getErrorBarData(data,t = 2.009): # for 50 is 2.009 if we calculate 20 times t is 2.086
    standardDeviation = statistics.stdev(data)
    squareData = math.sqrt(len(data))
    return t * (standardDeviation / squareData)

def drawMultipleGraph(dataNNdimension,folderNames,mode=1):
    for j in range(len(dataNNdimension)):
        splitArray = folderNames[j].split("_")
        CONGESTION = splitArray[0]
        PATHMANAGER = splitArray[1]
        SCHEDULAR = splitArray[2]
        means = []
        confidences = []
        dataNdimension = dataNNdimension[j]
        for i in range(len(dataNdimension)):
            confidence = getErrorBarData(dataNdimension[i])
            dataMean = statistics.mean(dataNdimension[i])
            means.append(dataMean)
            confidences.append(confidence)
        label = ""
        if mode == 1:
            label = PATHMANAGER + " "
            if SCHEDULAR == "rr":
                label += "roundrobin"
            elif SCHEDULAR == "rtt":
                label += "lowest rtt"
        else:
            label = CONGESTION
        color = "b"
        if j == 0:
            color = "b"
        elif j == 1:
            color = "r"
        elif j == 2:
            color = "g"
        elif j == 3:
            color = "m"
        elif j == 4:
            color = "c"

        plt.errorbar(["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50", "0-50"],
                     means, yerr=confidences, color=color, label=label)




    # for i in range(len(means)):
    #     means[i] += 1
    # for i in range(len(confidences)):
    #     confidences[i] -= 1
    # plt.errorbar(["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50", "0-50"], means, yerr=confidences, color='g', label='second')
    # for i in range(len(dataNNdimension)):
    #     plt.errorbar(["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50", "0-50"],
    #              nMeans[i], yerr=nConfidences[i], color=colors[i], label=labels[i])

    if len(dataNNdimension) == 1:
        splitArray = folderNames[0].split("_")
        CONGESTION = splitArray[0]
        PATHMANAGER = splitArray[1]
        SCHEDULAR = splitArray[2]
        title = "Throughput of " + CONGESTION + " and " + PATHMANAGER + " and "
        if SCHEDULAR == "rr":
            title += "roundrobin"
        elif SCHEDULAR == "rtt":
            title += "lowest rtt"
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Throughput")
        plt.show()
    else:
        splitArray = folderNames[0].split("_")
        CONGESTION = splitArray[0]
        PATHMANAGER = splitArray[1]
        SCHEDULAR = splitArray[2]
        title = ""
        if mode == 1:
            title = "Throughput of " + CONGESTION
        else:
            title = "Throughput of " + PATHMANAGER + " and " + SCHEDULAR
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Throughput")
        plt.legend()
        plt.show()

def floating(list):
    for i in range(len(list)):
        list[i] = float(list[i])
    return list

def draw3DGraph(dataNNdimension,folderNames):
    xList, yList, ThroughputList, ConfidenceList = [], [], [], []
    for i in range(len(folderNames)):
        splitText = folderNames[i].split("_")
        folderNames[i] = ' '.join(splitText)
        # ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50", "0-50"]
    for i,folderName in enumerate(range(len(folderNames))):
        for j,time in enumerate(range(11)):
            xList.append(folderName)
            yList.append(time)
            dataMean = statistics.mean(dataNNdimension[i][j])
            confidence = getErrorBarData(dataNNdimension[i][j])
            ThroughputList.append(dataMean)
            ConfidenceList.append(confidence)

    ax = plt.figure().add_subplot(projection='3d')
    # print(ax)
    ax.errorbar(floating(xList), floating(yList), floating(ThroughputList), zerr=floating(ConfidenceList))

    plt.xticks(range(len(folderNames)), folderNames)
    plt.yticks(range(11), ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50", "0-50"])

    ax.set_xlabel("algorithm")
    ax.set_ylabel("time")
    ax.set_zlabel("Throughput")

    plt.show()

def getDataNdimension(fileAddressList,expectedNumber):
    dataNdimension = []
    for i in range(len(fileAddressList)):
        oneData = getDataFromFile(fileAddressList[i],expectedNumber,1)
        if len(oneData) == 0:
            print("FALSE FALSE")
            return
        dataNdimension.append(oneData)
    return dataNdimension
    
# fileAddressList = ['resultH4-20ms-mode5.txt','resultH4-40ms-mode5.txt','resultH4-60ms-mode5.txt','resultH4-80ms-mode5.txt','resultH4-100ms-mode5.txt']
# dataNdimension = getDataNdimension(fileAddressList,20)
# # print(dataNdimension)
# draw(dataNdimension)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Statistics of MPTCP Project")

    parser.add_argument("--folder_names", "-f",
                        help="name of the folders that we want to process",nargs='+',required=True)
    parser.add_argument("--mode", "-m",
                        help="if congestion is fixed mode is 1 and if path manager and schedular is fixed mode is 2 and for calculation of mean of data mode is 3", default=1)
    parser.add_argument("--numberFile", "-n",
                        help="get number of files that we want to process",
                        default=50)
    parser.add_argument("--is3D", type=str2bool, nargs='?',
                        default=False,
                        help="Activate 3D mode.")

    args = parser.parse_args()

    nndimensionData = []
    for i in range(len(args.folder_names)):
        # splitArray = args.folder_names[i].split("_")
        # CONGESTION = splitArray[0]
        # PATHMANAGER = splitArray[1]
        # SCHEDULAR = splitArray[2]
        ndimensionData = getAllDatas(args.folder_names[i],int(args.numberFile))
        # print(ndimensionData)
        nndimensionData.append(ndimensionData)



    if args.is3D:
        draw3DGraph(nndimensionData,args.folder_names)
    else:
        if int(args.mode) == 3:
            ndimensionDataTransfer = getAllDatas(args.folder_names[0],int(args.numberFile),int(args.mode))
            calculateMeanData(args.folder_names[0],nndimensionData[0],ndimensionDataTransfer)
        else:
            drawMultipleGraph(nndimensionData,args.folder_names,int(args.mode))

