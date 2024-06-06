import math
from sbs_bes.beam_data_model import DesignCriteria, Data

f_prime_c: Data = Data(value=35, unit="MPa")
f_y_main: Data = Data(value=415, unit="MPa")
f_y_sec: Data = Data(value=276, unit="MPa")
y_conc: Data = Data(value=24, unit="kN/m3")
e_s: Data = Data(value=200000, unit="MPa")
cc: Data = Data(value=40, unit="mm")
phi_flex: float = 0.90
phi_shear: float = 0.75
lambda_dc: float = 1.0
f_y_sec_main: Data = f_y_main


def get_beta_1() -> float:
    beta_1: float = 0.85
    if f_prime_c.value > 28:
        beta_1 -= (0.05 / 7) * (f_prime_c.value - 28)
        beta_1 = round(beta_1, 15)

    if beta_1 > 0.65:
        return beta_1

    return 0.65


def get_rho_min_1() -> float:
    return round(
        max(1.4 / f_y_main.value, math.sqrt(f_prime_c.value) / (4 * f_y_main.value)), 15
    )


def get_rho_max() -> float:
    rho_max: float = (3 / 7) * 0.85 * f_prime_c.value * get_beta_1() / f_y_main.value
    return round(rho_max, 15)


print("beta_1 = ", get_beta_1())
print("rho_min_1 = ", get_rho_min_1())
print("rho_max = ", get_rho_max())


def get_design_criteria() -> DesignCriteria:
    return DesignCriteria(
        f_prime_c=f_prime_c,
        f_y_main=f_y_main,
        f_y_sec=f_y_sec,
        y_conc=y_conc,
        e_s=e_s,
        cc=cc,
        phi_flex=phi_flex,
        phi_shear=phi_shear,
        lambda_shear=lambda_dc,
        beta_1=get_beta_1(),
        rho_min_1=get_rho_min_1(),
        rho_max=get_rho_max(),
        d_mid=Data(value=0.5, unit="m"),
    )
