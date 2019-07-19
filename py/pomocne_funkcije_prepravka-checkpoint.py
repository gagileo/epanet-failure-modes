# ? STATUS  =>  Sredjen `code`, treba ga Testirati!

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#  ::: POMOCNE FUNKCIJE :::  #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

from operator import add, sub


# Pomocna funkcija za koriscenje operatora (+) i (-)
def putOperator(oper):
    """
    :param oper: string - '+' or '-'
    :return    : function - add or sub from operator module

    """

    return add if oper == '+' else sub


# Pomocna funkcija za dobijanje rastojanja izmedju dve tacke
def rastojanje(pts_1, pts_2):
    """
    :param  pts_1: list - Koordinate tacke 1 -> [x1, y1]
    :param  pts_2: list - Koordinate tacke 2 -> [x2, y2]
    :return      : number - Vraca rastojanje izmedju dve tacke.

    """
    [x1, y1], [x2, y2] = pts_1, pts_2

    return (abs(x2 - x1)**2 + abs(y2-y1)**2)**0.5


# Header format
def header_format(header_string):
    return f"[{header_string.upper()}]\n"


# Pomocna funkcija za izdvajanje podataka o zadatom zaglavlju npr. [JUNCTIONS]
def epa_blok(lst_epa_file, header):  # ! Sredjeno - TESTIRATI
    """
    :param  lst_epa_file : list   - lista podataka uvezenog inp-fajla
    :param  header       : string - zaglavlje unutar inp-fajla (npr. [JUNCTIONS]), 
                                    samo ime bez zagrada(mala ili velika slova, nije vazno!)
    :return              : list   - vraca listu podataka iz zadataog zaglavlja

    """
    header = header_format(header)

    header_index = lst_epa_file.index(header)

    lst_result = [lst_epa_file[header_index]]

    for i in lst_epa_file[header_index+1:]:
        if i[0] != '[':
            lst_result.append(i)
        else:
            break

    return lst_result


def epa_blok2blok(epa_lst, start_block, end_block):  # ! Sredjeno - TESTIRATI
    """
    :param  epa_lst     : list - Epanet-inp fajl u vidu liste
    :param  start_block : string zaglavlje od koga `krecemo`.
    :param  end_block   : string zaglavlje do koga `idemo`.
    :return             : list - Vraca listu sa podacima koji obuhvataju podatke od pocetnog do pocetka krajnjeg zaglavlja.
    """
    start_index = epa_lst.index(header_format(start_block), 0, len(epa_lst))
    end_index = epa_lst.index(header_format(end_block), 0, len(epa_lst))

    return epa_lst[start_index: end_index]


# Pomocna funkcija za korekciju broja string karaktera
# `pomFun1` staro ime f-je, novo ime jw `string_len_corection`
def string_len_corection(old_string, num_of_characters):  # ! Sredjeno - TESTIRATI
    """
    :param old_string        : string 
    :param num_of_characters : int
    :return                  : string - Vraca old_string sa dodatom duzinom zadatkog broja karaktera.

    """
    new_string = old_string + " " * (num_of_characters - len(old_string))
    return new_string


# Pomocna funkcija za pravljenje pattern-a
def new_pat(pat_name, mult_value):   # ! Sredjeno - TESTIRATI
    """
     :param  pat_name  : string - ime pattern-a
     :param  mult_value: float - Multiplikator - pogledaj EPANET-manual, npr. 0.7 (30% manje od 1)
     :return           : list - Vraca listu 

     :info:
     Program radi samo za vremenski interval od 0-24,
     tj. 25 vremenskih koraka.
     Za ise informacija pogledaj EPANET-manual.

    """
    # Pravimo liste od id-a plus 6 brojnih vrednosti
    # pored toga moraju se korigovati brojevi karaktera svakog elementa liste.
    # Posto ima 25 vrednosti pravimo 4 liste po 6 elemenata plus jednu listu sa jednim elementom.
    lst = [string_len_corection(' ' + pat_name, 17)] + \
          ['\t' + string_len_corection(str(mult_value), 12) for i in range(6)] + \
          ['\n']

    # Spajamo u `string`
    lst = ''.join(lst)

    # Poslednja vrednost za 24. sat
    lst24 = string_len_corection(' ' + pat_name, 17) + \
        '\t' + string_len_corection(str(mult_value), 12) + '\n'

    # Novo formirani patern od 0-24h
    pat = [';\n', lst, lst, lst, lst, lst24, '\n']
    return pat


