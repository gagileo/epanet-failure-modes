
# ***********************************************************************************************************************
#   PACKAGE:         epanet_api - Package of simplified functions of epanettools module
#
#   VERZIJA:         1.0         |  1.1
#   DATUM(d/m/y):    2016/11/15  |  2019/07/10
#
#   AUTOR:           Dragan Babic - Gagi
#   INFO:            This package is a part of MSc thesis:
#                    "Modeling failures in water & sewage systems, with EPANET & Python (2016)"
#
#   List of simplified functions:
#
#   getCount         - returns number of objects in the network
#   getIndex         - returns index-number of object for given ID
#   getID            - returns ID from given object index
#   getType          - returns type of an object(Pipe, Pump, Junction,...)
#   getValue         - returns value(s) for NODE(s) or LINK(s) of all network or for specific object(NODE or LINK)
#   setValue         - changing parameter value(i.e. EN_DIAMETER,..) of object in network
#   getPump          - returns dictionary pump IDs and their indexes({'pump1': pumpindex1, 'pump2': pumpindex2, ...})
# ***********************************************************************************************************************


# Import module
import epanettools.epanet2 as epa
import pandas as pd
import easygui as gui                     # za otvaranje fajla

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#  ::: GENERAL FUNCTIONS - for LINK and NODE objects :::  #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def openepafile(inp_file_path=''):  # ! Sredjeno - TESTIRATI -> RADI
    """
    :param  inp_file_path = '' : string - Ako ne unesemo putanju, otvara se `dialog-box` da odaberemo .inp-fajl.
    :return                    : Ne vraca nista

    :info:
    Otvaranje EPANET inp-fajla.
    Bilo bi JAKO korisno da se vrednost ove f-je sacuva u nekoj varijabli,
    zato sto putanju fajla koriste neke funkcije kao parametar,
    kao npr f-ja getQH(file_path)...

    :primer:
    epanetfilepath = openepafile()
    """

    if inp_file_path == '':
        # pretvaramo u `string` zato sto je u `unicode-u` ('uPAnekitext')
        epanetfile = str(gui.fileopenbox())

        n = len(epanetfile) - 3
        epa.ENopen(epanetfile, epanetfile[: n] + "rpt", "")

        return epanetfile

    elif inp_file_path != '':

        n = len(inp_file_path) - 3
        epa.ENopen(inp_file_path, inp_file_path[: n] + "rpt", "")

        return inp_file_path


def closefile():  # ! Sredjeno - TESTIRATI
    """
    :return: void - Zatvara EPANET-ov .inp fajl => zatvoren pristup fajlu.

    """
    epa.ENclose()


def tableview(dict_data):  # ! Sredjeno - TESTIRATI
    """
    :param  dict_data : dict or (matrix) - {'key1': lista1, 'key2': lista2, ...} or [[e11, e12,..],[e21, e22,..],..]
    :return           : pandas.DataFrame

    """
    if type(dict_data) == dict:
        return pd.DataFrame(dict_data)
    else:
        data_len = len(dict_data)
        column = [('col' + str(i)) for i in range(1, data_len + 1)]
        return pd.DataFrame(dict(zip(column, dict_data)))


def getCount(network_object):  # ! Sredjeno - TESTIRATI -> RADI
    """
        :param  network_object: string - 'node' ili 'link'
        :return               : int - broj objekata(node ili link) u mrezi

        :info:
        node-objekti: junctions(cvorovi), reservoirs(izvori, ponori), tanks(rezervoari).
        link-objekti: pipes(cevi), pumps(pumpe), valves(zatvaraci)

    """
    number_of_objects = {
        'node': epa.ENgetcount(epa.EN_NODECOUNT)[1],
        'link': epa.ENgetcount(epa.EN_LINKCOUNT)[1]
    }

    return number_of_objects[network_object]


