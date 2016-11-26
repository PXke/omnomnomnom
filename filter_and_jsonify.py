# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys
import time

def print_progress(iteration, total, prefix='', suffix='', decimals=1,
	barLength=100):
	"""Call in a loop to create terminal progress bar
	@params:
	    iteration   - Required  : current iteration (Int)
	    total       - Required  : total iterations (Int)
	    prefix      - Optional  : prefix string (Str)
	    suffix      - Optional  : suffix string (Str)
	    decimals    - Optional  : positive number of decimals in percent complete (Int)
	    barLength   - Optional  : character length of bar (Int)"""
	formatStr       = "{0:." + str(decimals) + "f}"
	percents        = formatStr.format(100 * (iteration / float(total)))
	filledLength    = int(round(barLength * iteration / float(total)))
	bar             = '█' * filledLength + '-' * (barLength - filledLength)
	sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
	if iteration == total:
	    sys.stdout.write('\n')
	sys.stdout.flush()

def clean_db(df) :

	for index, line in enumerate(df["results"][:]) :

		df['quantity'].iloc[index] = line['quantity']
		df['ingredients'].iloc[index] = line['ingredients']
		df['origins'].iloc[index] = line['origins']
		df['nutrients'].iloc[index] = line['nutrients']
		df['images'].iloc[index] = line['images']
		df['barcode'].iloc[index] = line['barcode']
		df['portion-quantity'].iloc[index] = line['portion-quantity']
		df['name'].iloc[index] = line['name']
		#df['status'].iloc[index] = line['status']
		df['unit'].iloc[index] = line['unit']
		df["products_names_fr"].iloc[index] = line['name-translations'].get("fr")
		df["products_names_en"].iloc[index] = line['name-translations'].get("en")
		df["products_names_it"].iloc[index] = line['name-translations'].get("it")
		df["products_names_de"].iloc[index] = line['name-translations'].get("de")
		df["origins_names_fr"].iloc[index] = line["origin-translations"].get("fr")
		df["origins_names_en"].iloc[index] = line["origin-translations"].get("en")
		df["origins_names_it"].iloc[index] = line["origin-translations"].get("it")
		df["origins_names_de"].iloc[index] = line["origin-translations"].get("de")
		df["ingredients_names_fr"].iloc[index] = line["ingredients-translations"].get("fr") 
		df["ingredients_names_en"].iloc[index] = line["ingredients-translations"].get("en") 
		df["ingredients_names_it"].iloc[index] = line["ingredients-translations"].get("it") 
		df["ingredients_names_de"].iloc[index] = line["ingredients-translations"].get("de") 
		print_progress(index+1,df.shape[0], decimals=2)
	df = df.drop(["results"], axis=1)
	return df


beg=time.time()
OUTPUTPATH = "../"
INPUTDB = "../subset.json"
#INPUTDB = "../Original_database.json"

db = pd.read_json(INPUTDB)
db['quantity'] = np.nan
db['ingredients'] = np.nan
db['origins'] = np.nan
db['nutrients'] = np.nan
db['images'] = np.nan
db['barcode'] = np.nan
db['portion-quantity'] = np.nan
db['name'] = np.nan
#db['status'] = np.nan
db['unit'] = np.nan
db["products_names_fr"] = np.nan
db["products_names_en"] = np.nan
db["products_names_it"] = np.nan
db["products_names_de"] = np.nan
db["origins_names_fr"]= np.nan
db["origins_names_en"]= np.nan
db["origins_names_it"]= np.nan
db["origins_names_de"]= np.nan
db["ingredients_names_fr"]= np.nan
db["ingredients_names_en"]= np.nan
db["ingredients_names_it"]= np.nan
db["ingredients_names_de"]= np.nan
print("...")


new_db = clean_db(db)
print(new_db)


new_db.to_csv(OUTPUTPATH+"/modified_db.csv")