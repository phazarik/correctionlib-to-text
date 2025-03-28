import json
import pandas as pd
import numpy as np
import correctionlib

def parse_bjet_eff(filename, correction_name, campaign):

    scale_factors=[]
    with open(filename, "r") as f: json_data = json.load(f)

    pt_edges  = [20.0, 30.0, 50.0, 70.0, 100.0, 140.0, 200.0, 300.0, 600.0, 1000.0] #Taken from the input file
    eta_edges = [0.0, 0.8, 1.6, 2.5] #Taken from the input file
    flavors = [0, 5, 4]

    correction_set = correctionlib.CorrectionSet.from_file(filename)
    for flav in flavors:
        for eta_low, eta_high in zip(eta_edges[:-1], eta_edges[1:]):
            for pt_low, pt_high in zip(pt_edges[:-1], pt_edges[1:]):
                
                eta = (eta_low + eta_high) / 2
                pt  = (pt_low  + pt_high) / 2
                wp = 'M'
                if flav in [4, 5]: correction = correction_set[correction_name] #For b and c jets
                else:
                    if 'Run3' in campaign: correction = correction_set['deepJet_light']
                    else:                  correction = correction_set['deepJet_incl']  #for light jets

                values      = ['central', 'M', flav, eta, pt]
                values_up   = ['up', 'M', flav, eta, pt]
                values_down = ['down', 'M', flav, eta, pt]
                #Options: central, up, up_correlated, up_uncorrelated, down, down_correlated, down_uncorrelated

                sf     = correction.evaluate(*values)
                sfup   = correction.evaluate(*values_up)
                sfdown = correction.evaluate(*values_down)
                
                scale_factors.append({
                    'campaign': campaign,
                    'eta_low' : eta_low,
                    'eta_high': eta_high, 
                    'pt_low'  : pt_low,
                    'pt_high' : pt_high,
                    'flav'    : flav,
                    'sfdown'  : sfdown,
                    'sf'      : sf,
                    'sfup'    : sfup
                })   
    
    df = pd.DataFrame(scale_factors)
    return df
