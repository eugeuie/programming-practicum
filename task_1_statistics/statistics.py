import json
import os
import pandas as pd

with open('data/inputfilenames.json', 'r') as f:
    inputfilenames = json.loads(f.read())

for inputfilename in inputfilenames:
    inputfile_path = os.path.join('data', inputfilename)
    data = pd.read_csv(inputfile_path, sep='\t', skiprows=2, skipfooter=2, usecols=['EVENT', 'AVGTSMR'], engine='python')

    data_info = data.groupby(by=['EVENT'])['AVGTSMR'].describe(percentiles=[.50, .90, .99, .999])
    outputfile_path = os.path.join('data', 'statfile_' + inputfilename.split('_stats')[0][-2:] + '.txt')
    with open(outputfile_path, 'w+') as f:
        for i in range(data_info.shape[0]):
            row = data_info.iloc[i]
            f.write(' '.join((
                row.name,
                'min={:.0f}'.format(row['min']),
                '50%={:.1f}'.format(row['50%']),
                '90%={:.1f}'.format(row['90%']),
                '99%={:.1f}'.format(row['99%']),
                '99.9%={:.1f}'.format(row['99.9%']),
                '\n'
            )))

    exectime_groups = pd.DataFrame(data[data['AVGTSMR'] % 5 == 0]['AVGTSMR'].sort_values().values).groupby(0).size()
    data_info_table = pd.DataFrame(data={'ExecTime': exectime_groups.index, 'TransNo': exectime_groups.values})
    data_info_table['Weight, %'] = data_info_table['TransNo'] / data.shape[0] * 100
    data_info_table['Percent'] = [data[data['AVGTSMR'] <= exectime]['AVGTSMR'].count() / data.shape[0] * 100 for exectime in data_info_table['ExecTime']]
    outputtable_path = os.path.join('data', 'stattable_' + inputfilename.split('_stats')[0][-2:] + '.html')
    data_info_table.to_html(outputtable_path)
