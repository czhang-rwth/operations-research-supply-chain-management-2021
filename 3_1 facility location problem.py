from gurobipy import *
import ast
import math

data = open(r"E:\OR_Coding\AASCM\facility_location_instance.txt")

for line in data:
    if line.find("m:") > -1:
        m = int(line.split(":")[1])
    if line.find("n:") > -1:
        n = int(line.split(":")[1])
    if line.find("f:") > -1:
        f = ast.literal_eval(line.split(":")[1])
    if line.find("C:") > -1:
        C = ast.literal_eval(line.split(":")[1])
    if line.find("d:") > -1:
        d = ast.literal_eval(line.split(":")[1])
    if line.find("x_depots:") > -1:
        x_depots = ast.literal_eval(line.split(":")[1])
    if line.find("y_depots:") > -1:
        y_depots = ast.literal_eval(line.split(":")[1])
    if line.find("x_customers:") > -1:
        x_customers = ast.literal_eval(line.split(":")[1])
    if line.find("y_customers:") > -1:
        y_customers = ast.literal_eval(line.split(":")[1])
        
data.close()

I = [i for i in range(m)]
J = [j for j in range(n)]

c = {}
for i in I:
    for j in J:
        c[i,j] = math.sqrt((x_depots[i] - x_customers[j])**2+(y_depots[i] - y_customers[j])**2)


def solve(C, f, c, d, I, J):
    
    model = Model('FacilityLocation')
    
    model.modelSense = GRB.MINIMIZE

    x={}
    for i in I:
        for j in J:
            x[i,j] = model.addVar(lb = 0, ub =1)
    
    y={}
    for i in I:
        y[i] = model.addVar(vtype=GRB.BINARY)
    
    model.update()

    model.setObjective(quicksum(quicksum(x[i,j]*c[i,j] for i in I) for j in J) + quicksum(f[i]*y[i] for i in I))

    for i in I:
          model.addConstr(quicksum(x[i,j]*d[j] for j in J) <= C[i]) 
         
    for j in range(n):
        model.addConstr(quicksum(x[i,j] for i in I) == 1)
    
    for i in I:
        for j in J:
            model.addConstr(x[i,j]<=y[i])
    
    model.optimize()
    
    
    assignments={}
    for i in I:
        assignments[i] = []
    open_depots=[]
    total_cost = 0
    
    if GRB.status.OPTIMAL == model.status:
        for i in I:
            for j in J:
                if x[i,j].x>0:
                    assignments[i].append(j)
            if round(y[i].x)==1:
                open_depots.append(i)
        total_cost = round(model.ObjVal,2)      
        
    return assignments, open_depots, total_cost



assignments, open_depots, total_cost = solve(C,f,c,d,I,J)

print('Assignments: ', assignments)
print('Open depots: ', open_depots)
print('Total cost: ', total_cost)



import matplotlib.pyplot as plt

def plot(I, J, x_depots, y_depots, x_customers, y_customers, assignments, open_depots):
    
    figure = plt.figure()
    
    for i in I:
        if i in open_depots:
            plt.scatter(x_depots[i], y_depots[i], color="green", alpha=1, marker='s', s=50, zorder=2)
        else:
            plt.scatter(x_depots[i], y_depots[i], color="darkgray", alpha=1, marker='s', s=50, zorder=2)
    
    for j in J:
        plt.scatter(x_customers[j], y_customers[j], color="red", alpha=1, marker='o', s=50, zorder=2)
    
    for i in I:
        for j in assignments[i]:
            plt.plot([x_depots[i], x_customers[j]],[y_depots[i], y_customers[j]], color="black", alpha=1, linewidth=1, zorder=1)
    
    figure.savefig(r"E:\OR_Coding\AASCM\facility_location_IP_solution.pdf")
    
    plt.close(fig=None)
    

plot(I, J, x_depots, y_depots, x_customers, y_customers, assignments, open_depots)