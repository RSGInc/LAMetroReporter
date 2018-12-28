import os
import sys

from io import StringIO

import numpy as np
import pandas as pd
import xlsxwriter
import yaml

from io import StringIO


project_list = [3797, 3765, 3766,
            3767, 3768, 3789, 
            3769, 3770, 3771,
            3772, 3773,	3774,
            3775, 3776, 3790,
            3791, 3792, 3777, 
            3778, 3779, 3780,
            3781, 3793, 3782,
            3783, 3784, 3794, 
            3785, 3786, 3787,
            3795, 3796, 3659]


def _parse_parameters(yaml_cfg):
    with open(yaml_cfg, 'r') as stream:
        yml = yaml.load(stream)
    
    return yml


def parse_table(result_file_path, table_label, yaml_cfg='metro_config.yml'):
    parse_parameters = _parse_parameters(yaml_cfg)[table_label]
    
    start_table_tag = parse_parameters['start_table_tag']
    
    parse_end_tag = False
    if 'end_table_tag_exp' in parse_parameters:
        parse_end_tag = parse_parameters['end_table_tag_exp']
    
    if parse_end_tag:
        end_table_tag = eval(parse_parameters['end_table_tag'].encode('UTF-8').decode('unicode_escape'))
    else:
        end_table_tag = parse_parameters['end_table_tag'].encode('UTF-8').decode('unicode_escape')

    skip_rows = parse_parameters['skip_rows']

    found_table = False
    table = StringIO('')

    with open(result_file_path, 'r') as result_file:
        for line in result_file:
            if start_table_tag in line:
                found_table = True
            
            if found_table:
                if line.startswith(end_table_tag):
                    found_table = False
                else:
                    table.write(line)

    table.seek(0)

    widths = parse_parameters['widths'] if ('widths' in parse_parameters) else None

    df = pd.read_fwf(table, widths=widths, skiprows=skip_rows)

    if 'df_drop_top_rows' in parse_parameters:
        df = df[parse_parameters['df_drop_top_rows']:]

    if 'df_drop_tail_rows' in parse_parameters:
        df = df[:-parse_parameters['df_drop_tail_rows']]

    if 'reset_header' in parse_parameters and parse_parameters['reset_header']:
        columns = df.columns
        df.columns = np.arange(len(columns))

    if 'rename_columns' in parse_parameters:
        df = df.rename(columns=parse_parameters['rename_columns'])

    if 'convert_numerics' in parse_parameters and parse_parameters['convert_numerics']:
        df = df.apply(pd.to_numeric)

    if 'int_columns' in parse_parameters:
        df[parse_parameters['int_columns']] = df[parse_parameters['int_columns']].astype(np.int64)

    if 'index_col' in parse_parameters:
        df = df.set_index(parse_parameters['index_col'])

    return df.copy()


def get_tod_purpose_table(dir, scenario, table):
    dfs = []
    for tod in ['pk', 'op']:
        for purp in ['hbo', 'hbu', 'hbw', 'nhb']:
            df = parse_table(os.path.join(dir, '{}_{}_{}.rpt'.format(scenario,tod, purp)),
                             table)
            df['tod'] = tod
            df['purp'] = purp
            dfs.append(df)
    
    return pd.concat(dfs)
    
def get_mode_choice_report(dir, scenario):
    return get_tod_purpose_table(dir, scenario, 'mode_summary')
    
def summarize_mode_choice(dir, scenario):
    df = get_mode_choice_report(dir, scenario)
    df = df[['sov','hov2','hov3','hov4', 'transit', 'non_motor']].sum()
    df['total'] = df.sum()
    return df


def get_brt_access(dir, scenario):
    return get_tod_purpose_table(dir, scenario, 'brt_access')
    
    
def summarize_brt_access(dir, scenario):
    cols = 'walk', 'bike', 'bus', 'pnr', 'knr', 'total'
    brt_access = get_brt_access(dir, scenario)
    return brt_access.reset_index().groupby(['psuedo_zone', 'station_name'])[cols].sum()

    
