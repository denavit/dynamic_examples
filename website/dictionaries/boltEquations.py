
def p(self):
    return 1 / self.n

def H(self):
    return sqrt(3) / (2 * self.n)

def d1bsc(self):
    return self.dbsc - 1.25 * self.H

def D1bsc(self):
    return self.d1bsc

def d2bsc(self):
    return self.dbsc - 0.75 * self.H

def D2bsc(self):
    return self.d2bsc

def Absc(self):
    '''
    Cross-sectional area based on dbsc
    '''
    return pi / 4 * self.dbsc ** 2

def As_FEDSTD_1a(self):
    '''
    Tensile stress area based on FED-STD-H28/2B (1991), Table II.B.1, Formula (1a)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    As = pi * (self.d2bsc / 2 - 3 * self.H / 16) ** 2
    return As

def As_FEDSTD_1b(self):
    '''
    Tensile stress area based on FED-STD-H28/2B (1991), Table II.B.1, Formula (1b)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    As = pi / 4 * (self.dbsc - (9 * sqrt(3)) / (16 * self.n)) ** 2
    return As

def As_MH_2b(self, override_limit=False):
    '''
    Tensile stress area based on Machinery's Handbook, 31st Edition Eq. (2b) on Page 1668

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    if (self.UTSs <= 180000) and (not override_limit):
        raise ValueError('As_MH_2b is only for steels of over 180,000 psi ultimate tensile strength')
    As = pi * ((self.d2min / 2) - (3 * sqrt(3)) / (32 * self.n)) ** 2
    return As

def ASn_min_FEDSTD_2a(self, LE=1):
    '''
    Shear area, internal threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (2a)
        (minimum material external and internal threads)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASn = pi * self.n * LE * self.dmin * ((1 / (2 * self.n)) + ((1 / sqrt(3)) * (self.dmin - self.D2max)))
    return ASn

def ASn_FEDSTD_3(self, LE=1, override_limit=False):
    '''
    Shear area, internal threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (3)
        (simplified: for d equal to or greater than 0.250 inch)

    Arguments:
    LE --- length of engagement (default = 1)
    override_limit --- option to ignore limit on diameter (default = False)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    if (self.dbsc < 0.250) and (not override_limit):
        raise ValueError('ASn_FEDSTD_3 should not be used with dbsc less than 0.250 inch')
    ASn = pi * self.D2bsc * (3 / 4) * LE
    return ASn

def ASs_min_FEDSTD_4a(self, LE=1):
    '''
    Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (4a)
        (minimum material external and internal threads)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASs = pi * self.n * LE * self.D1max * ((1 / (2 * self.n)) + ((1 / sqrt(3)) * (self.d2min - self.D1max)))
    return ASs

def ASs_FEDSTD_5(self, LE=1):
    '''
    Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (5)
        (simplified)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASs = pi * self.d2bsc * (5 / 8) * LE
    return ASs

def ASs_max_FEDSTD_6b(self, LE=1):
    '''
    Shear area, external threads based on FED-STD-H28/2B (1991), Table II.B.1, Formula (6b)
        (basic size external and internal threads)

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    ASs = pi * self.D1bsc * 0.75 * LE
    return ASs

def LEr_FEDSTD_13(self, As_eqn='1a'):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (13)
        (based upon combined shear failure of external and internal threads)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    '''
    if As_eqn == '1a':
        As = self.As_FEDSTD_1a()
    elif As_eqn == '1b':
        As = self.As_FEDSTD_1b()
    else:
        raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')
    LEr = (4 * As) / (pi * self.d2bsc)
    return LEr

def LEr_FEDSTD_14(self, As_eqn='1a', ASs_eqn='4a'):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (14)
        (based upon shear of external thread)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    ASs_eqn --- denotes which equation to use for As ('4a' or '4b', default = '4a')
    '''
    if As_eqn == '1a':
        As = self.As_FEDSTD_1a()
    elif As_eqn == '1b':
        As = self.As_FEDSTD_1b()
    else:
        raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')

    if ASs_eqn == '4a':
        ASs = self.ASs_min_FEDSTD_4a()
    elif ASs_eqn == '4b':
        raise ValueError(f'ASs_FEDSTD_4b is not yet implemented')
    else:
        raise ValueError(f'Invalid value for ASs_eqn: {ASs_eqn} (need ''4a'' or ''4b'')')

    LEr = 2 * As / ASs
    return LEr

