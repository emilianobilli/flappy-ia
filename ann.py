import random
import math

def sigmoid(x):
    try:
        sig = 1 / (1 + math.exp(-x))
    except Exception as e:
        return 0.0
    #sig = (1 - math.exp(-x)) / (1 + math.exp(-x))
    return sig

class AN(object):
    def __init__(self, w:tuple, func=sigmoid):
        self.w = w
        self.func = func

    def __call__(self, args:tuple):
        if len(args) != len(self.w):
            raise ValueError('Invalid Inputs')
        j = 0
        s = 0
        for i in args:
            s = s + (self.w[j]*i)
            j = j + 1
        return self.func(s)


class ANLayer(object):
    def __init__(self, n:list, func=sigmoid):
        self.layer = []
        self.inputs = None
        for i in n:
            if not self.layer:
                self.inputs = len(i)
            else:
                if self.inputs != len(i):
                    raise ValueError('All AN must have the same number of inputs')
            self.layer.append(AN(i,func))
        
    def __call__(self, args:tuple):
        if len(args) != self.inputs:
            if type(args).__name__ != 'tuple':
                raise ValueError('Invalid inputs, must be: %d and %d pased' % (self.inputs, len(args)))
            args = args[0]

        ret = []
        for n in self.layer:
            ret.append(n(args))

        return tuple([ret])

a = ANLayer([(2,),(3,)])

class Network(object):
    def __init__(self, inputs:int, layers:list, func=sigmoid):
        self.layers = []
        self.inputs = inputs
        for layer in layers:
            self.layers.append(ANLayer(layer))
    
    def __call__(self, args:tuple):
        if self.inputs != len(args):
            raise ValueError('Invalid number of Arguments')

        inputs = args
        for l in self.layers:
            inputs = l(inputs)

        return inputs

def GetWeightLen(inputs:int, topology:list):
    total = inputs * topology[0]
    inputs = topology[0]
    for t in topology[1:]:
        total = total + (inputs * t)
    return total

def CreateNetwork(inputs:int, topology:list, w:list, func=sigmoid):

    def split(elements, count):
        return [tuple(elements[i::count]) for i in range(count)]

    input_parameter = inputs

    if GetWeightLen(inputs, topology) != len(w):
        raise ValueError('Invalid Topology')

    total = inputs * topology[0]
    layer = [split(w[:total], topology[0])]
    w = w[total:]
    inputs = topology[0]
    for t in topology[1:]:
        total = inputs * t
        inputs = t
        layer.append(split(w[:total],inputs))
        w = w[:total]

    return Network(input_parameter, layer, func)

#print(GetWeightLen(1,[3,2,1]))

#c = CreateNetwork(2,[2],[0.2,0.1,-0.2,0.99])
#print(c(12,2))