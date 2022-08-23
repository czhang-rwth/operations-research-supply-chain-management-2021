import random

# local search for the single machine scheduling with set-up times s_kj
# neighborhood: taking a job in the schedule and inserting it in another position in the schedule
# acceptance-rejection criterion: first improvement
    
# INPUT PARAMETERS:
# n: number of jobs
# p: processing times of the jobs
# w: weights of the jobs
# s: set up times of the jobs
# initial schedule


def local_search(n, p, w, s, initial_schedule):
    
    J = range(n)
    
    def evaluate_schedule(schedule):
        
        C = {}
        C[schedule[0]] = p[schedule[0]]
        last_job = schedule[0]

        for job in schedule[1:]:
            C[job] = C[last_job] + s[last_job, job] + p[job]
            last_job = job
        
        obj = 0
        for job in J:
            obj += w[job] * C[job]
        
        return obj
    
    
    def move(job, position, schedule):
        
        new_schedule = schedule[:]
        
        new_schedule.remove(job)
        
        new_schedule.insert(position,job)
        
        return new_schedule
    
    
    current_schedule = initial_schedule[:]
    best_obj = evaluate_schedule(current_schedule)
    
    improvement_found = True
    
    while improvement_found:
        
        improvement_found = False
        
        for i in range(n):
            job = current_schedule[i]
            
            for position in range(len(current_schedule)):
                if position != i: 
                    new_schedule = move(job, position, current_schedule)
                    new_obj = evaluate_schedule(new_schedule)
                  
                    if new_obj < best_obj:
                        current_schedule = new_schedule
                        best_obj = new_obj
                        improvement_found = True
                        break
            if improvement_found:
                break
    
    return current_schedule, best_obj
  
n = 10
p = {0: 3, 1: 2, 2: 5, 3: 1, 4: 3, 5: 6, 6:2, 7:5 , 8:4 , 9:3 }
w = {0: 1, 1: 2, 2: 2, 3: 1, 4: 3, 5: 2, 6:3, 7:7 , 8:8 , 9:10 }
s = {}

random.seed(0)
for j in range(n):
    for k in range(n):
        s[j,k] = random.randint(1, 9)
        
starting_solution = [0,1,2,3,4,5,6,7,8,9]

                
solution, cost =   local_search(n, p, w, s, starting_solution)

print('Final Schedule: ', solution)
print('Cost: ', cost)