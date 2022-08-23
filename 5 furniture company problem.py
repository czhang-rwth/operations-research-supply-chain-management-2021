from gurobipy import *

P = ['Desk', 'Table', 'Chair']
R = ['lumber', 'carpentry', 'finishing']

c = {'lumber': 2, 'carpentry': 5.2, 'finishing': 4}
m = {'lumber': {'Desk': 8, 'Table': 6, 'Chair': 1}, 'carpentry': {'Desk': 2, 'Table': 1.5, 'Chair': 0.5}, 'finishing': {'Desk': 4, 'Table': 2, 'Chair': 1.5}}


e = {'Desk': 60, 'Table': 40, 'Chair': 10}


K = {1: 'low', 2:'most likely', 3: 'high'}
prob = {1:0.3, 2:0.4, 3:0.3}
D = {1:{'Desk': 50, 'Table': 20, 'Chair': 200}, 2:{'Desk': 150, 'Table': 110, 'Chair': 225}, 3:{'Desk': 250, 'Table': 250, 'Chair': 500}}


# write a function that defines and solves the stochastic problem

print('###########################################SP################################################')   

def solve_SP(P, R, c, m, e, K, prob, D):
    
    model = Model('SP')
    
    model.modelSense = GRB.MAXIMIZE
    model.setParam('OutputFlag', False)
    
    y={}
    for p in P:
        y[p] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    x={}
    for r in R:
        x[r] = model.addVar(lb=0)
        
    s={}
    for p in P:
        for k in K:
            s[p,k] = model.addVar(vtype=GRB.INTEGER, lb=0)
            
    model.update()
    
    model.setObjective(quicksum(prob[k] * quicksum(e[p]*s[p,k] for p in P) for k in K) - quicksum(c[r]*x[r] for r in R))
    
    for r in R:
        model.addConstr(quicksum(m[r][p] * y[p] for p in P) <= x[r])
        
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= D[k][p])  
            
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= y[p])
    
    model.optimize()
    
    if GRB.status.OPTIMAL == model.status:
        for p in P:
            print(p, y[p].x)
        for r in R:
            print(r, x[r].x)
        for k in K:
            for p in P:
                print(k,p,s[p,k].x)
        print('Obj', model.ObjVal)


solve_SP(P, R, c, m, e, K, prob, D)



# write a function that defines and solves the expected value problem


print('###########################################EV################################################')   

def solve_EV(P, R, c, m, e, K, prob, D):
    
    model = Model('EV')
    
    model.modelSense = GRB.MAXIMIZE
    model.setParam('OutputFlag', False)

    
    y={}
    for p in P:
        y[p] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    x={}
    for r in R:
        x[r] = model.addVar(lb=0)
        
    s={}
    for p in P:
        for k in K:
            s[p,k] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    model.update()
    
    model.setObjective(quicksum(prob[k] * quicksum(e[p]*s[p,k] for p in P) for k in K) - quicksum(c[r]*x[r] for r in R))
    
    for r in R:
        model.addConstr(quicksum(m[r][p] * y[p] for p in P) <= x[r])
        
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= D[k][p])  
            
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= y[p])
    
    model.optimize()
    
    y_bar = {}
    
    if GRB.status.OPTIMAL == model.status:
        for p in P:
            print(p, y[p].x)
            y_bar[p] = y[p].x
        for r in R:
            print(r, x[r].x)
        for k in K:
            for p in P:
                print(k,p,s[p,k].x)
        print('Obj', model.ObjVal)           
    
    return y_bar


K_average = {1: 'Average'}
p_average = {1:1}
D_average = {1:{}}
for p in P:
    D_average[1][p] = sum(prob[k]*D[k][p] for k in K)

y_bar = solve_EV(P, R, c, m, e, K_average, p_average, D_average)


      
# write a function that defines and solves the problem to calculate the expected result of using the EV solution

print('###########################################EEV###############################################')    
            
