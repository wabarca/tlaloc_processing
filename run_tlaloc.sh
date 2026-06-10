#!/bin/bash
source /home/wrf/.bashrc

BASE_DIR=/home/wrf/scripts
LOG_DIR=$BASE_DIR/logs
ENV_NAME=tlaloc

OUT_DIR=/compartido/web/paneles_ensemble
FECHA=$(date +"%Y-%m-%d")
ARCHIVE_DIR=/compartido/web/$FECHA

export TLALOC_RAW_DIR=/tmp/tlaloc_raw
export TLALOC_OUTPUT_DIR=$BASE_DIR/paneles_ensemble

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

# Limpieza de datos descargados anteriormente
rm -f /tmp/tlaloc_raw/*

if /home/wrf/miniconda3/envs/tlaloc/bin/python3 main.py >> $LOG_FILE 2>&1; then
    mkdir -p "$OUT_DIR" "$ARCHIVE_DIR"
    cp -R "$BASE_DIR/paneles_ensemble/." "$OUT_DIR/"
    cp -R "$OUT_DIR/." "$ARCHIVE_DIR/"
else
    echo "ERROR: main.py terminó con estado no exitoso" >> "$LOG_FILE"
    exit 1
fi

echo "Fin: $(date)" >> $LOG_FILE
echo "=================================" >> $LOG_FILE
