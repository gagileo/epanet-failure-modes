# Menjanje vrednosti tacaka QH-krive - setQH
#-----------------------------------------------------------------------------------------------------------------------

def setQH_test(file_path, ID_KRIVE, newXY_value):

	"""
	setQH(file_path, ID_KRIVE, newXY_value)

	:file_path: string putanja fajla
	:ID_KRIVE: string postojece IDkrive
	:newXY_value: lista [[x1, y1],[x2, y2],...]

	:Pravi novi .inp_newQH-fajl sa promenjenim podacima zadate krive, i smesta ga u isti folder.

	"""

	# 1 -  Uvoz i citanje fajla
	# ---------------------------------

	with open(file_path) as f:
		s = f.readlines()
	# =================================

	# Ova promenljiva nam treba za izvo novog .inp-fajla
	# ---------------------------------------------------
	putanja_Fajla = file_path

	# 2 -  Deljenje uvezenog fajla na blokove(celine)
	#      Prvi i poslednji blok nam sluze za izvoz modifikovanog .inp-fajla
	# -----------------------------------------------------------------------------------------------
	# [TITLE] - [CURVE] BLOK

	title_curve_blok = s[: s.index('[CURVES]\n', 0, len(s))]

	# [CURVES] BLOK

	curve_blok = s[s.index('[CURVES]\n', 0, len(s)): s.index('[CONTROLS]\n', 0, len(s))]
	curve_blok = curve_blok[:-1]  # Izbacijemo poslednji clan -> '\n', nema nikakv znacaj za podatke.
	curve_blok = [i[:-1] for i in curve_blok]  # Izbacivanje '\n' iz svakog elementa na kraju.

	# [CONTROLS] - [END] BLOK

	control_end_blok = s[s.index('[CONTROLS]\n', 0, len(s)):]
	# ===============================================================================================


	#  3 - Izvalcenje podataka o krivama ic [CURVES] BLOKA
	# -----------------------------------------------------------------------------

	# Dodajemo ma pocetak novog curve_blok-a .inp-fajla,
	# lista sadrzi '[CURVES]' i ';ID              \tX-Value     \tY-Value' string.
	# Treba na kraju svakog stringa dodati '\n'.
	curve_blok_header = curve_blok[:2]

	# Podaci bez prva dva reda, oni su opsti za svaku krivu
	# Iz ove liste izvlacimo podatke o QH-krivama.
	curves_data = curve_blok[2:]

	# Prvih 18 karaktera vrste vezano je za id-krive
	id_curves = [i[:17] for i in curves_data if i[0] != ';']
	id_curves = list(set(id_curves))  # izbacujemo duplikate sa set...

	# Header-i krivih ->';PUMP:....Opis'
	header_curves = [i for i in curves_data if i[0] == ';']

	# Kordinate QH-krivih -> xy_values,
	# svaki clan liste odgovara podacima za jednu krivu,
	# ...duzine id_cuves, header_curves i xy_values su jednake
	xy_values = []
	for id in id_curves:

		p = [i for i in curves_data if i[:17] == id]

		q = []

		for j in p:
			q.append([j[18:30], j[31:43]])

		xy_values.append(q)

	# Pravimo Dictionary QH-krivih - qhcurves
	zip_data = zip(id_curves, header_curves, xy_values)

	qhcurves = {}
	for i in range(len(zip_data)):
		qhcurves[zip_data[i][0]] = {'header': zip_data[i][1], 'xy_pts': zip_data[i][2]}

	# ====================================================================================



	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#Pomocna f-ja za sredjivanje unetog IDkrive jer postoji rezervisan broj karaktera
	#koji je dodeljen za ime IDkrive u .inp-fajlu pa ga moramo namestiti zbog unosa
	#korisnika,jer korisnik ne treba time da se zanima(bakce)!
	#------------------------------------------------------------------------------------------

	def srediKaraktereIDkrive(id_input_string):
		# IDkrive ima rezervisanih 17 karaktera, oduzimamo 1 jer dodajemo 1 na pocetku('space')
		return ' ' + id_input_string + ' '*((17-1)- len(id_input_string))

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#==========================================================================================


	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# Pomocna f-ja koja radi ali je ne koristim, ne znam sta cu sa njom?
	# ------------------------------------------------------------------------------------------------------------------

	def newQH(id_qh, qh_pts):
		# Duzine polja za ID, x-Value, y-Value
		poljeID, poljeX, poljeY = 17, 12, 12

		# Nova lista za smestanje u .inp-fajl
		new_qh = []
		for i in qh_pts:
			m = [poljeID - len(id_qh), poljeX - len(str(i[0])), poljeY - len(str(i[1]))]
			new_qh.append(
				str('{}' + ' ' * m[0] + '\t' +
				    '{}' + ' ' * m[1] + '\t' +
				    '{}' + ' ' * m[2] + '\n').format(id_qh, str(i[0]), str(i[1])))

		return new_qh

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# ==================================================================================================================

	# PITANJE da li uneti IDkrive postoji u .inp-fajlu
	# -------------------------------------------------
	ID_KRIVE = srediKaraktereIDkrive(ID_KRIVE)

	if ID_KRIVE in qhcurves:
		# Smestamo nove podatke(x i y vrednosti) u qhcurves Dictionary
		qhcurves[ID_KRIVE]['xy_pts'] = newXY_value

		new_qhcurves = []

		for i in qhcurves.items():
			new_qhcurves.append((i[1]['header']) + '\n')

			nxy = i[1]['xy_pts']

			for j in nxy:
				# Duzine polja za ID, x-Value, y-Value
				poljeID, poljeX, poljeY = 17, 12, 12

				# i[0] - idQH
				# j[0] - X-Value
				# j[1] - Y-Value

				m = [poljeID - len(i[0]), poljeX - len(str(j[0])), poljeY - len(str(j[1]))]

				new_qhcurves.append(
					str('{}' + ' ' * m[0] + '\t' +
					    '{}' + ' ' * m[1] + '\t' +
					    '{}' + ' ' * m[2] + '\n').format(i[0], str(j[0]), str(j[1])))

		new_inp_file = title_curve_blok + [curve_blok_header[0]] + ['\n'] + [curve_blok_header[1]] + [
			'\n'] + new_qhcurves + ['\n'] + control_end_blok

		# Pravljenje Novog .inp-fajla sa promenjenim tackama odabrane krive.
		# ------------------------------------------------------------------
		with open(putanja_Fajla[:-4] + '_newQH.inp', 'w') as f:
			f.writelines(new_inp_file)

		closefile()

	else:
		print 'Ne postoji uneti ID krive!'
		closefile()

#///////////////////////////////////////////////////////////////////////////////////////////////////////

from grf_master.epanet_fun import *

f = openepafile("C:\\PROJEKTI\\Net3\\Net3.inp")

xy     = getQH(f, '1', 'Yes')
xy_new = [[i[0]*0.8, i[1]*0.8] for i in xy]

setQH(f, '1', xy_new)

ff = openepafile("C:\\PROJEKTI\\Net3\\Net3_newQH.inp")
print getQH(f, '1', 'Yes')
print getQH(ff, '1', 'Yes')






# setQH_test