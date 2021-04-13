import csv

salju_train = []
salju_test = []

def load_data(filename):
	rawdata = []
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			if row[0] == 'id':
				continue
			rawdata.append(row)
			if len(rawdata) == 6: break
	return rawdata

def cleansing_data(rawdata):
	clean_data = []
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
			clean['kecepatan9'] = float(data[12])
			clean['kecepatan3'] = float(data[13])
			clean['lembab9'] = float(data[14])
			clean['lembab3'] = float(data[15])
			clean['tekanan9'] = float(data[16])
			clean['tekanan3'] = float(data[17])
			clean['awan9'] = float(data[18])
			clean['awan3'] = float(data[19])
			clean['suhu9'] = float(data[20])
			clean['suhu3'] = float(data[21])
			clean['hariini'] = data[22]
			clean['besok'] = data[23]
			clean_data.append(clean)

	return clean_data

rawdata = load_data('salju_train.csv')
salju_train = cleansing_data(rawdata)
print(salju_train)