def solve_EEV(P, R, c, m, e, K, prob, D, y_bar):
    
    model = Model('EEV')
    
    model.modelSense = GRB.MAXIMIZE
    model.setParam('OutputFlag', False)

    
    y={}
    for p in P:
        y[p] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    x={}
    for r in R:
        x[r] = model.addVar(lb=0)
        
    s={}
    for p in P:
        for k in K:
            s[p,k] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    model.update()
    
    model.setObjective(quicksum(prob[k] * quicksum(e[p]*s[p,k] for p in P) for k in K) - quicksum(c[r]*x[r] for r in R))
    
    for r in R:
        model.addConstr(quicksum(m[r][p] * y[p] for p in P) <= x[r])
        
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= D[k][p])  
            
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= y[p])
        
    for p in P:
        model.addConstr(y[p] == y_bar[p])
    
    model.optimize()
    
    if GRB.status.OPTIMAL == model.status:
        for p in P:
            print(p, y[p].x)
        for r in R:
            print(r, x[r].x)
        for k in K:
            for p in P:
                print(k,p,s[p,k].x)
        print('Obj', model.ObjVal)
            

solve_EEV(P, R, c, m, e, K, prob, D, y_bar)


# write a function that defines and solves the problem to calculate the expected skeleton solution value
            
print('###########################################ESSV##############################################')    
            
def solve_ESSV(P, R, c, m, e, K, prob, D, y_bar):
    
    model = Model('ESSV')
    
    model.modelSense = GRB.MAXIMIZE
    model.setParam('OutputFlag', False)

    
    y={}
    for p in P:
        y[p] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    x={}
    for r in R:
        x[r] = model.addVar(lb=0)
        
    s={}
    for p in P:
        for k in K:
            s[p,k] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    model.update()
    
    model.setObjective(quicksum(prob[k] * quicksum(e[p]*s[p,k] for p in P) for k in K) - quicksum(c[r]*x[r] for r in R))
    
    for r in R:
        model.addConstr(quicksum(m[r][p] * y[p] for p in P) <= x[r])
        
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= D[k][p])  
            
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= y[p])
        
    for p in P:
        if y_bar[p] == 0:
            model.addConstr(y[p] == y_bar[p])
    
    model.optimize()
    
    if GRB.status.OPTIMAL == model.status:
        for p in P:
            print(p, y[p].x)
        for r in R:
            print(r, x[r].x)
        for k in K:
            for p in P:
                print(k,p,s[p,k].x)
        print('Obj', model.ObjVal)
            
solve_ESSV(P, R, c, m, e, K, prob, D, y_bar)       


# write a function that defines and solves the problem to calculate the expected input value   
            
print('###########################################EIV###############################################')    
            
def solve_EIV(P, R, c, m, e, K, prob, D, y_bar):
   
    model = Model('EIV')
    
    model.modelSense = GRB.MAXIMIZE
    model.setParam('OutputFlag', False)

    
    y={}
    for p in P:
        y[p] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    x={}
    for r in R:
        x[r] = model.addVar(lb=0)
        
    s={}
    for p in P:
        for k in K:
            s[p,k] = model.addVar(vtype=GRB.INTEGER, lb=0)
    
    model.update()
    
    model.setObjective(quicksum(prob[k] * quicksum(e[p]*s[p,k] for p in P) for k in K) - quicksum(c[r]*x[r] for r in R))
    
    for r in R:
        model.addConstr(quicksum(m[r][p] * y[p] for p in P) <= x[r])
        
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= D[k][p])  
            
    for p in P:
        for k in K:
            model.addConstr(s[p,k] <= y[p])
        
    for p in P:
        model.addConstr(y[p] >= y_bar[p])
    
    model.optimize()
    
    if GRB.status.OPTIMAL == model.status:
        for p in P:
            print(p, y[p].x)
        for r in R:
            print(r, x[r].x)
        for k in K:
            for p in P:
                print(k,p,s[p,k].x)
        print('Obj', model.ObjVal)
            

solve_EIV(P, R, c, m, e, K, prob, D, y_bar)         