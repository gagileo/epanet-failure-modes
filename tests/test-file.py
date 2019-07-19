# =====================
# TEST - new QH-curv
# =====================

# from epanet_fun import *

# file_path = "NS_Test_Model_1H.inp"
# fid = enapi.openepafile(file_path)

# xy = getQH(fid, '1')
# xy_new = [[i[0]*0.8, i[1]*0.8] for i in xy]

# setQH(fid, '1', xy_new)

# ffid = enapi.openepafile(f"{file_path[:4]}_newQH.inp")
# print(getQH(fid, '1'))
# print(getQH(ffid, '1'))

# ============================================================
from epanet_fun import *

# Open EPANET.inp file
enapi.openepafile("NS_Test_Model_1H.inp")

# Network Info
nnodes = enapi.getCount('node')
nlinks = enapi.getCount('link')



# Close file
enapi.closefile()
