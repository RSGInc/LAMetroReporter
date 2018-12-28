import os
import sys

import pandas as pd

routes = {
    204: {'mode': 11, 'lines': [145, 610]},
    754: {'mode': 24, 'lines': [61, 62]},
    757: {'mode': 24, 'lines': [67,68]},
    720: {'mode': 24, 'lines': [69,70]},
    901: {'mode': 26, 'lines': [1,2,3]},
    910: {'mode': 25, 'lines': [13,14]},
    911: {'mode': 26, 'lines': [11,12]}, #Vermont BRT
    915: {'mode': 26, 'lines': [14,15]}, #Noho
    850: {'mode': 13, 'lines': [50]}
}

def line_ridership_totals(cwd, scenario):

    am = pd.read_csv(os.path.join(cwd, scenario, 'am', 'stops_summary.csv'))
    md = pd.read_csv(os.path.join(cwd, scenario, 'md', 'stops_summary.csv'))

    stops = pd.concat([am, md])


    for k,v in routes.items():
        route = stops[(stops['mode'] == v['mode']) & (stops['line'].isin(v['lines']))]

        route = route.groupby(['node', 'dir'])[['seq', 'on', 'off']].agg({'seq':'min', 'on':'sum', 'off': 'sum'})

        route['boardings'] = (route['on'] + route['off']) / 2.0
    
        print('Line {}: {:,.0f}'.format(k, route[['seq', 'boardings']].sum()['boardings']))
        

def line_station_boardings(cwd, scenario, route_id, route_seq_file='station_node_seq.csv'):

    am = pd.read_csv(os.path.join(cwd, scenario, 'am', 'stops_summary.csv'))
    md = pd.read_csv(os.path.join(cwd, scenario, 'md', 'stops_summary.csv'))

    stops = pd.concat([am, md]) 

    v = routes[route_id]
    route_sequence = pd.read_csv(route_seq_file)
    seq = route_sequence[route_sequence['route'] == route_id]
    
    route = stops[(stops['mode'] == v['mode']) & (stops['line'].isin(v['lines']))]

    route = route.groupby(['node'])[['on', 'off']].agg({'on':'sum', 'off': 'sum'})

    route['boardings'] = (route['on'] + route['off']) / 2.0

    route = pd.merge(route, seq[['node', 'seq']], left_index=True, right_on='node', how='right')
    
    route = route.fillna(0)

    return route.sort_values('seq')[['node', 'seq', 'boardings']]

if __name__ == '__main__':
    cwd = sys.argv[1]
    scenario = sys.argv[2]
    
    line_ridership_totals(cwd, scenario)
    print(line_station_boardings(cwd, scenario, 915))
    
    