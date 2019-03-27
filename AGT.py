# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
from itertools import permutations, combinations
"""
path 1: s - v1 - t
path 2: s - v2 - t
path 3: s - v3 - t
path 4: s - v2 - v1 -t
path 5: s - v3 - v2 - t
path 6: s - v3 - v2 - v1 - t
"""
paths = [1,2,3,4,5,6]


#enumerate all the ways all players choose the same path
all_on_one = list(permutations(paths, 1))
#enumerate all the ways two players can choose one path, the third player another
#order is important - use permuatations rather than combinations
two_on_one = list(permutations(paths, 2))
#enumerate all the ways all players choose a different path
all_different = list(combinations(paths, 3))
#which nodes make up which path
path_nodes = {1: ["s", "v1", "t"], 2: ["s", "v2", "t"], 3: ["s", "v3", "t"], 4: ["s", "v2", "v1", "t"], 5: ["s", "v3", "v2", "t"], 6:  ["s", "v3", "v2", "v1", "t"]}
#the cost of travelling between two nodes for 1, 2 and 3 players
subpath_costs = {("s", "v1"): [6, 7, 8], ("s", "v2"): [4,2,5], ("s", "v3"): [3, 7, 6], ("v1", "t"): [3, 9, 5], ("v2", "t"): [11, 10, 9], ("v3", "t"): [8,3,7], ("v2", "v1"): [2,4,5], ("v3", "v2"):[2,1,2]}

def get_cost(path):
    #return the cost to each player given the players' chosen paths
    #check number of players on each path
    if len(path) == 1:
        #all players on one path
        subpaths = []
        path = path[0]
        for i in range(len(path_nodes[path])-1):
            #list the node transitions made by each player
            subpaths.append((path_nodes[path][i], path_nodes[path][i+1]))
            #get the cost for all players
        cost_all = 0
        for subpath in subpaths:
            
            cost_all += subpath_costs[subpath][2]
        return [cost_all]*3
    if len(path) == 2:
        #2 players on first path, 1 on second
        subpaths_2p = []
        subpaths_1p = []
        path_2p = path[0]
        path_1p = path[1]
        for i in range(len(path_nodes[path_1p])-1):
            #list the node transitions made by the single player's path
            subpaths_1p.append((path_nodes[path_1p][i], path_nodes[path_1p][i+1]))
        for i in range(len(path_nodes[path_2p])-1):
            subpaths_2p.append((path_nodes[path_2p][i], path_nodes[path_2p][i+1]))            
        
        
        cost_1p = 0
        cost_2p = 0
        for subpath in subpaths_1p:
            #get the cost for the lone player if subpath not shared by other paths
            if subpath not in subpaths_2p:
                cost_1p += subpath_costs[subpath][0]
                
            #and if shared with other two players
            else:
                cost_1p += subpath_costs[subpath][2]
        for subpath in subpaths_2p:
            #get the cost for the pair of players if not sharing with the third
            if subpath not in subpaths_1p:
                cost_2p += subpath_costs[subpath][1]
            #and if shared by all players
            else:
                cost_2p += subpath_costs[subpath][2]
        return [cost_2p, cost_2p, cost_1p]
    if len(path) == 3:
        #3 players have all chosen different paths
        subpaths_p1 = []
        subpaths_p2 = []
        subpaths_p3 = []
        path_p1 = path[0]
        path_p2 = path[1]
        path_p3 = path[2]
        for i in range(len(path_nodes[path_p1])-1):
            #list the node transitions for player 1
            subpaths_p1.append((path_nodes[path_p1][i],path_nodes[path_p1][i+1]))
        for i in range(len(path_nodes[path_p2])-1):
            #list the node transitions for player 2
            subpaths_p2.append((path_nodes[path_p2][i],path_nodes[path_p2][i+1]))
        for i in range(len(path_nodes[path_p3])-1):
            #list the node transitions for player 3
            subpaths_p3.append((path_nodes[path_p3][i],path_nodes[path_p3][i+1]))
        #get costs to each player
        cost_p1 = 0
        cost_p2 = 0
        cost_p3 = 0
        for subpath in subpaths_p1:
            #if subpath only used by that player
            if subpath not in subpaths_p2 + subpaths_p3:
                cost_p1 += subpath_costs[subpath][0]
            #sharing subpath with at least one other player
           
            #sharing with both other players
            elif subpath in subpaths_p2 and subpath in subpaths_p3:
                cost_p1 += subpath_costs[subpath][2]
            #sharing with one other player
            else:
                cost_p1 += subpath_costs[subpath][1]
        for subpath in subpaths_p2:
            #if subpath only used by that player
            if subpath not in subpaths_p1 + subpaths_p3:
                cost_p2 += subpath_costs[subpath][0]
             #sharing with both other players
            elif subpath in subpaths_p1 and subpath in subpaths_p3:
                cost_p2 += subpath_costs[subpath][2]
            #sharing with one other player
            else:
                cost_p2 += subpath_costs[subpath][1]
        for subpath in subpaths_p3:
            #if subpath only used by that player
            if subpath not in subpaths_p2 + subpaths_p1:
                cost_p3 += subpath_costs[subpath][0]
             #sharing with both other players
            elif subpath in subpaths_p2 and subpath in subpaths_p1:
                cost_p3 += subpath_costs[subpath][2]
            #sharing with one other player
            else:
                cost_p3 += subpath_costs[subpath][1]
        return [cost_p1, cost_p2, cost_p3]
            


