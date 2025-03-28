import json
import pandas as pd
import correctionlib

def parse_pileup_wt(filename, campaign):

    ### print(f'Calculating pileup weight from {filename} for {campaign}')
    
    scale_factors = []
    with open(filename, "r") as f: json_data = json.load(f)

    nint_values = None
    correction_name = None

    for item in json_data['corrections']:
        correction_name = item['name']
        content = item['data']['content']
        for obj in content:
            nint_values = obj['value']['edges']
            break

    correction_set = correctionlib.CorrectionSet.from_file(filename)
    correction = correction_set[correction_name]

    for nint in nint_values:
        values = [nint, 'nominal']
        values_up = [nint, 'up']
        values_down = [nint, 'down']
        sf = correction.evaluate(*values)
        sfup = correction.evaluate(*values_up)
        sfdown = correction.evaluate(*values_down)

        scale_factors.append({
            'campaign': campaign,
            'nint': int(nint),
            'sfdown': round(sfdown, 6),
            'sf': round(sf, 6),
            'sfup': round(sfup, 6)
        })

    df = pd.DataFrame(scale_factors)
    return df