# Pomocna f-ja, pravi listu podataka za nove vrednosti QH-krive
def newQH(id_qh, qh_pts):    # ! Sredjeno - TESTIRATI
    """
    :param  id_qh : string - ID-QH krive
    :param  qh_pts: list - Koordinate tacaka QH krive -> [[x1, y1], [x2, y2], ...]
    :return       : list - Vraca listu string-elemenata -> ['ID-QH   x1-Value    y1-Value',
                                                            'ID-QH   x2-Value    y2-Value',...],
                    koju smestamo u blok CURVES za formiranje novog .inp-fajla.

    """
    # Nova lista za smestanje u .inp-fajl
    new_qh = []
    for i in qh_pts:
        m = [
            string_len_corection(' ' + id_qh, 17),
            string_len_corection(str(i[0]), 12),
            string_len_corection(str(i[1]), 12)
        ]

        new_qh.append(f"{m[0]}\t{m[1]}\t{m[2]}")

    return new_qh


# Pomocna f-ja, vraca id QH-krive za uneti ID-pumpe.
def pumpQH(file_path, pump_id):  # ! Sredjeno - TESTIRATI
    """
    :param  file_path: string - Putanja fajla.
    :param  pump_id  : string - ID pumpe
    :return          : string - ID QH-krive

    :info:
    Napomena: Koristi funkcije `string_len_corection` i `epa_blok`

    """
    # 1 - Trazenje QH-krive za uneti ID-pumpe
    # ------------------------------------------------------------------------
    # Korekcija karaktera stringa unetog ID-a pumpe
    # Ukupno zauzima 17 karaktera u inp-fajlu, s'tim sto je prvi `space`
    pump_id = f" {string_len_corection(pump_id, 16)}"

    # Otvaranje fajla i smestanje podataka u promenjljivu `s` (list-type)
    with open(file_path) as f:
        s = f.readlines()

    # Izdvajanje bloka [PUMPS]
    blok_pumps = epa_blok(s, 'pumps')

    # ----------------------------------------------
    # Izdvajanje podataka za uneti ID-pumpe (pumpu)
    # ----------------------------------------------

    # Izgled podataka za jednu pumpu u zaglavlju [PUMPS].
    # Potrebno je da se iz zaglavlja izdvoji string za zadati ID-pumpe.
    # Izgled stringa:
    # ' pumpa1          \tizvor1          \tcvor1           \tHEAD kriva1\tSPEED 0.70\t;\n'

    # To radi sledeci racunarski kod.
    pump_data = [i for i in blok_pumps if i[:17] == pump_id][0]

    # Izdvajamo podatke vezane za QH-krivu, bice dosta kontrole i seckanja stringa,
    # pa cemo promenljive obelezavati od curve_data_0 do curve_data_N
    # index 52 -> HEAD, pogledaj u primeru, komentar iznad...
    # -------------------------------------------------------------------------------
    curve_data_0 = pump_data[52:]

    # Izdvajanje karaktera stringa tip -> `HEAD kriva1`
    # --------------------------------------------------
    if '\t' in curve_data_0:
        # Pozicija `\t`, jer do njega je ime QH-krive
        pom_pos = curve_data_0.index('\t')
        curve_data_1 = curve_data_0[: pom_pos]
    elif ';' in curve_data_0:
        # Pozicija `;`, jer do njega je ime QH-krive
        pom_pos = curve_data_0.index(';')
        curve_data_1 = curve_data_0[: pom_pos]

    # ID QH-krive
    id_curve = curve_data_1[5:]

    return id_curve


# Pomocna f-ja (EPANET) za dobijanje koordinata cvora
def getCoord(file_path, node_id):  # ! Sredjeno - TESTIRATI
    """
    :param  file_path: string - Putanja fajla.
    :param  node_id  : string - ID cvora
    :return          : list - Lista koordinata tacka cvora.

    """
    # 1 - Otvaranje fajla i smestanje podataka u promenljivu `s` (list - type)
    # -----------------------------------------------------------
    with open(file_path) as f:
        s = f.readlines()

    # 2 - Trazenje koordinata iz zaglavlja [COORDINATES]
    # ---------------------------------------------------

    blok = epa_blok(s, 'COORDINATES')

    # Izdvajanje stringa sa podacima-koordinatama unetog ID-a cvora.
    node_data = [i for i in blok if node_id in i][0]

    x_value = float(node_data[18:34])
    y_value = float(node_data[35:51])

    return [x_value, y_value]


