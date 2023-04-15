import pickle, gzip, os, random
import sys
import os
import collections

from logic import *
from typing import Tuple, List

def input(filename):
    with open(filename, 'r') as f:
        alpha = f.readline().strip().split() # Read alpha statement
        num_clauses = (f.readline().strip().split()) # Read number of clauses in KB
        KB = []
        for _ in range(4):  # Read clauses in KB
            KB.append(f.readline().strip().split())
        return KB,alpha

KB,alpha = input('./input1.txt')
print(alpha)
print(type(KB[0][0][1]))
for i in range(len(KB)):
    print(KB[i])

A = Atom('A')
B = Atom('B')
C = Atom('C')
D = Atom('D1')
E = Atom('E')

# Tạo các quy tắc phân giải
rule1 = ResolutionRule()
rule2 = ResolutionRule()

# Áp dụng quy tắc phân giải giữa các công thức
form1 = Not(A)
form2 = A
form3 =  Or(Or(A, And(B, C)), D)     

def symmetric(atom):
    temp = atom.computeStrRepn()
    if 'Not' in temp:
        return Atom(temp[4])
    return Not(Atom(temp[0]))

def resolve(clause1, clause2):
    clauseA = flattenOr(clause1)
    clauseB = flattenOr(clause2)
    newClause = []
    newClause = clauseA
    tempClause = clauseB
    print(type(newClause[0]))
    for i in range(len(newClause)):
        for j in range(len(tempClause)):
            if  newClause[i] == symmetric(tempClause[j]):
                newClause.pop(i)
                tempClause.pop(j)
                newClause = newClause + tempClause
                if len(newClause) == 0:
                    return -1, OrList(newClause)  # hợp giải ra {}
                return 1, OrList(newClause)  # hợp giải ra clause mới
    return 0, OrList(newClause)   # hợp giải không ra clause mới


re = resolve(form1,form2)
for result in re:
    print(result)
print('------------------------')


form8 = Or(Not(A),Not(B))
form7 = Or(Not(C),Not(D))

Test1 = A
Test2 = Or(Not(A),B)

        

results = rule1.applyRule(Test1, Test2)
#In ra các kết quả phân giải
print("Kết quả phân giải:")
print(results)
for result in results:
    print(result)

# expressions = flattenOr(form3)
# for exp in expressions:
#     print(type(exp))   # class 'logic.Atom'
#     print(exp)
# form4 = OrList(expressions)
# print(type(form4))
# print(form4)


# Áp dụng quy tắc phân giải đối xứng giữa các công thức
form3 =  Or(Not(A),B) #Or(A, B)
form4 = Not(A) #Or(Not(A), E)
results_symmetric = rule2.applyRule(form3, form4)

Test3 = Or(A, B)
Test4 = Or(Not(A), E)
results_symmetric = rule2.applyRule(Test3, Test4)
# In ra các kết quả phân giải đối xứng
print("Kết quả phân giải đối xứng:")
for result in results_symmetric:
    print(result)
    