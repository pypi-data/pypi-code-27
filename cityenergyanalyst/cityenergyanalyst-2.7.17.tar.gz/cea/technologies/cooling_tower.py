"""
System Modeling: Cooling tower
"""
from __future__ import division
import pandas as pd
from math import ceil, log
from cea.optimization.constants import CT_MAX_SIZE

__author__ = "Thuy-An Nguyen"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Thuy-An Nguyen", "Tim Vollrath", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"

# technical model

def calc_CT(qhotdot_W, Qdesign_W):
    """
    For the operation of a water condenser + direct cooling tower based on [B. Stephane, 2012]_
    Maximum cooling power is 10 MW.
    
    :type qhotdot_W : float
    :param qhotdot_W: heating power to condenser, From Model_VCC
    :type Qdesign_W : float
    :param Qdesign_W: Nominal cooling power
    

    :type wdot : float
    :param wdot: electric power needed for the variable speed drive fan

    ..[B. Stephane, 2012] B. Stephane (2012), Evidence-Based Model Calibration for Efficient Building Energy Services.
    PhD Thesis, University de Liege, Belgium
    """
    wdot_W = 0
    if qhotdot_W > CT_MAX_SIZE:
        number_of_towers = int(ceil(qhotdot_W/CT_MAX_SIZE))
        qhotdot_W_per_chiller = qhotdot_W/number_of_towers
        for i in range(number_of_towers):
            qpartload = qhotdot_W / Qdesign_W

            wdesign_fan = 0.011 * Qdesign_W
            wpartload = 0.8603 * qpartload ** 3 + 0.2045 * qpartload ** 2 - 0.0623 * \
                        qpartload + 0.0026

            wdot_W = wdot_W + wpartload * wdesign_fan

    else:
        qpartload = qhotdot_W / Qdesign_W

        wdesign_fan = 0.011 * Qdesign_W
        wpartload = 0.8603 * qpartload ** 3 + 0.2045 * qpartload ** 2 - 0.0623 * \
                    qpartload + 0.0026

        wdot_W = wpartload * wdesign_fan
    
    return wdot_W
    

# Investment costs

def calc_Cinv_CT(CT_size_W, locator, config, technology_type):
    """
    Annualized investment costs for the Combined cycle

    :type CT_size_W : float
    :param CT_size_W: Size of the Cooling tower in [W]

    :rtype InvCa : float
    :returns InvCa: annualized investment costs in Dollars
    """
    Capex_a = 0
    Opex_fixed = 0

    if CT_size_W > 0:
        CT_cost_data = pd.read_excel(locator.get_supply_systems(config.region), sheetname="CT")
        CT_cost_data = CT_cost_data[CT_cost_data['code'] == technology_type]
        max_chiller_size = max(CT_cost_data['cap_max'].values)

        # if the Q_design is below the lowest capacity available for the technology, then it is replaced by the least
        # capacity for the corresponding technology from the database
        if CT_size_W < CT_cost_data.iloc[0]['cap_min']:
            CT_size_W = CT_cost_data.iloc[0]['cap_min']
        if CT_size_W <= max_chiller_size:
            CT_cost_data = CT_cost_data[
                (CT_cost_data['cap_min'] <= CT_size_W) & (CT_cost_data['cap_max'] > CT_size_W)]

            Inv_a = CT_cost_data.iloc[0]['a']
            Inv_b = CT_cost_data.iloc[0]['b']
            Inv_c = CT_cost_data.iloc[0]['c']
            Inv_d = CT_cost_data.iloc[0]['d']
            Inv_e = CT_cost_data.iloc[0]['e']
            Inv_IR = (CT_cost_data.iloc[0]['IR_%']) / 100
            Inv_LT = CT_cost_data.iloc[0]['LT_yr']
            Inv_OM = CT_cost_data.iloc[0]['O&M_%'] / 100

            InvC = Inv_a + Inv_b * (CT_size_W) ** Inv_c + (Inv_d + Inv_e * CT_size_W) * log(CT_size_W)

            Capex_a =  InvC * (Inv_IR) * (1+ Inv_IR) ** Inv_LT / ((1+Inv_IR) ** Inv_LT - 1)
            Opex_fixed = Capex_a * Inv_OM

        else:
            number_of_chillers = int(ceil(CT_size_W / max_chiller_size))
            Q_nom_each_CT = CT_size_W / number_of_chillers

            for i in range(number_of_chillers):
                CT_cost_data = CT_cost_data[
                    (CT_cost_data['cap_min'] <= Q_nom_each_CT) & (CT_cost_data['cap_max'] > Q_nom_each_CT)]
                Inv_a = CT_cost_data.iloc[0]['a']
                Inv_b = CT_cost_data.iloc[0]['b']
                Inv_c = CT_cost_data.iloc[0]['c']
                Inv_d = CT_cost_data.iloc[0]['d']
                Inv_e = CT_cost_data.iloc[0]['e']
                Inv_IR = (CT_cost_data.iloc[0]['IR_%']) / 100
                Inv_LT = CT_cost_data.iloc[0]['LT_yr']
                Inv_OM = CT_cost_data.iloc[0]['O&M_%'] / 100
                InvC = Inv_a + Inv_b * (Q_nom_each_CT) ** Inv_c + (Inv_d + Inv_e * Q_nom_each_CT) * log(Q_nom_each_CT)
                Capex_a1 = InvC * (Inv_IR) * (1 + Inv_IR) ** Inv_LT / ((1 + Inv_IR) ** Inv_LT - 1)
                Capex_a = Capex_a + Capex_a1
                Opex_fixed = Opex_fixed + Capex_a1 * Inv_OM

    return Capex_a, Opex_fixed














