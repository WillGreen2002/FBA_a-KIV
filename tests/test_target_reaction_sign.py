from cobra import Model, Reaction, Metabolite

def test_exchange_sign_convention_uptake_is_negative_lb():
    m=Model('m')
    met=Metabolite('lac__L_e', compartment='e')
    ex=Reaction('EX_lac__L_e'); ex.add_metabolites({met:-1}); ex.lower_bound=-10; ex.upper_bound=1000
    m.add_reactions([ex])
    assert m.reactions.EX_lac__L_e.lower_bound < 0
