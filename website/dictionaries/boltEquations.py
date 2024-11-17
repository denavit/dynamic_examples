from math import sqrt, pi

def p(n):
    return 1 / n

def H(n):
    return sqrt(3) / (2 * n)

def d1bsc(dbsc, H):
    return dbsc - (1.25 * H)

def D1bsc(d1bsc):
    return d1bsc

def d2bsc(dbsc, H):
    return dbsc - (0.75 * H)

def D2bsc(d2bsc):
    return d2bsc

def Absc(dbsc):
    '''
    Cross-sectional area based on dbsc
    '''
    return pi / 4 * dbsc ** 2

def As_FEDSTD_1a(d2bsc, H):
    '''
    Tensile stress area based on FED-STD-H28/2B (1991), Table II.B.1, Formula (1a)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    As = pi * (d2bsc / 2 - 3 * H / 16) ** 2
    return As

def As_FEDSTD_1b(dbsc, n):
    '''
    Tensile stress area based on FED-STD-H28/2B (1991), Table II.B.1, Formula (1b)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    As = pi / 4 * (dbsc - (9 * sqrt(3)) / (16 * n)) ** 2
    return As

def As_MH_2b(UTSs, d2min, n, override_limit=False):
    '''
    Tensile stress area based on Machinery's Handbook, 31st Edition Eq. (2b) on Page 1668

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    if (UTSs <= 180000) and (not override_limit):
        raise ValueError('As_MH_2b is only for steels of over 180,000 psi ultimate tensile strength')
    As = pi * ((d2min / 2) - (3 * sqrt(3)) / (32 * n)) ** 2
    return As

def ASn_min_FEDSTD_2a(n, dmin, D2max, LE=1):
    '''
    Shear area, internal threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (2a)
        (minimum material external and internal threads)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASn = pi * n * LE * dmin * ((1 / (2 * n)) + ((1 / sqrt(3)) * (dmin - D2max)))
    return ASn

def ASn_FEDSTD_3(dbsc, D2bsc, LE=1, override_limit=False):
    '''
    Shear area, internal threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (3)
        (simplified: for d equal to or greater than 0.250 inch)

    Arguments:
    LE --- length of engagement (default = 1)
    override_limit --- option to ignore limit on diameter (default = False)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    if (dbsc < 0.250) and (not override_limit):
        raise ValueError('ASn_FEDSTD_3 should not be used with dbsc less than 0.250 inch')
    ASn = pi * D2bsc * (3 / 4) * LE
    return ASn

def ASs_min_FEDSTD_4a(n, D1max, d2min, LE=1):
    '''
    Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (4a)
        (minimum material external and internal threads)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASs = pi * n * LE * D1max * ((1 / (2 * n)) + ((1 / sqrt(3)) * (d2min - D1max)))
    return ASs

def ASs_FEDSTD_5(d2bsc, LE=1):
    '''
    Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (5)
        (simplified)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASs = pi * d2bsc * (5 / 8) * LE
    return ASs

def ASs_max_FEDSTD_6b(D1bsc, LE=1):
    '''
    Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (6b)
        (basic size external and internal threads)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASs = pi * D1bsc * 0.75 * LE
    return ASs

def LEr_FEDSTD_13(d2bsc, H):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (13)
        (based upon combined shear failure of external and internal threads)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''

    As = As_FEDSTD_1a(d2bsc, H)

    LEr = (4 * As) / (pi * d2bsc)
    return LEr

def LEr_FEDSTD_14(d2bsc, H, dbsc, n, D1max, d2min, LE=1, As_eqn='1a', ASs_eqn='4a'):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (14)
        (based upon shear of external thread)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    ASs_eqn --- denotes which equation to use for As ('4a' or '4b', default = '4a')
    '''
    if As_eqn == '1a':
        As = As_FEDSTD_1a(d2bsc, H)
    elif As_eqn == '1b':
        As = As_FEDSTD_1b(dbsc, n)
    else:
        raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')

    if ASs_eqn == '4a':
        ASs = ASs_min_FEDSTD_4a(n, D1max, d2min, LE)
    elif ASs_eqn == '4b':
        raise ValueError(f'ASs_FEDSTD_4b is not yet implemented')
    else:
        raise ValueError(f'Invalid value for ASs_eqn: {ASs_eqn} (need ''4a'' or ''4b'')')

    LEr = 2 * As / ASs
    return LEr

def LEr_FEDSTD_15(d2bsc, H, D1bsc):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (15)
        (based upon shear of external thread)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    '''
    As = As_FEDSTD_1a(d2bsc, H)
    LEr = 2 * As / ASs_max_FEDSTD_6b(D1bsc)
    return LEr

