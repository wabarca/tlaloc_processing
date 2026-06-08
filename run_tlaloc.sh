#!/bin/bash
source /home/wrf/.bashrc

# Limpieza de datos
rm /tmp/tlaloc_raw/*

BASE_DIR=/home/wrf/scripts
LOG_DIR=$BASE_DIR/logs
ENV_NAME=tlaloc

OUT_DIR=/compartido/web/paneles_ensemble
FECHA=$(date +"%Y-%m-%d")

#$FECHA

mkdir -p /compartido/web/$FECHA

cp -R $OUT_DIR/* /compartido/web/$FECHA/

DATE=$(date +"%Y%m%d_%H%M")
LOG_FILE=$LOG_DIR/tlaloc_$DATE.log

mkdir -p $LOG_DIR

echo "=================================" >> $LOG_FILE
echo "Inicio: $(date)" >> $LOG_FILE

# cargar conda
source /home/wrf/miniconda3/etc/profile.d/conda.sh

# activar entorno
conda activate $ENV_NAME

cd $BASE_DIR

/home/wrf/miniconda3/envs/tlaloc/bin/python3 unico.py >> $LOG_FILE 2>&1

echo "Fin: $(date)" >> $LOG_FILE
echo "=================================" >> $LOG_FILE
