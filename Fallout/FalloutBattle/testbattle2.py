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
    for k in catalog["ammo"]:
        dd=catalog["ammo"][k].damage
        dd.debug=debug
        dd.quiet=quiet
        dd.verbose=verbose
        dd.logger=logger
        for dt in [ dd.physical, dd.burn, dd.radiation, dd.poison ]:
            if dt:
                dt.debug=debug
                dt.quiet=quiet
                dt.verbose=verbose
                dt.logger=logger
                for dx in dt.dice:
                    dx.debug=debug
                    dx.quiet=quiet
                    dx.verbose=verbose
                    dx.logger=logger

    return catalog


if __name__=="__main__":
    debug=False
    quiet=False
    verbose=False
    name="Boomer vs. Deathclaw"
    lgr=logging.getLogger(name=name)
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)
    
    catalog=load_catalog(filename="catalog.pck",debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)

    
    a=FalloutSimulator.Arena.Arena(name=name,
                                   quiet=quiet,debug=debug,verbose=verbose,
                                   logger=lgr)
    b=FalloutSimulator.Battle.Battle(name=name,arena=a,
                                     quiet=quiet,debug=debug,verbose=verbose,
                                     logger=lgr)

    r1=catalog["creature"]["raider boomer"].copy()
    r1.recalc_skills()
    r1.name="Raider Boomer"
    r1f=FalloutSimulator.Faction.Faction(name="Raider")
    r1.factions = [ r1f ]
    r1.skills.big_guns=80

    d1=catalog["creature"]["deathclaw"].copy()
    d1.recalc_skills()
    d1.name="Deathclaw"
    df=FalloutSimulator.Faction.Faction(name="deathclaw")
    d1.factions=[df]
    rc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    b.add_actor_at_coords(r1,rc.copy())
    b.add_actor_at_coords(d1,rc.copy())
    d1.coordinates.x=40
    d1.coordinates.y=40

    victors=b.fight()
    print("Victors:")
    for x in victors:
        print(x)