# Pomocna f-ja (SWMM) za dobijanje koordinata cvora
def swmm_getCoord(inp_file_path, node_id):  # ! Sredjeno - TESTIRATI
    """
    :param  inp_file_path: string - Putanja fajla.
    :param  node_id      : string - ID cvora
    :return              : list - Lista koordinata tacka cvora.

    :info:
    Vazi za SWMM-inp fajl, ne i za EPANET zbog razlicitog broja polja...

    """
    # 1 - Otvaranje fajla i smestanje podataka u promenljivu `s`
    # -----------------------------------------------------------
    with open(inp_file_path) as f:
        s = f.readlines()

    # 2 - Trazenje koordinata iz zaglavlja [COORDINATES]
    # ---------------------------------------------------

    blok = epa_blok(s, 'COORDINATES')

    # Izdvajanje stringa sa podacima-koordinatama unetog ID-a cvora.
    node_data = [i for i in blok if node_id in i][0]

    x_value = float(node_data[17:36])
    y_value = float(node_data[36:54])

    return [x_value, y_value]


# Pomocna funkcija za dobijanje koordinata novih cvorova
def coordFun(pts_1, pts_2, br_segmenata):  # ! Sredjeno - TESTIRATI
    """
    :param pts_1: list - [x1, y1], Koordinate 1.cvora.
    :param pts_2: list - [x2, y2], Koordinate 2.cvora.
    :param br_segmenata: int - Na koliko delova delimo cev.
    :return: list - Vraca listu koordinata tacaka -> broj tacaka je br_segmenata - 1

    """
    x1, y1 = pts_1
    x2, y2 = pts_2

    br_tacaka = br_segmenata - 1
    dx = abs(x2 - x1) / br_segmenata
    dy = abs(y2 - y1) / br_segmenata

    def append_new_points(x_or_y, plmin):
        """
        :param  x_or_y: string - 'x' or 'y'
        :param  plmin : string - '+' or '-'
        :return       : dictionary - liste koordinata tacaka po x i y.

        :info:
        Pomocna fn za dodavanje novih koordinata-tacaka.

        """
        new_points_dict = {
            'x':
            [
                [putOperator(plmin)(x1, i * dx), ((x1 - i * dx) - x1)
                 * (y2 - y1) / (x2 - x1) + y1]
                for i in range(1, br_tacaka + 1)
            ],
            'y':
            [
                [((y1 - i * dy) - y1) * (x2 - x1) / (y2 - y1) +
                 x1, putOperator(plmin)(y1, i * dy)]
                for i in range(1, br_tacaka + 1)
            ]
        }

        return new_points_dict

    if x1 == x2:

        if y1 > y2:  # Oduzimamo u `for`-petlji -> (y1 - i * dy)
            new_points = append_new_points('y', sub)

        else:  # Dodajemo u `for`-petlji -> (y1 + i * dy)
            new_points = append_new_points('y', add)

    else:

        if x1 > x2:
            new_points = append_new_points('x', sub)

        else:
            new_points = append_new_points('x', add)

    return new_points


# Pomocna funkcija za dobijanje koordinata novog cvora na zadatoj duzini od uzvodnog cvora cevi
# ! Sredjeno - TESTIRATI i promeniti ime funkcije!
def dodaj_coordFun(pts_1, pts_2, L_nove_tacke):
    """
    :param  pts_1       : list - Koordinate 1.cvora -> [x1, y1]
    :param  pts_2       : list - Koordinate 2.cvora -> [x2, y2]
    :param  L_nove_tacke: number(int or float) - Duzina na kojoj se nalazi tacka(posto je u pitanju cev)
    :return             : list - Vraca koordinate tacake -> [x_coord, x_coord]

    """
    [x1, y1], [x2, y2] = pts_1, pts_2

    # br_tacaka = br_segmenata - 1

    if x1 == x2:
        dy = L_nove_tacke

        if y1 > y2:
            new_points = [((y1 - dy) - y1) * (x2 - x1) /
                          (y2 - y1) + x1, (y1 - dy)]

        else:
            new_points = [((y1 + dy) - y1) * (x2 - x1) /
                          (y2 - y1) + x1, (y1 + dy)]

    else:
        dx = L_nove_tacke

        if x1 > x2:
            new_points = [(x1 - dx), ((x1 - dx) - x1)
                          * (y2 - y1) / (x2 - x1) + y1]

        else:
            new_points = [(x1 + dx), ((x1 + dx) - x1)
                          * (y2 - y1) / (x2 - x1) + y1]

    return new_points


