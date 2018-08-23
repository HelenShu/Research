#!/usr/local/bin python
from __future__ import division
import os
import sys
import os.path
import struct
import numpy as np
import math
import copy
from sklearn.preprocessing import normalize 
from numpy import linalg as li
import random
import pickle
from math import log, ceil, floor

from sklearn.linear_model import Perceptron
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

ave_classHVs = []
errors = []
similarities = []

# eats lists and returns a one hv per class
def oneHvPerClass(inputLabels, inputHVs, D, T):
    
    #This creates a dict with no duplicates
    labels = dict()
    
    for i in range(len(inputLabels)):
       
        name = inputLabels[i]
        if (name in labels.keys()):
            labels[name] = np.array(labels[name]) + np.array(inputHVs[i])
        else:
            labels[name] = np.array(inputHVs[i])

    # Contruct all zeros classHV
    #for key, item in labels.iteritems():
    #    labels[key] = np.zeros(4)
    
    return labels

def inner_product(x, y):
    return np.dot(x,y)  / (li.norm(x) * li.norm(y) + 0.0)

def ham_distance(x, y):
    return np.sum(x == y)

# change decimal numbers into keys
# The range of the values should be in [lowerBound, upperBound)
def numToKey (value, levelList):
    
    if (value == levelList[-1]):
        return len(levelList)-2
    
    upperIndex = len(levelList) - 1
    lowerIndex = 0
    keyIndex = 0
    
    while (upperIndex > lowerIndex):
        
        keyIndex = int((upperIndex + lowerIndex)/2)
        
        if (levelList[keyIndex] <= value and levelList[keyIndex+1] > value):
            return keyIndex
        
        if (levelList[keyIndex] > value):
            upperIndex = keyIndex
            keyIndex = int((upperIndex + lowerIndex)/2)
        else:
            lowerIndex = keyIndex
            keyIndex = int((upperIndex + lowerIndex)/2)
                
    return keyIndex
    

def getlevelList(vectors, totalLevel):
    minimum = vectors[0][0]
    maximum = vectors[0][0]
    levelList = []
    
    for vector in vectors:
        localMin = min(vector)
        localMax = max(vector)
        
        if (localMin < minimum):
            minimum = localMin
            
        if (localMax > maximum):
            maximum = localMax
            
    length = maximum - minimum
    gap = length / totalLevel
    
    for lv in range(totalLevel):
        levelList.append(minimum + lv*gap)
    
    levelList.append(maximum)
    
    return levelList

        
def genDictRandSandwich(totalLevel, dimension, den):
    
    print ('generating sandwich Dictionary')
    valueDict = dict()
    indexVector = range(dimension)
    print (dimension)
    print (den)
    choose = int((dimension * den) / 100)
    change = int(dimension / 2)
    
    #for all even positions, fill in with random HVs
    # if the last position is of odd index, give it a random HV
    for level in range(totalLevel):
        #if (level % 2 == 0 or level == totalLevel - 1 ):
        name = level
        base = np.full(dimension, baseVal)
        toOne = np.random.permutation(indexVector)[:choose]
            
        for index in toOne:
            base [index] = 1
                
        valueDict [name] = copy.deepcopy(base)
        return valueDict
    

def binarizeHV (v):
    #VSorted = np.sort(v)
    outV = copy.deepcopy(v)
    #threshold = VSorted[int(len(v) * (0.5))]
    #total = 0
    
    for i in range(len(v)):
        #print(v[i])
        if (v[i] >= 0):
            outV[i] = 1
            #total = total + 1
        else:
            outV[i] = baseVal
    #print(total)        
    return outV

def IDMultHV (inputBuffer, D, voiceDict, levelList, idDict):

    totalLevel = len(levelList) - 1
    totalPos = len(idDict.keys()) - 1
    sumHV = np.zeros(D, dtype = np.int)

    for keyVal in range(len(inputBuffer)):
        key = numToKey(inputBuffer[keyVal], levelList)
        voiceHV = voiceDict[key] 
        positionHV = idDict[keyVal]
        #sumHV = sumHV * np.roll((voiceHV ^ positionHV), keyVal)
        sumHV = sumHV + (voiceHV*positionHV)

    #sumHV = binarizeHV(sumHV, 50)
    return sumHV

def IDMultHVProjection (inputBuffer, D, voiceDict, levelList, idDict):
    N = 4;
    totalLevel = len(levelList) - 1
    totalPos = len(idDict.keys()) - 1
    sumHV = np.zeros(D, dtype = np.int)
    randHV = voiceDict[0]
    inLen = len(inputBuffer)
    numRep = int(D/inLen)
    newBuffer = np.concatenate((inputBuffer, inputBuffer))

    for i in range(numRep-2):
        newBuffer = np.concatenate((newBuffer, inputBuffer))


    for i in range(len(newBuffer) - (N-1)):
        dot = 0;
        for j in range(N):
            if(randHV[i + j] > 0):
                #add
                dot = dot + newBuffer[i + j]
            else:
                #subtract
                dot = dot - newBuffer[i + j]
        if(dot >= 0):
            sumHV[i] = 1
        else:
            sumHV[i] = -1

    #sumHV = binarizeHV(sumHV, 50)
    return sumHV



