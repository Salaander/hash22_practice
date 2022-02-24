import os
from collections import defaultdict

from common import get_file
from typing import List
import numpy as np
import bisect

class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

        self.schedule = {"start":[], "stop":[]} # closed interval
    def is_free(self, a,b):

        if a in self.schedule["start"] or a in self.schedule["stop"]:
            return False
        if b in self.schedule["start"] or b in self.schedule["stop"]:
            return False
        
        i_a_start = bisect.bisect_left(self.schedule["start"], a)
        i_b_start = bisect.bisect_left(self.schedule["start"], b)
        i_a_stop  = bisect.bisect_left(self.schedule["stop"],  a)
        i_b_stop  = bisect.bisect_left(self.schedule["stop"],  b)

        if i_a_start == i_a_stop+1:
            return False

        if i_b_start == i_b_stop+1:
            return False
            
        if i_a_start != i_b_start:
            return False

        return True
        
    def book_time(self, a,b):
        bisect.insort(self.schedule["start"], a)
        bisect.insort(self.schedule["stop"],  b)
        

    def __str__(self):
        return str(self.name) + " " + ' '.join([f"{skill} {level}" for skill, level in self.skills.items()])

class Project:
    def __init__(self, name, days_required, score, bb, roles):
        self.name = name
        self.days_required = days_required
        self.score = score
        self.bb = bb
        self.roles = roles

        self.scheduled = False
        self.assigned_workers = []

    def __str__(self):
        return ' '.join([str(self.name), str(self.days_required), str(self.score), str(self.bb)]) + " " + ' '.join([f"{skill} {level}" for skill, level in self.roles.items()])


class WorkerPool(object):

    def  __init__(self, workers):

        self.workers = workers

        self.skill2workers = {}
        for w in self.workers:
            for s in w.skills.keys():
                if s in self.skill2workers:
                    self.skill2workers[s].append(w)
                else:
                    self.skill2workers[s] = [w]
        for s in w.skills.keys():
            self.skill2workers[s] = sorted( self.skill2workers[s], key= lambda x : x.skills[s])

        self.skill2level2workers = {}
        for w in self.workers:
            for s, level in w.skills.items():
                if s in self.skill2level2workers:
                    if level in self.skill2level2workers[s]:
                        self.skill2level2workers[s][level].append(w)
                    else:
                        self.skill2level2workers[s][level] = [w]
                else:
                    self.skill2level2workers[s] = {w}
                    self.skill2level2workers[s][level] = [w]
        for k in self.skill2level2workers.keys():
            self.skill2level2workers[k] = sorted(self.skill2level2workers[k])

    def get_best_workers1(self, time, project):

        contributors = []
        for role, level in project.roles.items():
            role_filled = False
            for level_worker in self.skill2level2workers[role].keys():
                if level_worker>=level:
                    for p in self.skill2level2workers[role][level]:
                        if p.is_free(time, project.days_required + time):
                            contributors.append(p)
                            role_filled = True
                            continue
            if not role_filled: 
                return []

        return contributors
            
                
class Solver:
    def __init__(self):
        self.contributors = []
        self.projects = []

        self.solution = {}

        self.worker_pool = WorkerPool(self.contributors)

    def read(self, filename):
        with open(filename, 'r') as file:
            C, P = list(map(int, file.readline().split()))
            for i in range(C):
                name, N = file.readline().split()
                N = int(N)
                skills = {}
                for j in range(N):
                    skill, level = file.readline().split()
                    skills[skill] = int(level)
                contributor = Contributor(name, skills)
                self.contributors.append(contributor)
            for i in range(P):
                name, D, S, B, R = file.readline().split()
                D, S, B, R = list(map(int, [D, S, B, R]))
                roles = {}
                for j in range(R):
                    skill, level = file.readline().split()
                    roles[skill] = int(level)
                project = Project(name, D, S, B, roles)
                self.projects.append(project)

    def solve1(self):
        self.projects = sorted( self.projects, key= lambda x : x.bb - x.days_required, reverse=True)
        
        time = 0
        for p in self.projects:
            workers_selected = self.worker_pool.get_best_workers1(time, p)

            if len(workers_selected) > 0:
                for w in workers_selected:
                    w.book_time(time, time + p.days_required )

                p.scheduled = True
                p.assigned_workers = workers_selected


    def write(self, filename):
        with open(filename, 'w') as file:
            file.write(str(len(self.solution))+"\n")
            for p_id, contributors in self.solution.items():
                file.write(self.projects[p_id].name+"\n")
                file.write(" ".join([c.name for c in contributors])+"\n")

    def print(self):
        print(f"Contributors ({len(self.contributors)})")
        for c in self.contributors:
            print(c)
        print("")
        print(f"Projects ({len(self.projects)})")
        for p in self.projects:
            print(p)

inputs = [
    "a_an_example.in.txt",
    # "b_better_start_small.in.txt",
    # "c_collaboration.in.txt",
    # "d_dense_schedule.in.txt",
    # "e_exceptional_skills.in.txt",
    # "f_find_great_mentors.in.txt",
]

for input in inputs:
    solver = Solver()
    solver.read(os.path.join("in_data", input))
    solver.print()
