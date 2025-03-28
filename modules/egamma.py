import json
import pandas as pd
import numpy as np
import correctionlib

def parse_electron_sf(filename, correction_name, campaign):
    scale_factors = []
    with open(filename, "r") as f: json_data = json.load(f)

    pt_edges = None
    eta_edges = None
    phi_edges = None

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

    era_key = {
        '2016postVFP_UL':'2016postVFP',
        '2016preVFP_UL':'2016preVFP',
        '2017_UL':'2017',
        '2018_UL':'2018',
        'Run3Summer22':'2022Re-recoBCD',
        'Run3Summer22EE':'2022Re-recoE+PromptFG',
        'Run3Summer23':'2023PromptC',
        'Run3Summer23BPix':'2023PromptD'
    }

    for item in json_data['corrections']:
        #Each item is a dict
        if item['name'] != correction_name: continue
        
        content = item['data']['content']
        for obj in content:
            ### campaign name
            if obj['key'] not in corr_key[campaign]: continue
            #print('Extracting data for: '+obj['key'])
            
            subcontent = obj['value']['content']
            for subobj in subcontent:
                ### sf type
                if subobj['key'] != 'sf':continue
                #print('Extracting data for:'+subobj['key'])

                subsubcontent = subobj['value']['content']
                for subsubobj in subsubcontent:
                    ### Working point
                    if subsubobj['key'] != 'Medium': continue
                    #print('Extracting data for '+subsubobj['key']+' WP')

                    edges = subsubobj['value']['edges']
                    eta_edges = edges[0]
                    pt_edges  = edges[1]
                    if '23' in campaign: phi_edges = edges[2]
                    else: phi_edges = [-np.inf, np.inf]
                    
                    #print('Edges extracted!')

    # Now that the binning is calculated,
    #print(pt_edges)
    #print(eta_edges)
    #print(phi_edges)
    correction_set = correctionlib.CorrectionSet.from_file(filename)
    correction = correction_set[correction_name]
    MAX_PT = 1500
    MIN_ETA = -2.5
    MAX_ETA = 2.5
    MIN_PHI = -3.1416
    MAX_PHI = 3.1416
    
    #Given the pt and eta edges, loop over their midvalues.
    for eta_low, eta_high in zip(eta_edges[:-1], eta_edges[1:]):
        for pt_low, pt_high in zip(pt_edges[:-1], pt_edges[1:]):
            for phi_low, phi_high in zip(phi_edges[:-1], phi_edges[1:]):

                if not np.isfinite(eta_low):  eta_low  = MIN_ETA if eta_low  == -np.inf else MAX_ETA
                if not np.isfinite(eta_high): eta_high = MIN_ETA if eta_high == -np.inf else MAX_ETA
                if not np.isfinite(pt_low):   pt_low   = MAX_PT  if pt_low   == np.inf else 0
                if not np.isfinite(pt_high):  pt_high  = MAX_PT  if pt_high  == np.inf else 0
                if not np.isfinite(phi_low):  phi_low  = MIN_PHI if phi_low  == -np.inf else MAX_PHI
                if not np.isfinite(phi_high): phi_high = MIN_PHI if phi_high == -np.inf else MAX_PHI

                eta = (eta_low + eta_high) / 2
                pt  = (pt_low  + pt_high) / 2
                phi = (phi_low + phi_high) / 2
                #era = campaign.replace('_UL', '')
                era = era_key[campaign]
                wp = "Medium"

                values = [era, 'sf', wp, eta, pt]
                values_down = [era, 'sfdown', wp, eta, pt]
                values_up = [era, 'sfup', wp, eta, pt]
                if '23' in campaign:
                    values.append(phi)
                    values_down.append(phi)
                    values_up.append(phi)

                sfdown = correction.evaluate(*values_down)
                sf = correction.evaluate(*values)
                sfup = correction.evaluate(*values_up)
                
                scale_factors.append({
                    'campaign': campaign,
                    'eta_low' : eta_low,
                    'eta_high': eta_high, 
                    'pt_low'  : pt_low,
                    'pt_high' : pt_high,
                    'phi_low' : phi_low,
                    'phi_high': phi_high,
                    'sfdown'  : sfdown,
                    'sf'      : sf,
                    'sfup'    : sfup
                })

                #print(f"Scale factor: {sf}, sfdown: {sfdown}, sfup: {sfup}")
                #break ### phibin
            #break ### ptbin
        #break ### etabin
    #print(f"SF calculated for campaign = {campaign}")
        
    df = pd.DataFrame(scale_factors)
    return df
