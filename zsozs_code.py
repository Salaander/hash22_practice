import os
from pprint import pprint
from collections import defaultdict

from common import get_file
from typing import List


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def __str__(self):
        return str(self.name) + " " + ' '.join([f"{skill} {level}" for skill, level in self.skills.items()])

class Project:
    def __init__(self, name, days_required, score, bb, roles):
        self.name = name
        self.days_required = days_required
        self.score = score
        self.bb = bb
        self.roles = roles

    def __str__(self):
        return ' '.join([str(self.name), str(self.days_required), str(self.score), str(self.bb)]) + " " + ' '.join([f"{skill} {level}" for skill, level in self.roles.items()])


class Stat:
    def __init__(self):
        self.skills = {}

    def add_skill(self, name, level):
        if name not in self.skills:
            self.skills[name] = {"skills": {}, "roles": {}}
        if level not in self.skills[name]["skills"]:
            self.skills[name]["skills"][level] = 0
        self.skills[name]["skills"][level] += 1

    def add_role(self, name, level):
        if name not in self.skills:
            self.skills[name] = {"skills": {}, "roles": {}}
        if level not in self.skills[name]["roles"]:
            self.skills[name]["roles"][level] = 0
        self.skills[name]["roles"][level] += 1


class Solver:
    def __init__(self):
        self.contributors = []
        self.projects = []
        self.skills_to_people = {}

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

    def preprocess(self):
        for c in self.contributors:
            for s, l in c.skills.items():
                if s not in self.skills_to_people:
                    self.skills_to_people[s] = {}
                if l not in self.skills_to_people[s]:
                    self.skills_to_people[s][l] = []
                self.skills_to_people[s][l].append(c)
        pprint(self.skills_to_people)

    def solve(self):
        self.preprocess()

    def print(self, verbose = False):
        print("")
        print(f"Contributors ({len(self.contributors)})")
        if verbose:
            for c in self.contributors:
                print(c)
            print("")
        print(f"Projects ({len(self.projects)})")
        if verbose:
            for p in self.projects:
                print(p)
            print("")

    def print_stats(self):
        stat = Stat()
        for c in self.contributors:
            for s, l in c.skills.items():
                stat.add_skill(s, l)
        for p in self.projects:
            for s, l in p.roles.items():
                stat.add_role(s, l)
        print("Skills")
        pprint(stat.skills, width=200)
        print("")

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
    solver.print_stats()
    solver.solve()
