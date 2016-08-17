#!/usr/bin/env python3

import FalloutSimulator
import logging
import pickle

def clone_and_swap_ammo(weapon,newammo):
    w=weapon.copy()
    w.ammo=newammo.copy()
    w.damage=w.ammo.damage
    return w

def load_catalog(filename=None,debug=False,quiet=False,verbose=False,
                 logger=None):
    with open(filename,"rb") as f:
        catalog = pickle.load(f)
    for k in catalog:
        for kk in catalog[k]:
            catalog[k][kk].debug=debug
            catalog[k][kk].quiet=quiet
            catalog[k][kk].verbose=verbose
            catalog[k][kk].logger=logger
    return catalog


if __name__=="__main__":
    debug=False
    quiet=False
    verbose=False
    lgr=logging.getLogger(name="Deathclaws vs. Mutants")
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)
    
    catalog=load_catalog(filename="catalog.pck",debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)

    
    a=FalloutSimulator.Arena.Arena(name="Mutants vs. Deathclaw",
                                   quiet=quiet,debug=debug,verbose=verbose,
                                   logger=lgr)
    b=FalloutSimulator.Battle.Battle(name="Mutants vs. Deathclaw",arena=a,
                                     quiet=quiet,debug=debug,verbose=verbose,
                                     logger=lgr)

    m1=catalog["creature"]["super mutant overlord"].copy()
    m1.recalc_skills()
    m1.name="Super Mutant Overlord"
    m2=catalog["creature"]["super mutant (ranged)"].copy()
    m2.recalc_skills()
    m2.name="Super Mutant Ranged #1"
    m3=catalog["creature"]["super mutant (ranged)"].copy()
    m3.recalc_skills()    
    m3.name="Super Mutant Ranged #2"
    m4=catalog["creature"]["super mutant (melee)"].copy()
    m4.recalc_skills()    
    m4.name="Super Mutant Melee #1"
    m5=catalog["creature"]["super mutant (melee)"].copy()
    m5.recalc_skills()    
    m5.name="Super Mutant Melee #2"
    
    mf=FalloutSimulator.Faction.Faction(name="mutants")
    m1.factions = [ mf ]
    m2.factions = [ mf ]
    m3.factions = [ mf ]
    m4.factions = [ mf ]
    m5.factions = [ mf ]    

    d1=catalog["creature"]["deathclaw"].copy()
    d1.recalc_skills()
    d1.name="Deathclaw"
    df=FalloutSimulator.Faction.Faction(name="deathclaw")
    d1.factions=[df]
    
    mc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    b.add_actor_at_coords(m1,mc.copy())
    b.add_actor_at_coords(m2,mc.copy())
    m2.coordinates.x=9
    m2.coordinates.y=9
    b.add_actor_at_coords(m3,mc.copy())
    m3.coordinates.x=9
    m3.coordinates.y=11
    b.add_actor_at_coords(m4,mc.copy())
    m4.coordinates.x=11
    m4.coordinates.y=11
    b.add_actor_at_coords(m5,mc.copy())
    m4.coordinates.x=11
    m4.coordinates.y=9

    b.add_actor_at_coords(d1,mc.copy())
    d1.coordinates.x=40
    d1.coordinates.y=40    
    
    b.fight()

    print("Victors:")
    for x in b.get_actors():
        print(x)
