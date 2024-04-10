import unittest
import inspect
import sys

def isTestClass(x):
    return inspect.isclass(x) and issubclass(x, unittest.TestCase)


def isTestFunction(x):
    return inspect.isfunction(x) and x.__name__.startswith("test")

def suite(name):

    # get current module object
    module = sys.modules[name]

    # get all test className,class tuples in current module
    testClasses = [
        tup for tup in
        inspect.getmembers(module, isTestClass)
    ]

    # sort classes by line number
    testClasses.sort(key=lambda t: inspect.getsourcelines(t[1])[1])

    testSuite = unittest.TestSuite()

    for testClass in testClasses:
        # get list of testFunctionName,testFunction tuples in current class
        classTests = [
            tup for tup in
            inspect.getmembers(testClass[1], isTestFunction)
        ]

        # sort TestFunctions by line number
        classTests.sort(key=lambda t: inspect.getsourcelines(t[1])[1])

        # create TestCase instances and add to testSuite;
        for test in classTests:
            testSuite.addTest(testClass[1](test[0]))

    return testSuite