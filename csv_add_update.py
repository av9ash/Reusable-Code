from tempfile import NamedTemporaryFile
import csv
import shutil
import json

COLUMNNAMES = ['token', 'pr_number', 'gensim_recs', 'sklearn_recs', 'ensemble_recs', 'bert_rec', 'synopsis']

def write_to_csv(data):
    tod = date.today().strftime("%m%d")
    filename = CSV_PATH.format(tod)
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUMNNAMES)
            writer.writeheader()

    with open(filename, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNNAMES)
        writer.writerow(data)

        
def add_to_csv(res_dkt, tod):
    if not tod:
        tod = date.today().strftime("%m%d")
    filename = CSV_PATH.format(tod)
    if os.path.exists(filename):
        # filename = os.path.basename(filename)
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        with open(filename, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=COLUMNNAMES)
            writer = csv.DictWriter(tempfile, fieldnames=COLUMNNAMES)
            for row in reader:
                recs = res_dkt.get(row['token'])
                if recs:
                    recs = json.loads(recs)
                    row['sklearn_recs'] = recs
                    g_recs = json.loads(row['gensim_recs'].replace('\'', '"'))
                    if g_recs or recs:
                        row['ensemble_recs'] = borda_rank([g_recs, recs])
                        top_rec = next(iter(json.loads(row['ensemble_recs'])))
                        row['bert_rec'] = get_bert_rec(row['pr_number'], top_rec)
                    else:
                        row['ensemble_recs'] = {}

                row = {'token': row['token'], 'pr_number': row['pr_number'],
                       'gensim_recs': row['gensim_recs'], 'sklearn_recs': row['sklearn_recs'],
                       'ensemble_recs': row['ensemble_recs'], 'bert_rec': row['bert_rec'], 'synopsis': row['synopsis']}
                writer.writerow(row)

        shutil.move(tempfile.name, filename)
    else:
        print('CSV file containing tokens not found.')
