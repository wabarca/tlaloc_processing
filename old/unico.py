#!/usr/bin/env python3

import os
import requests
import numpy as np
import rasterio
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from tqdm import tqdm
from datetime import datetime, timedelta

from sklearn.cluster import KMeans


# =====================================================
# CONFIG
# =====================================================

BASE = "http://192.168.6.170"

MIEMBROS = [f"ut{i}" for i in range(1,10)]

NT = 87

PROBS = [25,50,100]

RAW = "/tmp/tlaloc_raw"
OUT = "/compartido/web/paneles_ensemble"

os.makedirs(RAW,exist_ok=True)
os.makedirs(OUT,exist_ok=True)


# =====================================================
# TIEMPO DE PRONOSTICO
# =====================================================

run_date = datetime.utcnow().date()

# GeoTIFF 1 = 00 UTC día anterior
start_valid = datetime.combine(run_date, datetime.min.time()) - timedelta(days=1)


# =====================================================
# EXTENT EL SALVADOR
# =====================================================

EXTENT = (-90.49,-87.09,12.36,14.93)


# =====================================================
# COLORMAPS
# =====================================================

rain_levels=[0,1,5,10,25,50,75,100,150,200]

rain_colors=[
"#ffffff","#b7e4ff","#6bc2ff","#2f8cff",
"#00b050","#ffff00","#ff9900","#ff0000","#990000"
]

rain_cmap=ListedColormap(rain_colors)
rain_norm=BoundaryNorm(rain_levels,rain_cmap.N)


prob_levels=[0,10,25,50,75,90,100]

prob_colors=[
"#ffffff","#c7e9c0","#74c476",
"#31a354","#006d2c","#00441b"
]

prob_cmap=ListedColormap(prob_colors)
prob_norm=BoundaryNorm(prob_levels,prob_cmap.N)


spread_levels=[0,2,5,10,20,40]

spread_colors=[
"#ffffff","#b3cde3","#6497b1",
"#005b96","#03396c"
]

spread_cmap=ListedColormap(spread_colors)
spread_norm=BoundaryNorm(spread_levels,spread_cmap.N)


# =====================================================
# DESCARGA
# =====================================================

def download(member,t):

    url=f"{BASE}/{member}/dominio2/00/geotiff/lluvia_{t}.tif"

    local=f"{RAW}/{member}_{t}.tif"

    if not os.path.exists(local):

        r=requests.get(url,timeout=30)

        if r.status_code!=200:
            raise Exception(url)

        with open(local,"wb") as f:
            f.write(r.content)

    return local


# =====================================================
# CARGAR ENSEMBLE
# =====================================================

def load_ensemble():

    print("Cargando ensemble")

    for t in tqdm(range(1,NT+1)):

        members=[]

        for m in MIEMBROS:

            path=f"{RAW}/{m}_{t}.tif"

            with rasterio.open(path) as src:

                data=src.read(1)
                transform=src.transform

            members.append(data)

        members=np.stack(members)

        if t==1:

            ny,nx=members.shape[1:]

            ensemble=np.zeros((NT,len(MIEMBROS),ny,nx))

        ensemble[t-1,:,:,:]=members

    return ensemble,transform


# =====================================================
# ENSEMBLE PRODUCTS
# =====================================================

def ensemble_products(stack):

    mean=np.mean(stack,axis=0)

    maxv=np.max(stack,axis=0)

    spread=np.std(stack,axis=0)

    probs={}

    for p in PROBS:
        probs[p]=np.mean(stack>p,axis=0)*100

    storm=np.mean(stack>10,axis=0)*100

    p25=np.percentile(stack,25,axis=0)
    p50=np.percentile(stack,50,axis=0)
    p75=np.percentile(stack,75,axis=0)

    return mean,maxv,spread,probs,storm,p25,p50,p75


# =====================================================
# BASE MAP
# =====================================================