def getIndex(network_object, id_objekta):  # ! Sredjeno - TESTIRATI -> RADI
    """
        :param  network_object: string - 'node' ili 'link'
        :param  id_objekta    : string - ID objekta
        :return               : int - vraca broj index-a .

        :info:
        EPANET broji od 1(jedinice) ne kao Python od 0(nule),
        ovo je vazno ukoliko koristimo npr. range f-ju u `Python`, pisemo range(1,...),
        ne range(0,...).

        :Primer:
        Ukoliko hocemo da dobijemo listu NODE-Index-a, sledi code:
        map(lambda x: getIndex('node', x), lista_id-eva)
        ili
        [getIndex('node', i) for i in lista_id-eva]
        Isto je za LINK-ove...

    """
    object_index = {
        'node': epa.ENgetnodeindex(id_objekta)[1],
        'link': epa.ENgetlinkindex(id_objekta)[1]
    }

    return object_index[network_object]


def getID(network_object, object_index):  # ! Sredjeno - TESTIRATI -> RADI
    """
        :param  network_object: string - 'node' ili 'link'
        :param  object_index  : int - index objekta
        :return               : string - vraca ID objekta .

        :info:
        EPANET broji od 1(jedinice) ne kao Python od 0(nule),
        ovo je vazno ukoliko koristimo range f-ju, pisemo range(1,...),
        ne range(0,...).

        :Primer:
        Ukoliko hocemo da dobijemo listu `node` ID-eva, sledi code:
        map(lambda x: getID('node', x), lista_indeksa)
        ili
        [getID('node', i) for i in lista_indeksa]
        Isto je za `link` ID-eve.

    """
    object_id = {
        'node': epa.ENgetnodeid(object_index)[1],
        'link': epa.ENgetlinkid(object_index)[1]
    }

    return object_id[network_object]


def getType(network_object, object_index):  # ! Sredjeno - TESTIRATI -> RADI
    """
        :param  network_object: string - 'node' ili 'link'
        :param  object_index  : int - index objekta
        :return               : string - vraca tip objekta (npr. Pump) .
    """
    # node - type index
    node_types = {
        '0': 'Junction node',
        '1': 'Reservoir node',
        '2': 'Tank node'
    }

    # link - type index
    link_types = {
        '0': 'Pipe with Check Valve',
        '1': 'Pipe',
        '2': 'Pump',
        '3': 'Pressure Reducing Valve',
        '4': 'Pressure Sustaining Valve',
        '5': 'Pressure Breaker Valve',
        '6': 'Flow Control Valve',
        '7': 'Throttle Control Valve',
        '8': 'General Purpose Valve'
    }

    if network_object == 'link':
        result = link_types[f"{epa.ENgetlinktype(object_index)[1]}"]
        return result
    elif network_object == 'node':
        result = node_types[f"{epa.ENgetnodetype(object_index)[1]}"]
        return result
    else:
        print("Object doesn't exist!")