# Pomocna funkcija za dobijanje liste atributa iz SWMM-bloka
def getBlokAtrib(blok):  # ! Sredjeno - TESTIRATI
    """
    :param  blok: list - Lista sa podacima bloka (npr. [JUNCTIONS],...)
    :return     : list - Vraca listu atributa iz zaglavlja bloka.

    : info:
    Vazi samo za SWMM-inp fajl, NE i za EPANET!!!

    """
    # Izbacivanje ;; i \n i dodavanje " " (space) jer se javlja neki bug bez ovoga!!!
    atr_str = blok[1][2:-1] + " "
    atr_str = atr_str.split(' ')  # Razdvajanje stringa

    # Spajamo stringove ako su odvojeni, npr 'From', 'Node' -> 'From Node'
    # ----------------------------------------------------------------------
    pom1 = []

    for i in range(0, len(atr_str) - 1):

        if len(atr_str[i]) != 0 and len(atr_str[i + 1]) != 0:
            pom1.append(atr_str[i] + ' ' + atr_str[i + 1])

        else:
            pom1.append(atr_str[i])

    # Indekse u listi gde se nalaze "viskovi"
    # ----------------------------------------
    pom2 = []

    for i in range(0, len(pom1) - 1):

        if len(pom1[i]) != 0 and len(pom1[i + 1]) != 0:
            pom2.append(i + 1)

    # Prebacivanje vrednosti visaka u ''
    for i in pom2:
        pom1[i] = ''

    # KONACNO - izbacujemo sve elemente -> ''
    atr_lsp = [i for i in pom1 if i != '']

    return atr_lsp


# Pomocna funkcija za dobijanje liste blokova iz SWMM-inp fajla
def sw_blocks(sw_lsp, blok=''):  # ! Sredjeno - TESTIRATI
    """
    :param  sw_lsp : list - Lista uvezenog swmm-inp fajla -> ["[TITLE]\n",...]
    :param  blok='': string - Ime bloka, malim ili velikim slovima, svejedno. #! STA AKO OSTAVIMO PRAZNO?
    :return        : list - Vraca listu gde svaki element liste sadrzi podatke o jednom zaglavlju(bloku) swmm-inp fajla.

    """
    lst_headers = [i for i in sw_lsp if i[0] == '[']

    indeksi = [sw_lsp.index(i, 0, len(sw_lsp))
               for i in lst_headers] + [len(sw_lsp)]

    blokovi = [sw_lsp[indeksi[i]: indeksi[i + 1]]
               for i in range(0, len(indeksi) - 1)]

    if blok == '':
        return blokovi
    elif blok != '':
        return [i for i in blokovi if blok in i[0]][0]
    else:
        print(" Blok(zaglavlje) ne postoji!")


# Pomocna funkcija za dobijanje liste-matrice podataka bloka, SWMM-inp fajla
def getBlokData(blok):  # ! Sredjeno - TESTIRATI
    """
    :param  blok: list - Lista sa podacima bloka (npr. [JUNCTIONS],...)
    :return     : list - Vraca listu sa vrednostima atributa, sve vrednosti su String-tipa,
                         po potrebi ih treba konvertovati u neki drugi tip...npr '23.4' -> 23.4 ...

    """
    blok_data = []
    blok[3:-1]
    for i in blok[3:-1]:
        # i[:-1].split(' ') -> [-1] , izbacujemo '\n'
        blok_data.append([j for j in i[:-1].split(' ') if j != ''])

    return blok_data


