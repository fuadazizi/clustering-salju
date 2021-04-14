import csv

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
			clean['iddata'] = data[0]
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
		skor = scaling(T_min, T_max, data['suhumin']) + scaling(T_min, T_max, data['suhumax']) + scaling(hujan_min, hujan_max, data['hujan']) + scaling(penguapan_min, penguapan_max, data['penguapan']) + scaling(sinar_min, sinar_max,data['sinar']) + scaling(kecepatan_min, kecepatan_max, data['kecepatan']) + scaling(lembab_min, lembab_max, data['lembab']) + scaling(tekanan_min, tekanan_min, data['tekanan']) + scaling(awan_min, awan_max, data['awan'])
		clean_data[i]['skor'] = skor

	return clean_data

def minmax(min_now, max_now, x):
	if (min_now > x): 
		min_now = x
	elif (max_now < x): 
		max_now = x

def scaling(min, max, x):
	return ((x - min) / (max - min)) * 100 if (max - min) != 0 else 0

salju_train = cleansing_data(rawdata)

for data in salju_train:
	print(data['skor'])

