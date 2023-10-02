import pandas as pd

def toexcelandcsv(dataframe):
    df = pd.DataFrame(dataframe, columns = ['Title', 'Link', 'Day', 'Time', 'Where', 'ImageName'])

    # Convert the dataframe to excel file
    df.to_excel('Washingtonian.xlsx', index=False)
    df.to_csv('Washingtonian.csv', index=False)

    print("Data Scrapped")


