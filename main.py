
# %%
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from enum import Enum

class Type(Enum):
    response = '========== Response  =========='
    request = '========== Request =========='

pd.set_option('display.max_rows', 1000); pd.set_option('display.max_columns', 1000); pd.set_option('display.width', 1000)

# %%
with open('file1.txt') as file:
    print("here1")

    df = pd.DataFrame()
    lines = file.readlines()
    # print(lines)
    for i in range(0, len(lines)):
        # print(line)
        line = lines[i]
        # print(line)
        if line.startswith('='):
            if str(line).strip('= ').startswith('Request'):
                # print("request")
                arr = '{"Type": "Request"'
            if str(line).strip('= ').startswith('Response'):
                # print("response")
                arr = '{"Type": "Response"'

            while lines[i+1] != '\n' and not(lines[i+1].strip() == ''):
                i = i+1
                line = lines[i].strip('\n')
                split = str(line).split(": ")
                # print(split)
                try:
                    arr += ', "' + split[0] + '":"' + split[1] + '"'
                except:
                    print("ERROR" + str(split))
                    split = str(line).split(':\t')
                    arr += ', "' + split[0] + '":"' + split[1] + '"'
            arr += '}'
            # print(arr)
            arr = json.loads(arr)
            dfnew = pd.DataFrame.from_dict(arr, orient="index")
            # dfnew = pd.pivot_table(dfnew)
            dfnew = dfnew.T
            # print("here")
            # print(dfnew)
            df = pd.concat([df, dfnew])
            # print("here2")
            # print(df)





    # print(df)
    dfrequest = df.loc[df['Type'] == 'Request']
    dfrequest['Endpoint'] = dfrequest['Endpoint'].apply(lambda x: x[5:] if x.startswith("(OWL) ") else x)
    dfrequest['Controller'] = dfrequest['Controller'].apply(lambda x: x.strip())
    dfresponse = df.loc[df['Type'] == 'Response']
    dfresponse['Endpoint'] = dfresponse['Endpoint'].apply(lambda x: x.split("(OWL) ")[1] if x.strip(" ").startswith("(") else x)
    dfresponse['Controller'] = dfresponse['Controller'].apply(lambda x: x.strip())

    dfmerged = dfrequest.merge(dfresponse, left_on=["Controller", "Endpoint"], right_on=["Controller", "Endpoint"])
    dfmerged = dfmerged.dropna(axis='columns')
    dfmerged.columns = dfmerged.columns.to_series().apply(lambda x: x.split("_")[0])

    # print(dfmerged['Controller', 'Endpoint', 'Type_x'])
    # print(dfmerged)
    print(dfmerged[['Username', 'Address', 'Red Meat', 'Grains', 'Dairy', 'Cellphone', 'TV', 'Computer', 'Car', 'Walking', 'Public Transport']])

# NEW PART!!
# Function to convert to kg
def convertKg(weight):
    return round(float(weight.split()[0]) * 0.453592, 2)

# Change columns by using the conversion function
dfmerged["Red Meat"] = dfmerged["Red Meat"].apply(convertKg)
dfmerged["Grains"] = dfmerged["Grains"].apply(convertKg)
dfmerged["Dairy"] = dfmerged["Dairy"].apply(convertKg)

# Remove the word hours from data
dfmerged = dfmerged.replace(to_replace = " hours", value = "", regex = True)
dfmerged = dfmerged.replace(to_replace = " hour", value = "", regex = True)


print(dfmerged)

# Convert values to float
dfmerged[['Red Meat','Grains','Dairy','Cellphone','TV','Computer','Car','Walking','Public Transport']] = dfmerged[['Red Meat','Grains','Dairy','Cellphone','TV','Computer','Car','Walking','Public Transport']].astype(float)

# %%

fig, ax = plt.subplots()

ax.bar(dfmerged['Username'], dfmerged['Red Meat'], label='Red Meat')
ax.bar(dfmerged['Username'], dfmerged['Grains'], label='Grains')
ax.bar(dfmerged['Username'], dfmerged['Dairy'], label='Dairy')
ax.bar(dfmerged['Username'], dfmerged['Cellphone'], label='Cellphone')
ax.bar(dfmerged['Username'], dfmerged['TV'], label='TV')
ax.bar(dfmerged['Username'], dfmerged['Computer'], label='Computer')
ax.bar(dfmerged['Username'], dfmerged['Car'], label='Car')
ax.bar(dfmerged['Username'], dfmerged['Walking'], label='Walking')
ax.bar(dfmerged['Username'], dfmerged['Public Transport'], label='Public Transport')

ax.set_ylabel('Amount of CO2')
ax.set_title('CO2 by Director')
ax.legend()

plt.xticks(rotation=80)
#plt.ylim(0, 500)

plt.show()
