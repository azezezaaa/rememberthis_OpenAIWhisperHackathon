import pygsheets
import pandas as pd
#authorization


def sendToSheets(keyword, text):

    gc = pygsheets.authorize(service_file='./sheetsKey.json')

    # Create empty dataframe
    df = pd.DataFrame()

    # Create a column
    my_dict={'keyword':[keyword],
	           'text':[text]}
    df = pd.DataFrame(data=my_dict)
    #open the google spreadsheet (where 'Sheet1' is the name of my sheet)
    sh = gc.open('Whisper4Lokal - Saved texts')

    #select the first sheet 
    wks = sh[0]

    #update the first sheet with df, starting at cell. 
    cells = wks.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    if last_row>1:
        wks.set_dataframe(df,(last_row+1,1))
        wks.delete_rows(last_row+1)
    else:
        wks.set_dataframe(df,(1,1))