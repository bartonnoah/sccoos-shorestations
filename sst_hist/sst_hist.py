


data_dir = "ELENA TODO" #e.x. '/Users/noahbarton/Documents/shorestations_nonQCed/
stations = (("non-QC'd SIO Shore Station Data.csv", 'SIO Pier'),
            ("non-QC'd San Clemente Shore Station Data.csv", 'San Clemente'),
            ("non-QC'd Newport Beach Shore Station Data.csv", 'Newport Beach'),
            ("non-QC'd Zuma Beach Shore Station Data.csv", 'Zuma Beach'),
            ("non-QC'd Santa Barbara Shore Station Data.csv", 'Santa Barbara'),
            ("non-QC'd Granite Canyon Station Data.csv", 'Granite Canyon'),
            ("non-QC'd Pacific Grove Station Data.csv", 'Pacific Grove'),
            ("non-QC'd Farallon Staion Data.csv", 'SE Farallon Island'),
            ("non-QC'd Trinidad Beach Data.csv", 'Trinidad Beach'),
            ("non-QC'd Trinidad Bay Data.csv", 'Trinidad Bay'))

for station in stations:
    sst_hist(data_dir+station[0], station[1])
