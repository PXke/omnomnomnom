# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys

def split_names(string): # There is probably a library that does that but I don't want to look for it...
	split_string = []
	new_word = ""
	start = False

	for letter in string:
		if letter == "\"" and not start:
			start = True
			continue

		elif letter == "\"" and start :
			split_string.append(new_word)
			new_word = ""
			start = False
			continue
		if start :
			new_word += letter
			continue

	return split_string


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

OUTPUTPATH = "./JSON_files/"

nutrients = pd.read_csv("nutrients.csv")
products = pd.read_csv("products.csv")
product_nutrients = pd.read_csv("product_nutrients.csv")

#Some cleaning on the original files
df_products = products.dropna(subset=["name_translations"])
df_products = df_products.drop(["created_at","updated_at", "remarks", "origin_translations"], axis = 1)
df_product_nutrients = product_nutrients.drop(["created_at","updated_at"], axis = 1) 
df_nutrients = nutrients.drop(["created_at","updated_at"], axis = 1)

df_products.to_json("chose.json")

df_products["products_names_fr"] = np.nan
df_products["products_names_en"] = np.nan
df_products["products_names_it"] = np.nan
df_products["products_names_de"] = np.nan

print(df_products[:5])

for index, products in enumerate(df_products["name_translations"]) :
	
	products = split_names(products)

	for i in range(0,len(products)//2, 2) :
		if products[i] == "fr" :
			df_products["products_names_fr"].iloc[index] = products[i+1]
		elif products[i] == "de":
			df_products["products_names_de"].iloc[index] = products[i+1]
		elif products[i] == "en":
			df_products["products_names_en"].iloc[index] = products[i+1]
		elif products[i] == "it":
			df_products["products_names_it"].iloc[index] = products[i+1]
		else :
			print("error : incorrect language detected :\n {}".format(products[i]))

	print_progress(index, df_products.shape[0], barLength=50)

#df_products = df_products.drop(["name_translations"], axis=1)

#df_products.to_sql("chose.xml")

#Mapping the files to the final dataframe

df_products.to_json(OUTPUTPATH+"filtered_products.json", orient="records")
df_products.to_csv(OUTPUTPATH+"filtered_products.csv")
df_product_nutrients.to_json(OUTPUTPATH+"filtered_products_nutrients.json", orient="records")
df_product_nutrients.to_csv(OUTPUTPATH+"filtered_products_nutrients.csv")
df_nutrients.to_json(OUTPUTPATH+"filtered_nutrients.json", orient="records")
df_nutrients.to_csv(OUTPUTPATH+"filtered_nutrients.csv")