def LEr_FEDSTD_15(self, As_eqn='1a'):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (15)
        (based upon shear of external thread)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    '''
    if As_eqn == '1a':
        As = self.As_FEDSTD_1a()
    elif As_eqn == '1b':
        As = self.As_FEDSTD_1b()
    else:
        raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')

    LEr = 2 * As / self.ASs_max_FEDSTD_6b()
    return LEr

def LEr_FEDSTD_16(self, As_eqn='1a', ASn_eqn='2a'):
    '''
    Length of engagement required for tensile failure based on FED-STD-H28/2B (1991), Table II.B.1, Formula (16)
        (based upon shear of external thread)

    Arguments:
    As_eqn --- denotes which equation to use for As ('1a' or '1b', default = '1a')
    ASn_eqn --- denotes which equation to use for ASn ('2a' or '2b', default = '2a')
    '''
    if As_eqn == '1a':
        As = self.As_FEDSTD_1a()
    elif As_eqn == '1b':
        As = self.As_FEDSTD_1b()
    else:
        raise ValueError(f'Invalid value for As_eqn: {As_eqn} (need ''1a'' or ''1b'')')

    if ASn_eqn == '2a':
        ASn = self.ASn_min_FEDSTD_2a()
    elif ASn_eqn == '2b':
        raise ValueError(f'ASn_FEDSTD_2a is not yet implemented')
    else:
        raise ValueError(f'Invalid value for As_eqn: {ASn_eqn} (need ''2a'' or ''2b'')')

    R2 = self.UTSn / self.UTSs
    LEr = (2 * As / ASn) / R2
    # FED-STD-H28/2B (1991), Table II.B.1, Formula (16) is
    #   LE = "LE from (15)" x R1/R2
    # where
    #   "LE from (15)" = 2 As / ASs
    #   R1 = ASs/ASn
    # The equation used in this function is algebraically identical to the equation in
    # FED-STD-H28/2B and does not require evaluation of ASs
    return LEr

def LEr_FEDSTD(self, As_eqn='1a', ASs_eqn='4a', ASn_eqn='2a', combined_failure_range=0.05):
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
    R1 = self.ASs_max_FEDSTD_6b() / self.ASn_min_FEDSTD_2a()  # @todo - code in options here see formula (8)
    R2 = self.UTSn / self.UTSs
    if R1 / R2 < (1 - combined_failure_range):
        # External thread failure, Formula (15)
        LEr = self.LEr_FEDSTD_14(As_eqn, ASs_eqn)
    else:
        # Internal thread failure or combined failure, Formula (13) or (16)
        LEr_13 = self.LEr_FEDSTD_13(As_eqn)
        LEr_16 = self.LEr_FEDSTD_16(As_eqn, ASn_eqn)
        LEr = max(LEr_13, LEr_16)
    return LEr

def As_ISO(self):
    """
    Tensile stress area based on ISO/TR 16224:2012(E), Section 4.2.2.2
    """
    d3 = self.d1bsc - (self.H / 6)
    As = pi / 4 * ((self.d2bsc + d3) / 2) ** 2
    return As

def ASb_ISO(self, LE=1):
    """
    Shear Area, External Threads (Bolt) based on ISO/TR 16224:2012(E), Section 4.2.3.1

    Arguments:
    LE --- length of engagement (default = 1)

    Note: numbers with decimals replaced with equivalent mathematical expressions.
    """

    if self.dims_ISO == 'basic':
        if self.use_Dm_ISO:
            Dm = 1.026 * self.D1bsc
            ASb = (0.6 * (LE / self.p) * pi * self.D1bsc * (self.p / 2 + (self.d2bsc - self.D1bsc) / sqrt(3))) + \
                    (0.4 * (LE / self.p) * pi * Dm * (self.p / 2 + (self.d2bsc - Dm) / sqrt(3)))
        else:
            ASb = (LE / self.p) * pi * self.D1bsc * (self.p / 2 + (self.d2bsc - self.D1bsc) / sqrt(3))
    elif self.dims_ISO == 'min':
        if self.use_Dm_ISO:
            Dm = Dm = 1.026 * self.D1max
            ASb = (0.6 * (LE / self.p) * pi * self.D1max * (self.p / 2 + (self.d2min - self.D1max) / sqrt(3))) + \
                    (0.4 * (LE / self.p) * pi * Dm * (self.p / 2 + (self.d2min - Dm) / sqrt(3)))
        else:
            ASb = (LE / self.p) * pi * self.D1max * (self.p / 2 + (self.d2min - self.D1max) / sqrt(3))
    else:
        raise ValueError(f'Unknown option for dims_ISO: {self.dims_ISO}')

    return ASb

def ASn_ISO(self, LE=1):
    """
    Shear Area, Internal Threads (Bolt) based on ISO/TR 16224:2012(E), Section 4.2.3.1

    Arguments:
    LE --- length of engagement (default = 1)
    """
    if self.dims_ISO == 'basic':
        ASn = (LE / self.p) * pi * self.dbsc * (self.p / 2 + (self.dbsc - self.D2bsc) / sqrt(3))
    elif self.dims_ISO == 'min':
        ASn = (LE / self.p) * pi * self.dmin * (self.p / 2 + (self.dmin - self.D2max) / sqrt(3))
    else:
        raise ValueError(f'Unknown option for dims_ISO: {self.dims_ISO}')

    return ASn

def C1_ISO(self, s):
    """
    Modification factor for nut dilation based on ISO/TR 16224:2012(E), Section 4.2.3.1

    C1 is undefined for when s/D < 1.4
    C1 taken equal to 1.0 when s/D >= 1.8 (this is slighly different than the equation in ISO/TR 16224:2012(E))

    Arguments:
    s --- width across flats of the nut
    """
    s_over_d = s / self.dbsc
    return C1_ISO(s_over_d)

def C2_ISO(self):
    """
    Modification factor for thread bending effect based on ISO/TR 16224:2012(E), Section 4.2.3.1
    """
    Rs = (self.UTSn * self.ASn_ISO()) / (self.UTSs * self.ASb_ISO())
    return C2_ISO(Rs)

def C3_ISO(self):
    """
    Modification factor for thread bending effect based on ISO/TR 16224:2012(E), Section 4.2.3.1
    """
    Rs = (self.UTSn * self.ASn_ISO()) / (self.UTSs * self.ASb_ISO())
    return C3_ISO(Rs)

def LEr_ISO(self, s):
    """
    Length of engagement required for tensile failure based on Analysis and Design of Threaded Assemblies,
        E.M. Alexander

    Arguments:
    s --- width across flats of the nut
    """
    LEr1 = self.As_ISO() / (0.6 * self.ASb_ISO() * self.C1_ISO(s) * self.C2_ISO())
    LEr2 = (self.As_ISO() * self.UTSs) / (0.6 * self.UTSn * self.ASn_ISO() * self.C1_ISO(s) * self.C3_ISO())
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