import csv
import numpy as np
import random

salju_train = []
salju_test = []
rawdata = []
with open('salju_train.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		if row[0] == 'id':
			continue
		# mengganti setiap attribut yang kosong menjadi 0
		for i in range(len(row)):
			if row[i] == '':
				row[i] = 0
		rawdata.append(row)

# CLEAN DATA & SCORING

def cleansing_data(rawdata):
	clean_data = []
	T_min, T_max = 0, 0
	hujan_min, hujan_max = 0, 0
	penguapan_min, penguapan_max = 0, 0
	sinar_min, sinar_max = 0, 0
	kecepatan_min, kecepatan_max = 0, 0
	lembab_min, lembab_max = 0, 0
	tekanan_min, tekanan_max = 0, 0
	awan_min, awan_max = 0, 0

	for data in rawdata:
		# menghapus beberapa kolom
		# mengecek dan menghapus baris data yang tidak memiliki data salju hari ini dan besok
		if (data[22] != '' and data[23] != ''):
			clean = {}
			clean['iddata'] = int(data[0])
			clean['tanggal'] = data[1]
			clean['kodelokasi'] = data[2]
			clean['suhumin'] = float(data[3])
			clean['suhumax'] = float(data[4])
			clean['hujan'] = float(data[5])
			clean['penguapan'] = float(data[6])
			clean['sinar'] = float(data[7])
			clean['kecepatan'] = (float(data[12]) + float(data[13])) / 2
			clean['lembab'] = (float(data[14]) + float(data[15])) / 2
			clean['tekanan'] = (float(data[16]) + float(data[17])) / 2
			clean['awan'] = (float(data[18]) + float(data[19])) / 2
			clean['hariini'] = data[22]
			clean['besok'] = data[23]
			clean_data.append(clean)

			if (T_min > clean['suhumin']): T_min = clean['suhumin']
			if (T_max < clean['suhumax']): T_max = clean['suhumax']

			minmax(hujan_min, hujan_max, clean['hujan'])
			minmax(penguapan_min, penguapan_max, clean['penguapan'])
			minmax(sinar_min, sinar_max, clean['sinar'])
			minmax(kecepatan_min, kecepatan_max, clean['kecepatan'])
			minmax(lembab_min, lembab_max, clean['lembab'])
			minmax(tekanan_min, tekanan_max, clean['tekanan'])
			minmax(awan_min, awan_max, clean['awan'])

	for i in range(len(clean_data)):
		data = clean_data[i]
		score = scaling(T_min, T_max, data['suhumin']) + scaling(T_min, T_max, data['suhumax']) + scaling(hujan_min, hujan_max, data['hujan']) + scaling(penguapan_min, penguapan_max, data['penguapan']) + scaling(sinar_min, sinar_max,data['sinar']) + scaling(kecepatan_min, kecepatan_max, data['kecepatan']) + scaling(lembab_min, lembab_max, data['lembab']) + scaling(tekanan_min, tekanan_min, data['tekanan']) + scaling(awan_min, awan_max, data['awan'])
		clean_data[i]['score'] = score

	return clean_data

def minmax(min_now, max_now, x):
	if (min_now > x): 
		min_now = x
	elif (max_now < x): 
		max_now = x

def scaling(min, max, x):
	return ((x - min) / (max - min)) if (max - min) != 0 else 0

salju_train = cleansing_data(rawdata)

# MODELLING

# pick random cluster centroid
starting_point = []
c = 5
for i in range(c):
	randomize = random.randint(0,len(salju_train))
	if randomize not in starting_point:
		starting_point.append(randomize)

def define_cluster(starting_point):
	cluster = []
	for i in range(len(starting_point)):
		temp = []
		temp.append(starting_point[i])
		cluster.append(temp)
	return cluster

# cluster each data
while True:
	cluster = define_cluster(starting_point)
	score_sum = [0] * len(cluster)
	new_start = []
	# define each data into a cluster
	# data stored in cluster is INDEX OF DATA IN EXCEL
	for idx_salju in range(len(salju_train)):
		salju = salju_train[idx_salju]
		deviation = []
		for idx_center in range(len(starting_point)):
			deviation.append(abs(salju['score'] - salju_train[starting_point[idx_center]]['score']))
		cluster[deviation.index(min(deviation))].append(idx_salju)
		score_sum[deviation.index(min(deviation))]+= salju['score']
	# re-centroid each cluster
	for i in range(len(score_sum)):
		score_avg = (score_sum[i]/len(cluster[i]))
		centroid = 0
		min_deviation = abs(salju_train[centroid]['score'] - score_avg)
		for item in cluster[i]:
			if ((salju_train[item]['score'] - score_avg) < min_deviation) :
				min_deviation = abs(salju_train[item]['score'] - score_avg)
				centroid = item
		new_start.append(centroid)
	if (new_start == starting_point):
		break
	else:
		starting_point = new_start
	print(new_start)

# EVALUATING
sse_cluster = []
print(starting_point)
for row in cluster:
	#centroid = salju_train[row[0]]['iddata'] - 1
	centroid = row[0]
	sse = 0
	for data in row:
		#idx = salju_train[data]['iddata'] - 1
		idx = data
		sse += (salju_train[idx]['score'] - salju_train[centroid]['score']) ** 2
	sse_cluster.append(sse)

#print(cluster)
print(sse_cluster)

'''for data in salju_train:
	print(data['score'])
'''

