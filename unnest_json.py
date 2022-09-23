from datetime import datetime
import os
import pandas as pd


BASE_DIR = os.path.abspath(os.path.dirname('__file__'))
SMP_DIR = os.path.join(BASE_DIR, 'simple_raw_data')
JSON_DIR = os.path.join(BASE_DIR, 'json')
DATA_DIR = os.path.join(BASE_DIR, 'dataframe')


def datetime_str():
    '''
        get current datetime without special characters
    '''
    return datetime.now().strftime('%Y%m%d%H%M%S')


def generate_json(file: str) -> None:
    '''
        this function will get a raw txt data and just
        insert a curly brackets into it to allow the
        final file be read as a simple json
    '''
    # open file
    f = open(SMP_DIR + '\\' + file, 'rb')
    data = f.readlines()

    # insert curly brackets at the start
    data.insert(0, b'{\n')
    idx = len(data)

    # insert curly brackets in the end
    data.insert(idx, b'\n}')
    f.close()

    # save new file
    with open(os.path.join(JSON_DIR, file.replace('.txt', '.json')), 'wb') as f:
        f.writelines(data)

    print(f'Json file was saved in {JSON_DIR}.')

def generate_csv(column_id: str, list_data: list, file_name: str) -> None:
    '''
        this function receives a list and split data by column id passed
    '''
    car = {}
    consolidate = []
    char_scape = ["{", "{\n", "\n\n}", "\n}", " ", "\n", "\n\n", "}"]
    for i, valor in enumerate(list_data):
        if valor not in char_scape:
            try:
                k, v = valor.replace(',', '').replace('"', "'").replace('\n', '').split(':')
                if column_id in k and i > 10:
                    car = {}
                    car[k] = v
                    consolidate.append(car)
                else:
                    car[k] = v
                    consolidate.append(car)
            except Exception as e:
                k, v, *_ = valor.split(':')
                car[k] = v
                consolidate.append(car)
    
    df = pd.DataFrame(consolidate)
    df.to_csv(file_name, index=False)
    print(f'File {file_name} saved successeful!')
    print(df.head())


def unnest(list_data: list, path_key=None, file_name=None) -> None:
    '''
        This function will receive a list and iterate over it to get key value 
        pair to unnest the data in json object.
        This function just show the data on the screen for the user analyse 
        the desired data.
        params: list_data -> List containing dict or other list
        path_key: key name to create the column names
    '''
    try:
        for data in list_data:
            for key, value in data.items():
                if isinstance(value, list):
                    unnest(list_data=value, path_key=key, file_name=file_name)

                elif isinstance(value, dict):
                    for k, v in value.items():
                        if isinstance(v, list):
                            unnest(list_data=v,
                                   path_key=f'{key}.{k}', file_name=file_name)
                        elif isinstance(v, dict):
                            for under_k, under_v in v.items():
                                with open(file_name, 'a', encoding='utf-8') as f:
                                    if isinstance(under_v, str):
                                        under_v = under_v.replace('\n', '')
                                        f.write(
                                            f'"{path_key}.{key}.{k}.{under_k}": "{under_v}",\n')
                                    else:
                                        f.write(
                                            f'"{path_key}.{key}.{k}.{under_k}": {under_v},\n')
                        else:
                            if path_key:
                                # print(f'{path_key}.{key}.{k}: {v}')
                                with open(file_name, 'a', encoding='utf-8') as f:
                                    if isinstance(v, str):
                                        v = v.replace('\n', '')
                                        f.write(
                                            f'"{path_key}.{key}.{k}": "{v}",\n')
                                    else:
                                        f.write(
                                            f'"{path_key}.{key}.{k}": {v},\n')
                            else:
                                # print(f'{key}.{k}: {v}')
                                with open(file_name, 'a', encoding='utf-8') as f:
                                    if isinstance(v, str):
                                        v = v.replace('\n', '')
                                        f.write(f'"{key}.{k}": "{v}",\n')
                                    else:
                                        f.write(f'"{key}.{k}": {v},\n')
                else:
                    if path_key:
                        # print(f'{path_key}.{key}: {value}')
                        with open(file_name, 'a', encoding='utf-8') as f:
                            if isinstance(value, str):
                                value = value.replace('\n', '')
                                f.write(f'"{path_key}.{key}": "{value}",\n')
                            else:
                                f.write(f'"{path_key}.{key}": {value},\n')
                    else:
                        # print(f'{key}: {value}')
                        with open(file_name, 'a', encoding='utf-8') as f:
                            if isinstance(value, str):
                                value = value.replace('\n', '')
                                f.write(f'"{key}": "{value}",\n')
                            else:
                                f.write(f'"{key}": {value},\n')
    except:
        # error triggered after trying to get data.items()
        value = ''.join([value for value in list_data])
        # print(f'{path_key}: {value}')
        with open(file_name, 'a', encoding='utf-8') as f:
            if isinstance(value, str):
                value = value.replace('\n', '')
                f.write(f'"{path_key}": "{value}",\n')
            else:
                f.write(f'"{path_key}": {value},\n')
