import json
import pandas as pd
import numpy as np
import correctionlib

def parse_muon_sf(filename, correction_name, campaign):
    scale_factors=[]
    with open(filename, "r") as f: json_data = json.load(f)

    pt_edges = None
    eta_edges = None

    corr_key = {
        '2016postVFP_UL':'2016postVFP_UL',
        '2016preVFP_UL':'2016preVFP_UL',
        '2017_UL':'2017_UL',
        '2018_UL':'2018_UL',
        'Run3Summer22':'2022Re-recoBCD',
        'Run3Summer22EE':'2022Re-recoE+PromptFG',
        'Run3Summer23':'2023PromptC',
        'Run3Summer23BPix':'2023PromptD'
    }

    for item in json_data['corrections']:
        if 'Run3' in campaign: continue
        
        #Each item is a dict
        if item['name'] != correction_name: continue

        content = item['data']['content']
        for obj in content:
            
            ### eta bins
            if obj['key'] not in corr_key[campaign]: continue
            #print('Extracting data for: '+obj['key'])
            eta_edges = obj['value']['edges']
            subcontent = obj['value']['content']
            for subobj in subcontent:
                ### pt bins
                pt_edges = subobj['edges']
                #print('Edges extracted!')
                break ### found pt endges

    # Now that the binning is calculated,
    if 'Run3' in campaign:
        pt_edges  = [15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0, np.inf]
        eta_edges = [0.0, 0.9, 1.2, 2.1, 2.4]
        
    #print(pt_edges)
    #print(eta_edges)
    
    correction_set = correctionlib.CorrectionSet.from_file(filename)
    correction = correction_set[correction_name]
    MAX_PT = 1500
    MIN_ETA = 0
    MAX_ETA = 2.5
    
    #Given the pt and eta edges, loop over their midvalues.
    for eta_low, eta_high in zip(eta_edges[:-1], eta_edges[1:]):
        for pt_low, pt_high in zip(pt_edges[:-1], pt_edges[1:]):
            if not np.isfinite(pt_high):   pt_high = MAX_PT if pt_high == np.inf else 0

            eta = (eta_low + eta_high) / 2
            pt  = (pt_low  + pt_high) / 2
            era = campaign

            values = [era, eta, pt, 'sf']
            values_down = [era, eta, pt, 'systdown']
            values_up = [era, eta, pt, 'systup']
            if 'Run3' in campaign:
                values = values[1:]
                values_down = values_down[1:]
                values_up = values_up[1:]
                values[-1] = 'nominal'
            
            sfdown = correction.evaluate(*values_down)
            sf = correction.evaluate(*values)
            sfup = correction.evaluate(*values_up)
            
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
                
    df = pd.DataFrame(scale_factors)
    return df
