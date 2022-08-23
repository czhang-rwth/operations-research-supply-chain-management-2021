import math

def LDT(n, m, p):
    
    assignment = {} # key: job, value: machine
    start_time_jobs = {} # key: job, value: start time of the job
    end_time_jobs = {} # key: job, value: end time ofthe job
    end_time_machines = {} # key: machine, value: end time of the job finishing last on the machine
    
    for j in range(n):
        assignment[j] = None
         
    jobs_to_assign = [j for j in range(n)]
    jobs_to_assign.sort(key=lambda j: p[j], reverse = True)
    
    jobs_assigned = []
    
    for i in range(m):
        assignment[jobs_to_assign[i]] = i
        jobs_assigned.append(jobs_to_assign[i])
        start_time_jobs[jobs_to_assign[i]] = 0
        end_time_jobs[jobs_to_assign[i]] = p[jobs_to_assign[i]]
        end_time_machines[i] = p[jobs_to_assign[i]]
      
    for j in jobs_assigned:
        jobs_to_assign.remove(j)
    
    
    while jobs_to_assign:
        
        next_job = jobs_to_assign[0]
        
        selected_machine = None
        best_time = math.inf
        
        for i in range(m):
            if end_time_machines[i] < best_time:
                selected_machine = i
                best_time = end_time_machines[i]

        assignment[jobs_to_assign[0]] = selected_machine
        start_time_jobs[jobs_to_assign[0]] = end_time_machines[selected_machine]
        end_time_jobs[jobs_to_assign[0]] = end_time_machines[selected_machine] + p[jobs_to_assign[0]]
        end_time_machines[selected_machine] += p[jobs_to_assign[0]]
        
        jobs_to_assign.remove(next_job)
        
        obj = max(end_time_machines.values())
    
    return assignment, start_time_jobs, end_time_jobs, end_time_machines, obj

n = 7
m = 3
p = [12,5,7,7,9,4,6]
        
assignment, start_time_jobs, end_time_jobs, end_time_machines, obj = LDT(n,m,p)
        
print(assignment)
print(start_time_jobs)
print(end_time_jobs)
print(end_time_machines) 
print(obj)