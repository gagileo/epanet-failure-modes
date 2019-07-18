
# ***********************************************************************************************************************
#   PAKET:           epanet_fun
#
#   VERZIJA:         1.0         |  1.1
#   DATUM(d/m/y):    2016/11/15  |  2019/07/10
#   
#   AUTOR:           Dragan Babic - Gagi
#   INFO:            Deo master rada
#
#   Paket sadrzi sledece funkcije:
#
#   openepafile      - Otvaranje EPANET inp-fajla
#   closefile        - Zatvaranje EPANET inp-fajla
#   tableview        - Predstavljanje podataka u vidu tabele
#
#   CVOROVI:
#   junctions        - Dictionary cvorova u mrezi
#   junctelevation   - Nadmorska visina cvora(cvorova)
#   junctbasedemand  - Inicijalna cvorna potrosnja
#   junctdemand      - Cvorna potrosnja u vremenskom koraku
#   junctpressure    - Pritisak u cvoru(cvorovima)
#   juncthead        - Visina pritiska u cvoru(cvorovima)
#
#   CEVI:
#   pipes            - Dictionary cevi u mrezi
#   pipenodes        - Cvorovi na krajevima cevi
#   pipestatus       - Status cevi (Otvorena ili Zatvorena)
#   pipelength       - Duzina cevi(cevima)
#   pipediameter     - Precnik cevi(cevima)
#   piperoughness    - Rapavost cevi(cevima)
#   pipeflow         - Protok u cevi(cevima)
#   pipevelocity     - Brzina u cevi(cevima)
#
#   PUMPE:
#   pumps            - Dictionary pumpi u mrezi
#   pumpnodes        - Cvorovi za koje je vezana pumpa
#   pumpstatus       - Status pumpe (Otvorena ili Zatvorena)
#   pumpspeed        - Parametar koji smanjuje ili uvecava krivu pumpe...tako nesto
#   pumpsflow        - Protok kroz pumpu
#   getQH            - QH krive
#
#   REZERVOARI:
#   tanks            - Dictionary tank-ova(rezervoara) u mrezi
#   tankselevation   - Nadmorska visina rezervoara
#   tankinitlevel    - Inicijalni nivo u rezervoaru
#   tankminlevel     - Minimalni nivo u rezervoaru
#   tankmaxlevel     - Maksimalni nivo u rezervoaru
#   tankminvolume    - Minimalna zapremina rezervoara
#   tankpressure     - Pritisak u rezervoaru
#
#   IZVORI:
#   reservoirs       - Dictionary izvora u mrezi
#
#   OTKAZI (MODES of FAILURES):
#   rescapacityfail  - Pad kapaciteta izvorista
#   pipecapacityfail - Pad kapaciteta cevi
#   pumpcapacityfail - Pad kapaciteta pumpe
#   pipeleakfail     - Curenje cevi
#   tankleakfail     - Curenje rezervoara
#   reseconomfail    - Zamena rezervoara pumpom sa regulatorom pritiska
#
# ***********************************************************************************************************************

import epanet_api as enapi
import utilfns as uf
import pandas as pd


# --------------------------------- #
# ::: C V O R O V I (JUNCTIONS) ::: #
# --------------------------------- #

def junctions():  # ! Sredjeno - TESTIRATI
    """
    :return: dict - Vraca dictionary tip -> {'id_cvora': 'index_cvora',...},

    :info:
    lista ID-eva  -> junctions().keys()
    lista Index-a -> junctions().values()
    Po default-u dictionary-tip nije sortiran.(Mozda se promeni u narednim verzijama Python-a)

    :primer:
    Provera da li postoji ID_cvora u mrezi:
    'ID_cvora' in junctions() -> True (False)

    """
    # Broj Cvorova u Mrezi
    nnode = enapi.getCount('node')

    # Pozicije(index-i) `junction`-tipova...bez `tank` i `reservoir` tipova.
    node_pos = [i for i in range(1, nnode + 1)
                if enapi.getType('node', i) == 'Junction node']

    id_cvorova = [enapi.getID('node', i) for i in node_pos]

    return dict(zip(id_cvorova, node_pos))


def junctelevation(object_index='', value=''):   # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  value=''        : depends of object type
    :return                 : junctelevation() -> vraca kotu-terena u svim cvorovima mreze.
                              junctelevation(index_cvora) -> vraca kotu-terena u cvoru zadatog object_index-a.
                              junctelevation(index_cvora, vrednost u metrima) -> zadaje novu vrednost kote-terena.

    :NAPOMENA:
    junctelevation f-ja isto daje ili menja vrednost `Total Head` vrednosti `Reservoir`-objekta!

    """
    if object_index == '':
        # Broj Cvorova u Mrezi
        nnode = enapi.getCount('node')
        # Pozicije(object_index-i) `junction`-tipova...bez `tank` i `reservoir` tipova.
        node_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Junction node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_ELEVATION, p), node_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_ELEVATION, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_ELEVATION, object_index, value)


def junctbasedemand(object_index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='': int
    :param  value=''       : number
    :return                : junctbasedemand() -> vraca inicijalnu cvornu potrosnu u svim cvorovima mreze.
                             junctbasedemand(index_cvora) -> vraca inicijalnu cvornu potrosnu u cvoru zadatog object_index-a.
                             junctbasedemand(index_cvora, vrednost u L/s) -> zadaje novu vrednost inicijalne cvorne potrosnje
                                                                             u zatatom cvoru.

        """
    if object_index == '':
        # Broj Cvorova u Mrezi
        nnode = enapi.getCount('node')
        # Pozicije(object_index-i) `junction`-tipova...bez `tank` i `reservoir` tipova.
        node_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Junction node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_BASEDEMAND, p), node_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_BASEDEMAND, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_BASEDEMAND, object_index, value)


