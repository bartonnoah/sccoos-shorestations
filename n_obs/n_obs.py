#import required libraries
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

def count_nobs(station, mode, *filenames):
    if station == 'trinidad': #Special case: Trinidad Beach & Bay needs to read 2 files
        obs_count = 0
        for filename in filenames:
            skiprows = skip_rows(filename)
            df = pd.read_excel(filename, skiprows=skiprows)
            obs_count += np.count_nonzero(~np.isnan(df.SURF_TEMP_C.values))
    elif station == 'scripps': #Special case: Scripps Pier has SST and SBT
        df = pd.read_csv(filenames[0], skiprows=skiprows)
        if mode == 'SST':
            obs_count = np.count_nonzero(~np.isnan(df.SURF_TEMP_C.values))
        elif mode == 'SBT':
            obs_count = np.count_nonzero(~np.isnan(df.BOT_TEMP_C.values))
    else: #normal cases
        skip_rows = skip_rows(filenames[0])
        df = pd.read_excel(filenames[0], skiprows=skip_rows)
        obs_count = df.shape[0]
    return [str(obs_count), station+mode]

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

    plt.annotate(obs_count[0:2]+','+obs_count[2:], fontsize = 85, c='hotpink', xy=(.1,.9), xycoords="axes fraction")
    filename = station+'.png'
    plt.savefig(filename, bbox_inches='tight', dpi=400)
    
    uncropped = Image.open(filename)
    image_box = uncropped.getbbox()
    cropped = uncropped.crop(image_box)
    cropped.save(filename)

scripps_SST = count_nobs('scripps', 'SST', 'data/')
scripps_SBT = count_nobs('scripps', 'SBT', 'TODO ADD FILE')
san_clemente = count_nobs('san_clemente', 'SST', 'TODO ADD FILE')
newport = count_nobs('newport', 'SST', 'TODO ADD FILE')
zuma = count_nobs('zuma', 'SST', 'TODO ADD FILE')
santa_barbara = count_nobs('santa_barbara', 'SST', 'TODO ADD FILE')
granite = count_nobs('granite', 'SST', 'TODO ADD FILE')
grove = count_nobs('grove', 'SST', 'TODO ADD FILE')
farallons = count_nobs('farallons', 'SST', 'TODO ADD FILE')
trinidad = count_nobs('trinidad', 'SST', 'TODO ADD FILE', 'TODO ADD FILE')

draw_nobs(scripps_SST)
draw_nobs(scripps_SBT)
draw_nobs(san_clemente)
draw_nobs(newport)
draw_nobs(zuma)
draw_nobs(santa_barbara)
draw_nobs(granite)
draw_nobs(grove)
draw_nobs(farallons)
draw_nobs(trinidad)
