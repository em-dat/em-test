from .data_loader import load_UNSD_areas, load_GAUL_code

areas = load_UNSD_areas()

ISO3_LIST = areas['ISO-alpha3 Code']
COUNTRY_LIST = areas['Country or Area']
REGION_LIST = areas['Region Name']
SUBREGION_LIST = areas['Sub-region Name']
ADM1_GAUL_LIST = load_GAUL_code(1)
ADM2_GAUL_LIST = load_GAUL_code(2)