def getValue(network_object, object_property, object_index=''):   # ! Sredjeno - TESTIRATI -> RADI
    """
        :param  network_object    : string - 'node' ili 'link'
        :param  object_property   : parametar u vidu velicine koju trazimo, pogledaj dole listu parametara za oredjene objekte.
        :param  object_index = '' : int - index objekta, ako ne unesemo broj index-a objekta, izbacuje vrednosti za sve objekte
        :return                   : vraca velicinu(e), u zaviasnosti od unetog `object_index` parametra, NODE-a ili LINK-a 

        *node - properties*
        epa.EN_PRESSURE   - pritisak u cvoru
        epa.EN_HEAD       - piezometrijska kota
        epa.EN_ELEVATION  - apsolutna kota cvora
        epa.EN_BASEDEMAND - potreba za vodom u cvoru
                            itd. pogledaj EPANET-Toolkit-PDF-fajl

        *link - properties*
        epa.EN_FLOW        - protok u cevi
        epa.EN_VELOCITY    - brzina vode u cevi
        epa.EN_INITSTATUS  - inicijalni status (Open ili Closed)
        epa.EN_DIAMETER    - precnik cevi
                             itd. pogledaj EPANET-Toolkit-PDF-fajl

        :info: 
        Vremenski korak podesen je na 1h tj. 3600s !!!
     """

    count_param = {
        'link': epa.EN_LINKCOUNT,
        'node': epa.EN_NODECOUNT
    }

    # Provera da li smo ubacili index objekta.
    if type(object_index) == int:
        nobjects = 1
    else:
        nobjects = epa.ENgetcount(count_param[network_object])[1]

    # Lista indeksa objekata u mrezi
    objects = []
    object_value = []

    id_fun = {
        'link': epa.ENgetlinkid,
        'node': epa.ENgetnodeid
    }

    if type(object_index) == int:
        objects.append(object_index)

    else:
        for index in range(1, nobjects + 1):
            t = id_fun[network_object](index)[1]
            objects.append(t)
            object_value.append([])

    value_fun = {
        'link': epa.ENgetlinkvalue,
        'node': epa.ENgetnodevalue
    }

    # ** Hidraulicki Proracun **
    # Hidraulicki proracun zapocinjemo ovim dvema f-jama.
    epa.ENopenH()
    epa.ENinitH(0)

    time = []

    while True:
        t = epa.ENrunH()[1]

        # Ovaj deo je ubacen kao korekcija jer se javlja BUG u source_code-u
        # Ako je tstep != 3600, petlja ga preskoci, u suprotnom imamo visak podataka!
        if t % 3600 == 0:
            time.append(t)

            # Ako trazimo vrednosti samo jednog objekta
            if nobjects == 1:
                # Retrieve hydraulic results for time t
                # posto EPAnet broji od jedan moramo da uvecamo indeks za 1!
                p = value_fun[network_object](object_index, object_property)[1]
                object_value.append(p)

                # Vremenski Korak - u nasem slucaju svakih = 3600s
                tstep = epa.ENnextH()[1]

            # Ako trazimo vrednosti za celu mrezu
            else:
                # Retrieve hydraulic results for time t
                for i in range(0, len(objects)):
                    # posto EPAnet broji od jedan moramo da uvecamo indeks za 1!
                    p = value_fun[network_object](i + 1, object_property)[1]
                    object_value[i].append(p)

                # Vremenski Korak - u nasem slucaju svakih = 3600s
                tstep = epa.ENnextH()[1]

            if tstep <= 0:
                break

        else:
            tstep = epa.ENnextH()[1]
            if tstep <= 0:
                break
            continue

    epa.ENcloseH()  # Kraj Hidraulickog proracuna.

    return object_value

# POMOCNA_FUNKCIJA - prit_manji_od_nule
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Pomocna f-ja za korigovanje rezultata dobijenih pritisaka u cvoru.
# Ako nema pritiska u cvoru EPANET vraca negativnu vrednost,
# pa radi citljivosti rezultata pretvaramo ih u 0(nulu) tj.nema pritiska.
# prit_manji_od_nule = lambda x: 0 if x < 0 else x
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


def setValue(network_object, object_property, object_index, new_value):   # ! Sredjeno - TESTIRATI
    """
        :param  network_object    : string - 'node' ili 'link'
        :param  object_property   : parametar u vidu funkcije(property), pogledaj dole listu parametara za oredjene objekte.
        :param  object_index = '' : int - index objekta, ako ne unesemo broj index-a objekta, izbacuje vrednosti za sve objekte
        :param  new_value         : number or string - vrednost(zavisno od objekta -> tip podatka) koju menjamo na objektu
        :return                   : void - Namesti unetu vrednost gde treba i to je to.

        :info:
        Dodeljuje Novu Vrednost Odabranog Parametra

        *node - properties*
        epa.EN_ELEVATION
        epa.EN_BASEDEMAND
        epa.EN_TANKLEVEL
        itd. pogledaj EPANET_toolkit_help.pdf - str.56 i 57

        *link - properties*
        epa.EN_INITSETTING ->  Pipe roughness, Initial pump speed, Initial valve setting
        epa.EN_INITSTATUS  ->  1 - Open, 0 - Closed
        epa.EN_DIAMETER
        epa.EN_LENGTH
        itd. pogledaj EPANET_toolkit_help.pdf - str.57
    """

    # Namestanje set_fun promenljive u zavisnosti od tipa objekta.
    set_fun = {
        'link': epa.ENsetlinkvalue,
        'node': epa.ENsetnodevalue
    }

    # Funkcija set_fun ne vraca vrednost, jer samo namesti vrednost parametra,
    # ustvari vrati 0 da je "operacija uspela" :).
    # VAZNO: Ne menja vrednost u izvornom .inp fajlu!

    set_fun[network_object](object_index, object_property, new_value)

# === END ===
