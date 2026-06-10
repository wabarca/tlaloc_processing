import os

# =====================================================
# SERVIDOR WRF
# =====================================================

BASE_URL = "http://192.168.6.170"


# =====================================================
# ENSEMBLE
# =====================================================

MEMBERS = [f"ut{i}" for i in range(1, 10)]

NT = 87


# =====================================================
# DIRECTORIOS
# =====================================================

RAW_DIR = os.environ.get(
    "TLALOC_RAW_DIR",
    "/tmp/tlaloc_raw",
)

OUTPUT_DIR = os.environ.get(
    "TLALOC_OUTPUT_DIR",
    "paneles_ensemble",
)

OPERATIONAL_DIR = f"{OUTPUT_DIR}/operational"

UNCERTAINTY_DIR = f"{OUTPUT_DIR}/uncertainty"

PROBABILITY_DIR = f"{OUTPUT_DIR}/probability"


# =====================================================
# DOMINIO
# =====================================================

EXTENT = (
    -90.49,
    -87.09,
    12.36,
    14.93,
)


# =====================================================
# DESCARGA
# =====================================================

DOWNLOAD_WORKERS = 24

REQUEST_TIMEOUT = 30

MAX_RETRIES = 3

RETRY_BACKOFF = 1


# =====================================================
# ENSEMBLE PRODUCTS
# =====================================================

PROBABILITY_THRESHOLDS = [
    1,
    10,
    25,
    50,
    100,
]

PERCENTILES = [
    10,
    25,
    50,
    75,
    90,
]

MIN_RELATIVE_SPREAD_MEAN = 0.1


# =====================================================
# PRECIPITATION COLORMAP
# =====================================================

RAIN_LEVELS = [
    0,
    1,
    5,
    10,
    25,
    50,
    75,
    100,
    150,
    200,
]

RAIN_COLORS = [
    "#ffffff",
    "#b7e4ff",
    "#6bc2ff",
    "#2f8cff",
    "#00b050",
    "#ffff00",
    "#ff9900",
    "#ff0000",
    "#990000",
]


# =====================================================
# PROBABILITY COLORMAP
# =====================================================

PROB_LEVELS = [
    0,
    10,
    25,
    50,
    75,
    90,
    100,
]

PROB_COLORS = [
    "#ffffff",
    "#c7e9c0",
    "#74c476",
    "#31a354",
    "#006d2c",
    "#00441b",
]


# =====================================================
# SPREAD COLORMAP
# =====================================================

SPREAD_LEVELS = [
    0,
    2,
    5,
    10,
    20,
    40,
]

SPREAD_COLORS = [
    "#ffffff",
    "#b3cde3",
    "#6497b1",
    "#005b96",
    "#03396c",
]


# =====================================================
# RELATIVE SPREAD COLORMAP
# =====================================================

RELATIVE_SPREAD_LEVELS = [
    0,
    25,
    50,
    75,
    100,
    150,
    200,
]

RELATIVE_SPREAD_COLORS = [
    "#ffffff",
    "#d9f0a3",
    "#addd8e",
    "#78c679",
    "#31a354",
    "#006837",
]


# =====================================================
# SHAPEFILES
# =====================================================

SHAPEFILES_DIR = "assets/shapefiles"

COUNTRIES_SHP = f"{SHAPEFILES_DIR}/Centro_America.shp"

DEPARTMENTS_SHP = f"{SHAPEFILES_DIR}/El_Salvador_departamentos.shp"

COASTLINE_SHP = f"{SHAPEFILES_DIR}/GSHHS_h_L1.shp"


# =====================================================
# FIGURES
# =====================================================

FIGSIZE = (
    21,
    18,
)

DPI = 150

PANEL_ROWS = 3

PANEL_COLS = 3