def get_neighbours(profile):
    #return the profiles which can be obtained if one player unilaterally switches from the current profile
    if len(profile) == 1:
        #unilateral switch will mean two players on old path, one on a new one
        new_profiles = []
        for item in two_on_one:
            if item[0] == profile[0]:
                new_profiles.append(item)
        return new_profiles
    if len(profile) == 2:
        #unilateral switch can get a new profile of any length
        new_profiles = []
        #add profiles where all players choose same path
        new_profiles.append(((profile[0]),))
        #add profiles where two different paths chosen
        for item in two_on_one:
            if item[0] == profile[0]:
                new_profiles.append(item)
        #add profiles where all players choose different paths
        for item in all_different:
            if profile[0] in item and profile[1] in item:
                new_profiles.append(item)
        return new_profiles
        
    if len(profile) == 3:
        #unilateral switch can produce a profile with three or two paths played
        new_profiles = []
        #add profiles with two paths used
        for item in two_on_one:
            if item in permutations(profile, 2):
                new_profiles.append(item)
        for item in all_different:
            
            if len(set(profile)&set(item)) == 2 :
                #only 1 item has changed between the two profiles, i.e one unilateral switch
                new_profiles.append(item)
            
        return new_profiles
    
def get_NE():
    #return all Nash Equilbira of the game
    NE = []
    j = 1
    #iterate over all possible profiles
    all_profiles = all_different + two_on_one + all_on_one
    for profile in all_profiles:
        profile_costs = get_cost(profile)
        neighbours = get_neighbours(profile)
        
        
        isNE = True
        
        for neighbour in neighbours:
           
                
        #only continue to check while current profile may be NE
        #check if any neighbours have a lower cost
            neighbour_cost = get_cost(neighbour)
            print("checking profile", profile, j, "of ", len(all_profiles))
            if neighbour_cost[0] < profile_costs[0]:
                #neighbour has a lower cost for P1, current profile is not NE
                isNE = False
                print("profile cost: ", profile_costs)
                print("neighbour cost: ", neighbour_cost)
                print("Lower cost found p1 ^")
                break
            elif neighbour_cost[1] < profile_costs[1]:
                #neighbour has a lower cost for P2, current profile is not NE
                isNE = False
                print("profile cost: ", profile_costs)
                print("neighbour cost: ", neighbour_cost)
                print("Lower cost found p2 ^")
                break
            elif neighbour_cost[2] < profile_costs[2]:
                #neighbour has a lower cost for P3, current profile is not NE
                isNE = False
                print("profile cost: ", profile_costs)
                print("neighbour cost: ", neighbour_cost)
                print("Lower cost found p3 ^")
                break
           
           
                
        #all neighbours checked, no lower cost for any player with a unilateral switch, profile is NS
        if isNE:
            NE.append(profile)
        
        j += 1
    return NE

def get_best_social_welfare():
    #iterate over profiles, return profile with greatest social welfare (lowest total cost), along with the cost to all players
    lowest_cost = np.inf
    best_profile = None
    all_profiles = all_different + two_on_one + all_on_one
    for profile in all_profiles:
        profile_costs = sum(get_cost(profile))
        
        if profile_costs < lowest_cost:
            lowest_cost = profile_costs
            best_profile = profile
    return best_profile, lowest_cost
    
    

test = get_NE()
social_welfare_profile, amount = get_best_social_welfare()
        


          

        
