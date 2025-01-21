from modeles import ModelesPCentre
from data import PCentreData
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionClassique(ModelesPCentre):
    
    #____________________________________Override virtuals methods  to create a p-center model
