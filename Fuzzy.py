import csv
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd


m = 27
N = 0
def read_data(filename):
    global N    
    items = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            itemFeatures = []
            for j in range(len(row)):
                v = float(row[j])
                itemFeatures.append(v)
            items.append(itemFeatures)
    items.pop(len(items) - 1)
    N = len(items)
    return items 

def normlize(item, center):
    distance = 0
    for i in range(len(item)):
        distance += (item[i]-center[i])**2
    return distance**0.5

def Ui(items , centers):
    # print(len(items))
    U = np.zeros((len(centers) , len(items)))
    for x in range(len(centers)):
        for y in range(len(items)):
            if normlize(items   [y] , centers[x]) != 0:
                all = 0 
                for w in range(len(centers)):
                    all = all + (normlize(items[y],centers[x])/normlize(items[y],centers[w]))**(2/(m-1))
                U[x,y] = 1 / all
            else:
                U[x,y] = 1
    return U

def Vi(belongs , items , centers ):
    for i in range(len(centers)):
        up = 0.0
        down = 0.0
        for j in range(len(items)):
            up = up + (np.power(belongs[i , j],m)*np.array(items[j]))
            down = down + np.power(belongs[i, j],m)
        centers[i] = up/down
    return centers



def cost(belongs , items , centers):
    cost = 0
    for i in range(len(items)):
        for j in range(len(centers)):
            cost += ((belongs[j][i])**m)*(normlize(items[i], centers[j])**2)
    return cost


def plot_2D(items , belongs ,  centers):
    classes = []
    for i in range(len(items)):
        n = [0 , -1]
        for k in range(len(centers)):
            if(n[1] < belongs[k , i]):
                n = [k , belongs[k , i]]
        classes.append(n[0])
    x = []
    y = []
    # print(items)
    # print("---------------")
    # print(items[0][0])
    # print("---------------")
    # print(items[0])
    # print("---------------")
    # print(items[1])
    for i in range(len(items)):
        x.append(items[0][i])
        y.append(items[1][i])
    plt.scatter(x , y , s=10 , c=classes)
    plt.show()




# items = read_data("data1.csv")

items = pd.read_csv("data3.csv", header = None)
item = np.array(items.values)
xxpoint = []
yypoint = []
col_min = np.amin(item, axis=0)
col_max = np.amax(item, axis=0)
# print(item)
centers = []
for class_number in range(4):
    class_number = class_number + 1
    xpoints = []
    ypoints = []
    node = []
    for j in range(len(col_min)):
        node.append(random.uniform(col_min[j], col_max[j]))
    centers.append(node)
    for i in range(100):
        belong = Ui(item, centers)
        centers = Vi(belong , item, centers)
    xpoints.append(i)
    ypoints.append(cost(belong , item , centers))
    print(belong)
    plot_2D(items , belong ,centers)
    xxpoint.append(class_number)
    yypoint.append(min(ypoints))
plt.plot(xxpoint , yypoint)
plt.show()