import csv

salju_train = []
salju_test = []


rawdata = []
with open('salju_train.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		rawdata.append(row)
		if len(rawdata) == 6: break

#print(rawdata)
#salju_train = load_data('salju_train.csv')
#print(salju_train)

date1 = /7/2010
date2 = 7/7/2010
print(date2-date1)