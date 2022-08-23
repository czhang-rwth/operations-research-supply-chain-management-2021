from gurobipy import *

NT = 8
d_r = [0,400,400,800,800,1200,1200,1200,1200]
s_ini_r = 200
q_r = 5000
p_r = 100 
h_r = 5
d_m = [0,200,200,200,200,200,200,500,500]
s_ini_m = 0
q_m = 3000
p_m = 60 
h_m = 3


def solve_model(NT, d_r, d_m, s_ini_r, s_ini_m, q_r, q_m, p_r, p_m, h_r, h_m):
    
    
    model = Model('BikeModel')
    
    model.modelSense = GRB.MINIMIZE

    x_r={}
    for t in range(1,NT+1):
        x_r[t] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    s_r={}
    for t in range(0,NT+1):
        s_r[t] = model.addVar(vtype=GRB.INTEGER, lb=0)
        
    y_r={}
    for t in range(1,NT+1):
        y_r[t] = model.addVar(vtype=GRB.BINARY)
        
    x_m={}
    for t in range(1,NT+1):
        x_m[t] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    s_m={}
    for t in range(0,NT+1):
        s_m[t] = model.addVar(vtype=GRB.INTEGER, lb=0)
        
    y_m={}
    for t in range(1,NT+1):
        y_m[t] = model.addVar(vtype=GRB.BINARY)
    
    model.update()

    model.setObjective(quicksum(p_r*x_r[t] + q_r*y_r[t] + h_r*((s_r[t-1]+s_r[t])/2) for t in range(1,NT+1)) + quicksum(p_m*x_m[t] + q_m*y_m[t] + h_m*((s_m[t-1]+s_m[t])/2) for t in range(1,NT+1)))

    for t in range(1,NT+1):
          model.addConstr(s_r[t-1] + x_r[t] == d_r[t] + s_r[t]) 
         
    model.addConstr(s_r[0] == s_ini_r)
    
    model.addConstr(s_r[NT] == 0)
    
    for t in range(1,NT+1):
        model.addConstr(x_r[t] <= quicksum(d_r[k] for k in range(t,NT+1)) * y_r[t])
        
    for t in range(1,NT+1):
          model.addConstr(s_m[t-1] + x_m[t] == d_m[t] + s_m[t]) 
         
    model.addConstr(s_m[0] == s_ini_m)
    
    model.addConstr(s_m[NT] == 0)
    
    for t in range(1,NT+1):
        model.addConstr(x_m[t] <= quicksum(d_m[k] for k in range(t,NT+1)) * y_m[t])
        
    for t in range(1,NT+1):
        model.addConstr(x_r[t]+x_m[t] <= 1500)
        

    model.optimize()
    
    
    production_mountain_bikes=[]
    inventory_mountain_bikes=[]
    production_racing_bikes=[]
    inventory_racing_bikes=[]
    total_cost = 0
    
    if GRB.status.OPTIMAL == model.status:
        for t in range(1,NT+1):
            production_mountain_bikes.append(round(x_m[t].x))
            inventory_mountain_bikes.append(round(s_m[t].x))
            production_racing_bikes.append(round(x_r[t].x))
            inventory_racing_bikes.append(round(s_r[t].x))
            total_cost = round(model.ObjVal)  
    
    
    
    return production_mountain_bikes, inventory_mountain_bikes, production_racing_bikes, inventory_racing_bikes, total_cost
    
    
    

production_mountain_bikes, inventory_mountain_bikes, production_racing_bikes, inventory_racing_bikes, total_cost = solve_model(NT, d_r, d_m, s_ini_r, s_ini_m, q_r, q_m, p_r, p_m, h_r, h_m)

print(production_mountain_bikes)
print(inventory_mountain_bikes)
print(production_racing_bikes)
print(inventory_racing_bikes)
print(total_cost)