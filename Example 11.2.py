# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    #Create lists
    l = [25, 35, 30, 40, 35] #length
    w = [20, 20, 30, 20, 35] #width
    cl = [ #clearance
        [0, 3.5, 5.0, 5.0, 5.0],
        [3.5, 0, 5.0, 3.0, 5.0],
        [5.0, 5.0, 0, 5.0, 5.0],
        [5.0, 3.0, 5.0, 0, 5.0],
        [5.0, 5.0, 5.0, 5.0, 0]
        ]
    f = [ #flow
        [0, 25, 35, 50, 0],
        [25, 0, 10, 15, 20],
        [35, 10, 0, 50, 10],
        [50, 15, 50, 0, 15],
        [0, 20, 10, 15, 0]
        ]
    cost = 1.00 #cost/unit distance
    
    #indices
    n = len(l)
    M = 999
    
    #Create model
    m = Model("Example 11.2")
    
    #Declare decision variables
    x = m.addVars(range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "Center")
    xp = m.addVars(range(n), range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "XP")
    xn = m.addVars(range(n), range(n), lb = 0, vtype = GRB.CONTINUOUS, name = "XN")
    z = m.addVars(range(n), range(n), vtype = GRB.BINARY, name = "Z")
    
    #Set objective fuction
    m.setObjective(quicksum(cost * f[i][j] * (xp[i,j] + xn[i,j]) for i in range(n-1) for j in range(i+1, n)), GRB.MINIMIZE)
    
    for i in range(n-1):
        for j in range(i+1, n):
            m.addConstr(x[i] - x[j] == xp[i,j] - xn[i,j], name = "Absolute_Value_Constraint")
            m.addConstr(x[i] - x[j] + M * z[i,j] >= 0.5 * (l[i] + l[j]) + cl[i][j], name = "Constraint 11.11")
            m.addConstr(x[j] - x[i] + M *(1 - z[i,j]) >= 0.5 * (l[i] + l[j]) + cl[i][j], name = "Constraint 11.12")
            
    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           if v.x > 0:
               print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')