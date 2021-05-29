import mysql.connector
import json
import csv

cnx = mysql.connector.connect(
    host='localhost', user='root', password='sefteghoot', database='umls')


def get_cui_count(from_cui=None):
    query = "SELECT count(DISTINCT CUI) FROM MRCONSO"
    if from_cui:
        query += " WHERE CUI > %s"
    cursor = cnx.cursor(buffered=True)
    params = (from_cui,) if from_cui else None
    cursor.execute(query, params)
    return cursor.fetchone()[0]


def get_all_cuis(batch_size=2000, from_cui=None):
    count = get_cui_count(from_cui)
    cursor = cnx.cursor()
    if from_cui:
        query = "SELECT DISTINCT CUI FROM MRCONSO WHERE CUI >= %s ORDER BY CUI LIMIT %s OFFSET %s"
    else:
        query = "SELECT DISTINCT CUI FROM MRCONSO ORDER BY CUI LIMIT %s OFFSET %s"
    for offset in range(0, count, batch_size):
        params = (from_cui, batch_size, offset) if from_cui else (batch_size, offset)
        cursor.execute(query, params)
        for result in cursor.fetchall():
            yield result[0]


def get_cui_data(cui):
    cursor = cnx.cursor()
    query = '''SELECT 
                    cons.CUI, cons.ISPREF, cons.STR, def.def 
                FROM MRCONSO as cons 
                LEFT JOIN MRDEF as def ON def.cui = cons.cui 
                WHERE cons.cui = %s'''
    cursor.execute(query, (cui,))
    terms = []
    pref_terms = []
    definition = None
    for res in cursor.fetchall():
        if not definition and res[3]:
            definition = res[3]
        terms.append(res[2])
        if res[1] == 'Y':
            pref_terms.append(res[2])
    return pref_terms, terms, definition


def create_json():

    for cui in get_all_cuis():
        pref_term, terms, definition = get_cui_data(cui)
        data = {cui : {'pref_term': pref_term, 'terms': terms, 'definition': definition}}
        with open('cui_terms.json', 'a') as j_writer:
            j_writer.write(json.dumps(data) + '\n')
    

def fix_json(file:str):
    final_dict = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            temp_dict = json.loads(line)
            for key, value in temp_dict.items():
                final_dict[key] = value

    fixed_address = 'fixed.json'
    with open(fixed_address, 'w') as fixed:
        json.dump(final_dict, fixed)
        
    return fixed_address
        
        
def create_concept_sentence(cui_dict):
        concept_sentence = cui_dict['pref_term'][0] + ' means '
        if cui_dict['definition']:
            concept_sentence += cui_dict['definition'] + '; '
        concept_sentence += '; '.join(cui_dict['terms'])
        return concept_sentence



def create_csv(json_address: str):
    with open(json_address) as f:
        data = json.load(f)
        for cui, values in data.items():
            with open('cui_sentence.csv', 'a') as csv_f:
                csv_writer = csv.writer(csv_f, delimiter=',')
                csv_writer.writerow([cui, create_concept_sentence(values)])
        

if __name__ == '__main__':
    create_json()
    fixed = fix_json('cui_terms.json')
    create_csv(fixed)

