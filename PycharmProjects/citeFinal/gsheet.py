import pandas as pd
import pygsheets


def get_data():
    gc = pygsheets.authorize(service_file='citation-400707-a260f9c710db.json')
    spreadsheet = gc.open('ref-data')
    worksheet = spreadsheet.sheet1
    all_values = worksheet.get_all_values()
    new_value = []
    new_pos = 0
    for i in range(len(all_values)):
        if all_values[i][0] != '':
            new_value.append(all_values[i][0:4])
        else:
            new_pos = i
            break
    try:
        df = pd.DataFrame(new_value[1:], columns=new_value[0][0:4])
    except IndexError:
        df = pd.DataFrame(columns=['Reference', 'BibTex', 'EndNote', 'RefMan'])
        worksheet.set_dataframe(df, start='A1')
    return [df, worksheet, new_pos]