class voiceModel(object):

    # buffers
    def __init__(self, buffers, classes, dimensions, totalLevel, density, trainingModel = 0):
        
        if len(buffers) != len(classes):
            print("Buffers and labels are not the same size")
            return
                
        self.buffers = buffers
        self.classes = classes
        self.dimensions = dimensions
        self.density = density
        self.totalLevel = totalLevel
        
        self.size = len(buffers)
        self.posIdNum = len(self.buffers[0])
        
        if (trainingModel == 0):
            self.levelList = getlevelList(self.buffers, self.totalLevel)
            self.voiceDict = genDictRandSandwich(self.totalLevel, self.dimensions, self.density)
            self.posDict   = genDictRandSandwich(self.posIdNum, self.dimensions, self.density)
        else:
            self.levelList = trainingModel.levelList
            self.voiceDict = trainingModel.voiceDict
            self.posDict = trainingModel.posDict
        
        self.bufferHVs = []
        self.classHVs = []


    def buildBufferHVs(self, mode, dimensions):
        print("Building a hv model")

        if mode == "train":
            if os.path.exists('./../data/face/train_bufferHVs_' + str(dimensions) +'.pkl'):
                print "loading training HVs"
                with open('./../data/face/train_bufferHVs_' + str(dimensions) + '.pkl', 'rb') as f:
                    self.bufferHVs = pickle.load(f)
            else:       
                for index in range(len(self.buffers)):
                    #print(index)
                    self.bufferHVs.append \
                        (IDMultHVProjection(np.array(self.buffers[index]), self.dimensions, self.voiceDict, self.levelList, self.posDict))
                with open('./../data/face/train_bufferHVs_' + str(dimensions) + '.pkl', 'wb') as f:
                    pickle.dump(self.bufferHVs, f)

        else:
            if os.path.exists('./../data/face/test_bufferHVs_' + str(dimensions) +'.pkl'):
                print "loading testing HVs"
                with open('./../data/face/test_bufferHVs_' + str(dimensions) +'.pkl', 'rb') as f:
                    self.bufferHVs = pickle.load(f)

            else:       
                for index in range(len(self.buffers)):
                    #print(index)
                    self.bufferHVs.append \
                        (IDMultHVProjection(np.array(self.buffers[index]), self.dimensions, self.voiceDict, self.levelList, self.posDict))
                with open('./../data/face/test_bufferHVs_' + str(dimensions) +'.pkl', 'wb') as f:
                    pickle.dump(self.bufferHVs, f)
                    
        self.classHVs = oneHvPerClass(self.classes, self.bufferHVs, self.dimensions, 0)
                    
def readChoirDat(filename):
    """ Parse a choir_dat file """
    with open(filename) as f:
        nFeatures = struct.unpack('i', f.read(4))[0]
        nClasses = struct.unpack('i', f.read(4))[0]
        X = []
        y = []

        while True:
            newDP = []
            for i in range(nFeatures):
                v_in_bytes = f.read(4)
                if v_in_bytes is None or len(v_in_bytes) == 0:
                    return nFeatures, nClasses, X, y
                
                v = struct.unpack('f', v_in_bytes)[0]
                newDP.append(v)
                
            l = struct.unpack('i', f.read(4))[0]
            X.append(newDP)
            y.append(l)
            
    return nFeatures, nClasses, X, y

def clearAndNormHVs(classHVs, percentage, dimension):
    
    sparseClassHV = copy.deepcopy(classHVs)
    clearNum = dimension * percentage / 100
    startIndex = int ((dimension - clearNum)/2)
    endIndex = int ((dimension + clearNum) / 2)

    if (startIndex >= endIndex):
        return sparseClassHV
    
    for key in sparseClassHV.keys():
        sortedHV = np.sort(sparseClassHV[key])
        startVal = sortedHV[startIndex]
        endVal = sortedHV[endIndex]

        for i in range(len(sparseClassHV[key])):
            if (sparseClassHV[key][i] >= startVal and sparseClassHV[key][i] <= endVal):
                sparseClassHV[key][i] = 0         

    return sparseClassHV
    
def Rounding(x):
    if x > 0:
        return pow(2, int(log(x, 2) + 0.5))
    elif x == 0:
        return x
    else:
        x = - x
        return -pow(2, int(log(x, 2) + 0.5))

def RoundToPowerOfTwo(classHVs):
    p2ClassHV = copy.deepcopy(classHVs)
    for key in p2ClassHV.keys():
        vf = np.vectorize(Rounding)
        p2ClassHV[key] = vf(p2ClassHV[key])

    return p2ClassHV

def drawAccuracy(all_accu, iteration_time, dataset_name):
    plt.xlabel('iteration time')
    plt.ylabel('accuracy')
    plt.title(dataset_name)

    iteration_time = np.array(range(len(all_accu)))
    #sparseAccu = test(classHVs, testModel.bufferHVs, testModel.classes)

    plt.plot(iteration_time, all_accu, 'r--')
    plt.grid(True)
    plt.show()

