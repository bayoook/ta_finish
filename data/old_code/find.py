from pymongo import MongoClient
from pprint import pprint
from itertools import groupby
from datetime import datetime
import os
client = MongoClient()
db = client['dataSaham']
nama = ["ACES", "ADHI", "ADRO", "ANDI", "ANTM", "APLN", "ASII", "BAPI", "BBCA", "BBNI", "BBRI", "BMRI", "BMTR", "BNLI", "BRMS", "CLEO", "CTRA", "DEAL", "DOID", "ENVY", "ESSA", "FREN", "GGRM", "GIAA", "HMSP", "ICBP", "IMAS", "INDY", "IRRA", "ISAT", "ITMG", "JSKY", "KBLI", "LPPF", "MAIN", "MDIA", "MKNT", "MNCN", "MYRX", "NUSA", "NZIA-W", "POSA", "PPRE", "PSAB", "PTBA", "PURE", "PURE-W", "SIMP", "SMBR", "SMRA", "SQMI", "SRIL", "SWAT", "TMAS", "TRAM", "TRAM-W", "UNVR", "WEGE", "WIKA", "WSBP", "WSKT", "ABBA", "AGRO", "AUTO", "BABP-W3", "BBKP", "BDMN", "BEEF", "BEST", "BJBR", "BNGA", "BRPT", "BSDE", "BTEK", "BUMI", "CASS", "CFIN", "CPIN", "EAST-W", "ELSA", "ENRG", "ESTI", "ETWA", "EXCL", "FILM", "FIRE", "FITT", "FITT-W", "GMFI", "HOKI", "HOME", "HRUM", "INCO", "INDF", "INKP", "INTP", "IPTV", "IPTV-W", "JPFA", "JSMR", "KAYU", "KIAS", "KLBF", "KPIG", "LUCK", "MAMI", "MAPI", "MBAP", "MCOR", "MDKA", "MEDC", "MIKA", "MPMX", "MPPA", "MTDL", "NIKL", "OPMS", "PANR", "PGAS", "POSA-W", "POWR", "PWON", "RALS", "RBMS", "SATU", "SCMA", "SIDO", "SIMA", "SSMS", "TELE", "TINS", "TKIM", "TLKM", "TOTL", "TOWR", "UNTR", "WTON", "AALI", "AKRA", "ASSA", "BBTN", "BHIT", "BJTM", "BKSL", "BTPS", "CLAY", "DMAS", "ERAA", "FOOD", "INDX", "INOV", "ISSP", "JRPT", "KPAL", "LPKR", "MCAS", "PEHA", "POOL", "PTPP", "PTSN", "SAME", "SLIS", "SMSM", "SPTO", "SSIA", "WIIM", "YELO", "ZINC", "BAPI-W", "BGTG", "BTPN", "CENT", "DMMX", "HRME", "IIKP", "INCF", "IPCC", "KIJA", "KOTA-W", "KPAS-W", "KREN", "LSIP", "SMGR", "TARA", "TBIG", "TPIA", "ASRI", "BMSR", "BNBA", "BOGA", "BPTR", "CAMP", "COCO", "DKFT", "DYAN", "IMJS", "ITIC", "KAEF", "KEEN", "MDLN", "MYOR", "PAMG", "PNBS", "PNIN", "PSSI", "PTRO", "PZZA", "ROTI", "AKPI", "BIPI-W", "BOLA", "BTON", "BULL", "DIVA", "DSNG", "FREN-W", "GJTL", "IKAI", "INTD", "IPCM", "JAYA", "MBSS", "MDKI", "MOLI", "NFCX", "NZIA", "RAJA", "RIMO", "VINS-W", "ZONE", "KARW", "PNBN", "PPRO", "TAMU", "TDPM", "ULTJ", "ACST", "BNII", "BWPT", "CARS", "CPRI-W", "DUCK", "EAST", "GTBO", "HEXA", "KRAS", "MFMI", "MLPL", "MLPT", "PADI", "PNLF", "POLL", "SOCI", "TBLA", "TCPI", "TGRA", "ADES", "ARMY", "DLTA", "DWGL", "DWGL-W", "GDST", "GOOD", "MAMI-W", "POLY", "RODA", "SGRO", "URBN-W", "WOOD", "YELO-W", "ADMF", "HKMU", "KINO", "NUSA-W", "PKPK", "WAPO", "WOMF", "BKDP", "FUJI", "GGRP", "JAST", "KKGI", "LPCK", "MERK", "MPRO", "NISP", "OKAS", "PBRX", "SILO", "VIVA", "BSSR", "GLOB", "KOTA", "SKRN", "TFAS", "XIIF", "ARKA", "BSIM", "IMPC", "MMLP", "MTWI", "PANS", "PICO", "SRTG", "APEX", "BRIS", "CTTH", "MLIA", "MSIN", "PCAR", "PRDA", "SKYB", "BVIC", "MARK", "SOTS", "AGII", "CCSI", "CPRI", "KRAH", "LPIN", "MEDC-W", "MPOW", "NRCA", "AKSI", "HELI-W", "JTPE", "LAND", "SMAR", "BAJA", "BCAP", "CAKK", "CAKK-W", "GZCO", "PORT", "SULI", "BKSL-W", "DILD", "MINA", "ARTO", "BOSS", "PBSA", "VOKS", "WEHA", "CMNP", "IKBI", "INPS", "SMKL-W", "SRSN", "IGAR", "TIRT", "UNIT", "ARNA", "BAPA", "INPC", "ADMG", "CASA", "KOBX", "ASMI", "BPFI", "BRPT-W", "EKAD", "ITMA-W", "KIOS", "KPAS", "MLBI", "NATO", "SOSS", "TRIM", "BEEF-W", "CEKA", "DSFI", "HDFA", "NASA", "RISE", "SRAJ", "TIFA", "TNCA", "PRIM-W", "SMDR", "TOPS", "BIRD", "ICON", "MAYA", "INDR", "PANI", "PGLI", "SOTS-W", "ARTA", "KICI", "ASGR", "BIPI", "BUVA", "CSAP", "HEAL", "KBLM", "HDIT", "INDS", "AHAP", "BUKK", "CNTX", "ELTY", "TRUK", "XCIS", "BFIN", "CSIS", "INPC-W", "LTLS", "RANC", "SMCB", "AGRS", "APIC", "LPPS", "TURI", "CLPI", "DIGI", "MGRO", "XIJI", "BISI", "HRTA", "LMAS", "TRIS", "BUDI", "MTPS", "PBID", "DEFI", "DEWA", "CPRO", "EMDE", "SHIP", "BABP", "DVLA", "IPOL", "XIIC", "BCIP", "INAF", "SDPC", "BBYB", "MAPA", "POLA", "TPMA", "TSPC", "BLUE", "BOLT", "VINS", "BACA", "APLI", "RMBA", "UNSP", "FORZ", "GPRA", "IATA", "KMTR", "DFAM", "FPNI", "RICY", "TIRA", "META", "GDYR", "SCCO", "XAFA", "TMPI", "ITMA", "JSPT", "SMMA", "TOTO", "RIGS", "SMMT", "WINS", "AMFG", "INTA", "GSMF", "LPLI", "KOPI", "MTPS-W", "MBTO", "VICO", "DPNS", "SMKL", "RDTX", "XPLQ", "AMIN", "BBHI", "SURE", "SFAN", "TGKA", "MASA", "MARI", "LMPI", "POLI", "CINT", "INPP", "ATIC", "BYAN", "HOTL", "LRNA", "SMDM", "PALM", "TFCO", "NIRO", "PUDP", "R-LQ45X", "AMRT", "BNBR", "ERTX", "JAYA-W", "MTLA", "DAYA", "XPMI", "GEMA", "LINK", "CITY", "CITY-W", "DNET", "ECII", "GMTD", "HOKI-W", "IBFN", "XCID", "BATA", "BRAM", "SIPD", "JAWA", "VRNA", "JIHD", "LION", "DNAR", "PRIM", "WOWS", "PJAA", "MRAT", "SINI-W", "MTRA", "BALI", "DPUM", "UNIC", "SINI", "AKKU", "BEKS", "LEAD", "BIPP", "FORU", "SPMA", "TAXI", "SHID", "MYTX", "PTSP", "SOSS-W", "KDSI", "SMRU", "ASJT", "BIMA", "KJEN", "XIIT", "ALMI", "CITA", "KONI", "MICE", "MYOH", "PEGE", "INCI", "STAR", "MABA", "ANJT", "POLU", "BULL-W2", "PSDN", "ALTO", "NIPS", "ALDO", "WICO", "INAI", "YULE", "URBN", "XASG", "LPGI", "XISR", "SAFE", "DGIK", "MFIN", "ASRM", "HADE", "HELI", "MTFN", "PSKT", "IBFN-W", "ALKA", "FINN", "CANI", "BELL", "NOBU", "SONA", "BKSW", "SFAN-W", "TRUS", "LCKM", "IDPR", "OCAP", "TBMS", "GAMA", "LIFE", "FAST", "BSIM-W3", "SDMU", "BLTA", "SDRA", "ARTI", "CNKO", "FMII", "MAGP", "PYFA", "BMAS", "YPAS", "FIRE-W", "MEGA", "MREI", "NICK", "COWL", "HITS", "JGLE", "FASW", "BINA", "INRU", "PRAS", "XSBC", "XBNI", "TOBA", "OMRE", "MGNA", "RELI", "TCID", "MAPB", "BLTZ", "AMAG", "APII", "LAPD", "GWSA", "BBLD", "INTA-W", "KBLV", "MYRXP", "NELY", "TUGU", "HERO", "SAPX", "PDES", "SKBM", "DSSA", "TMPO", "COCO-W", "BIKA", "LMSH", "XIPI", "XISI", "POLA-W", "MIRA", "XPFT", "RUIS", "BOGA-W", "NATO-W", "OASA", "XKIV", "TALF", "MTSM", "TRST", "DART", "ASBI", "PLIN", "BULL-W", "KIOS-W", "GHON", "XIHD", "BBRM", "MDRN", "XBID", "XBLQ", "GOLD", "DEAL-W", "MKPI", "IBST", "EPMT", "ESIP-W", "ESIP", "MSKY", "XISC", "XAQA", "ABMM", "CASA-W", "XBSK", "KOIN", "DUTI", "XPID", "TEBE", "XSSI", "BAYU", "BRNA", "FISH", "BBMD", "JKON", "XMIG", "ARII", "SUPR", "KEJU", "PSGO", "XDIF", "BPII", "SKLT", "ASDM", "XCLQ", "GREN", "SSTM", "XPTD", "MIDI", "EMTK", "PTIS", "JMAS", "AGAR", "XPDV", "IFSH", "BABP-W4", "REAL", "REAL-W", "BABP-R", "ZBRA", "XNVE", "HDFA-R", "TRIS-R", "IFII", "TRIS-W", "NASA-W", "MAYA-R", "PNSE", "BORN", "DFAM-W", "STTP", "PMJS", "XMTS"]
# cursor = db.data.find({'date': '18122019'})
cursor = list(db.data.find({'date': '19122019'}))
cursor.sort(key=lambda y: y['name'])
for k, v in groupby(cursor, key=lambda y: y['name']):
    v1 = list(v)
    if k == 'APLN' or k == 'WSBP' or k == 'BRIS' or k == 'BHIT' or k == 'BWPT' or k == 'DMAS' or k == 'VIVA' or k == 'WIIM' or k == 'WTON':
        print(k, len(v1), v1[0]['data']['open'])
        x = os.popen('cat data/order/order_18122019.txt | grep ' + k).read()
        x = x.splitlines()
        for y in x:
            y = y.split(' ')
            dt = datetime.fromtimestamp(int(y[2][:-2])/1000)
            s = ''
            if y[1] == '1':
                s = 'sell'
            elif y[1] == '2':
                s = 'buy'
            try:
                print(dt, s, y[3], y[4], y[5], y[6], y[7], y[8])
            except:
                pass
        
        # print(x)


"""
APLN
# WSBP
BRIS
BHIT
BWPT
DMAS
# VIVA
WIIM
WTON
"""