# Pomocna funkcija za dobijanje Dictionary-tipa od uvezenog SWMM-inp fajla
def swDict(file_path):   # ! Sredjeno - TESTIRATI
    """
    :param  file_path: string - Putanja inp-fajla.
    :return         : dict - Vraca Dictionary-tip sa podacima o inp-fajlu.

    :info:
    Koristi se samo za SWMM-inp fajlove.

    """
    # Ucitavanje podataka iz inp-fajla
    # -----------------------------------
    with open(file_path) as f:
        s = f.readlines()

    # /K O R E K C I J A/   `s` liste zbog moguce pojave novih imena kolona unutar zaglavlja,
    # pri promeni tipova cevi u swmm-fajlu(tako radi software...).
    # --------------------------------------------------------------------------------------
    # KOREKCIJA imena kolona zaglavlja [JUNCTIONS]
    # --------------------------------------------
    # Ako je zaglavlje ovakvo, mora da se menja sa donjim, inace program nece raditi!!!

    test1 = [s.index(i, 0, len(s)) for i in s if 'Elevation' in i]

    if test1 != []:  # Postoji index, tj. postoji Elevaton koje moramo da zamenimo sa Invert.

        # Izgled zaglavlja za koje program radi
        zag_junct = ';;Junction       Invert     MaxDepth   InitDepth  SurDepth   Aponded   \n'
        # Zamena zaglavlja
        s[test1[0]] = zag_junct

    # KOREKCIJA [XSECTIONS] zaglavlja
    # --------------------------------
    # Ako je zaglavlje ovakvo, mora da se menja sa donjim...program nece raditi!!!
    test2 = [s.index(i, 0, len(s)) for i in s if 'Culvert' in i]

    if test2 != []:
        # Izgled zaglavlja za koje program radi
        zag_xsec = ';;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels   \n'
        # Zamena zaglavlja
        s[test2[0]] = zag_xsec
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Svi Blokovi koje necemo za sada modifikovati, tako da je bolje samo da ih upakujemo u izvornom obliku.
    zag_tip1 = ['TITLE', 'OPTIONS', 'EVAPORATION', 'INFILTRATION',
                'RAINGAGES', 'OUTFALLS', 'TIMESERIES', 'REPORT',
                'SUBCATCHMENTS', 'SUBAREAS', 'TAGS', 'MAP',
                'VERTICES', 'Polygons', 'SYMBOLS']

    # Prazan Dictionary za smestanje svih podataka iz swmm-inp fajla.
    sw_dict = {}

    # Glavni Dictionary - sw_dict -> prvo pakujemo Blokove iz zag_tip1 liste
    sw_dict = {}
    for i in zag_tip1:
        sw_dict[i] = sw_blocks(s, i)

    # Lista svih zaglavlja
    # [1:-2] -> bez '[...]\n' , samo text.
    zag = [i[1:-2] for i in s if i[0] == '[']

    # Formiranje liste zaglavlja koje smestamo u sw_dict na drugi nacin -> njima kasnije mozemo menjati strukturu.
    zag_tip2 = [i for i in zag if i not in zag_tip1]

    # Lista blokova nad kojima mozemo menjati strukturu
    blokovi = [sw_blocks(s, i) for i in zag_tip2]

    for b in blokovi:
        zagbloka = b[:3]        # od [...] do ;; -----  -----  ....
        imebloka = b[0][1:-2]   # Ovo je npr. JUNCTIONS

        blokatrib = getBlokAtrib(b)     # Lista atributa bloka
        blokdata = getBlokData(b)      # Lista-matrica podataka, bloka

        sw_dict[imebloka] = {}
        # ubacivanje zaglavlja u dictionari, sluzi kasnije za pravljenje novog fajla.
        sw_dict[imebloka]["ZAGLAVLJE"] = zagbloka
        # ubacivanje liste atributa, korisno ako dodajemo nove objekte u blok.
        sw_dict[imebloka]["ATRIBUTI"] = blokatrib

        for row in blokdata:
            sw_dict[imebloka][row[0]] = {}

            for i in range(1, len(blokatrib)):
                sw_dict[imebloka][row[0]][blokatrib[i]] = row[i]

    return sw_dict


# Pomocna funkcija za dobijanje liste duzina na kojima se javlja poremecaj u cevi
def duzineCevi(L, L1, L2):  # ! Sredjeno - TESTIRATI
    """
    :param  L : number - Duzina cevi u metrima
    :param  L1: number - Duzina od koje se javlja "poremecaj"
    :param  L2: number - Duzina do koje traje "poremecaj"
    :return   : list - Vraca listu sa podeljenim duzinama cevi.

    """
    if L1 == 0 and L2 == L:
        return [L]  # Ne menja se duzina

    elif L1 == 0 and 0 < L2 < L:
        return [L2, L - L2]  # Dve duzine => dve cevi

    elif L1 > 0 and L2 == L:
        return [L1, L - L1]  # Dve duzine => dve cevi

    elif L1 > 0 and 0 < L2 < L:
        return [L1, L2 - L1, L - L2]  # Tri duzine => tri cevi


def srediKaraktereIDkrive(id_input_string):  # ! Sredjeno - TESTIRATI
    """
    :param id_input_string: string
    :return               : string

    :info:
    Pomocna f-ja za sredjivanje unetog IDkrive jer postoji rezervisan broj karaktera
    koji je dodeljen za ime IDkrive u .inp-fajlu pa ga moramo namestiti zbog unosa
    korisnika,jer korisnik ne treba time da se zanima(bakce)!

    """
    # IDkrive ima rezervisanih 17 karaktera, oduzimamo 1 jer dodajemo 1 na pocetku('space')
    return f" {id_input_string}{' ' * (16 - len(id_input_string))}"


def epa_file_to_list(file_path):
    """
    :param  file_path: string - Putanja Epanet .inp fajla
    :return          : list - sadrzaj Epanet .inp fajla u vidu liste, elem.liste -> linija .inp-fajla.

    """
    with open(file_path, "r") as f:
        result = f.readlines()

    return result

# === END ===
