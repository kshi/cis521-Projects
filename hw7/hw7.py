#!/usr/bin/python

from numpy import *
from Dataset import Dataset

# Bayesian Classifier
# First, we need to build the probability model

d = Dataset("rec.sport.hockey.txt", "rec.sport.baseball.txt", cutoff=1000)
#d = Dataset("comp.sys.mac.hardware.txt", "comp.sys.ibm.pc.hardware.txt", cutoff=2000)
(Xtrain, Ytrain, Xtest, Ytest) = d.getTrainAndTestSets(0.8, seed=1)
wordlist = d.getWordList()

def trainNaiveBayes(X, Y):
  # First, count frequencies given the category
  print Y
  yFlat = Y.flatten()
  yOne = yFlat == 1
  yZero = yFlat == 0
  cat1 = array([sum(X[yOne,j]) / sum(yOne) for j in range(X.shape[1])])
  cat2 = array([sum(X[yZero,j]) / sum(Zero) for j in range(X.shape[1])])
  return (cat1, cat2)

def naiveBayesClassify(cat1, cat2, x):
  # Not actually implemented!
  return 1

# trainNaiveBayes(Xtrain,Ytrain)

def ridgeTrain(X, Y, l = 1):
  Xt = matrix(X.T)
  return linalg.inv(Xt * matrix(X) + l * identity(X.shape[1])) * Xt * matrix(Y)

def classify(x, w):
  return sign(dot(w, x))

def perceptronTrain(X,Y, l = 1):
  w = random.rand(X.shape[1])
  perfect = False
  iterations = 0
  models = []
  while (not perfect and iterations < 100):
    iterations += 1
    perfect = True
    for i in range(X.shape[0]):
      result = classify(w, X[i])
      if (result != Y[i]):
        perfect = False
        w = w + l * (Y[i] * X[i])
    models = models + [w]
  m = array(models)
  w = array([average(m[:,i]) for i in range(m.shape[1])])
  return (w, iterations)

def l2Error(w,X,Y,columns, l):
   #print (Y)
   #print (Y - dot(w.T, (X[:,columns])[0]))
   s1 = sum([linalg.norm(Y - dot(w.T,x)) for x in X[:,columns]])
   s2 = l * linalg.norm(w)
   print(s1,s2)
   s3 = s1 + s2
   return s3

def error(w, X, Y, columns):
  X = X[:,columns]
  right = 0
  wrong = 0
  for i in range(X.shape[0]):
    result = classify(w,X[i]) 
    if result == Y[i]:
      right += 1
    else:
      wrong += 1
  return wrong

def streamwiseTrain(X, Y, l = 1):
  cols = []
  w = zeros(X.shape[0])
  e = sum([linalg.norm(Y) for x in X])
  for j in range(X.shape[1]):
    print("Now on " + str(j))
    # print("e = " + str(e))
    newCols = cols + [j]
    w = ridgeTrain(X[:,newCols], Y, l)
    curr = error(w,X,Y,newCols)  + l * linalg.norm(w)
    if curr < e:
      cols = newCols
      e = curr
  #print cols
  return (ridgeTrain(X[:,cols],Y,l),cols)

def stepwiseTrain(X, Y, l = 1, maxFeatures = 10):
  cols = []
  w = zeros(X.shape[0])
  e = sum([linalg.norm(Y) for x in X])
  while len(cols) < maxFeatures:
    print("Now on " + str(len(cols)))
    best = None
    for j in range(X.shape[1]):
      if j in cols:
        continue
      newCols = cols + [j]
      w = ridgeTrain(X[:,newCols], Y, l)
      curr = error(w,X,Y,newCols) + l * linalg.norm(w)
      if curr < e:
        best = j
        e = curr
    if best == None:
      break
    else:
      cols = cols + [best]
  return (ridgeTrain(X[:,cols],Y,l),cols)

(w, iterations) = perceptronTrain(Xtrain, Ytrain)
# w = ridgeTrain(Xtrain, Ytrain)
# (w,cols) = streamwiseTrain(Xtrain, Ytrain)
# (w,cols) = stepwiseTrain(Xtrain, Ytrain)

e = error(w,Xtest, Ytest, range(Xtest.shape[1]))
# e = error(w, Xtest, Ytest, cols)
print("Right: " + str(Ytest.shape[0] - e))
print("Wrong: " + str(e))
#print(error(w,Xtrain, Ytrain, range(Xtrain.shape[1])))
# print("Right: " + str(right) + "; wrong: " + str(wrong))
