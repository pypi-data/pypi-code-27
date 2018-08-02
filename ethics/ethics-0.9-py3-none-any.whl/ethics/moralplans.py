import itertools
import json
import io
import copy

class Action:
    def __init__(self, name, pre, eff, intrinsicvalue):
        self.name = name
        self.pre = pre
        self.eff = eff
        self.intrinsicvalue = intrinsicvalue
        
    def __str__(self):
        return self.name
        
class Event:
    def __init__(self, name, pre, eff, times = []):
        self.name = name
        self.pre = pre
        self.eff = eff
        self.times = times

class Situation:
    def __init__(self, json):
        self.parseJSON(json)
 
    def parseJSON(self, jsonfile):
        with io.open(jsonfile) as data_file:
            data = json.load(data_file)
            self.actions = []
            for a in data["actions"]:
                action = Action(a["name"], a["preconditions"], a["effects"], a["intrinsicvalue"])
                self.actions += [action]
            self.events = []
            for a in data["events"]:
                event = Event(a["name"], a["preconditions"], a["effects"], a["timepoints"])
                self.events += [event]
            self.affects = data["affects"]
            self.goal = data["goal"]
            planactions = []
            for a in data["plan"]:
                for b in self.actions:
                    if a == b.name:
                        planactions += [b]
            self.plan = Plan(planactions, self.events, self.goal)
            self.init = data["initialState"]
            self.utilities = data["utilities"]
            self.harmful = []
            for u in self.utilities:
                if u["utility"] < 0:
                    self.harmful += [u["fact"]]
            self.alternatives = []
    
    def getAllConsequences(self):
        return self.plan.simulate(self.init)

    def getUtility(self, fact):
        for u in self.utilities:
            if fact == u["fact"]:
                return u["utility"]
        return 0

    def getFinalUtility(self):
        utility = 0
        sn = self.plan.simulate(self.init)
        for k, v in sn.items():
            utility += self.getUtility({k:v})
        return utility
        
    def isInstrumentalAt(self, effect, positions):
        sn = self.plan.simulate(self.init, blockEffect = effect, blockPositions = positions)
        return not self.plan.satisfiesGoal(sn)    
        
    def isInstrumental(self, effect):
        for p in self.plan.getSubPlans(len(self.plan.plan)):
            if self.isInstrumentalAt(effect, p):
                return True
        return False
        
    def treatsAsEnd(self, p):
        for e in self.affects[p]["neg"]:
            if self.plan.isSatisfied(e, self.goal):
                return False
        for e in self.affects[p]["pos"]:
            if self.plan.isSatisfied(e, self.goal):
                return True
        return False
        
    def treatsAsMeans(self, p):
        for e in self.affects[p]["pos"] + self.affects[p]["neg"]:
            if self.isInstrumental(e):
                return True
        return False
        
    def agentivelyCaused(self, effect):
        sn = self.plan.simulate(self.init)
        if not self.plan.isSatisfied(effect, sn):
            return False
        for p in self.plan.getSubPlans():
            sn = self.plan.simulate(self.init, p)
            if not self.plan.isSatisfied(effect, sn):
                return True
        return False
        
    def evaluate(self, principle):
        if principle == Utilitarianism:
            return principle().permissible(self, self.alternatives)
        return principle().permissible(self)
        

class Plan:
    """
    Assumes a plan that successfully reaches its goal.
    """
    def __init__(self, endoPlan, exoActions, goal):
        self.plan = endoPlan
        self.exoActions = exoActions
        self.goal = goal
        
    def __str__(self):
        s = "["
        for a in self.plan:
            s += str(a) + ","
        return s+"]"
         
    """
    param init: The initial State
    param skip: A list of bits representing for each endogeneous action in the plan whether or not to execute it.
    param blockEffect: An effect to counterfactually not been added to a successor state at actions specified in blockPositions.
    param blockPositions: Positions in the plan where the blockEffect should be blocked (given as a list of bits, one for each endogeneous action in the plan).
    """
    def simulate(self, init, skip = None, blockEffect = None, blockPositions = None):
        init = init.copy()
        if skip == None:
            skip = [0]*len(self.plan)
        if blockEffect == None:
            blockEffect = {}
        if blockPositions == None:
            blockPositions = [0] * len(self.plan)
        cur = init
        for t in range(len(self.plan)):
            if not skip[t]:
                if blockPositions[t] == 1:
                    cur = self.execute(self.plan[t], cur, blockEffect)
                else:
                    cur = self.execute(self.plan[t], cur)
            for e in self.exoActions:
                if t in e.times:
                    cur = self.execute(e, cur)
        if self.latestExo() >= len(self.plan):
            for t in range(len(self.plan), self.latestExo()+1):        
                for e in self.exoActions:
                    if t in e.times:
                        cur = self.execute(e, cur)
        return cur
    
    def execute(self, action, state, blockEffect = None):
        if blockEffect == None:
            blockEffect = {}
        if self.isApplicable(action, state):
            return self.apply(action, state, blockEffect)
        return state
            
    def isApplicable(self, action, state):
        return self.isSatisfied(action.pre, state)
        
    def apply(self, action, state, blockEffect = None):
        if blockEffect == None:
            blockEffect = {}
        si = copy.deepcopy(state)
        for condeff in action.eff:
            if self.isSatisfied(condeff["condition"], si):
                for v in condeff["effect"].keys():
                    if not v in blockEffect or blockEffect[v] != condeff["effect"][v]:    
                        state[v] = condeff["effect"][v]
        return state
    
    def isSatisfied(self, cond, state):
        for k in cond.keys():
            if k not in state or cond[k] != state[k]:
                return False
        return True
        
    def satisfiesGoal(self, state):
        return self.isSatisfied(self.goal, state)
        
    def latestExo(self):
        m = 0
        for e in self.exoActions:
            if max(e.times) > m:
                m = max(e.times)
        return m
        
    def getSubPlans(self, n = None):       
        if n == None:
            n = len(self.plan)
        return itertools.product([0, 1], repeat=n)
        

    
class Deontology:
    def permissible(self, situation):
        for a in situation.plan.plan:
            if a.intrinsicvalue == "bad":
                return False
        return True

class DoNoHarm:
    def permissible(self, situation):
        sn = situation.plan.simulate(situation.init)
        for h in situation.harmful:
            if situation.plan.isSatisfied(h, sn):
                causes = situation.agentivelyCaused(h)
                if causes:
                    return False
        return True

class DoNoInstrumentalHarm:
    def permissible(self, situation):
        for h in situation.harmful:
            if situation.isInstrumental(h):
                return False
        return True

class KantianHumanity:
    def permissible(self, situation):
        for p in situation.affects.keys():
            if situation.treatsAsMeans(p) and not situation.treatsAsEnd(p):
                return False
        return True

class Utilitarianism:
    def permissible(self, situation, alternatives):
        u = situation.getFinalUtility()
        for a in alternatives:
            if a.getFinalUtility() > u:
                return False, u
        return True
        
class DoubleEffectPrinciple:
    def permissible(self, situation):
        # Deontology
        if not Deontology().permissible(situation):
            return False, "deon"
        # No bad goals, one good one
        foundgood = False
        for k,v in situation.goal.items():
            if situation.getUtility({k:v}) < 0:
                return False, "bad goal"
            if situation.getUtility({k:v}) > 0:
                foundgood = True
        if not foundgood:
            return False
        # No bad means
        if not DoNoInstrumentalHarm().permissible(situation):
            return False
        # All in all positive
        return situation.getFinalUtility() > 0

