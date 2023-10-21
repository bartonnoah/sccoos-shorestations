#import required libraries
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

def count_nobs(station, mode, filename):
    df = pd.read_csv(filename, usecols = ['SURF_TEMP_C','MONTH','DAY'])
    obs_count = np.count_nonzero(~np.isnan(df.SURF_TEMP_C.values))
    return [str(obs_count), station]

def draw_nobs(nobs):
    obs_count = nobs[0]
    station = nobs[1]
    fig, ax = plt.subplots(figsize=(1,0.1), dpi=400)

    x = np.arange(0, 10, 0.1)
    y = 1

    ax.plot(y, color='blue', label='Sine wave')

    plt.xlim([0, 50])
    plt.ylim([0, 20])

    plt.axis('off')

    plt.annotate(obs_count[0:2]+','+obs_count[2:], fontsize = 85, c='hotpink', xy=(.1,.9), xycoords="axes fraction") #TODO Change to hot pink
    filename = station+'_count'+'.png'
    plt.savefig(filename, bbox_inches='tight', dpi=400)
    
    uncropped = Image.open(filename)
    image_box = uncropped.getbbox()
    cropped = uncropped.crop(image_box)
    cropped.save(filename)

data_dir = "ELENA TODO" #e.x. '/Users/noahbarton/Documents/shorestations_nonQCed/
scripps_SST = count_nobs('scripps', 'SST', data_dir+"non-QC'd SIO Shore Station Data.csv")
san_clemente = count_nobs('san_clemente', 'SST', data_dir+"non-QC'd San Clemente Shore Station Data.csv")
newport = count_nobs('newport', 'SST', data_dir+"non-QC'd Newport Beach Shore Station Data.csv")
zuma = count_nobs('zuma', 'SST', data_dir+"non-QC'd Zuma Beach Shore Station Data.csv")
santa_barbara = count_nobs('santa_barbara', 'SST', data_dir+"non-QC'd Santa Barbara Shore Station Data.csv")
granite = count_nobs('granite', 'SST', data_dir+"non-QC'd Granite Canyon Station Data.csv")
grove = count_nobs('grove', 'SST', data_dir+"non-QC'd Pacific Grove Station Data.csv")
farallons = count_nobs('farallons', 'SST', data_dir+"non-QC'd Farallon Staion Data.csv")
trinidad = count_nobs('trinidad', 'SST', data_dir+"non-QC'd Trinidad Bay Data.csv")

draw_nobs(scripps_SST)
draw_nobs(san_clemente)
draw_nobs(newport)
draw_nobs(zuma)
draw_nobs(santa_barbara)
draw_nobs(granite)
draw_nobs(grove)
draw_nobs(farallons)
draw_nobs(trinidad)
