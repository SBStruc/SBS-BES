from pydantic import BaseModel


class Data(BaseModel):
    value: float
    unit: str


class BeamCrossSection(BaseModel):
    b: Data
    h: Data


class BarLocation(BaseModel):
    support_or_mid: str
    location: str
    bar_count: int
    bar_thickness: Data


class Layer(BaseModel):
    layer_number: int
    location: BarLocation


class DesignCriteria(BaseModel):
    f_prime_c: Data  # concrete strength
    f_y_main: Data  # main rebar yield tensile strength
    f_y_sec: Data  # secondary rebar yield tensile strength
    y_conc: Data  # concrete specific weight
    e_s: Data
    cc: Data  # concrete cover
    phi_flex: float
    phi_shear: float
    lambda_shear: float
    beta_1: float
    rho_min_1: float
    rho_max: float
    d_mid: Data


class Flexure(BaseModel):
    design_criteria: DesignCriteria
    phi_main: Data
    phi_sec: Data
    beam_cross_section: BeamCrossSection
    mu_neg: Data  # abs_max_moment_z
    mu_pos: Data  # abs_min_moment_z
    flex_parameters: None


class Shear(BaseModel):
    pass


class Beam(BaseModel):
    beam_name: str
    vu: Data  # abs_max_shear_y
    tu: Data  # abs_max_torsion
    layer: Layer
    flexure: Flexure

    # support bars
    # midspan bars
    # add flexure
    # add shear
    # add torsion
