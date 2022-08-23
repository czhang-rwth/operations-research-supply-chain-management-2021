from gurobipy import *

T = 4
P = ['A', 'B', 'C', 'D']
c = {'A': 8000, 'B': 5000, 'C': 8000, 'D': 15000}
h_pp = {'A': 35, 'B': 39, 'C': 45, 'D': 85}
h_up = {'A': 31, 'B': 35, 'C': 41, 'D': 81}
demand_A = [0, 5000, 6000, 3000, 10000]
demand_B = [0, 900, 1000, 4000, 5000]
demand_C = [0, 6000, 9000, 4000, 2000]
demand_D = [0, 10000, 11000, 14000, 16000]
d = {'A': demand_A, 'B': demand_B, 'C': demand_C, 'D': demand_D}
su = {'A': 500000, 'B': 900000, 'C': 800000, 'D': 900000}


def solve_model(T,P,c,h_pp,h_up,d, su):

    model = Model('Production Planning')

    model.modelSense = GRB.MINIMIZE

    x = {}
    for t in range(1, T+1):
        for p in P:
            x[p,t] = model.addVar(vtype=GRB.INTEGER, lb=0)

    y = {}
    for t in range(1, T+1):
        for p in P:
            y[p,t] = model.addVar(vtype=GRB.INTEGER, lb=0)

    i_up = {}
    for t in range(0, T+1):
        for p in P:
            i_up[p,t] = model.addVar(vtype=GRB.INTEGER, lb=0)

    i_pp = {}
    for t in range(0, T+1):
        for p in P:
            i_pp[p, t] = model.addVar(vtype=GRB.INTEGER, lb=0)

    z = {}
    for t in range(1, T+1):
        for p in P:
            z[p,t] = model.addVar(vtype=GRB.BINARY)

    model.update()

    model.setObjective(quicksum(quicksum(h_up[p] * ((i_up[p,t-1] + i_up[p,t]) / 2) + h_pp[p] * ((i_pp[p,t-1] + i_pp[p,t]) / 2) + su[p] * z[p,t] for t in range(1, T + 1)) for p in P))

    for t in range(1, T+1):
        for p in P:
            model.addConstr(x[p,t] <= c[p])

    for t in range(1, T+1):
        model.addConstr(quicksum(y[p,t] for p in P) <= 28000)

    for p in P:
        model.addConstr(i_up[p,0] == 0)

    for t in range(1, T+1):
        for p in P:
            model.addConstr(i_up[p,t] == i_up[p,t-1] + x[p,t] - y[p,t])

    for p in P:
        model.addConstr(i_pp[p, 0] == 0)

    for t in range(1, T+1):
        for p in P:
            model.addConstr(i_pp[p,t] == i_pp[p,t-1] + y[p,t] - d[p][t])

    for t in range(1, T+1):
        for p in P:
            model.addConstr(y[p,t] <= quicksum(d[p][k] for k in range(t, T+1)) * z[p,t])

    model.optimize()

    production = {'A':[], 'B':[], 'C':[], 'D':[]}
    packaging = {'A':[], 'B':[], 'C':[], 'D':[]}
    inventory_unpacked = {'A':[], 'B':[], 'C':[], 'D':[]}
    inventory_packed = {'A':[], 'B':[], 'C':[], 'D':[]}

    if GRB.status.OPTIMAL == model.status:
        for t in range(1, T+1):
            for p in P:
                production[p].append(round(x[p,t].x))
                packaging[p].append(round(y[p,t].x))
                inventory_unpacked[p].append(round(i_up[p,t].x))
                inventory_packed[p].append(round(i_pp[p,t].x))


    return production, packaging, inventory_unpacked, inventory_packed


production, packaging, inventory_unpacked, inventory_packed = solve_model(T,P,c,h_pp,h_up,d, su)

print(production)
print(packaging)
print(inventory_unpacked)
print(inventory_packed)