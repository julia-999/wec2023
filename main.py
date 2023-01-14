
# %%
import pandas as pd
import json

# %%
with open('file1.txt') as file:
    print("here1")

    df = pd.DataFrame()
    lines = file.readlines()
    # print(lines)
    for i in range(0, len(lines)):
        # print(line)
        line = lines[i]
        print(line)
        if line.startswith('='):
            if str(line).strip('= ').startswith('Request'):
                print("request")
                arr = '{"Type": "Request"'
                while lines[i+1] != '\n':
                    i = i+1
                    line = lines[i].strip('\n')
                    split = str(line).split(": ")
                    # print(split)
                    arr += ', "' + split[0] + '":"' + split[1] + '"'
                arr += '}'
                # print(arr)
                arr = json.loads(arr)
                dfnew = pd.DataFrame.from_dict(arr, orient="index")
                # dfnew = pd.pivot_table(dfnew)
                dfnew = dfnew.T
                print("here")
                print(dfnew)
                df = pd.concat([df, dfnew])
                print("here2")
                print(df)


            if line.strip('= ').startswith('Response'):
                print("response")
    # print(df)


# %%
