import ast

data = open('E:\OR_Coding\AASCM\MRP_data.txt')

for line in data:
    if line.find("Number of periods") > -1:
        NT = int(line.split(": ")[1])
    if line.find("Number of items of C needed for one item of FP") > -1:
        n_FP = int(line.split(": ")[1])
    if line.find("Number of items of C needed for one item of A") > -1:
        n_A = int(line.split(": ")[1])
    if line.find("Lead time") > -1:
        lead_time = int(line.split(": ")[1])
    if line.find("Safety time") > -1:
        safety_time = int(line.split(": ")[1])
    if line.find("Safety stock") > -1:
        safety_stock = int(line.split(": ")[1])
    if line.find("Current inventory level") > -1:
        curr_inv = int(line.split(": ")[1])
    if line.find("EOQ") > -1:
        EOQ = int(line.split(": ")[1])
    if line.find("Orders of FP") > -1:
        orders_FP = ast.literal_eval(line.split(": ")[1])
    if line.find("Orders of A") > -1:
        orders_A = ast.literal_eval(line.split(": ")[1])
    if line.find("Scheduled receipts") > -1:
        scheduled_receipts = ast.literal_eval(line.split(": ")[1])
data.close()


def solve_MRP(NT, n_FP, n_A, lead_time, safety_time, safety_stock, curr_inv, EOQ, orders_FP, orders_A, scheduled_receipts):
    
    gross_requirements = [-1 for i in range(NT+1)]
    end_inventory_level = [-1 for i in range(NT+1)]
    end_inventory_level[0] = curr_inv
    net_requirements = [-1 for i in range(NT+1)]
    suggested_orders_end = [-1 for i in range(NT+1)]
    suggested_orders_start = [-1 for i in range(NT+1)]
    
    for i in range(1,NT+1):
        gross_requirements[i] = n_FP * orders_FP[i] + n_A * orders_A[i]
    
    for i in range(1,NT+1):
        if gross_requirements[i] - scheduled_receipts[i] <= end_inventory_level[i-1] - safety_stock:
            net_requirements[i] = 0
            end_inventory_level[i] = end_inventory_level[i-1] - gross_requirements[i] + scheduled_receipts[i]
            suggested_orders_end[i] = 0 
        else:
            net_requirements[i] = gross_requirements[i] - scheduled_receipts[i] - end_inventory_level[i-1] + safety_stock
            for k in range(1,10):
                 if (k-1)*EOQ < net_requirements[i] <= k*EOQ:
                     suggested_orders_end[i] = k*EOQ
            end_inventory_level[i] = suggested_orders_end[i] + end_inventory_level[i-1] -gross_requirements[i] + scheduled_receipts[i]


    for i in range(1,NT+1-safety_time-lead_time):
        suggested_orders_start[i] = suggested_orders_end[i+lead_time+safety_time]
    for i in range(NT+1-safety_time-lead_time,NT+1):
        suggested_orders_start[i] = 0
        
    
    return gross_requirements, end_inventory_level, net_requirements, suggested_orders_end, suggested_orders_start



gross_requirements, end_inventory_level, net_requirements, suggested_orders_end, suggested_orders_start = solve_MRP(NT, n_FP, n_A, lead_time, safety_time, safety_stock, curr_inv, EOQ, orders_FP, orders_A, scheduled_receipts)

print('Gross', gross_requirements)
print('Net', net_requirements)
print('Inventory', end_inventory_level)
print('Orders End', suggested_orders_end)
print('Orders Start', suggested_orders_start)