def junctdemand(object_index=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :return                 : junctdemand(object_index = ''),
                              junctdemand() -> vraca cvornu potrosnu u svim cvorovima mreze.
                              junctdemand(index_cvora) -> vraca cvornu potrosnu u cvoru zadatog object_index-a.

    """
    if object_index == '':
        # Broj Cvorova u Mrezi
        nnode = enapi.getCount('node')

        # Pozicije(object_index-i) `junction`-tipova...bez `tank` i `reservoir` tipova.
        node_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Junction node']
        return map(lambda p: enapi.getValue('node', enapi.epa.EN_DEMAND, p), node_pos)

    else:
        return enapi.getValue('node', enapi.epa.EN_DEMAND, object_index)


def junctpressure(object_index=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :return                 : junctpressure(object_index = ''),
                              junctpressure() -> vraca pritiske u svim cvorovima mreze.
                              junctpressure(index_cvora) -> vraca pritisak u cvoru zadatog object_index-a.

    """
    if object_index == '':
        # Broj Cvorova u Mrezi
        nnode = enapi.getCount('node')

        # Pozicije(object_index-i) `junction`-tipova...bez `tank` i `reservoir` tipova.
        node_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Junction node']
        return map(lambda p: enapi.getValue('node', enapi.epa.EN_PRESSURE, p), node_pos)

    else:
        return enapi.getValue('node', enapi.epa.EN_PRESSURE, object_index)


def juncthead(object_index=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :return                 : juncthead(object_index = ''),
                              juncthead() -> vraca visinu-pritiska u svim cvorovima mreze.
                              juncthead(index_cvora) -> vraca visinu-pritiska u cvoru zadatog object_index-a.

    """
    if object_index == '':
        # Broj Cvorova u Mrezi
        nnode = enapi.getCount('node')

        # Pozicije(object_index-i) `junction`-tipova...bez `tank` i `reservoir` tipova.
        node_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Junction node']
        return map(lambda p: enapi.getValue('node', enapi.epa.EN_HEAD, p), node_pos)

    else:
        return enapi.getValue('node', enapi.epa.EN_HEAD, object_index)


# ----------------------- #
# ::: C E V I (PIPES) ::: #
# ----------------------- #

def pipes():  # ! Sredjeno - TESTIRATI
    """
    :return: dict - Vraca dictionary tip -> {'id_cevi': 'index_cevi',...}

    :info:
    lista ID-eva  -> pipes().keys()
    lista Index-a -> pipes().values()
    Po default-u dictionary-tip nije sortiran.(Mozda se promeni u narednim verzijama Python-a)

    :Primer:
    Provera da li postoji ID_cevi u mrezi:
    'ID_cvora' in junctions() -> True (False)

    """
    # Broj `link`-objekata u mrezi
    nlink = enapi.getCount('link')
    # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
    # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
    pipe_pos = [i for i in range(1, nlink + 1) if enapi.getType('link', i)[:4] == 'Pipe']
    # id-jevi cevi
    id_cevi = [enapi.getID('link', i) for i in pipe_pos]

    # Rezultat u vidu dictionary tipa (key -> value)
    return dict(zip(id_cevi, pipe_pos))


def pipenodes(pipe_id):  # ! Sredjeno - TESTIRATI
    """
    :param  pipe_id : string - ID cevi
    :return         : list - Vraca listu -> [ID-uzvodnog_cvora, ID-nizvodnog_cvora]

    """
    if enapi.getType('link', enapi.getIndex('link', pipe_id)) == 'Pipe':
        # izbacujemo 1.vrednost -> [1:] jer je u pitanju 0 ....
        indeksi_cvorova = enapi.epa.ENgetlinknodes(enapi.getIndex('link', pipe_id))[1:]

        return map(lambda n: enapi.getID('node', n), indeksi_cvorova)

    else:
        print(' ->  Uneti parametar nije cev!')


def pipestatus(object_index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  value=''        : number
    :return                 : list - vraca listu jedinica i nula, 1 -> Open ili 0 -> Closed,
                              za svaki vremenski korak.

    :info:
    Ako unesemo i status koji je po default-u value = '':
    value = 1 -> Open
    value = 0 -> Closed
    podesavamo inicijalne vrednosti cevi, i tada nam f-ja ne vraca nista, samo
    podesi zadate inicijalne vrednosti.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')
        # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
        # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
        pipe_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i)[:4] == 'Pipe']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_STATUS, p), pipe_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('link', enapi.epa.EN_STATUS, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('link', enapi.epa.EN_INITSTATUS, object_index, value)


def pipelength(object_index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  value=''        : number
    :return                 : pipelength() -> vraca duzinu svih cevi u mrezi.
                              pipelength(index_cevi) -> vraca duzinu-cevi zadatog object_index-a.
                              pipelength(index_cevi, vrednost u metrima) -> zadaje novu vrednost duzine-cevi.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')
        # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
        # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
        pipe_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i)[:4] == 'Pipe']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_LENGTH, p), pipe_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('link', enapi.epa.EN_LENGTH, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('link', enapi.epa.EN_LENGTH, object_index, value)


def pipediameter(object_index='', new_value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  new_value=''        : number
    :return                 : pipediameter() -> vraca precnik svih cevi u mrezi.
                              pipediameter(index_cevi) -> vraca precnik-cevi zadatog object_index-a.
                              pipediameter(index_cevi, vrednost u milimetrima) -> zadaje novu vrednost precnika-cevi.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')
        # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
        # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
        pipe_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i)[:4] == 'Pipe']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_DIAMETER, p), pipe_pos)

    elif object_index != '' and new_value == '':
        return enapi.getValue('link', enapi.epa.EN_DIAMETER, object_index)

    elif object_index != '' and new_value != '':
        return enapi.setValue('link', enapi.epa.EN_DIAMETER, object_index, new_value)


def piperoughness(object_index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  value=''        : number
    :return                 : piperoughness() -> vraca koef.trenja svih cevi u mrezi.
                              piperoughness(index_cevi) -> vraca koef.trenja zadatog object_index-a cevi.
                              piperoughness(index_cevi, vrednost) -> zadaje novu vrednost koef.trenja.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')
        # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
        # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
        pipe_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i)[:4] == 'Pipe']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_SETTING, p), pipe_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('link', enapi.epa.EN_SETTING, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('link', enapi.epa.EN_INITSETTING, object_index, value)


def pipeflow(object_index=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :return                 : pipeflow() -> vraca protoke u svim cevima mreze.
                              pipeflow(index_cevi) -> vraca protoke u cevi zadatog object_index-a.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')
        # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
        # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
        pipe_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i)[:4] == 'Pipe']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_FLOW, p), pipe_pos)

    else:
        return enapi.getValue('link', enapi.epa.EN_FLOW, object_index)


def pipevelocity(object_index=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :return                 : pipevelocity() -> vraca brzine u svim cevima mreze.
                              pipevelocity(index_cevi) -> vraca brzine u cevi zadatog object_index-a.
                              Lista brzina za svaki vremenski korak.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')
        # Pozicije `pipe`-tipova...bez `pump` i `valve` tipova.
        # [:4] -> zato sto postoji i 'Pipe with Check Valve' pa nam treba samo 4 karaktera...
        pipe_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i)[:4] == 'Pipe']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_VELOCITY, p), pipe_pos)

    else:
        return enapi.getValue('link', enapi.epa.EN_VELOCITY, object_index)


# ------------------------- #
# ::: P U M P E (PUMPS) ::: #
# ------------------------- #

def getPump():   # ! Sredjeno - TESTIRATI
    """
    :return: dict - Kolekcija Pumpi u Mrezi sa parovima idPumpe : indexPumpe, ako postoje u mrezi.

    """
    number_of_objects = enapi.getCount("link")
    pump_indexes = [i for i in range(1, number_of_objects + 1) if enapi.getType('link', i) == 'Pump']
    pump_ids = [enapi.getID('link', i) for i in pump_indexes]

    return dict(list(zip(pump_ids, pump_indexes)))


def pumpstatus(object_index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  value=''        : number
    :return                 : Vraca listu, 1 -> Open ili 0 -> Closed,
                              Za svaki vremenski korak.
                              Ako unesemo i status koji je po default-u value = '':

    :info:
    value = 1 -> Open
    value = 0 -> Closed
    podesavamo inicijalne vrednosti pumpe, i tada nam f-ja ne vraca nista, samo
    podesi zadate inicijalne vrednosti.

    """
    if object_index == '':
        nlink = enapi.getCount('link')
        # Pozicije `pump`-tipova...bez `pipe` i `valve` tipova.
        pump_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i) == 'Pump']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_STATUS, p), pump_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('link', enapi.epa.EN_STATUS, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('link', enapi.epa.EN_INITSTATUS, object_index, value)


def pumpnodes(pump_id):  # ! Sredjeno - TESTIRATI
    """
    :param  pump_id : string - ID pumpe
    :return         : list - Vraca listu -> [ID-uzvodnog_cvora, ID-nizvodnog_cvora]

    """
    if enapi.getType('link', enapi.getIndex('link', pump_id)) == 'Pump':
        # izbacujemo 1.vrednost -> [1:] jer je u pitanju 0 ....
        indeksi_cvorova = enapi.epa.ENgetlinknodes(enapi.getIndex('link', pump_id))[1:]

        return list(map(lambda n: enapi.getID('node', n), indeksi_cvorova))

    else:
        print(' ->  Uneti parametar nije pumpa!')


def pumpspeed(object_index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :param  value=''        : number
    :return                 : pumpspeed() -> vraca brzinu pumpe(ili koef. brzine...?).
                              pumpspeed(index_cevi) -> vraca brzinu pumpe(ili koef. brzine...?) zadatog object_index-a cevi.
                              pumpspeed(index_cevi, vrednost) -> zadaje novu vrednost brzine pumpe(ili koef. brzine...?).

    """
    if object_index == '':
        nlink = enapi.getCount('link')
        pump_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i) == 'Pump']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_SETTING, p), pump_pos)

    elif object_index != '' and value == '':
        return enapi.getValue('link', enapi.epa.EN_SETTING, object_index)

    elif object_index != '' and value != '':
        return enapi.setValue('link', enapi.epa.EN_INITSETTING, object_index, value)


def pumpflow(object_index=''):  # ! Sredjeno - TESTIRATI
    """
    :param  object_index='' : int
    :return                 : pumpflow(object_index = ''),
                              pumpflow() -> vraca protoke u svim cevima mreze.
                              pumpflow(index_cevi) -> vraca protoke u cevi zadatog object_index-a.

    """
    if object_index == '':
        # Broj `link`-objekata u mrezi
        nlink = enapi.getCount('link')

        # Pozicije `pump`-tipova...bez `pipe` i `valve` tipova.
        pump_pos = [i for i in range(1, nlink + 1)
                    if enapi.getType('link', i) == 'Pump']

        return map(lambda p: enapi.getValue('link', enapi.epa.EN_FLOW, p), pump_pos)

    else:
        return enapi.getValue('link', enapi.epa.EN_FLOW, object_index)


def getQH(file_path, curve_id=''):  # ! Sredjeno - TESTIRATI
    """
    :param  file_path   : string - putanja Epanet .inp fajla
    :param  curve_id='' : string - ime QH-krive
    :return             : dict  or list

    """
    # Sedjivanje duzine stringa da se poklopi kao u fajlu
    curve_id = f" {curve_id}{' ' * (16-len(curve_id))}" if curve_id != '' else ''
    epa_file_lst = uf.epa_file_to_list(file_path)
    curve_blok = uf.epa_blok(epa_file_lst, 'curves')
    curve_ids_lst_all = [i for i in curve_blok if i[0] not in ['[', ';', '\n']]
    # remove duplicates
    curve_ids_lst = list(set([i[:17] for i in curve_ids_lst_all]))
    curves_dict = {i: [[float(j[18:30]), float(j[31:])]
                       for j in curve_ids_lst_all if j[:17] == i] for i in curve_ids_lst}

    if curve_id == '':
        return curves_dict

    elif curve_id in curve_ids_lst:
        return curves_dict[curve_id]

    else:
        print(f"\n{curve_id} curve is not in file!\n")


def setQH(file_path, ID_KRIVE, newXY_value):  # ! Sredjeno - TESTIRATI
    """
    :param  file_path   : string - putanja fajla
    :param  ID_KRIVE    : string - postojece IDkrive
    :param  newXY_value : list   - [[x1, y1],[x2, y2],...]

    :return             : string - Pravi novi .inp_newQH-fajl sa promenjenim
                                   podacima zadate krive, i smesta ga u isti folder.

    """
    # 1 -  Uvoz i citanje fajla
    epa_file_lst = uf.epa_file_to_list(file_path)

    # Ova promenljiva nam treba za izvo novog .inp-fajla
    putanja_Fajla = file_path

    # 2 -  Deljenje uvezenog fajla na blokove(celine)
    #      Prvi i poslednji blok nam sluze za izvoz modifikovanog .inp-fajla
    title_curve_blok = uf.epa_blok2blok(epa_file_lst, 'curves', 'end')

    # [CURVES] BLOK
    curve_blok = uf.epa_blok(epa_file_lst, 'curves')
    # Izbacijemo poslednji clan -> '\n', nema nikakv znacaj za podatke.
    curve_blok = curve_blok[:-1]
    # Izbacivanje '\n' iz svakog elementa na kraju.
    curve_blok = [i[:-1] for i in curve_blok]

    # [CONTROLS] - [END] BLOK
    control_end_blok = uf.epa_blok2blok(epa_file_lst, 'controls', 'end')

    #  3 - Izvalcenje podataka o krivama iz [CURVES] BLOKA
    # Dodajemo na pocetak novog curve_blok-a .inp-fajla,
    # lista sadrzi '[CURVES]' i ';ID              \tX-Value     \tY-Value' string.
    # Treba na kraju svakog stringa dodati '\n'.
    curve_blok_header = curve_blok[:2]

    # Podaci bez prva dva reda, oni su opsti za svaku krivu
    # Iz ove liste izvlacimo podatke o QH-krivama.
    curves_data = curve_blok[2:]

    # Prvih 18 karaktera vrste vezano je za id-krive
    id_curves = [i[:17] for i in curves_data if i[0] != ';']
    id_curves = list(set(id_curves))

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
    zip_data = list(zip(id_curves, header_curves, xy_values))

    qhcurves = {}
    for i in range(len(zip_data)):
        qhcurves[zip_data[i][0]] = {
            'header': zip_data[i][1], 
            'xy_pts': zip_data[i][2]
            }

    # PITANJE da li uneti IDkrive postoji u .inp-fajlu
    ID_KRIVE = uf.srediKaraktereIDkrive(ID_KRIVE)

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

                m = [poljeID - len(i[0]), poljeX -
                     len(str(j[0])), poljeY - len(str(j[1]))]

                new_qhcurves.append(f"\
                    {i[0]}{' ' * m[0]}\t\
                    {j[0]}{' ' * m[1]}\t\
                    {j[1]}{' ' * m[2]}\n")

        new_inp_file = title_curve_blok + [curve_blok_header[0]] + ['\n'] + [curve_blok_header[1]] + \
            ['\n'] + new_qhcurves + ['\n'] + control_end_blok

        # Pravljenje Novog .inp-fajla sa promenjenim tackama odabrane krive.
        with open(putanja_Fajla[:-4] + '_newQH.inp', 'w') as f:
            f.writelines(new_inp_file)
        enapi.closefile()

    else:
        print('Ne postoji uneti ID krive!')
        enapi.closefile()


# ---------------------------------------- #
# ::: R E Z E R V O A R I (RESERVOIRS) ::: #    # ! SREDJENO
# ---------------------------------------- #

def tanks():  # ! Sredjeno - TESTIRATI
    """
    :return: vraca dictionary tip -> {'id_cvora': 'index_cvora',...},

    :info:
    lista ID-eva  -> tanks().keys()
    lista Index-a -> tanks().values()

    :primer:
    Provera da li postoji ID_tank u mrezi:
    'ID_tank' in tanks() -> True (False)

    """
    # Broj Cvorova u Mrezi
    nnode = enapi.getCount('node')
    # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
    tank_pos = [i for i in range(1, nnode + 1)
                if enapi.getType('node', i) == 'Tank node']

    # id-jevi tank-objekata(rezervoara)
    id_cvorova = [enapi.getID('node', i) for i in tank_pos]

    # Rezultat u vidu dictionary tipa (key -> value)
    return dict(zip(id_cvorova, tank_pos))


def tankelevation(index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :return: tankelevation() -> vraca kotu-terena u svim tank-objektima(rezervoarima) mreze.
             tankelevation(index_cvora) -> vraca kotu-terena u tank-objektu zadatog index-a.
             tankelevation(index_cvora, vrednost u metrima) -> zadaje novu vrednost kote-teren
    :NAPOMENA:
    tanktelevation f-ja isto daje ili menja vrednost `Total Head` vrednosti `Reservoir`-objekta!

    """
    if index == '':
        nnode = enapi.getCount('node')
        # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
        tank_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Tank node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_ELEVATION, p), tank_pos)

    elif index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_ELEVATION, index)

    elif index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_ELEVATION, index, value)


def tankinitlevel(index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :return: tankinitlevel(index = ''),
             tankinitlevel() -> vraca inicijalni-nivo vode u svim tank-objektima(rezervoarima) mreze.
             tankinitlevel(index_cvora) -> vraca inicijalni-nivo vode u tank-objektu zadatog index-a.
             tankinitlevel(index_cvora, vrednost u metrima) -> zadaje novu vrednost inicijalnog-nivoa vode.

    """
    if index == '':
        # Broj Cvorova u Mrezi
        nnode = enapi.getCount('node')

        # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
        tank_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Tank node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_TANKLEVEL, p), tank_pos)

    elif index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_TANKLEVEL, index)

    elif index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_TANKLEVEL, index, value)


def tankminlevel(index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :return: tankminlevel(index = ''),
             tankminlevel() -> vraca minimalni-nivo vode u svim tank-objektima(rezervoarima) mreze.
             tankminlevel(index_cvora) -> vraca minimalni-nivo vode u tank-objektu zadatog index-a.
             tankminlevel(index_cvora, vrednost u metrima) -> zadaje novu vrednost minimalnog-nivoa vode.

    """
    if index == '':
        nnode = enapi.getCount('node')
        # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
        tank_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Tank node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_MINLEVEL, p), tank_pos)

    elif index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_MINLEVEL, index)

    elif index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_MINLEVEL, index, value)