# This function attempts to guess the class of the input vector based on the model given
# The given model should be one HV per class
def checkVector(classDict, inputHV):
    
    returnClass = classDict.keys()[0]
    #inputHV  = transformer.transform(inputHV)
    maximum = np.NINF

    count = {}

    for key in classDict.keys():
        count[key] = inner_product(classDict[key], inputHV)
        
        if (count[key] > maximum):
            #print(count[key],"is larger than", maximum)
            returnClass = key
            maximum = count[key]
            
    return returnClass

def checkVectorH(classDict, inputHV):
    returnClass = classDict.keys()[0]
    #inputHV  = transformer.transform(inputHV)
    maximum = np.NINF

    count = {}

    for key in classDict.keys():
        count[key] = ham_distance(classDict[key], inputHV)
        
        if (count[key] > maximum):
            #print(count[key],"is larger than", maximum)
            returnClass = key
            maximum = count[key]
            
    return returnClass

def binarizeClassHVs(classHVs):

    retClassHVs = copy.deepcopy(classHVs)

    for key in retClassHVs.keys():
        retClassHVs[key] = binarizeHV(retClassHVs[key])

    return retClassHVs

def trainOneTime(classHVs, binClassHVs, trainingHV, trainingOut):
    
    retClassHVs = copy.deepcopy (classHVs)
    wrong_num = 0

    for index in range(len(trainingOut)):
        guess = checkVector(binClassHVs, trainingHV[index])
        
        if not (trainingOut[index] == guess):
            wrong_num += 1
            retClassHVs[guess] = retClassHVs[guess] - trainingHV[index]*0.1
            retClassHVs[trainingOut[index]] = retClassHVs[trainingOut[index]]
            + trainingHV[index]*0.1

    error = (wrong_num+0.0) / len(trainingOut)
    print('Error: ' + str(error))
    return retClassHVs, error


def test (classHVs, testHVs, realOutcomes):
    correct = 0
    
    for index in range(len(testHVs)):
        
        guess = checkVector(classHVs, testHVs[index])
      
        if (realOutcomes[index] == guess):
            correct += 1
        #else:
        #    print("should be " + str(realOutomes[index]) + ' but is '+ guess[3:] + '.')
    
    accuracy = (correct / len(realOutcomes)) * 100
    print ('the accuracy is: ' + str(accuracy))
    return (accuracy)

def testHam (classHVs, testHVs, realOutcomes):
    correct = 0

    for index in range(len(testHVs)):
        
        guess = checkVectorH(classHVs, binarizeHV(testHVs[index]))
      
        if (realOutcomes[index] == guess):
            correct += 1
        #else:
        #    print("should be " + str(realOutomes[index]) + ' but is '+ guess[3:] + '.')
    
    accuracy = (correct / len(realOutcomes)) * 100
    print ('the accuracy is: ' + str(accuracy))
    return (accuracy)

    

def trainNTimes (classHVs, trainingHV, trainingOut, n, testAccuracy, testHV, testOut, dimension):

    accuracy = []
    currClassHV = copy.deepcopy (classHVs)
    binClassHV = binarizeClassHVs(currClassHV)
    ave_classHVs = []
    accuracy.append(test(binClassHV, testHV, testOut))
    #accuracy.append(testHam(binClassHV, testHV, testOut))
    for i in range(n):
        print(i)
        currClassHV, error = trainOneTime(currClassHV, binClassHV, trainingHV, trainingOut)
        errors.append(error)
        binClassHV = binarizeClassHVs(currClassHV)
        accuracy.append(test(binClassHV, testHV, testOut))

    return binClassHV, accuracy

if __name__ == '__main__':
    baseVal = -1
  #  working_dir = os.path.abspath("./../")
  #  data_dir = os.path.join(working_dir, 'data')
  #  data_dir = os.path.join(data_dir, 'face')
  #  test_path = os.path.join(data_dir, 'face_test.choir_dat')
  #  train_path = os.path.join(data_dir, 'face_train.choir_dat')
    test_path = "face_test.choir_dat"
    train_path = "face_train.choir_dat"
    dataset_name = "face"

    test_nFeatures, test_nClasses, test_buffers, test_classes = readChoirDat(test_path)
    train_nFeatures, train_nClasses, training_buffers, training_classes = readChoirDat(train_path)
    #print(test_nFeatures)
    #print(train_nFeatures)

    dimensions = 4000
    totalLevel = 20
    density = 50
    n = 20
    testAccuracy = True

    trainingModel = voiceModel(training_buffers, training_classes, dimensions, totalLevel, density, trainingModel = 0)
    testModel = voiceModel(test_buffers, test_classes, dimensions, totalLevel, density, trainingModel)
    trainingModel.buildBufferHVs("train", dimensions)
    testModel.buildBufferHVs("test", dimensions)
    
    classHVs, accuracy = trainNTimes(trainingModel.classHVs, trainingModel.bufferHVs, trainingModel.classes, n,  testAccuracy, testModel.bufferHVs, testModel.classes, dimensions)

    print(max(accuracy)) 
