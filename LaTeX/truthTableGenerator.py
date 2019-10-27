from math import pow
"""
truthTableBuilder.py v1.0 by Minhduc Cao - 2019.10.26
Creates user-defined variable truth tables for use in LaTeX documents
"""
BASE = 2                # For creating truth table patterns


def collectAttributes():
    """Collects user input for expressions and # of columns"""
    varNum, intColNum, finColNum = 0, 0, 0
    varList = [varNum, intColNum, finColNum]
    valid = False

    # Column Count
    while not valid:
        try:
            varList = [int(x) for x in input("Enter the # of variables, intermediate columns, and final columns you want, separated by spaces.\nExample: 2 3 2\n").split()]
            if len(varList) != 3 or varList[0] < 1:
                print("Invalid number of inputs or the # of variables isn't above 0.")
                raise ValueError
            valid = True
        except ValueError:
            print("Please try again.\n")

    # Variable Names
    varNames = []
    for i in range(int(varList[0])):
        varNames.append(input("Enter variable " + str(i + 1) + "\'s name: "))

    # Expressions
    expNames = []
    for i in range(int(varList[1])):
        expNames.append(input("Enter the expression for intermediate column " + str(i + 1) + ": "))
    for i in range(int(varList[2])):
        expNames.append(input("Enter the expression for final column " + str(i + 1) + ": "))
    return varNames, expNames


def createTable(varNames, expNames):
    """Creates LaTeX truth table given column numbers and expressions"""
    colNum = len(varNames) + len(expNames)
    rows = int(pow(BASE, len(varNames)))

    # Table Setup
    print('Copy-paste the following into your LaTeX editor:\n\n')
    print('\n\\begin{tabular}{', end='')
    for i in range(colNum):
        print('|c', end='')
    print('|}\n \\hline\n', end=' ')

    # Expressions Header
    varExpNames = varNames + expNames
    for i in range(colNum - 1):
        print('$' + varExpNames[i] + '$ & ', end='')
    print('$' + varExpNames[colNum - 1] + '$\\\\\n', end=' \\hline\n')

    # Table Contents
    counter = [0] * len(varNames)
    countIndex = len(varNames) - 1
    for i in range(rows):
        print(' ', end='')
        for j in range(countIndex, -1, -1):
            print('T' if counter[j] < pow(BASE, j) else 'F', end=' & ')
            counter[j] += 1
            if counter[j] == pow(BASE, j + 1):
                counter[j] = 0
        for k in range(len(expNames) - 1):
            print('x & ', end='')
        print('x\\\\')

    # Close Table
    print(' \\hline\n\\end{tabular}')


if __name__ == '__main__':
    while True:
        vNames, eNames = collectAttributes()
        createTable(vNames, eNames)
        print()

