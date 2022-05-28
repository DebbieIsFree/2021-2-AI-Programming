import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def createProblem():
    ## Read in an expression and its domain from a file.
    ## Then, return a problem.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    fileName = input("Enter the file name of a function: ")
    infile = open(fileName, 'r')
    expression = infile.readline()      # 수식 구함
    varNames =[]                    
    low = []
    up = []
    line = infile.readline()
    while(line != ""):      
        data = line.split(',')
        varNames.append(data[0])
        low.append(float(data[1]))
        up.append(float(data[2]))
        line = infile.readline()
    domain = [varNames, low, up]
    return expression, domain


def randomInit(p): # Return a random initial point as a list
    init = [] 
    for i in range(len(p[1][0])):   # 변수 개수 만큼 반복
        l = p[1][1][i]              # i번째 변수의 lower bound
        u = p[1][2][i]              # i번째 변수의 upper bound
        tmp = random.uniform(l, u) 
        init.append(tmp)
    return init    # Return a random initial point  as a list of values


def evaluate(current, p):  
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])  
        exec(assignment)    # 각 변수에 값 대입
    return eval(expr)       # 수식 계산한 값 리턴


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u: 
        curCopy[i] += d  
    return curCopy  #  i 번째 변수에 d만큼 더한 값이 범위 내에 있으면 리턴


def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 


def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))


def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple

