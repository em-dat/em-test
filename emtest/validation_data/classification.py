from .data_loader import load_classification

classification = load_classification()

KEY_LIST = classification['classif_key'].unique()
GROUP_LIST = classification['group'].unique()
SUBGROUP_LIST = classification['subgroup'].unique()
TYPE_LIST = classification['type'].unique()
SUBTYPE_LIST = classification['subtype'].unique()
