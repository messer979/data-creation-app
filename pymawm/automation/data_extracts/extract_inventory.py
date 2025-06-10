from pymawm.automation.db import get_connection
from pymawm.automation.data_extracts.funcs import determine_volume

def run_extract(active):
    res = active.dci.get_inv(size=500)
    total = res['header']
    size = res['size']
    if total < size:
        determine_volume()
