import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import random

class Function:

    def __init__(self, f, eval, arity):
        '''
        f is the function itself
        eval is an evaluation function. Given an input image, a set of parameters, and the desired output, it returns how close the output is to the desired output
        '''

        self.parameters = [[]] * arity
        self.f = f
        self.eval = f
        # Dictionary for memoization
        self.cache = {}

    def addParameter(self, name, index, minLimit, maxLimit, value=None):
        param = Parameter(index, minLimit, maxLimit, value=value)
        self.parameters[index] = param

    def evaluate(self, data):
        assert(all(self.parameters))
        values = [param.value for param in self.parameters]

        errorVec = []
        for (img, tag) in data:
            if values in self.cache:
                error = self.cache[values]
            else:
                output = self.f(*values)
                error = self.eval(output, desiredOutput)
                self.cache[values] = error
            errorVec.append(error)
        return errorVec

    def checkError(errorVec, maxError, outliers):
        count = len([error for error in errorVec if error > maxError])
        if float(count) / len(errorVec) > outliers:
            return False
        return True


    def fit(self, data, maxError, outliers, steps=10):
        '''
        Fit the parameters to the data to achieve results within error for all but a certain percentage of the images (outliers)

        * data is a list of (img, tag) tuples
        * maxError is a float where we want self.eval(*) < error
        * outliers is a float between 0 and 1, indicating the percentage of images we are allowed to inaccurately classify
        * steps is how many values we test for each parameter
        '''
        done = False
        while not done:

            errorOrigVec = self.evaluate(data)
            errorOrig = avg(errorVec)
            for param in self.parameters:
                param.backup()
                param.increase(steps)
                errorIncVec = self.evaluate(data)
                errorInc = avg(errorIncVec)
                param.reset()
                param.decrease(steps)
                errorDecVec = self.evaluate(data)
                errorDec = avg(errorDecVec)
                param.reset()

                if errorInc < errorOrig and errorInc < errorDec:
                    param.increase()
                    errorOrigVec = errorIncVec
                    errorOrig = errorInc
                elif errorDec < errorOrig and errorDec < errorInc:
                    param.decrease()
                    errorOrigVec = errorDecVec
                    errorOrig = errorDec


            if checkError(errorOrigVec, maxError, outliers):
                done = True

        self.show()
        return [param.value for param in self.parameters]

    def show(self):
        print 'Parameters:'
        for param in self.parameters:
            print '%s (%d): %.3f (%.3f < %s < %.3f)' % (param.name,
                                                        param.index,
                                                        param.value,
                                                        param.minLimit,
                                                        param.name,
                                                        param.maxLimit)

    def plot(self, paramName1, paramName2, steps=10):
        paramNames = [param.name for param in self.parameters]
        index1 = self.paramNames.index(paramName1)
        index2 = self.paramNames.index(paramName2)
        param1 = self.parameters[index1]
        param2 = self.parameters[index2]
        points = {}
        for paramValues, error in self.cache.items():
            key = (paramValues[index1], paramValues[index2])
            points[key] = points.get(key, []).append(error)

        x = []
        y = []
        z = []
        for key, errorVec in points:
            x.append(key[0])
            y.append(key[1])
            z.append(avg(errorVec))

        f = interpolate.interp2d(x, y, z, 'cubic')

        xSpan = np.linspace(param1.minLimit, param1.maxLimit, steps)
        # xSpan = xSpan.flatten()
        ySpan = np.linspace(param2.minLimit, param2.maxLimit, steps)
        # ySpan = ySpan.flatten()
        meshx, meshy = np.mesh(xSpan, ySpan)
        meshz = f(xSpan, ySpan)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(meshx, meshy, meshz)
        plt.show()


class Parameter:

    def __init__(self, name, index, minLimit, maxLimit, value=None):
        assert minLimit <= maxLimit
        self.name = name
        self.index = index
        self.minLimit = minLimit
        self.maxLimit
        if value is None:
            self.value = (self.minLimit + self.maxLimit) / 2.0
        else:
            self.value = value

    def decrease(self, steps):
        delta = float(self.maxLimit - self.minLimit) / steps
        if self.value - delta < minLimit:
            self.value = minLimit
            return False
        else:
            self.value -= delta
            return True

    def increase(self, steps):
        delta = float(self.maxLimit - self.minLimit) / steps
        if self.value + delta > maxLimit:
            self.value = maxLimit
            return False
        else:
            self.value += delta
            return True

    def backup(self):
        self.valueBackup = self.value
        self.value = value

    def reset(self):
        self.value = self.valueBackup


def tagImage(img, number, type):
    '''User manually tags a certain attribute in the image.
    The attributes can be:
        * point
        * line
        * circle

    The number should be an integer. To accept many, let it be -1
    '''

def avg(vec):
    return float(sum(vec)) / len(vec)
