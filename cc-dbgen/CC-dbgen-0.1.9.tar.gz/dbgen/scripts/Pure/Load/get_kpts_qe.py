from typing import Dict,Tuple

def get_kpts_qe(trip:Tuple[str,str,str]) -> Tuple[int,int,int]:
    """
    K point info (? ? ? kx ky kz) - assumed to be in last line of pw.inp
    """

    _,pwinp,_ = trip
    line  = pwinp.strip().split('\n')[-1]
    raw   = line.split()[:3]
    return int(raw[0]),int(raw[1]),int(raw[2])
