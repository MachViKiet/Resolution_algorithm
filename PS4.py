import pickle, gzip, os, random
import sys
import os
import collections

from logic import *
from typing import Tuple, List

def input(filename):
    with open(filename, 'r') as f:
        alpha_input = f.readline().strip().split() # Read alpha statement
        num_clauses = (f.readline().strip().split()) # Read number of clauses in KB
        KB_input = []
        for temp in range(4):  # Read clauses in KB
            KB_input.append(f.readline().strip().split())
        return KB_input,alpha_input

def output(filename,result,KB,NewKB,NumOfLoop):
    with open(filename, mode='w') as f:
        NewstartNode = len(KB)
        for i in range(len(NumOfLoop)):
            if i == len(NumOfLoop) - 1 and result == True:
                f.write(str(NumOfLoop[i] + 1))
                f.write('\n')
            else: 
                f.write(str(NumOfLoop[i]))
                f.write('\n')
            for j in range(NumOfLoop[i]):
                atom = flattenOr(NewKB[NewstartNode])
                for k in range(len(atom)):
                    ch = atom[k].computeStrRepn()
                    if 'Not' in ch:
                        f.write(('-' + ch[4]))
                    else:
                        f.write((ch[0]))
                    if k != len(atom) - 1:
                        f.write(' OR ')
                    else:
                        f.write('\n')
                NewstartNode = NewstartNode + 1
            if i == len(NumOfLoop) - 1 and result == True:
                f.write('{}\n')
        if result == True:
            f.write('Yes')
        else:
            f.write('No')
 
def symmetric(atom):    
    temp = atom.computeStrRepn()
    if 'Not' in temp:
        return Atom(temp[4])
    return Not(Atom(temp[0]))

def toClause(list):    # string to clause
    form = []
    for atom in list:
        if atom == 'OR':
            continue
        size = len(atom)
        if len(atom) != 1:
            form.append(Not(Atom(atom[1])))
            continue
        form.append(Atom(atom))
    return OrList(reduceFormulas(form,Or))

def toClauses(KB):     # many string to many clause in KB
    Clauses = []
    for temp in KB:
        clause = toClause(temp)
        Clauses.append(clause)
    return Clauses
    
def compareClause(clause1,clause2)-> bool:    # compare 2 clauses
    items1 = flattenOr(clause1)
    items2 = flattenOr(clause2)
    len1 = len(items1)
    len2 = len(items2)
    if len1 != len2:
        return False
    for i in range(len(items1)):
        #if symmetric(items2[i]) in items1 and len(items1) > 1 and len(items2) > 1:
        #    continue
        if items1[i] != items2[i]:
            return False
    return True
        
def IsexistedInBK(clause, BK)->bool:   #Check new clause exist in BK
    for clauseInBK in BK:
        if compareClause(clause,clauseInBK) == True:
            #print( '   SAME  : ', clauseInBK)
            return True
    return False

def resolve(clause1, clause2):
    # kiểm tra 2 clause giống hệt nhau 
    if compareClause(clause1, clause2) == True:
        return 0,clause1
    clauseA = flattenOr(clause1)
    clauseB = flattenOr(clause2)
    newClause = []
    newClause = clauseA
    tempClause = clauseB
    for i in range(len(newClause)):
        for j in range(len(tempClause)):
            # kiểm tra 2 clause có đối ngẫu
            if  newClause[i] == symmetric(tempClause[j]):
                newClause.pop(i)
                tempClause.pop(j)
                newClause = newClause + tempClause
                newClause = reduceFormulas(newClause,Or)
                if len(newClause) == 0:
                    return -1, OrList(newClause)  # hợp giải ra {}
                return 1, OrList(newClause)  # hợp giải ra clause mới
            # kiểm tra 2 clause có phần giao  
            if newClause[i] == tempClause[j]:
                newClause = newClause + tempClause
                newClause = reduceFormulas(newClause,Or)
                if len(newClause) == 0:
                    return -1, OrList(newClause)  # hợp giải ra {}
                return 0, OrList(newClause)  # hợp giải ra clause mới
    
    return 0, OrList(reduceFormulas(newClause + tempClause,Or))   # hợp giải không ra clause mới

def PL_Resolution(BK,alpha):
    print('[BK]\n',BK)
    BK2 = BK
    BK3 = BK
    alphaList = []
    temp = flattenOr(alpha)
    for i in range(len(temp)):
        alpha2 = symmetric(temp[i])
        alphaList.append(alpha2)
    NewClause = []
    loop = 0
    result = [[]]
    rule = ResolutionRule()
    
    for i in alphaList:
        BK2.append(i)
        print('[alpha]\n', i)
    NewClauseInLoop = []
    while(True):
        loop = loop + 1
        numOfNewClause = 0
        NewClause = []
        for i in range(len(BK2)):
            for j in range(len(BK3)):
                check, form = resolve(BK2[i],BK3[j])
                #print('  [%d][%d]   %d *'%(i,j,check),BK2[i], ' AND ',BK3[j], ' => ' ,form )
                if check == -1:
                    print('[Result]\n',BK2[i], ' AND ',BK3[j], ' => {}\n True' )    
                    BK2 = BK2 + NewClause
                    NewClauseInLoop.append(len(NewClause))
                    return True,BK2,NewClauseInLoop
                if form != True and check == 1: 
                    #Kiểm tra clause mới có trong BK hay chưa
                    if IsexistedInBK(form,BK2) == True: 
                        continue
                    if IsexistedInBK(form,NewClause) == True: 
                        continue
                    if len(NewClause) != 0 and IsexistedInBK(form,NewClause) == True:
                        continue
                    #print(' => ' ,form )
                    numOfNewClause = numOfNewClause + 1
                    NewClause.append(form) 
                    #BK2.append(form)     
        BK2 = BK2 + NewClause
        NewClauseInLoop.append(len(NewClause))
        BK3 = NewClause
        if numOfNewClause == 0:
            break
    print('[Result]\n False' )
    return False,BK2,NewClauseInLoop


  
                     

#-------------   Main   -------------------------
KB_input,alpha_input = input('./input2.txt')
alpha = toClause(alpha_input)
KB = toClauses(KB_input)

result,NewKB,NumOfLoop = PL_Resolution(KB,alpha)

output('output.txt',result,KB,NewKB,NumOfLoop)
#------------------------------------------------

        