def get_brt_egress(dir, scenario):
    return get_tod_purpose_table(dir, scenario, 'brt_egress')

    
def summarize_brt_egress(dir, scenario):
    cols = 'walk', 'bike', 'bus', 'drive', 'total'
    brt_egress = get_brt_egress(dir, scenario)
    return brt_egress.reset_index().groupby(['psuedo_zone', 'station_name'])[cols].sum()
    

def get_transfers(dir, scenario):
    return get_tod_purpose_table(dir, scenario, 'xfer_summary')

    
def summarize_transfers(dir, scenario):
    xfers = get_transfers(dir, scenario)
    return xfers.reset_index().groupby(['from_station', 'from_station_name', 
                                        'to_station', 'to_station_name']).sum().reset_index()
    

def create_project_summary(dir, scenario, output_file):
    print(os.path.join(dir, output_file))
    writer = pd.ExcelWriter(os.path.join(dir, output_file), engine='xlsxwriter')

    access = get_brt_access(dir, scenario).reset_index()
    egress = get_brt_egress(dir, scenario).reset_index()
    xfers = get_transfers(dir, scenario).reset_index(drop=True)
    
    egress = egress.rename(columns={'drive': 'knr'})
    
    for zone in project_list:
        station = pd.concat([access[access['psuedo_zone'] == zone],
                             egress[egress['psuedo_zone'] == zone]], sort=True)
        station = station.groupby(['psuedo_zone', 'station_name', 'tod', 'purp']).sum().astype(np.int64)
        
                             
        from_xfers = xfers[xfers['from_station'] == zone]
        from_xfers = from_xfers.groupby(['from_station', 'from_station_name', 'tod', 'purp'])['trips'].sum()
        from_xfers = from_xfers.reset_index().rename(columns={'from_station': 'psuedo_zone', 'from_station_name': 'station_name'})
        
        to_xfers = xfers[xfers['to_station'] == zone]
        to_xfers = to_xfers.groupby(['to_station', 'to_station_name', 'tod', 'purp'])['trips'].sum()
        to_xfers = to_xfers.reset_index().rename(columns={'to_station': 'psuedo_zone', 'to_station_name': 'station_name'})
        
        station_xfers = pd.concat([from_xfers, to_xfers], sort=True)
        station_xfers = station_xfers.groupby(['psuedo_zone', 'station_name', 'tod', 'purp'])[['trips']].sum()
        station_xfers = station_xfers.rename(columns={'trips': 'xfers'})
        
        if station_xfers.empty:
            station['xfers'] = 0
        else:
            join_cols = ['psuedo_zone', 'station_name', 'tod', 'purp']
            station = pd.merge(station.reset_index(), station_xfers.reset_index(), on=join_cols, how='outer')
            station.set_index(join_cols)
        
        station = station.reset_index()
        station[['walk', 'bike', 'bus', 'pnr', 'knr']] = station[['walk', 'bike', 'bus', 'pnr', 'knr']] / 2
        station['total'] = station[['walk',	'bike', 'bus', 'pnr', 'knr']].sum(axis=1)
        station = station.set_index(['psuedo_zone', 'station_name', 'tod', 'purp'])
        station = np.round(station, 0).astype(int)

        if not station.empty:
            sheet_title = station.index.get_level_values('station_name')[0]
            sheet_title = sheet_title.replace('/', '-')[:15]
            
            station[['walk', 'bike', 'bus', 'pnr', 'knr', 'total', 'xfers']].to_excel(writer,
                                                                    sheet_name=sheet_title)

    writer.save()
    writer.close()
    
    
if __name__ == '__main__':
    dir = sys.argv[1]
    scenario = sys.argv[2]
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    
    #create_project_summary(dir, scenario, output_file)
    print(get_mode_choice_report(dir, scenario))
    #print(summarize_mode_choice(dir, scenario))