def tankmaxlevel(index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :return: tankmaxlevel(index = ''),
             tankmaxlevel() -> vraca maksimalni-nivo vode u svim tank-objektima(rezervoarima) mreze.
             tankmaxlevel(index_cvora) -> vraca maksimalni-nivo vode u tank-objektu zadatog index-a.
             tankmaxlevel(index_cvora, vrednost u metrima) -> zadaje novu vrednost maksimalnog-nivoa vode.

    """
    if index == '':
        nnode = enapi.getCount('node')
        # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
        tank_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Tank node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_MAXLEVEL, p), tank_pos)

    elif index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_MAXLEVEL, index)

    elif index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_MAXLEVEL, index, value)


def tankminvolume(index='', value=''):  # ! Sredjeno - TESTIRATI
    """
    :return: tankminvolume(index = ''),
             tankminvolume() -> vraca minimalnu-zapreminu vode u svim tank-objektima(rezervoarima) mreze.
             tankminvolume(index_cvora) -> vraca minimalnu-zapreminu vode u tank-objektu zadatog index-a.
             tankminvolume(index_cvora, vrednost u metrima) -> zadaje novu vrednost minimalne-zapremine vode.

    """
    if index == '':
        nnode = enapi.getCount('node')
        # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
        tank_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Tank node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_MINVOLUME, p), tank_pos)

    elif index != '' and value == '':
        return enapi.getValue('node', enapi.epa.EN_MINVOLUME, index)

    elif index != '' and value != '':
        return enapi.setValue('node', enapi.epa.EN_MINVOLUME, index, value)


def tankpressure(index=''):  # ! Sredjeno - TESTIRATI
    """
    :return: tankpressure(index = ''),
             tankpressure() -> vraca pritiske u svim rezervoarima mreze.
             tankpressure(index_cvora) -> vraca pritisak u rezervoaru zadatog index-a.

    """
    if index == '':
        nnode = enapi.getCount('node')
        # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
        tank_pos = [i for i in range(1, nnode + 1)
                    if enapi.getType('node', i) == 'Tank node']

        return map(lambda p: enapi.getValue('node', enapi.epa.EN_PRESSURE, p), tank_pos)

    else:
        return enapi.getValue('node', enapi.epa.EN_PRESSURE, index)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TEST - TEST - TEST
# f = enapi.openepafile()
#
# print getQH(f, '2', 'Yes')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# -------------------------------- #
# ::: I Z V O R I (RESERVOIRS) ::: #    #! SREDJENO
# -------------------------------- #

def reservoirs():
    """
    :return: vraca dictionary tip -> {'id_cvora': 'index_cvora',...},
             po default-u dictionary-tip nije sortiran.

    :info:
    lista ID-eva  -> reservoirs().keys()
    lista Index-a -> reservoirs().values()

    """
    nnode = enapi.getCount('node')
    # Pozicije(index-i) `tank`-tipova...bez `junction` i `reservoir` tipova.
    reservoir_pos = [i for i in range(
        1, nnode + 1) if enapi.getType('node', i) == 'Reservoir node']
    # id-jevi tank-objekata(rezervoara)
    id_cvorova = [enapi.getID('node', i) for i in reservoir_pos]

    # Rezultat u vidu dictionary tipa (key -> value)
    return dict(zip(id_cvorova, reservoir_pos))


# ------------------------------ #
# ::: O T K A Z I (FAILURES) ::: #
# ------------------------------ #

def rescapacityfail(f_path, id_res, mul_value, pat_name):  # ! Sredjeno - TESTIRATI
    """
    :param f_path: String -> Putanja EPANET-inp-fajla
    :param id_res: String -> ID-izvora
    :param mul_value: Vrednost Multiplayer-a, pogledaj EPANET-help
    :param pat_name: Ime paterna, max 17 karaktera u imenu
    :return: Ne vraca vrednost -> pravi novi EPANET-inp-fajl sa dodatkom na ime fajla _NewPattern

    :info:
    Kako funkcija formira novi fajl, zatvara prethodno ucitane, ako su ucitani, i ucitava novoformirani
    nad koji vrsimo simulaciju otkaza, a posledice sagledavamo preko pritisaka, brzina,...

    """
    # 1 - Uvoz .inp-fajla, i smestanje u promenljivu `f`
    with open(f_path) as fid:
        f = fid.readlines()

    # 2 - Formiranje blokova uvezenog .inp-fajla
    # Delimo fajl na 5 blokova:
    # 1. [TITLE] - [RESERVOIRS]
    # 2. [RESERVOIR- koristimo funkciju `uf.epa_blok` jer nema medjublokova.
    # 3. [RESERVOIRS] - [PNije - ATTERNS]
    # 4. [PATTERNS] - istimo funkciju `uf.epa_blok` jer nema medjublokova.
    # 5. [CURVES] - [END]
    # Blokove 2 i 4 modifikujemo zbog formiranja novog paterna,
    # a ostali blokovi suluze za pravljenje novog .inp-fajla

    blok_1 = f[f.index('[TITLE]\n'): f.index('[RESERVOIRS]\n')]
    blok_2 = uf.epa_blok(f, '[RESERVO]\n')
    blok_3 = f[f.index('[RESERVOIRS]\n'): f.index('[PATTERNije - NS]\n')]
    blok_4 = uf.epa_blok(f, '[PATTERNS]\n')
    blok_5 = f[f.index('[CURVES]\n'):]

    # 3 - Kreiranje novog PATTERN-a i novog bloka-4 (PATTERNS)
    blok_4_novi = blok_4 + uf.new_pat(pat_name, mul_value)

    # 4   - Smestanje kreiranog PATTERN-a u blok_2 (RESERVOIRS - Head Patern atribut)
    # 4.1 - Trazenje zadatog rezevoara preko unetog ID-a, i formiranje bloka_2(zamena linije sa rezervoarom)
    # Korekcija broja karaktera unetog ID-a, mora biti 17.
    id_res = uf.string_len_corection(' ' + id_res, 17)
    # Pomocna lista, izdvaja samo vrednost unetog ID-a rezervoara.
    p = [i for i in blok_2 if i[:17] == id_res]
    pom_str = p[0]  # String sa podacima o rezervoaru
    # index stringa rezervoara u blok_2 listi.
    pom_index = blok_2.index(pom_str, 0, len(blok_2))
    # novi string sa unetim pattern-om
    novi_str = f"{pom_str[0: 31]}{pat_name}{pom_str[-5: ]}"
    # Zamenjeni clan liste blok_2 sa novim podacima o rezervoaru(novi patern)
    blok_2[pom_index] = novi_str

    # 5 - Sastavljanje blokova i formiranje novog.inp-fajla
    novi_inp_file = blok_1 + blok_2 + blok_3 + blok_4_novi + blok_5
    novi_f_path = f_path[: -4] + "_newPattern" + ".inp"

    # 6 - Izvoz novo formiranog .inp-fajla
    with open(novi_f_path, 'w') as f:
        f.writelines(novi_inp_file)

    # 7 - Posto funkciji prethodi otvaranje .inp-fajla f-jom enapi.openepafile()
    # otvoreni fajl moramo zatvoriti i ucitati novo formirani fajl kojim
    # simuliramo otkaz pada kapaciteta izvorista
    enapi.closefile()  # Procitaj u opisu zasto i koji fajl zatvaramo.
    # Otvaramo novoformirani fajl nad kojim simuliramo
    enapi.openepafile(novi_f_path)
    # otaz i sagledavamo posledice preko pritisaka,
    # brzine, protoka,...

    # Ovo je samo radi kontrole, moze da se smisli nesto bolje
    print(novi_f_path)


def pipecapacityfail(f_path, id_input, pipe_segments):  # ! Sredjeno - TESTIRATI
    """
        Pad kapaciteta cevi - pipecapacityfail
        pipecapacityfail(f_path, id_input, pipe_segments) -> deli cev na segmente i umanjuje precnike od uzvodnog ka nizvodnom cvoru.
        Funkcija se moze koristiti za simulaciju otkaza pada kapaciteta cevi.

        :param f_path:        String -> Putanja .inp-fajla
        :param id_input:        String -> ID-cevi
        :param pipe_segments:   Int -> broj jednak ili veci od 2.
        :return:                Ne vraca nista. Pravi novi .inp fajl sa sufiksom "_newPipes" na postojece ime fajla

        """

    # IDEJA:
    # ------------------------------------------------------------
    # Odabranu cev podeliti u vise cevi(min 2 cevi).
    # Podela podrazumeva zamenu postojece cevi novim cevima,
    # i dodavanje novih veza(cvorova), kao i novih koordinata zbog
    # crteza u EPANET-u.
    # ============================================================

    # Uvoz .inp-fajla, i smestanje u promenljivu `f`
    with open(f_path) as fid:
        f = fid.readlines()

    # FORMIRANJE BLOKOVA INP-fajla
    # Lista `Blokova` ([pipes], [pumps], ...)  u .inp-fajlu.
    # Blokove trazimo tako da je prvi karakter
    uf.epa_blokovi = [i for i in f if i[0] == '[']
    # svakog elementa liste `f` jednak uglastoj zagradi ('['),
    # posto su svi blokovi smesteni u uglastim zagradama([pipes],..)

    # Delimo fajl na 7 blokova:
    # 1. [TITLE] - [PIPES]
    # 2. [PIPES]
    # 3. [RESERVOIRS] - [pipes]
    # 4. [pipes]
    # 5. [pumps] - [COORDINTES]
    # 6. [coordinates]
    # 7. [vertices] - [END]
    # Blokove 2, 4 i 6 modifikujemo zbog dodavanja novih objekata,
    # a ostali blokovi nam sluze za formiranje novog .inp-fajla.

    blok_1 = f[f.index('[TITLE]\n'): f.index('[PIPES]\n')]
    blok_2 = f[f.index('[PIPES]\n'): f.index('[RESERVOIRS]\n')]
    blok_3 = f[f.index('[RESERVOIRS]\n'): f.index('[pipes]\n')]
    blok_4 = f[f.index('[pipes]\n'): f.index('[pumps]\n')]
    blok_5 = f[f.index('[pumps]\n'): f.index('[coordinates]\n')]
    blok_6 = f[f.index('[coordinates]\n'): f.index('[vertices]\n')]
    blok_7 = f[f.index('[vertices]\n'): f.index('[END]\n')]

    # TRAZENJE UNETOG ID-A CEVI
    # Korekcija unosa ID-a, prvi clan mora biti `space`
    if id_input[0] != " ":
        id_input = " " + id_input

    # Korekcija broja karaktera ID-a, mora biti 17 rezervisanih karaktera.
    id_input = uf.string_len_corection(id_input, 17)

    pipe_data = [i for i in blok_4 if i[:17] ==
                 id_input][0]  # string sa podacima o cevi
    # izbacivanje \t iz stringa -> vraca list-type...
    pipe_data = pipe_data.split('\t')
    # ...sadrzi vrednosti atributa cevi

    # Pravimo Dictionary sa atributima cevi.
    pipe = {}
    pipe_atributes = ['ID', 'Node1', 'Node2', 'Length',
                      'Diameter', 'Roughness', 'MinorLoss', 'Status']

    for i in range(len(pipe_atributes)):
        pipe[pipe_atributes[i]] = pipe_data[i]

    # Iz konstruisanog Dictionary-pipe dobijamo zeljene informacije atributa
    # Dodajem " " ispred ID-noda jer je tako zapisano u JUNCTION - bloku...
    pipe_node1 = ' ' + pipe['Node1']
    pipe_node2 = ' ' + pipe['Node2']

    # broj novih cvorova nastalih usled podele cevi.
    br_cvorova = pipe_segments - 1

    # BLOK_2 - PIPES
    # Trazimo indekse cvorova u fajlu kako bi definisali pod-blokove..
    pom_index_1 = blok_2.index([i for i in blok_2 if i[:17] == pipe_node1][0])
    # pom_index_2 = blok_2.index([i for i in blok_2 if i[:17] == pipe_node2][0])

    # Pravimo pod-blokove bloka_2 da bi ubacili nove cvorove
    blok_2_start = blok_2[: pom_index_1 + 1]
    # Treba da napravimo novi blok cvorova izmedju ova dva!
    blok_2_end = blok_2[pom_index_1 + 1:]

    # Shema PIPES Bloka
    # ' S1              \t50          \t0           \t                \t;\n'
    # ----------------------------------------------------------------------------------------------------------------------------
    # p - pomocna promenljiva u kojoj se nalazi ID 1.cvora, samo tekst bez pranih polja
    p = pipe_node1.split()[0]
    # zato koristimo .split()[0] -> uzimamo 0-ti clan jer vraca listu.

    # lista novih ID-eva cvorova
    new_node_IDs = [" " + p + "_" + str(i) for i in range(1, br_cvorova + 1)]
    # Korekcija broja karaktera ID-eva
    new_node_IDs = [uf.string_len_corection(i, 17) for i in new_node_IDs]

    # Vrednosti atributa `Node1`, potrebno jer svaki dodati cvor je njegov klon sa razlicitim ID-em.
    # lista -> npr. ['S1','50','0',';']
    node1_values = blok_2[pom_index_1].split()
    # nemoj da te zbuni sadrzaj liste jer fali polje Pattern koje nema vrednosti

    # k - pomocna promenljiva za formiranje node_values liste.
    k = blok_2[pom_index_1]

    # Atributi ->    ID       Elevation Demand    Pattern
    node1_values = [k[: 17], k[18:30], k[31:43], k[44:60]]

    blok_2_new_nodes = [f"\
        {new_node_IDs[i]}\t{node1_values[1]}\t\
        {node1_values[2]}\t{node1_values[3]}\t\n"
                        for i in range(len(new_node_IDs))]

    # NOVI `PIPES` - B L O K !!!
    new_blok_2 = blok_2_start + blok_2_new_nodes + blok_2_end

    # BLOK_6 - coordinates
    # Indeksi cvorova odabrane cevi u bloku coordinates - blok_6
    pom_index_coord_1 = blok_6.index(
        [i for i in blok_6 if i[:17] == pipe_node1][0])
    # pom_index_coord_2 = blok_6.index([i for i in blok_6 if i[:17] == pipe_node2][0])

    # Pravimo pod-blokove bloka_6 da bi ubacili kordinate novih cvorova
    blok_6_start = blok_6[: pom_index_coord_1 + 1]
    # Treba da napravimo novi blok cvorova-koordinata izmedju ova dva!
    blok_6_end = blok_6[pom_index_coord_1 + 1:]

    # Koordinate prvog-cvorova odabrane cevi
    coord_node1 = [i for i in blok_6 if i[:17] == pipe_node1][0]
    coord_node1 = coord_node1.split('\t')
    coord_node1 = [float(coord_node1[1]), float(
        coord_node1[2])]  # lista koordinata 1.cvora

    # Koordinate drugog-cvorova odabrane cevi
    coord_node2 = [i for i in blok_6 if i[:17] == pipe_node2][0]
    coord_node2 = coord_node2.split('\t')
    coord_node2 = [float(coord_node2[1]), float(
        coord_node2[2])]  # lista koordinata 2.cvora

    # Lista novih koordinata cvorova - Moraju se kasnije prebaciti u String-tip
    new_nodes_coord = uf.coordFun(coord_node1, coord_node2, pipe_segments)
    # treba srediti broj karaktera Stringova,
    new_nodes_coord = [[str(i[0]), str(i[1])] for i in new_nodes_coord]
    new_nodes_coord = [[uf.string_len_corection(i[0], 16), uf.string_len_corection(i[1], 16)] for i in
                       new_nodes_coord]  # sredjeni i karakteri

    # Pravljenje bloka novih koordinata cvorova
    # p - pomocna promenljiva u kojoj se nalazi ID 1.cvora, samo tekst bez pranih polja...
    p = pipe_node1.split()[0]
    # ...zato koristimo .split()[0] -> uzimamo 0-ti clan jer vraca listu.

    # lista novih ID-eva cvorova
    new_node_IDs = [f" {p}_{i}" for i in range(1, br_cvorova + 1)]
    # Korekcija broja karaktera ID-eva
    new_node_IDs = [uf.string_len_corection(i, 17) for i in new_node_IDs]

    # Shema Stringa u coordinates bloku:
    # ' S1              \t1624.15         \t7653.06         \n'
    # Pravimo Blok za nove cvorove na isti nacin.
    blok_6_new_nodes = [f"{new_node_IDs[i]}\t{new_nodes_coord[i][0]}\t{new_nodes_coord[i][1]}\n" for i in
                        range(len(new_node_IDs))]

    # NOVI coordinates  - B L O K !!!
    new_blok_6 = blok_6_start + blok_6_new_nodes + blok_6_end

    # BLOK_4 - pipes
    # Shema pipes Blok - vrste:
    # ' C1              \tS1              \tS2              \t800         \t75          \t0.0015      \t0           \tOpen  \t;\n'
    # ------------------------------------------------------------------------------------------------------------------------------

    # ID odabrane cevi - sredjujemo String da bi uspesno dodali nove ID-eve
    pipe_id = pipe['ID'].split()[0]
    pipe_id = " " + pipe_id

    # ID-evi novih cevi
    new_pipe_IDs = [uf.string_len_corection(
        pipe_id + "_" + str(i), 17) for i in range(1, pipe_segments + 1)]

    # i[1:17] -> uzimamo od `1` jer izbacujemo prvi karakter koji je jednak `space`, za ovaj blok ne ide `space` za ID...
    new_pipe_nodes_ID = [uf.string_len_corection(
        i[1:17], 16) for i in blok_6_new_nodes]

    # Dodamo i postojece ID-eve cvorova odabrane cevi
    new_pipe_nodes_ID = [pipe['Node1']] + new_pipe_nodes_ID + [pipe['Node2']]

    # Pravimo parove cvorova za svaku novu cev
    parovi_node_ID = [[new_pipe_nodes_ID[i - 1], new_pipe_nodes_ID[i]]
                      for i in range(1, len(new_pipe_nodes_ID))]

    # Duzina cevi
    pipe_length = float(pipe['Length'])

    # Precnik cevi
    pipe_diameter = float(pipe['Diameter'])

    # Podjednaka duzina svakog segmenta nove cevi
    dL_pipe = round(pipe_length / float(pipe_segments), 2)
    dL_pipe = uf.string_len_corection(str(dL_pipe), 12)

    test_index = [i for i in blok_4 if i[:17]
                  == uf.string_len_corection(pipe_id, 17)][0]
    pipe_index = blok_4.index(test_index)

    # Pravimo pod-blokove bloka_4 da bi ubacili nove cevi
    blok_4_start = blok_4[: pipe_index]
    # Treba da napravimo novi blok cevi izmedju ova dva!
    blok_4_end = blok_4[pipe_index + 1:]

    # Slican fajl kao pipe_data samo je u pitanju String a ne Lista
    pipe_data_0 = [i for i in blok_4 if i[:17] == id_input][0]

    # Precnik se smanjuje za svaki novi segment cevi
    # ID, Node1, Node2, Length, Diameter, Rouhness, MinorLoss, Status
    blok_4_new_pipes = [f"\
    {new_pipe_IDs[i]}\t\
    {parovi_node_ID[i][0]}\t\
    {parovi_node_ID[i][1]}\t\
    {dL_pipe}\t\
    {uf.string_len_corection(str(pipe_diameter / (i + 1)), 12)}\t\
    {pipe_data_0[78:90]}\t\
    {pipe_data_0[91:103]}\t\
    {pipe_data_0[104:110]}\t;\n" for i in range(len(new_pipe_IDs))]

    # NOVI pipes  - B L O K !!!
    new_blok_4 = blok_4_start + blok_4_new_pipes + blok_4_end

    # NOVI EPANET-FILE
    new_inp_file = blok_1 + new_blok_2 + blok_3 + \
        new_blok_4 + blok_5 + new_blok_6 + blok_7

    new_f_path = f"{f_path[:-4]}_newPipes.inp"

    with open(new_f_path, 'w') as f:
        f.writelines(new_inp_file)

    # Posto funkciji prethodi otvaranje .inp-fajla f-jom enapi.openepafile()
    # otvoreni fajl moramo zatvoriti i ucitati novo formirani fajl kojim
    # simuliramo otkaz pada kapaciteta izvorista
    enapi.closefile()  # Procitaj u opisu zasto i koji fajl zatvaramo.
    enapi.openepafile(new_f_path)  # Otvaramo novoformirani fajl nad kojim simuliramo
    # otaz i sagledavamo posledice preko pritisaka,
    # brzine, protoka,...

    # Ovo je samo radi kontrole, moze da se smisli nesto bolje
    print(new_f_path)


# Pad kapaciteta pumpe - pumpcapacityfail
def pumpcapacityfail(f_path, pump_id, percent_value):  # ! Sredjeno - TESTIRATI
    """
    :param  f_path        : Putanja inp-fajla
    :param  pump_id       : ID pumpe
    :param  percent_value : Procenat umanjenja vrednosti QH-krive odabrane pumpe
    :return               : Ne vraca vrednost -> pravi novi inp-fajl sa promenjenim vrednostima QH-krive,
                            i otvara ga f-jom `enapi.openepafile` => simulacija...

    """
    # 1 - Trazenje QH-krive za uneti ID-pumpe
    # Korekcija karaktera stringa unetog ID-a pumpe
    # Ukupno zauzima 17 karaktera u inp-fajlu, s'tim sto je prvi `space`
    pump_id = ' ' + uf.string_len_corection(pump_id, 16)

    # Otvaranje fajla i smestanje podataka u promenjljivu `s`
    with open(f_path) as f:
        s = f.readlines()

    # Izdvajanje bloka [pumps]
    blok_pumps = uf.epa_blok(s, 'pumps')

    # Izdvajanje podataka za uneti ID-pumpe (pumpu)
    # Izgled podataka za jednu pumpu u zaglavlju [pumps], potrebno je da se iz zaglavlja
    # izdvoji ovakav strin za zadati ID-pumpe, to radi sledeci racunarski kod.

    # ' pumpa1          \tizvor1          \tcvor1           \tHEAD kriva1\tSPEED 0.70\t;\n'

    pump_data = [i for i in blok_pumps if i[:17] == pump_id][0]

    # Izdvajamo podatke vezane za QH-krivu, bice dosta kontrole i seckanja stringa,
    # pa cemo promenljive obelezavati od curve_data_0 do curve_data_N
    # index 52 -> HEAD, pogledaj u primeru, komentar iznad...
    curve_data_0 = pump_data[52:]

    # Izdvajanje karaktera stringa tip -> `HEAD kriva1`
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

    # #NOVO - TEST
    # id_curve = pumpQH(f_path, pump_id)
    # # NOVO - TEST

    # 2 - QH-kriva
    # Izvlacenje x i y vrednosti QH-krive odabrane pumpe
    # Koristimo f-ju getQH za izvlacenje podataka.
    # xy -> lista [x, y] parova koord.tacaka. QH-krive
    xy = getQH(f_path, id_curve)

    # Novi podaci QH-krive umanjeni za zadati procenat (npr. 20 -> 20%)
    xy_new = [[i * (1 - percent_value / 100.), j *
               (1 - percent_value / 100.)] for i, j in xy]

    # Sredjovanje decimala (zaokruzivanje na 2 decimale)
    # round je f-ja iz paketa epanet_fun
    xy_new = round(xy_new, 2)

    # Koristimo f-ju setQH za kreiranje novog fajla sa novim vrednostima QH-krive.
    setQH(f_path, id_curve, xy_new)

    # Funkcija setQh formira novi inp-fajl sa dodatkom na ime fajla -> _newQH
    # Pravimo novu promenljivu da bi u sledecem koraku ucitali novi fajl sa novom QH-krivom
    novi_f_path = f_path[:-4] + "_newQH" + ".inp"

    # Posto funkciji prethodi otvaranje .inp-fajla f-jom enapi.openepafile()
    # otvoreni fajl moramo zatvoriti i ucitati novo formirani fajl kojim
    # simuliramo otkaz pada kapaciteta izvorista

    # Procitaj u opisu zasto i koji fajl zatvaramo.
    # Otvaramo novoformirani fajl nad kojim simuliramo
    enapi.openepafile(novi_f_path)
    # otaz i sagledavamo posledice preko pritisaka,
    # brzine, protoka,...

    # Ovo je samo radi kontrole, moze da se smisli nesto bolje
    print(novi_f_path)


# Curenje cevi - pipeleakfail
def pipeleakfail(f_path, id_pipe, pipe_segments, leak_percent):  # ! Sredjeno - TESTIRATI
    """
    :param  f_path        : string - Putanja .inp-fajla
    :param  id_pipe       : string - ID-cevi
    :param  pipe_segments : int - broj jednak ili veci od 2.
    :param  leak_percent  : number - Procenat curenja -> deo koji uzimamo od Qsr i
                                     rasporedjujemo po mestima curenja(novim cvorovima)
    :return               : Ne vraca nista. Pravi novi .inp fajl sa sufiksom "_Pipe_Leak" na postojece ime fajla

    :info:
    pipeleakfail(f_path, id_pipe, pipe_segments, leak_percent) -> deli cev na segmente i dodaje potrosnju u novim
    cvorovima koja je jednaka Qp = Qsr*pocenat/br_segmenat_acevi.
    Funkcija se moze koristiti za simulaciju curenja cevi.

    """
    # IDEJA:
    # ------------------------------------------------------------
    # Odabranu cev podeliti u vise cevi(min 2 cevi).
    # Podela podrazumeva zamenu postojece cevi novim cevima,
    # i dodavanje novih veza(cvorova), kao i novih koordinata zbog
    # crteza u EPANET-u.
    # ============================================================

    # Treba prvo naci Qsrv od odabrane cevi
    enapi.openepafile(f_path)  # Otvaramo fajl da bi dobili inform. o Q
    # Lista vrednosti protoka u cevi, 0-24h
    Q = pipeflow(enapi.getIndex('link', id_pipe))
    Qsr = round(sum(Q) / len(Q), 2)  # Srednji protok kroz cev
    enapi.closefile()  # Zatvarama fajl

    # Potrsnja u novim cvorovima koja simulira curenje Qp,
    # Qp = (Qsrv * procenat) / br.segenata
    # Zaokruzimo na dve decimale.
    Qp = round((Qsr * leak_percent * 0.01) / pipe_segments, 2)

    # Uvoz .inp-fajla, i smestanje u promenljivu `f` -> lista podataka inp-fajla
    with open(f_path) as fid:
        f = fid.readlines()

    # FORMIRANJE BLOKOVA INP-fajla
    # Lista `Blokova` ([pipes], [pumps], ...)  u .inp-fajlu.
    # Blokove trazimo tako da je prvi karakter
    uf.epa_blokovi = [i for i in f if i[0] == '[']
    # svakog elementa liste `f` jednak uglastoj zagradi ('['),
    # posto su svi blokovi smesteni u uglastim zagradama([pipes],..)

    # Delimo fajl na 7 blokova:
    # 1. [TITLE] - [PIPES]
    # 2. [PIPES]
    # 3. [RESERVOIRS] - [pipes]
    # 4. [pipes]
    # 5. [pumps] - [COORDINTES]
    # 6. [coordinates]
    # 7. [vertices] - [END]
    # Blokove 2, 4 i 6 modifikujemo zbog dodavanja novih objekata,
    # a ostali blokovi nam sluze za formiranje novog .inp-fajla.

    blok_1 = f[f.index('[TITLE]\n'): f.index('[PIPES]\n')]
    blok_2 = f[f.index('[PIPES]\n'): f.index('[RESERVOIRS]\n')]
    blok_3 = f[f.index('[RESERVOIRS]\n'): f.index('[pipes]\n')]
    blok_4 = f[f.index('[pipes]\n'): f.index('[pumps]\n')]
    blok_5 = f[f.index('[pumps]\n'): f.index('[coordinates]\n')]
    blok_6 = f[f.index('[coordinates]\n'): f.index('[vertices]\n')]
    blok_7 = f[f.index('[vertices]\n'): f.index('[END]\n')]

    # TRAZENJE UNETOG ID-A CEVI
    # Korekcija unosa ID-a, prvi clan mora biti `space`
    if id_pipe[0] != " ":
        id_pipe = " " + id_pipe

    # Korekcija broja karaktera ID-a, mora biti 17 rezervisanih karaktera.
    id_pipe = uf.string_len_corection(id_pipe, 17)

    pipe_data = [i for i in blok_4 if i[:17] ==
                 id_pipe][0]  # string sa podacima o cevi

    # izbacivanje \t iz stringa -> vraca list-type
    pipe_data = pipe_data.split('\t')
    # sadrzi vrednosti atributa cevi

    # Pravimo Dictionary sa atributima cevi.
    pipe = {}
    pipe_atributes = ['ID', 'Node1', 'Node2', 'Length',
                      'Diameter', 'Roughness', 'MinorLoss', 'Status']

    for i in range(len(pipe_atributes)):
        pipe[pipe_atributes[i]] = pipe_data[i]

    # Iz konstruisanog Dictionary-pipe dobijamo zeljene informacije atributa
    # Dodajem " " ispred ID-noda jer je tako zapisano u JUNCTION - bloku...
    pipe_node1 = ' ' + pipe['Node1']
    pipe_node2 = ' ' + pipe['Node2']

    # broj novih cvorova nastalih usled podele cevi.
    br_cvorova = pipe_segments - 1

    # BLOK_2 - PIPES
    # Trazimo indekse cvorova u fajlu kako bi definisali pod-blokove..
    pom_index_1 = blok_2.index([i for i in blok_2 if i[:17] == pipe_node1][0])
    # pom_index_2 = blok_2.index([i for i in blok_2 if i[:17] == pipe_node2][0])

    # Pravimo pod-blokove bloka_2 da bi ubacili nove cvorove
    blok_2_start = blok_2[: pom_index_1 + 1]
    # Treba da napravimo novi blok cvorova izmedju ova dva!
    blok_2_end = blok_2[pom_index_1 + 1:]

    # Shema PIPES Bloka
    # ' S1              \t50          \t0           \t                \t;\n'

    # p - pomocna promenljiva u kojoj se nalazi ID 1.cvora, samo tekst bez pranih polja
    p = pipe_node1.split()[0]
    # zato koristimo .split()[0] -> uzimamo 0-ti clan jer vraca listu.

    # lista novih ID-eva cvorova
    new_node_IDs = [" " + p + "_" + str(i) for i in range(1, br_cvorova + 1)]
    # Korekcija broja karaktera ID-eva
    new_node_IDs = [uf.string_len_corection(i, 17) for i in new_node_IDs]

    # Vrednosti atributa `Node1`, potrebno jer svaki dodati cvor je njegov klon sa razlicitim ID-em.
    # lista -> npr. ['S1','50','0',';']
    node1_values = blok_2[pom_index_1].split()
    # nemoj da te zbuni sadrzaj liste jer fali polje Pattern koje nema vrednosti

    # k - pomocna promenljiva za formiranje node_values liste.
    k = blok_2[pom_index_1]

    # Atributi ->    ID       Elevation    Demand      Pattern
    node1_values = [k[: 17], k[18:30],
                    uf.string_len_corection(str(Qp), 12), k[44:60]]

    blok_2_new_nodes = [
        new_node_IDs[i] + '\t' + node1_values[1] + '\t' +
        node1_values[2] + '\t' + node1_values[3] + '\t' + ';' + '\n'
        for i in range(len(new_node_IDs))]

    # NOVI `PIPES` - B L O K !!!
    new_blok_2 = blok_2_start + blok_2_new_nodes + blok_2_end

    # BLOK_6 - coordinates
    # Indeksi cvorova odabrane cevi u bloku coordinates - blok_6
    pom_index_coord_1 = blok_6.index(
        [i for i in blok_6 if i[:17] == pipe_node1][0])
    # pom_index_coord_2 = blok_6.index([i for i in blok_6 if i[:17] == pipe_node2][0])

    # Pravimo pod-blokove bloka_6 da bi ubacili kordinate novih cvorova
    blok_6_start = blok_6[: pom_index_coord_1 + 1]
    # Treba da napravimo novi blok cvorova-koordinata izmedju ova dva!
    blok_6_end = blok_6[pom_index_coord_1 + 1:]

    # Koordinate prvog-cvorova odabrane cevi
    coord_node1 = [i for i in blok_6 if i[:17] == pipe_node1][0]
    coord_node1 = coord_node1.split('\t')
    coord_node1 = [float(coord_node1[1]), float(
        coord_node1[2])]  # lista koordinata 1.cvora

    # Koordinate drugog-cvorova odabrane cevi
    coord_node2 = [i for i in blok_6 if i[:17] == pipe_node2][0]
    coord_node2 = coord_node2.split('\t')
    coord_node2 = [float(coord_node2[1]), float(
        coord_node2[2])]  # lista koordinata 2.cvora

    # Lista novih koordinata cvorova - Moraju se kasnije prebaciti u String-tip
    new_nodes_coord = uf.coordFun(coord_node1, coord_node2, pipe_segments)
    # treba srediti broj karaktera Stringova,
    new_nodes_coord = [[str(i[0]), str(i[1])] for i in new_nodes_coord]
    new_nodes_coord = [[uf.string_len_corection(i[0], 16), uf.string_len_corection(
        i[1], 16)] for i in new_nodes_coord]  # sredjeni i karakteri

    # Pravljenje bloka novih koordinata cvorova
    # p - pomocna promenljiva u kojoj se nalazi ID 1.cvora, samo tekst bez pranih polja...
    p = pipe_node1.split()[0]
    # ...zato koristimo .split()[0] -> uzimamo 0-ti clan jer vraca listu.

    # lista novih ID-eva cvorova
    new_node_IDs = [" " + p + "_" + str(i) for i in range(1, br_cvorova + 1)]
    # Korekcija broja karaktera ID-eva
    new_node_IDs = [uf.string_len_corection(i, 17) for i in new_node_IDs]

    # Shema Stringa u coordinates bloku:
    # ' S1              \t1624.15         \t7653.06         \n'
    # Pravimo Blok za nove cvorove na isti nacin.
    blok_6_new_nodes = [new_node_IDs[i] + '\t' + new_nodes_coord[i][0] + '\t' + new_nodes_coord[i][1] + '\n' for i in
                        range(len(new_node_IDs))]

    # NOVI coordinates  - B L O K !!!
    new_blok_6 = blok_6_start + blok_6_new_nodes + blok_6_end

    # BLOK_4 - pipes
    # Shema pipes Blok - vrste:
    # ' C1              \tS1              \tS2              \t800         \t75          \t0.0015      \t0           \tOpen  \t;\n'

    # ID odabrane cevi - sredjujemo String da bi uspesno dodali nove ID-eve
    pipe_id = pipe['ID'].split()[0]
    pipe_id = " " + pipe_id

    # ID-evi novih cevi
    new_pipe_IDs = [uf.string_len_corection(
        pipe_id + "_" + str(i), 17) for i in range(1, pipe_segments + 1)]

    # i[1:17] -> uzimamo od `1` jer izbacujemo prvi karakter koji je jednak `space`, za ovaj blok ne ide `space` za ID...
    new_pipe_nodes_ID = [uf.string_len_corection(
        i[1:17], 16) for i in blok_6_new_nodes]

    # Dodamo i postojece ID-eve cvorova odabrane cevi
    new_pipe_nodes_ID = [pipe['Node1']] + new_pipe_nodes_ID + [pipe['Node2']]

    # Pravimo parove cvorova za svaku novu cev
    parovi_node_ID = [[new_pipe_nodes_ID[i - 1], new_pipe_nodes_ID[i]]
                      for i in range(1, len(new_pipe_nodes_ID))]

    # Duzina cevi
    pipe_length = float(pipe['Length'])

    # Precnik cevi
    pipe_diameter = float(pipe['Diameter'])

    # Podjednaka duzina svakog segmenta nove cevi
    dL_pipe = round(pipe_length / float(pipe_segments), 2)
    dL_pipe = uf.string_len_corection(str(dL_pipe), 12)

    test_index = [i for i in blok_4 if i[:17]
                  == uf.string_len_corection(pipe_id, 17)][0]
    pipe_index = blok_4.index(test_index)

    # Pravimo pod-blokove bloka_4 da bi ubacili nove cevi
    blok_4_start = blok_4[: pipe_index]
    # Treba da napravimo novi blok cevi izmedju ova dva!
    blok_4_end = blok_4[pipe_index + 1:]

    # Slican fajl kao pipe_data samo je u pitanju String a ne Lista
    pipe_data_0 = [i for i in blok_4 if i[:17] == id_pipe][0]

    # Precnik se smanjuje za svaki novi segment cevi
    # ID, Node1, Node2, Length, Diameter, Roughness, MinorLoss, Status
    blok_4_new_pipes = [f"\
    {new_pipe_IDs[i]}\t\
    {parovi_node_ID[i][0]}\t\
    {parovi_node_ID[i][1]}\t\
    {dL_pipe}\t\
    {uf.string_len_corection(str(pipe_diameter), 12)}\t\
    {pipe_data_0[78:90]}\t\
    {pipe_data_0[91:103]}\t\
    {pipe_data_0[104:110]}\t;\n" for i in range(len(new_pipe_IDs))]

    # NOVI pipes  - B L O K !!!
    new_blok_4 = blok_4_start + blok_4_new_pipes + blok_4_end

    # NOVI EPANET-FILE
    new_inp_file = blok_1 + new_blok_2 + blok_3 + \
        new_blok_4 + blok_5 + new_blok_6 + blok_7

    new_f_path = f_path[:-4] + "_Pipe_Leak" + ".inp"

    with open(new_f_path, 'w') as f:
        f.writelines(new_inp_file)

    # enapi.closefile()
    enapi.openepafile(new_f_path)  # Otvaramo novoformirani fajl nad kojim simuliramo
    # otaz i sagledavamo posledice preko pritisaka,
    # brzine, protoka,...

    # Ovo je samo radi kontrole, moze da se smisli nesto bolje
    print(new_f_path)


# Curenje rezervoara - tankleakfail
def tankleakfail(f_path, id_tank, tank_leak):  # ! Sredjeno - TESTIRATI
    """
        tankleakfail(f_path, id_tank, tank_leak)
        :param f_path:     Putanja fajla
        :param id_tank:    Naziv rezervoara
        :param tank_leak:  Curenje iz tanka, kroz dodatni cvor preko "Base Demand" atributa.
        :return: Ne vraca vrednost -> Pravi novi fajl koji ucitavamo i simuliramo otkaz

        """
    # 1 - Otvaranje fajla i formiranje liste podataka...
    with open(f_path) as f:
        s = f.readlines()

    coord_blok = uf.epa_blok(s, 'coordinates')

    # String sa podacima o koordinatama rezervoara
    coord_data = [i for i in coord_blok if id_tank in i][0]

    # Koordinate tacke rezervoara
    x = round(float(coord_data[18:34]), 2)
    y = round(float(coord_data[35:51]), 2)

    # Formiranje koordinata tacaka novog cvora - proizvoljno uvecanje = 500 mernih jedinica
    x_cvora = round(x + 100, 2)
    y_cvora = round(y + 100, 2)

    # Tank Elevation
    enapi.openepafile(f_path)
    tank_elev = tankelevation(enapi.getIndex('node', id_tank))[0]
    enapi.closefile()

    # 2 - Kreiranje novog cvora, blokova i smestanje u novi fajl
    # BLOKOVI
    blok1 = uf.epa_blok2blok(s, 'title', 'junctions')
    blok2 = uf.epa_blok(s, 'junctions')
    blok3 = uf.epa_blok2blok(s, 'reservoirs', 'pipes')
    blok4 = uf.epa_blok(s, 'pipes')
    blok5 = uf.epa_blok2blok(s, 'pumps', 'coordinates')
    blok6 = uf.epa_blok(s, 'coordinates')
    blok7 = uf.epa_blok2blok(s, 'vertices', 'end')
    # blok8 = uf.epa_blok(s, 'end')

    # 3 - Formiranje podataka o novom cvoru
    newID_cvor = id_tank + '_leak'
    # ID, Elevation, Demand, Pattern - nema podataka
    novi_cvor = f"\
    {uf.string_len_corection(' ' + newID_cvor, 17)}\t\
    {uf.string_len_corection(str(tank_elev), 12)}\t\
    {uf.string_len_corection(str(tank_leak), 12)}\t\
    {uf.string_len_corection(' ', 16)}\t;\n"

    # Ubaceni novi cvor u [PIPES] zaglavlje
    new_blok2 = blok2[:-1] + [novi_cvor] + [blok2[-1]]
    # ID, Node1, Node2, Length, Diameter, Roughness, MinorLoss, Status
    nova_cev = f"\
    {uf.string_len_corection(' ' + id_tank + '_pipe', 17)}\t\
    {uf.string_len_corection(id_tank, 16)}\t\
    {uf.string_len_corection(id_tank + '_leak', 16)}\t\
    {uf.string_len_corection(str(100), 12)}\t\
    {uf.string_len_corection(str(75), 12)}\t\
    {uf.string_len_corection(str(0.0015), 12)}\t\
    {uf.string_len_corection(str(0), 12)}\t\
    {uf.string_len_corection('Open', 6)}\t;\n"

    # Ubacena nova cev u [pipes] zaglavlje
    new_blok4 = blok4[:-1] + [nova_cev] + [blok4[-1]]

    nove_coord = f"\
    {uf.string_len_corection(' ' + newID_cvor, 17)}\t\
    {uf.string_len_corection(str(x_cvora), 16)}\t\
    {uf.string_len_corection(str(y_cvora), 16)}\t\n"

    new_blok6 = blok6[:-1] + [nove_coord] + [blok6[-1]]

    new_inp_file = blok1 + new_blok2 + blok3 + \
        new_blok4 + blok5 + new_blok6 + blok7 + ['[END]\n']

    # 4 - Izvoz novoformiranog fajla
    new_f_path = f_path[:-4] + "_Tank_Leak" + ".inp"

    with open(new_f_path, 'w') as f:
        f.writelines(new_inp_file)

    enapi.openepafile(new_f_path)  # Otvaranje novog inp-fajla -> simulacija otkaza

    # Informacija o putanji i imenu novog fajla
    print(new_f_path)


# Zamena rezervoara sa regulatorom pritiska pumpe - reseconomfail
def reseconomfail(f_path, tank_id, pump_id, pipe_id):  # ! Sredjeno - TESTIRATI
    """
    reseconomfail(f_path, res_id, pump_id, pipe_id)

    :param  f_path  : Putanja fajla
    :param  tank_id : ID rezervoara (u EPANET-u je to `TANK` objekat ne `RESERVOIR` !)
    :param  pump_id : ID pumpe na koju vezujemo zatvarac(tipa PRV - regulator pritiska)
    :param  pipe_id : ID nizvodne cevi - moze biti vise nizvodnih cevi u cvoru, nama treba samo jedna,
                                                                            zbog vrednosti PRECNIKA koji kao vrednost dodajemo zatvaracu.

    :return:        Ne vraca vrednost -> Brise Rezervoar i dodaje zatvarac(PRV) koji vezuje za pumpu,
                                         zatim pravi novi fajl nad kojim simuliramo posledice promene strukture sistema.

        """
    # Pomocna funkcija - mean (srednja vrednost) - koristimo da osrednjimo pritiske u cvoru.
    def mean(lsp): return sum(lsp) / len(lsp)

    # 1 - Otvaranje fajla preko epanettools-paketa radi prikupljanja podataka
    #     o pritiscima prvog nizvodnog cvora odabrane pumpe, kote teraena cvora.
    enapi.openepafile(f_path)

    # NIZVODNI CVOR
    cvorovi_pumpe = pumpnodes(pump_id)

    # Trazimo uzvodni cvor za koji je vezana pumpa
    id_uzv_cvor = cvorovi_pumpe[0]
    # [0] -> uzvodni cvor

    # Trazimo nizvodni cvor za koji je vezana pumpa
    id_niz_cvor = cvorovi_pumpe[1]
    # [1] -> nizvodni cvor

    # Koordinate tacaka cvorova
    x1, y1 = uf.getCoord(f_path, id_uzv_cvor)  # Koordinate uzvodnog cvora
    x2, y2 = uf.getCoord(f_path, id_niz_cvor)  # Koordinate nizvodnog cvora

    # Nove koordinate cvora za koji vezujemo zatvarac(PRV)
    x_new, y_new = uf.coordFun([x1, y1], [x2, y2], 2)[0]  # [[x, y]][0] -> [x, y]

    # Nivo nizvodnog cvora, potrebno za formiranje novog cvora
    el_cvora = junctelevation(enapi.getIndex('node', id_niz_cvor))[0]

    # Srednji pritisak u cvoru (za period od 0 do 24h)
    # Zaokruzimo na dve decimale
    psr = round(mean(junctpressure(enapi.getIndex('node', id_niz_cvor))), 2)

    # CEV NIZVODNOG CVORA
    # Precnik cevi nizvodnog cvora -> dodeljujemo zatvaracu.
    pecnik_cevi = pipediameter(enapi.getIndex('link', pipe_id))[0]

    enapi.closefile()  # Zatvaramo fajl

    # 2 - Otvaranje fajla i smestanje podataka u promenljivu `s`,
    #	  radi menjanja strukture fajla

    with open(f_path) as f:
        s = f.readlines()

    # BLOKOVI
    # M -> Modifikacija
    blok1 = uf.epa_blok2blok(s, 'title', 'junctions')
    blok2 = uf.epa_blok(s, 'junctions')                  # M
    blok3 = uf.epa_blok2blok(s, 'reservoirs', 'tanks')
    blok4 = uf.epa_blok(s, 'tanks')                      # M
    blok5 = uf.epa_blok(s, 'pipes')                      # M
    blok6 = uf.epa_blok(s, 'pumps')                      # M
    blok7 = uf.epa_blok(s, 'valves')                     # M
    blok8 = uf.epa_blok2blok(s, 'tags', 'coordinates')
    blok9 = uf.epa_blok(s, 'coordinates')                # M
    blok10 = uf.epa_blok(s, 'vertices')
    # Dodamo i [END] kada formiramo novi fajl.

    # Novi cvor
    # Stringgovi respektivno -> Id, Elevation, Demand, Pattern
    novi_cvor = f"\
        {uf.string_len_corection(' ' + id_niz_cvor + '_novi', 17)}\t\
        {uf.string_len_corection(str(el_cvora), 12)}\t\
        {uf.string_len_corection(str(0), 12)}\t\
        {uf.string_len_corection('', 16)}\t;\n"

    novi_blok2 = blok2[:-1] + [novi_cvor] + [blok2[-1]]

    # Brisanje rezervoara -> [:17] polozaji gde se nalazi vrednost u stringu.
    novi_blok4 = [i for i in blok4 if i[:17] !=
                  uf.string_len_corection(' ' + tank_id, 17)]

    # Brisanje cevi vezane za rezervoar -> [18:34] polozaji gde se nalazi vrednost u stringu.
    novi_blok5 = [i for i in blok5 if tank_id not in i]

    # Menjanje cvorova za koje je pumpa zakacena
    # menjanje_cvora = f"{uf.string_len_corection(id_niz_cvor + '_novi', 16)}\t"

    pump_data = [i for i in blok6 if i[:17] ==
                 uf.string_len_corection(' ' + pump_id, 17)][0]

    new_pump_data =\
        f"{pump_data[:34]}\t{uf.string_len_corection(id_niz_cvor + '_novi', 16)}{pump_data[51:]}"

    # Prvo izbacimo liniju sa pumpom, sa starim cvorom
    novi_blok6 = [i for i in blok6 if i[35:51]
                  != uf.string_len_corection(id_niz_cvor, 16)]
    # Zatim formiramo konacan novi_blok6
    novi_blok6 = novi_blok6[:-1] + [new_pump_data] + [novi_blok6[-1]]

    # ZATVARAC
    # Stringovi respektivno -> ID, Node1, Node2, Diameter, Type, Setting-Pressure, MinorLoss
    zatvarac = f"\
        {uf.string_len_corection(' PRV_zat', 17)}\t\
        {uf.string_len_corection(f'{id_niz_cvor}_novi', 16)}\t\
        {uf.string_len_corection(id_niz_cvor, 16)}\t\
        {uf.string_len_corection(f'{pecnik_cevi}', 12)}\t\
        {uf.string_len_corection('PRV', 4)}\t\
        {uf.string_len_corection(str(psr), 12)}\t\
        {uf.string_len_corection(f'{0}', 12)}\t;\n"

    novi_blok7 = blok7[:-1] + [zatvarac] + [blok7[-1]]

    # KOORDINATE
    # Izbacimo koordinate rezervoara posto smo ga izbrisali iz modela
    novi_blok9 = [i for i in blok9 if i[:17] !=
                  uf.string_len_corection(' ' + tank_id, 17)]
    # Ubacivanje koordinate novog cvora za koji vezujemo kraj pumpe i pocetak zatvaraca.
    nove_coord = f"\
        {uf.string_len_corection(' ' + id_niz_cvor + '_novi', 17)}\t\
        {uf.string_len_corection(str(x_new), 16)}\t\
        {uf.string_len_corection(str(y_new), 17)}\n"

    novi_blok9 = novi_blok9[:-1] + [nove_coord] + [novi_blok9[-1]]

    new_inp_file = \
        blok1 + novi_blok2 + blok3 + novi_blok4 + \
        novi_blok5 + novi_blok6 + novi_blok7 + \
        blok8 + novi_blok9 + blok10 + ['[END]\n']

    new_f_path = f"{f_path[:-4]}_TANK_to_VALVE.inp"

    # Kreiranje novog fajla sa izbrisanim rezervoarom i cevi koja ga spaja i dodavanje PRV zatvaraca
    with open(new_f_path, 'w') as f:
        f.writelines(new_inp_file)

    enapi.openepafile(new_f_path)  # Otvaranje novog inp-fajla -> simulacija otkaza

    print(new_f_path)

# Pojava korene mase (korenja) na nekoj duzini cevi


def swmmRM(f_path, id_conduit, L1, L2, parametar):  # ! Sredjeno - TESTIRATI
    """
    :param  f_path     : string - Putanja fajla
    :param  id_conduit : string - ID - cevi
    :param  L1         : number - Duzina od koje se javlja korenje
    :param  L2         : number - Duzina do koje se javlja korenje
    :param  parametar  : number - Procenat umanjenja MaxDepth - dubine popune cevi (npr. 30% manja 'MaxDepth')
    :return            : Ne vraca vrednost -  pravi novi, modifikovani swmm-inp fajl.
    """

    # Smestanje podataka inp-fajla u Dictionary-tip
    swmodel = uf.swDict(f_path)

    # [CONDUITS] - Vrednosti atributa odabrane cevi
    uzvCvor = swmodel['CONDUITS'][id_conduit]['From Node']
    nizCvor = swmodel['CONDUITS'][id_conduit]['To Node']
    condLength = swmodel['CONDUITS'][id_conduit]['Length']
    condRoughness = swmodel['CONDUITS'][id_conduit]['Roughness']
    condInOffset = swmodel['CONDUITS'][id_conduit]['InOffset']
    condOutOffset = swmodel['CONDUITS'][id_conduit]['OutOffset']
    condInitFlow = swmodel['CONDUITS'][id_conduit]['InitFlow']
    condMaxFlow = swmodel['CONDUITS'][id_conduit]['MaxFlow']

    # [XSECTIONS]
    condShape = swmodel['XSECTIONS'][id_conduit]['Shape']
    # Malo je nejasan naziv...tri razlicita imena za istu velicinu.
    condMaxHeight = swmodel['XSECTIONS'][id_conduit]['Geom1']
    condGeom2 = swmodel['XSECTIONS'][id_conduit]['Geom2']
    condGeom3 = swmodel['XSECTIONS'][id_conduit]['Geom3']
    condGeom4 = swmodel['XSECTIONS'][id_conduit]['Geom4']
    condBarrels = swmodel['XSECTIONS'][id_conduit]['Barrels']

    # [PIPES] - Vrednosti atributa uzvodnog cvora cevi
    junctInvert = swmodel['PIPES'][uzvCvor]['Invert']
    junctMaxDepth = swmodel['PIPES'][uzvCvor]['MaxDepth']
    junctInitDepth = swmodel['PIPES'][uzvCvor]['InitDepth']
    junctSurDepth = swmodel['PIPES'][uzvCvor]['SurDepth']
    junctAponded = swmodel['PIPES'][uzvCvor]['Aponded']

    # Kote-dna nizvodnog i uzvodnog cvora
    elv_Uzv = float(junctInvert)
    elv_Niz = float(swmodel['PIPES'][nizCvor]['Invert'])

    # Za unete duzine L1 i L2 formiramo listu novih duzina cevi(prebacujemo cev u vise cevi usled poremecaja...)
    noveduzinecevi = uf.duzineCevi(float(condLength), L1, L2)

    # Slucaj ako je poremecaj na sredini cevi
    if len(noveduzinecevi) != 1:
        # Lista novih ID-eva cevi
        noviIdCevi = [id_conduit + '_' + str(i + 1)
                      for i in range(len(noveduzinecevi))]
        # Lista novih ID-eva cvorova
        noviIdCvorovi = [uzvCvor + '_' + str(i + 1)
                         for i in range(len(noveduzinecevi) - 1)]
        # Lista starih i novih ID-eva cvorova
        noviIdCvorovi = [uzvCvor] + noviIdCvorovi + [nizCvor]

        # Pakovanje NOVIH cevi u Dictionary swmodel
        for i in range(len(noviIdCevi)):
            # [CONDUITS]
            # Prvo mora da se napravi novi pod-dictionary za novu cev.
            swmodel['CONDUITS'][noviIdCevi[i]] = {}
            swmodel['CONDUITS'][noviIdCevi[i]
                                ]['From Node'] = noviIdCvorovi[i]   # Menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]
                                ]['To Node'] = noviIdCvorovi[i + 1]  # Menja se vrednost
            # Menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['Length'] = noveduzinecevi[i]
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['Roughness'] = condRoughness
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['InOffset'] = condInOffset
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['OutOffset'] = condOutOffset
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['InitFlow'] = condInitFlow
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['MaxFlow'] = condMaxFlow

            # [XSECTIONS]
            swmodel['XSECTIONS'][noviIdCevi[i]] = {}
            swmodel['XSECTIONS'][noviIdCevi[i]]['Shape'] = condShape

            # MaxDepth(Geom1) menjam za deo cevi gde je nastao poremecaj
            # Deo cevi gde se javlja poremecaj
            if noveduzinecevi[i] == (L2 - L1):
                swmodel['XSECTIONS'][noviIdCevi[i]]['Geom1'] = \
                    round(float(condMaxHeight) * (1 - parametar / 100.), 2)
            else:
                # Ako nije, vrednost ostaje ista
                swmodel['XSECTIONS'][noviIdCevi[i]]['Geom1'] = condMaxHeight

            swmodel['XSECTIONS'][noviIdCevi[i]]['Geom2'] = condGeom2
            swmodel['XSECTIONS'][noviIdCevi[i]]['Geom3'] = condGeom3
            swmodel['XSECTIONS'][noviIdCevi[i]]['Geom4'] = condGeom4
            swmodel['XSECTIONS'][noviIdCevi[i]]['Barrels'] = condBarrels

        # [PIPES]
        # Visina izmedju uzvodnog i nizvodnog cvora cevi.
        H = abs(elv_Uzv - elv_Niz)
        I = H / float(condLength)  # Nagib linije izmedju dve tacke

        # Pomocmi niz sa sume duzina cevi, potreban zbog racunanja koda dna cvora
        suma_L = [sum(noveduzinecevi[0:i])
                  for i in range(1, len(noveduzinecevi) + 1)]

        # Lista kota novih cvorova.
        # elev_novihcvorova = [round(elv_Uzv - (H * i / float(condLength)), 2) for i in suma_L]

        elev_novihcvorova = [round(elv_Uzv - (I * i), 2) for i in suma_L]

        # [1:-1] -> Bez uzvodnog i nizvodnog cvora cevi, oni su vec u modelu
        for i in range(1, len(noviIdCvorovi) - 1):
            swmodel['PIPES'][noviIdCvorovi[i]] = {}
            swmodel['PIPES'][noviIdCvorovi[i]
                             ]['Invert'] = elev_novihcvorova[i - 1]  # Menja se vrednost
            swmodel['PIPES'][noviIdCvorovi[i]]['MaxDepth'] = junctMaxDepth
            swmodel['PIPES'][noviIdCvorovi[i]]['InitDepth'] = junctInitDepth
            swmodel['PIPES'][noviIdCvorovi[i]]['SurDepth'] = junctSurDepth
            swmodel['PIPES'][noviIdCvorovi[i]]['Aponded'] = junctAponded

        # Posto je uneta cev zamenjena sa novim cevima, moramo je obrisati iz [CONDUIT]-bloka
        del (swmodel['CONDUITS'][id_conduit])
        del (swmodel['XSECTIONS'][id_conduit])

        # [COORDINATES] - Ubacivanje novih Cvorova i njihovih koordinata
        coordUzvCvor = [float(swmodel['coordinates'][uzvCvor]['X-Coord']),
                        float(swmodel['coordinates'][uzvCvor]['Y-Coord'])]
        coordNizCvor = [float(swmodel['coordinates'][nizCvor]['X-Coord']),
                        float(swmodel['coordinates'][nizCvor]['Y-Coord'])]

        noveCoordCvorova = round(
            uf.coordFun(coordUzvCvor, coordNizCvor, len(noviIdCevi)), 2)

        for i in range(1, len(noviIdCvorovi) - 1):
            swmodel['coordinates'][noviIdCvorovi[i]] = {}
            swmodel['coordinates'][noviIdCvorovi[i]
                                   ]['X-Coord'] = noveCoordCvorova[i - 1][0]
            swmodel['coordinates'][noviIdCvorovi[i]
                                   ]['Y-Coord'] = noveCoordCvorova[i - 1][1]

    # PAKOVANJE NOVOG FAJLA KADA MODIFIKUJEMO SWMM-ulazni fajl
    # Pakovanje [coordinates] - bloka za novi fajl
    idCvorova = [i for i in swmodel['coordinates'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idCvorova.sort()

    newCoordBlokData = [f"\
            {uf.string_len_corection(i, 17)}\
            {uf.string_len_corection(str(swmodel['coordinates'][i]['X-Coord']), 19)}\
            {uf.string_len_corection(str(swmodel['coordinates'][i]['Y-Coord']), 18)}"
                        for i in idCvorova]

    newCoordBlokData = swmodel['coordinates']['ZAGLAVLJE'] + \
        newCoordBlokData + ['\n']

    # Pakovanje [CONDUITS] - bloka za novi fajl
    idCevi = [i for i in swmodel['CONDUITS'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idCevi.sort()

    newConduitBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['From Node']), 17)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['To Node']), 17)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['Length']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['Roughness']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['InOffset']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['OutOffset']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['InitFlow']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['MaxFlow']), 10)}\n" for i in idCevi]

    newConduitBlokData = swmodel['CONDUITS']['ZAGLAVLJE'] + \
        newConduitBlokData + ['\n']

    # Pakovanje XSECTIONS - bloka za novi fajl
    idXsections = [i for i in swmodel['XSECTIONS'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idXsections.sort()

    newXsectionBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Shape']), 13)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom1']), 17)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom2']), 11)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom3']), 11)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom4']), 11)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Barrels']), 21)}\n" for i in idXsections]

    newXsectionBlokData = swmodel['XSECTIONS']['ZAGLAVLJE'] + \
        newXsectionBlokData + ['\n']

    # Pakovanje PIPES - bloka za novi fajl
    idJunctions = [i for i in swmodel['PIPES'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idJunctions.sort()

    newJunctionBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['Invert']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['MaxDepth']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['InitDepth']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['SurDepth']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['Aponded']), 10)}\n" for i in idJunctions]

    newJunctionBlokData = swmodel['PIPES']['ZAGLAVLJE'] + \
        newJunctionBlokData + ['\n']

    # Zaglavlja koja nismo modfikovali
    zag_tip1 = ['TITLE', 'OPTIONS', 'EVAPORATION', 'RAINGAGES', 'SUBCATCHMENTS', 'SUBAREAS', 'INFILTRATION',
                'OUTFALLS', 'TIMESERIES', 'REPORT', 'tags', 'MAP', 'vertices', 'Polygons', 'SYMBOLS']

    # zag_tip2 = [i for i in swmodel.keys() if i not in zag_tip1]

    # Formiramo listu blokova (blokovi_0) koju nismo modifikovali
    pom_0 = [swmodel[i] for i in zag_tip1]

    blokovi_0 = pom_0[0]
    for i in range(1, len(pom_0)):
        blokovi_0 = blokovi_0 + pom_0[i]

    # Podaci za novi fajl
    novi_swmm_file = blokovi_0 + newJunctionBlokData + \
        newConduitBlokData + newXsectionBlokData + newCoordBlokData

    novi_f_path = f"{f_path[:-4]}_swmm_RM.inp"

    with open(novi_f_path, 'w') as f:
        f.writelines(novi_swmm_file)

    print(novi_f_path)


# Deformacija cevi na nekoj duzini                   # ! Sredjeno - TESTIRATI
def swmmD(f_path, id_conduit, L1, L2, parametar):
    """
    :param  f_path     : string - Putanja fajla
    :param  id_conduit : string - ID - cevi
    :param  L1         : number - Duzina od koje se javlja deformacija
    :param  L2         : number - Duzina do koje se javlja deformacija
    :param  parametar  : number - Parametar umanjenjea i uvecanja za pojedine preseke cevi, npr. 20%
    :return            : Ne vraca vrednost -  pravi novi, modifikovani swmm-inp fajl.
    """

    # Smestanje podataka inp-fajla u Dictionary-tip
    swmodel = uf.swDict(f_path)

    # [CONDUITS] - Vrednosti atributa odabrane cevi
    uzvCvor = swmodel['CONDUITS'][id_conduit]['From Node']
    nizCvor = swmodel['CONDUITS'][id_conduit]['To Node']
    condLength = swmodel['CONDUITS'][id_conduit]['Length']
    condRoughness = swmodel['CONDUITS'][id_conduit]['Roughness']
    condInOffset = swmodel['CONDUITS'][id_conduit]['InOffset']
    condOutOffset = swmodel['CONDUITS'][id_conduit]['OutOffset']
    condInitFlow = swmodel['CONDUITS'][id_conduit]['InitFlow']
    condMaxFlow = swmodel['CONDUITS'][id_conduit]['MaxFlow']

    # [XSECTIONS]
    condShape = swmodel['XSECTIONS'][id_conduit]['Shape']
    # Malo je nejasan naziv...tri razlicita imena za istu velicinu.
    condMaxHeight = swmodel['XSECTIONS'][id_conduit]['Geom1']
    condGeom2 = swmodel['XSECTIONS'][id_conduit]['Geom2']
    condGeom3 = swmodel['XSECTIONS'][id_conduit]['Geom3']
    condGeom4 = swmodel['XSECTIONS'][id_conduit]['Geom4']
    condBarrels = swmodel['XSECTIONS'][id_conduit]['Barrels']

    # [PIPES] - Vrednosti atributa uzvodnog cvora cevi
    junctInvert = swmodel['PIPES'][uzvCvor]['Invert']
    junctMaxDepth = swmodel['PIPES'][uzvCvor]['MaxDepth']
    junctInitDepth = swmodel['PIPES'][uzvCvor]['InitDepth']
    junctSurDepth = swmodel['PIPES'][uzvCvor]['SurDepth']
    junctAponded = swmodel['PIPES'][uzvCvor]['Aponded']

    # Kote-dna nizvodnog i uzvodnog cvora
    elv_Uzv = float(junctInvert)
    elv_Niz = float(swmodel['PIPES'][nizCvor]['Invert'])

    # Za unete duzine L1 i L2 formiramo listu novih duzina cevi(prebacujemo cev u vise cevi usled poremecaja...)
    noveduzinecevi = uf.duzineCevi(float(condLength), L1, L2)

    # Slucaj ako je poremecaj na sredini cevi
    if len(noveduzinecevi) != 1:
        # Lista novih ID-eva cevi
        noviIdCevi = [
            f"{id_conduit}_{i + 1}" for i in range(len(noveduzinecevi))]
        # Lista novih ID-eva cvorova
        noviIdCvorovi = [
            f"{uzvCvor}_{i + 1}" for i in range(len(noveduzinecevi) - 1)]
        # Lista starih i novih ID-eva cvorova
        noviIdCvorovi = [uzvCvor] + noviIdCvorovi + [nizCvor]

        # Pakovanje NOVIH cevi u Dictionary swmodel
        for i in range(len(noviIdCevi)):
            # [CONDUITS]
            # Prvo mora da se napravi novi pod-dictionary za novu cev.
            swmodel['CONDUITS'][noviIdCevi[i]] = {}
            # Menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['From Node'] = noviIdCvorovi[i]
            swmodel['CONDUITS'][noviIdCevi[i]
                                ]['To Node'] = noviIdCvorovi[i + 1]  # Menja se vrednost
            # Menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['Length'] = noveduzinecevi[i]
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['Roughness'] = condRoughness
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['InOffset'] = condInOffset
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['OutOffset'] = condOutOffset
            # Ne menja se vrednost
            swmodel['CONDUITS'][noviIdCevi[i]]['InitFlow'] = condInitFlow
            swmodel['CONDUITS'][noviIdCevi[i]]['MaxFlow'] = condMaxFlow

            # [XSECTIONS]
            # swmodel['XSECTIONS'][noviIdCevi[i]] = {}

            if noveduzinecevi[i] == (L2 - L1):

                if condShape == 'CIRCULAR':
                    swmodel['XSECTIONS'][noviIdCevi[i]] = {}
                    swmodel['XSECTIONS'][noviIdCevi[i]
                                         ]['Shape'] = 'HORIZ_ELLIPSE'
                    swmodel['XSECTIONS'][noviIdCevi[i]
                                         ]['Geom1'] = condMaxHeight
                    # Uvecamo za 20% jer za ovaj tip cevi ovaj parametar mora biti veci od "Geom1"
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom2'] = \
                        round(float(condMaxHeight) * (1 + parametar / 100.), 2)
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom3'] = condGeom3
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom4'] = condGeom4
                    swmodel['XSECTIONS'][noviIdCevi[i]
                                         ]['Barrels'] = condBarrels

                elif condShape == 'ARCH':
                    swmodel['XSECTIONS'][noviIdCevi[i]] = {}
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Shape'] = 'ARCH'
                    # Umanjimo visinu za neki procenat - ovde 20%
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom1'] = \
                        round(float(condMaxHeight) * (1 - parametar / 100.), 2)
                    # Uvecamo za 20% jer za ovaj tip cevi ovaj parametar mora biti veci od "Geom1"
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom2'] = \
                        round(float(condMaxHeight) * (1 + parametar / 100.), 2)
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom3'] = condGeom3
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom4'] = condGeom4
                    swmodel['XSECTIONS'][noviIdCevi[i]
                                         ]['Barrels'] = condBarrels

                elif condShape == 'RECT_OPEN':
                    swmodel['XSECTIONS'][noviIdCevi[i]] = {}
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Shape'] = 'RECT_OPEN'
                    # Umanjimo visinu za neki procenat - ovde 20%
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom1'] = \
                        round(float(condMaxHeight) * (1 - parametar / 100.), 2)
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom2'] = condGeom2
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom3'] = condGeom3
                    swmodel['XSECTIONS'][noviIdCevi[i]]['Geom4'] = condGeom4
                    swmodel['XSECTIONS'][noviIdCevi[i]
                                         ]['Barrels'] = condBarrels

            else:
                swmodel['XSECTIONS'][noviIdCevi[i]] = {}
                swmodel['XSECTIONS'][noviIdCevi[i]
                                     ]['Shape'] = condShape  # Ovaj deo menjamo
                swmodel['XSECTIONS'][noviIdCevi[i]]['Geom1'] = condMaxHeight
                swmodel['XSECTIONS'][noviIdCevi[i]]['Geom2'] = condGeom2
                swmodel['XSECTIONS'][noviIdCevi[i]]['Geom3'] = condGeom3
                swmodel['XSECTIONS'][noviIdCevi[i]]['Geom4'] = condGeom4
                swmodel['XSECTIONS'][noviIdCevi[i]]['Barrels'] = condBarrels

        # [PIPES]
        # Visina izmedju uzvodnog i nizvodnog cvora cevi.
        H = abs(elv_Uzv - elv_Niz)
        I = H / float(condLength)  # Nagib linije izmedju dve tacke

        # Pomocmi niz sa sume duzina cevi, potreban zbog racunanja koda dna cvora
        suma_L = [sum(noveduzinecevi[0:i])
                  for i in range(1, len(noveduzinecevi) + 1)]

        elev_novihcvorova = [round(elv_Uzv - (I * i), 2) for i in suma_L]

        # [1:-1] -> Bez uzvodnog i nizvodnog cvora cevi, oni su vec u modelu
        for i in range(1, len(noviIdCvorovi) - 1):
            swmodel['PIPES'][noviIdCvorovi[i]] = {}
            swmodel['PIPES'][noviIdCvorovi[i]
                             ]['Invert'] = elev_novihcvorova[i - 1]  # Menja se vrednost
            swmodel['PIPES'][noviIdCvorovi[i]]['MaxDepth'] = junctMaxDepth
            swmodel['PIPES'][noviIdCvorovi[i]]['InitDepth'] = junctInitDepth
            swmodel['PIPES'][noviIdCvorovi[i]]['SurDepth'] = junctSurDepth
            swmodel['PIPES'][noviIdCvorovi[i]]['Aponded'] = junctAponded

        # Posto je uneta cev zamenjena sa novim cevima, moramo je obrisati iz [CONDUIT]-bloka
        del (swmodel['CONDUITS'][id_conduit])
        del (swmodel['XSECTIONS'][id_conduit])

        # [coordinates] - Ubacivanje novih Cvorova i njihovih koordinata
        coordUzvCvor = [float(swmodel['coordinates'][uzvCvor]['X-Coord']),
                        float(swmodel['coordinates'][uzvCvor]['Y-Coord'])]
        coordNizCvor = [float(swmodel['coordinates'][nizCvor]['X-Coord']),
                        float(swmodel['coordinates'][nizCvor]['Y-Coord'])]

        noveCoordCvorova = round(
            uf.coordFun(coordUzvCvor, coordNizCvor, len(noviIdCevi)), 2)

        for i in range(1, len(noviIdCvorovi) - 1):
            swmodel['coordinates'][noviIdCvorovi[i]] = {}
            swmodel['coordinates'][noviIdCvorovi[i]
                                   ]['X-Coord'] = noveCoordCvorova[i - 1][0]
            swmodel['coordinates'][noviIdCvorovi[i]
                                   ]['Y-Coord'] = noveCoordCvorova[i - 1][1]

    # PAKOVANJE NOVOG FAJLA KADA MODIFIKUJEMO SWMM-ulazni fajl
    # Pakovanje [coordinates] - bloka za novi fajl
    idCvorova = [i for i in swmodel['coordinates'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idCvorova.sort()

    newCoordBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['coordinates'][i]['X-Coord']), 19)}\
        {uf.string_len_corection(str(swmodel['coordinates'][i]['Y-Coord']), 18)}\n" for i in idCvorova]

    newCoordBlokData = swmodel['coordinates']['ZAGLAVLJE'] + \
        newCoordBlokData + ['\n']

    # Pakovanje [CONDUITS] - bloka za novi fajl
    idCevi = [i for i in swmodel['CONDUITS'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idCevi.sort()

    newConduitBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['From Node']), 17)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['To Node']), 17)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['Length']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['Roughness']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['InOffset']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['OutOffset']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['InitFlow']), 11)}\
        {uf.string_len_corection(str(swmodel['CONDUITS'][i]['MaxFlow']), 10)}\n" for i in idCevi]

    newConduitBlokData = swmodel['CONDUITS']['ZAGLAVLJE'] + \
        newConduitBlokData + ['\n']

    # Pakovanje XSECTIONS - bloka za novi fajl
    idXsections = [i for i in swmodel['XSECTIONS'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idXsections.sort()

    # Treba 13-karaktera za `Shape`, ali ne radi mi za HORIZ_ELLIPSE tip
    newXsectionBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Shape']), 14)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom1']), 17)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom2']), 11)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom3']), 11)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Geom4']), 11)}\
        {uf.string_len_corection(str(swmodel['XSECTIONS'][i]['Barrels']), 21)}\n" for i in idXsections]

    newXsectionBlokData = swmodel['XSECTIONS']['ZAGLAVLJE'] + \
        newXsectionBlokData + ['\n']

    # Pakovanje PIPES - bloka za novi fajl
    idJunctions = [i for i in swmodel['PIPES'].keys() if i not in [
        'ZAGLAVLJE', 'ATRIBUTI']]
    idJunctions.sort()

    newJunctionBlokData = [f"\
        {uf.string_len_corection(i, 17)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['Invert']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['MaxDepth']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['InitDepth']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['SurDepth']), 11)}\
        {uf.string_len_corection(str(swmodel['PIPES'][i]['Aponded']), 10)}\n" for i in idJunctions]

    newJunctionBlokData = swmodel['PIPES']['ZAGLAVLJE'] + \
        newJunctionBlokData + ['\n']

    # Zaglavlja koja nismo modfikovali
    zag_tip1 = ['TITLE', 'OPTIONS', 'EVAPORATION', 'RAINGAGES', 'SUBCATCHMENTS', 'SUBAREAS', 'INFILTRATION',
                'OUTFALLS', 'TIMESERIES', 'REPORT', 'tags', 'MAP', 'vertices', 'Polygons', 'SYMBOLS']

    # zag_tip2 = [i for i in swmodel.keys() if i not in zag_tip1]

    # Formiramo listu blokova koju nismo modifikovali
    pom_0 = [swmodel[i] for i in zag_tip1]

    blokovi_0 = pom_0[0]
    for i in range(1, len(pom_0)):
        blokovi_0 = blokovi_0 + pom_0[i]

    novi_swmm_file = blokovi_0 + newJunctionBlokData + \
        newConduitBlokData + newXsectionBlokData + newCoordBlokData

    novi_f_path = f"{f_path[:-4]}_swmm_D.inp"

    with open(novi_f_path, 'w') as f:
        f.writelines(novi_swmm_file)

    print(novi_f_path)

# ==== END =====
