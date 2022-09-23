# Unnest Json Data

#### Elias Rodrigues

---

This function was built to allow users to analyse the data from a json file
in a strucured form.

After simplifie the file another json file is generate in \json.

The txt file simplified is stored into /simple_raw_data after unnesting.

---

You will need to send a list of dictionary or a list o list for the function.
The function uses recursion to call it self building a structured data
with pair of key and values.

# Simple Usage:

        import unnest_json as un
        import os
        import json


        if __name__ == '__main__':
            # get json data nested
            with open('test_file_3.json', 'rb') as f:
                # remember this data needs to be a list
                list_data = json.load(f)

            # data = dict_data['SearchResults']
            file_name = f'unnest_pbi_model_model_{un.datetime_str()}.txt'

            # unnest data
            un.unnest(list_data=[list_data], path_key=None,
                   file_name=os.path.join(un.SMP_DIR, file_name))
            print('Please wait, unnesting data...')
            print('File saved in root of the project.')

            # generate unnested json file
            un.un.generate_json(file_name)

            # =============================================================== #
            # generate the final csv file
            with open(os.path.join(un.JSON_DIR, file_name.replace('.txt', '.json')), 'r', encoding='utf-8') as f:
                # generate a list to feed the function below
                d = f.readlines()
            # generate data
            un.generate_csv(column_id='cacheId', list_data=d,
                         file_name=os.path.join(un.DATA_DIR, file_name.replace('.txt', '.csv')))

            # =============================================================== #
            # generate the final csv file
            with open(os.path.join(un.JSON_DIR, file_name.replace('.txt', '.json')), 'r', encoding='utf-8') as f:
                # generate a list to feed the function below
                d = f.readlines()
            # generate data
            un.generate_csv(column_id='cacheId', list_data=d,
                         file_name=os.path.join(un.DATA_DIR, file_name.replace('.txt', '.csv')))