def LEr_FEDSTD_16(n, dmin, D2max, UTSn, UTSs):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (16)
        (based upon shear of external thread)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    ASn_eqn --- denotes which equation to use for ASn ('2a' or '2b', default = '2a')
    '''
    As = As_FEDSTD_1a(d2bsc, H)

    ASn = ASn_min_FEDSTD_2a(n, dmin, D2max)

    R2 = UTSn / UTSs
    LEr = (2 * As / ASn) / R2
    # FED-STD-H28/2B (1991), Table II.B.1, Formula (16) is
    #   LE = "LE from (15)" x R1/R2
    # where
    #   "LE from (15)" = 2 As / ASs
    #   R1 = ASs/ASn
    # The equation used in this function is algebraically identical to the equation in
    # FED-STD-H28/2B and does not require evaluation of ASs
    return LEr

def LEr_FEDSTD(n, D1bsc, dmin, D2max, UTSn, UTSs, d2bsc, H, dbsc, D1max, d2min, combined_failure_range=0.05):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formulas (13),
        (15), and (16)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    ASn_eqn --- denotes which equation to use for ASn ('2a' or '2b', default = '2a')
    ASs_eqn --- denotes which equation to use for ASn ('4a' or '4b', default = '4a')
    combined_failure_range --- parameter that defines the limit of applicability of the combined failure mode
        (default = 0.05)s
    '''
    R1 = ASs_max_FEDSTD_6b(D1bsc) / ASn_min_FEDSTD_2a(n, dmin, D2max)  # @todo - code in options here see formula (8)
    R2 = UTSn / UTSs
    if R1 / R2 < (1 - combined_failure_range):
        # External thread failure, Formula (15)
        LEr = LEr_FEDSTD_14(d2bsc, H, dbsc, n, D1max, d2min)
    else:
        # Internal thread failure or combined failure, Formula (13) or (16)
        LEr_13 = LEr_FEDSTD_13(d2bsc)
        LEr_16 = LEr_FEDSTD_16(n, dmin, D2max, UTSn, UTSs)
        LEr = max(LEr_13, LEr_16)
    return LEr

def As_ISO(self):
    """
    Tensile stress area based on ISO/TR 16224:2012(E), Section 4.2.2.2
    """
    d3 = d1bsc - (H / 6)
    As = pi / 4 * ((d2bsc + d3) / 2) ** 2
    return As

def ASb_ISO(self, LE=1):
    """
    Shear Area, External Threads (Bolt) based on ISO/TR 16224:2012(E), Section 4.2.3.1

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    """

    if dims_ISO == 'basic':
        if use_Dm_ISO:
            Dm = 1.026 * D1bsc
            ASb = (0.6 * (LE / p) * pi * D1bsc * (p / 2 + (d2bsc - D1bsc) / sqrt(3))) + \
                    (0.4 * (LE / p) * pi * Dm * (p / 2 + (d2bsc - Dm) / sqrt(3)))
        else:
            ASb = (LE / p) * pi * D1bsc * (p / 2 + (d2bsc - D1bsc) / sqrt(3))
    elif dims_ISO == 'min':
        if use_Dm_ISO:
            Dm = Dm = 1.026 * D1max
            ASb = (0.6 * (LE / p) * pi * D1max * (p / 2 + (d2min - D1max) / sqrt(3))) + \
                    (0.4 * (LE / p) * pi * Dm * (p / 2 + (d2min - Dm) / sqrt(3)))
        else:
            ASb = (LE / p) * pi * D1max * (p / 2 + (d2min - D1max) / sqrt(3))
    else:
        raise ValueError(f'Unknown option for dims_ISO: {dims_ISO}')

    return ASb

def ASn_ISO(self, LE=1):
    """
    Shear Area, Internal Threads (Bolt) based on ISO/TR 16224:2012(E), Section 4.2.3.1

    Arguments:
    LE --- length of engagement (default = 1)
    """
    if dims_ISO == 'basic':
        ASn = (LE / p) * pi * dbsc * (p / 2 + (dbsc - D2bsc) / sqrt(3))
    elif dims_ISO == 'min':
        ASn = (LE / p) * pi * dmin * (p / 2 + (dmin - D2max) / sqrt(3))
    else:
        raise ValueError(f'Unknown option for dims_ISO: {dims_ISO}')

    return ASn

