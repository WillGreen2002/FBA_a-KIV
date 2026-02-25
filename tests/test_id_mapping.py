from src.id_mapper import find_metabolites_by_synonyms
from cobra import Model, Metabolite

def test_find_metabolites_by_synonyms():
    m=Model('x')
    met=Metabolite('3mob_c', name='2-ketoisovalerate', compartment='c')
    m.add_metabolites([met])
    df=find_metabolites_by_synonyms(m,['ketoisovalerate'])
    assert not df.empty
