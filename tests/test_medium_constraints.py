from src.medium_builder import set_oxygen_bound
from cobra import Model, Reaction, Metabolite

def test_set_oxygen_bound():
    m=Model('m')
    o2=Metabolite('o2_e', compartment='e')
    ex=Reaction('EX_o2_e'); ex.lower_bound=-20; ex.upper_bound=1000; ex.add_metabolites({o2:-1})
    m.add_reactions([ex])
    set_oxygen_bound(m,-5)
    assert m.reactions.EX_o2_e.lower_bound == -5