def draw_base(ax):

    ax.set_extent(EXTENT,crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.OCEAN,facecolor="#eeeeee")
    ax.add_feature(cfeature.COASTLINE,linewidth=0.9)
    ax.add_feature(cfeature.BORDERS,linewidth=0.9)

    ax.gridlines(
        draw_labels=False,
        linewidth=0.3,
        linestyle="--",
        alpha=0.4
    )


# =====================================================
# PLOT
# =====================================================

def plot_field(ax,data,title,cmap,norm):

    draw_base(ax)

    m=ax.imshow(
        data,
        origin="upper",
        extent=EXTENT,
        transform=ccrs.PlateCarree(),
        cmap=cmap,
        norm=norm
    )

    ax.set_title(title,fontsize=10)

    cbar=plt.colorbar(
        m,
        ax=ax,
        orientation="horizontal",
        pad=0.02,
        shrink=0.75
    )

    cbar.ax.tick_params(labelsize=7)


# =====================================================
# PANEL
# =====================================================

def make_panel(stack,hour,outfile):

    mean,maxv,spread,probs,storm,p25,p50,p75=ensemble_products(stack)

    valid_time = start_valid + timedelta(hours=hour-1)

    valid_str = valid_time.strftime("%Y-%m-%d %H:%M UTC")

    fig,axs=plt.subplots(
        3,3,
        figsize=(15,12),
        subplot_kw={"projection":ccrs.PlateCarree()},
        constrained_layout=True
    )

    axs=axs.flatten()

    plot_field(axs[0],mean,"Mean precipitation (mm)",rain_cmap,rain_norm)
    plot_field(axs[1],maxv,"Maximum precipitation (mm)",rain_cmap,rain_norm)

    plot_field(axs[2],probs[25],"Probability >25 mm (%)",prob_cmap,prob_norm)
    plot_field(axs[3],probs[50],"Probability >50 mm (%)",prob_cmap,prob_norm)
    plot_field(axs[4],probs[100],"Probability >100 mm (%)",prob_cmap,prob_norm)

    plot_field(axs[5],spread,"Ensemble spread (mm)",spread_cmap,spread_norm)

    plot_field(axs[6],storm,"Storm consensus (%)",prob_cmap,prob_norm)

    plot_field(axs[7],p50,"Median precipitation (mm)",rain_cmap,rain_norm)

    plot_field(axs[8],p75,"75th percentile (mm)",rain_cmap,rain_norm)

    fig.suptitle(
        f"WRF Ensemble Precipitation | Valid: {valid_str}",
        fontsize=14,
        fontweight="bold"
    )

    plt.savefig(outfile,dpi=150,bbox_inches="tight")

    plt.close()


# =====================================================
# PIPELINE
# =====================================================

print("Descargando GeoTIFF")

for m in MIEMBROS:
    for t in range(1,NT+1):
        download(m,t)


ensemble,_=load_ensemble()


# =====================================================
# HORARIOS
# =====================================================

print("Paneles horarios")

for t in range(NT):

    stack=ensemble[t,:,:,:]

    make_panel(
        stack,
        t+1,
        f"{OUT}/panel_h_{t+1:03}.png"
    )


# =====================================================
# 6 HORAS
# =====================================================

print("Paneles 6h")

for start in range(0,NT,6):

    end=min(start+6,NT)

    stack=np.sum(ensemble[start:end,:,:,:],axis=0)

    make_panel(
        stack,
        start+1,
        f"{OUT}/panel_6h_{start+1:03}.png"
    )


# =====================================================
# 24 / 48 / 72 HORAS
# =====================================================

print("Panel acumulados")

start=18

stack=np.sum(ensemble[start:start+24,:,:,:],axis=0)
d1=stack

make_panel(
    d1,
    start+1,
    f"{OUT}/panel_24h.png"
)

stack=np.sum(ensemble[start:start+48,:,:,:],axis=0)
d2=stack-d1
make_panel(
    d2,
    start+1,
    f"{OUT}/panel_48h.png"
)

stack=np.sum(ensemble[start:start+72,:,:,:],axis=0)
d3=stack-d2-d1
make_panel(
    d3,
    start+1,
    f"{OUT}/panel_72h.png"
)

print("Proceso terminado")
