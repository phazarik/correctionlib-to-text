import json
import pandas as pd
import numpy as np
import correctionlib

def parse_jet_jec_sf(filename, correction_name, campaign):
    scale_factors=[]
    with open(filename, "r") as f: json_data = json.load(f)

    pt_edges = None
    eta_edges = None
    
    match_found = False
    for item in json_data['corrections']:
        if item['name'] != correction_name: continue
        match_found = True
            
        #print(item['data'].keys())
        #print(item['data']['input'])
        #print(item['data']['edges'])
        eta_edges = item['data']['edges']
        content = item['data']['content']
        for obj in content:
            #print(obj.keys())
            #print(obj['input'])
            #print(obj['edges'])
            pt_edges = obj['edges']
            #print('Edges extracted!')
            break

    if not match_found: warning(f'Not found: {correction_name}')
    if eta_edges ==None or pt_edges == None: return pd.DataFrame([])
    #print(f'JEC pT edges = {pt_edges}')
    #print(f'JEC eta edges = {eta_edges}')

    # Now that the binning is calculated,
    correction_set = correctionlib.CorrectionSet.from_file(filename)
    correction = correction_set[correction_name]
    
    #Given the pt and eta edges, loop over their midvalues.
    for eta_low, eta_high in zip(eta_edges[:-1], eta_edges[1:]):
        for pt_low, pt_high in zip(pt_edges[:-1], pt_edges[1:]):
            
            eta = (eta_low + eta_high) / 2
            pt  = (pt_low  + pt_high) / 2
            values = [eta, pt]
            unc = correction.evaluate(*values)
            sf = np.ones_like(unc)
            
            scale_factors.append({
                'campaign': campaign,
                'eta_low' : eta_low,
                'eta_high': eta_high, 
                'pt_low'  : pt_low,
                'pt_high' : pt_high,
                'sfdown'  : sf-unc,
                'sf'      : sf,
                'sfup'    : sf+unc
            })

    df = pd.DataFrame(scale_factors)
    return df

def parse_jet_jer_sf(filename, correction_name, campaign):

    scale_factors=[]
    with open(filename, "r") as f: json_data = json.load(f)

    pt_edges = [0, np.inf]
    eta_edges = None

    match_found = False
    for item in json_data['corrections']:
        if item['name'] != correction_name: continue
        match_found = True

        #print(item['data'].keys())
        #print(item['data']['input'])
        #print(item['data']['edges'])
        eta_edges = item['data']['edges']

        if 'Run3' in campaign:
            content = item['data']['content']
            for obj in content:
                pt_edges = obj['edges']
        #print('Edges extracted!')

    if not match_found: warning(f'Not found: {correction_name}')
    #if eta_edges ==None or pt_edges == None: return pd.DataFrame([])
    #print(f'JER eta edges = {eta_edges}')
    #print(f'JER pt edges = {pt_edges}')
    
    correction_set = correctionlib.CorrectionSet.from_file(filename)
    correction = correction_set[correction_name]
    MAX_PT = 4000

    for eta_low, eta_high in zip(eta_edges[:-1], eta_edges[1:]):
        eta = (eta_low + eta_high) / 2

        if 'Run3' in campaign:
            for pt_low, pt_high in zip(pt_edges[:-1], pt_edges[1:]):
                if not np.isfinite(pt_low):   pt_low   = MAX_PT  if pt_low   == np.inf else 0
                if not np.isfinite(pt_high):  pt_high  = MAX_PT  if pt_high  == np.inf else 0

                pt = (pt_low + pt_high) / 2
                values_nom  = [eta, pt, 'nom']
                values_up   = [eta, pt, 'up']
                values_down = [eta, pt, 'down']
            
                sf     = correction.evaluate(*values_nom)
                sfup   = correction.evaluate(*values_up)
                sfdown = correction.evaluate(*values_down)
        
                scale_factors.append({
                    'campaign': campaign,
                    'eta_low' : eta_low,
                    'eta_high': eta_high,
                    'pt_low'  : pt_low,
                    'pt_high' : pt_high,
                    'sfdown'  : sfdown,
                    'sf'      : sf,
                    'sfup'    : sfup
                })

        else:
            values_nom  = [eta, 'nom']
            values_up   = [eta, 'up']
            values_down = [eta, 'down']
            
            sf     = correction.evaluate(*values_nom)
            sfup   = correction.evaluate(*values_up)
            sfdown = correction.evaluate(*values_down)
        
            scale_factors.append({
                'campaign': campaign,
                'eta_low' : eta_low,
                'eta_high': eta_high,
                'pt_low'  : 0,
                'pt_high' : np.inf,
                'sfdown'  : sfdown,
                'sf'      : sf,
                'sfup'    : sfup
            })
            
        
    df = pd.DataFrame(scale_factors)
    return df


def parse_jet_ptres_sf(filename, correction_name, campaign):

    scale_factors=[]
    with open(filename, "r") as f: json_data = json.load(f)

    # This is a function based correction. So pT ednges are not available.
    # In order to write in the text file, I pciked the same pT edges as in JEC and JER
    pt_edges = [9.0, 11.0, 13.5, 16.5, 19.5, 22.5, 26.0, 30.0, 34.5, 40.0,
                46.0, 52.5, 60.0, 69.0, 79.0, 90.5, 105.5, 123.5, 143.0,
                163.5, 185.0, 208.0, 232.5, 258.5, 286.0, 331.0, 396.0,
                468.5, 549.5, 639.0, 738.0, 847.5, 968.5, 1102.0, 1249.5,
                1412.0, 1590.5, 1787.0, 2003.0, 2241.0, 2503.0, 2790.5, 3107.0,
                3455.0, 3837.0, 4257.0, 4719.0, 5226.5, 5784.0, 6538.0]

    # Since rho is an integer, I am goign with integer values.
    rho_edges = np.arange(91)
    eta_edges = None

    match_found = False
    for item in json_data['corrections']:
        if item['name'] != correction_name: continue
        match_found = True

        eta_edges = item['data']['edges']
        content = item['data']['content']
        for obj in content:
            rho_edges = obj['edges']
            #print('Edges extracted!')
            break

    #print(f'pT-res eta edges = {eta_edges}')
    #print(f'pT-res rho edges = {rho_edges}')

    if not match_found: warning(f'Not found: {correction_name}')

    # Now that the binning is calculated,
    correction_set = correctionlib.CorrectionSet.from_file(filename)
    correction = correction_set[correction_name]
    
    #Given the pt and eta edges, loop over their midvalues.
    for eta_low, eta_high in zip(eta_edges[:-1], eta_edges[1:]):
        for pt_low, pt_high in zip(pt_edges[:-1], pt_edges[1:]):
            for rho_low, rho_high in zip(rho_edges[:-1], rho_edges[1:]):
            
                eta = (eta_low + eta_high) / 2
                pt  = (pt_low  + pt_high) / 2
                rho  = (rho_low  + rho_high) / 2
                values = [eta, pt, rho]
                sf = correction.evaluate(*values)
                
                scale_factors.append({
                    'campaign': campaign,
                    'eta_low' : eta_low,
                    'eta_high': eta_high, 
                    'pt_low'  : pt_low,
                    'pt_high' : pt_high,
                    'rho_low'  : rho_low,
                    'rho_high' : rho_high,
                    'sf'      : sf,
                })
    
    df = pd.DataFrame(scale_factors)
    return df