def C1_ISO(self, s):
    """
    Modification factor for nut dilation based on ISO/TR 16224:2012(E), Section 4.2.3.1

    C1 is undefined for when s/D < 1.4
    C1 taken equal to 1.0 when s/D >= 1.8 (this is slighly different than the equation in ISO/TR 16224:2012(E))

    Arguments:
    s --- width across flats of the nut
    """
    s_over_d = s / dbsc
    return C1_ISO(s_over_d)

def C2_ISO(self):
    """
    Modification factor for thread bending effect based on ISO/TR 16224:2012(E), Section 4.2.3.1
    """
    Rs = (UTSn * ASn_ISO()) / (UTSs * ASb_ISO())
    return C2_ISO(Rs)

def C3_ISO(self):
    """
    Modification factor for thread bending effect based on ISO/TR 16224:2012(E), Section 4.2.3.1
    """
    Rs = (UTSn * ASn_ISO()) / (UTSs * ASb_ISO())
    return C3_ISO(Rs)

def LEr_ISO(self, s):
    """
    Length of engagement required for tensile failure based on Analysis and Design of Threaded Assemblies,
        E.M. Alexander

    Arguments:
    s --- width across flats of the nut
    """
    LEr1 = As_ISO() / (0.6 * ASb_ISO() * C1_ISO(s) * C2_ISO())
    LEr2 = (As_ISO() * UTSs) / (0.6 * UTSn * ASn_ISO() * C1_ISO(s) * C3_ISO())
    LEr = max(LEr1, LEr2)
    return LEr


def C1_ISO(s_over_d, C1_out_of_range=None):
    """
    Modification factor for nut dilation based on ISO/TR 16224:2012(E), Section 4.2.3.1, Equation (6)

    C1 is undefined for when s/D < 1.4 (function returns C1_out_of_range if the argument is given)
    C1 taken equal to 1.0 when s/D >= 1.8 (this is slighly different than the equation in ISO/TR 16224:2012(E))

    Arguments:
    s_over_d --- ratio of width across flats of the nut to XXXXX
    C1_out_of_range --- value to return if s/D is out of range (i.e., s/D < 1.4) (default = None)
                        if "None", the the function raises a ValueError if out of range
    """
    if s_over_d < 1.4:
        if C1_out_of_range is None:
            raise ValueError('C1 is undefined because s/dbsc < 1.4')
        else:
            C1 = C1_out_of_range
    elif s_over_d < 1.8:
        C1 = (-1) * s_over_d ** 2 + 3.8 * s_over_d - 2.6
    else:
        C1 = 1.0
    return C1


def C2_ISO(Rs, C2_out_of_range=None):
    """
    Modification factor for thread bending effect based on ISO/TR 16224:2012(E), Section 4.2.3.1, Equation (6)

    Arguments:
    Rs --- Strength Ratio
    C2_out_of_range --- value to return if Rs is out of range (i.e., Rs >= 2.2) (default = None)
                        if "None", the the function raises a ValueError if out of range
    """
    if Rs <= 1:
        C2 = 0.897
    elif 1 < Rs < 2.2:
        C2 = 5.594 - 13.682 * Rs + 14.107 * Rs ** 2 - 6.057 * Rs ** 3 + 0.9353 * Rs ** 4
    else:
        if C2_out_of_range is None:
            raise ValueError('Rs not in range, Rs must be < 2.2')
        else:
            C2 = C2_out_of_range
    return C2


def C3_ISO(Rs, C3_out_of_range=None):
    """
    Modification factor for thread bending effect based on ISO/TR 16224:2012(E), Section 4.2.3.1, Equation (6)

    Arguments:
    Rs --- Strength Ratio
    C3_out_of_range --- value to return if Rs is out of range (i.e., Rs < 2.2) (default = None)
                        if "None", the the function raises a ValueError if out of range
    """
    if Rs >= 1:
        C3 = 0.897
    elif 0.4 < Rs < 1:
        C3 = 0.728 + 1.769 * Rs - 2.896 * Rs ** 2 + 1.296 * Rs ** 3
    else:
        if C3_out_of_range is None:
            raise ValueError('C3 not in range, Rs must be > 0.4')
        else:
            C3 = C3_out_of_range
    return C3