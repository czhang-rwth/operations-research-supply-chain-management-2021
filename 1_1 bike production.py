from gurobipy import *

NT = 8
d = [0,400,400,800,800,1200,1200,1200,1200]
s_ini = 200
q = 5000
p = 100
h = 5


def solve_model(NT, d, s_ini, q, p, h):
    
    model = Model('BikeModel')
    
    model.modelSense = GRB.MINIMIZE

    x={}
    for t in range(1,NT+1):
        x[t] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    s={}
    for t in range(0,NT+1):
        s[t] = model.addVar(vtype=GRB.INTEGER, lb=0)
        
    y={}
    for t in range(1,NT+1):
        y[t] = model.addVar(vtype=GRB.BINARY)
    
    model.update()

    model.setObjective(quicksum(p*x[t] + q*y[t] + h*((s[t-1]+s[t])/2) for t in range(1,NT+1)))

    for t in range(1,NT+1):
          model.addConstr(s[t-1] + x[t] == d[t] + s[t]) 
         
    model.addConstr(s[0] == s_ini)
    
    model.addConstr(s[NT] == 0)
    
    for t in range(1,NT+1):
        model.addConstr(x[t] <= quicksum(d[k] for k in range(t,NT+1)) * y[t])

    
    model.optimize()
    

    production=[]
    inventory=[]
    if GRB.status.OPTIMAL == model.status:
        for t in range(1,NT+1):
            production.append(x[t].x)
            inventory.append(s[t].x)
    
    return production, inventory


production, inventory = solve_model(NT, d, s_ini, q, p, h)
print(production)
print(inventory)