__author__ = 'reynolds12'


def BitShiftLeft(a, b):
    """
    :param a: integer
    :param b: integer
    :return:  integer
    """
    return a<<b

def BitShiftRight(a, b):
    """
    :param a: integer
    :param b: integer
    :return:  integer
    """
    return a>>b

def BitOr(a, b):
    """
    :param a: integer
    :param b: integer
    :return:  integer
    """
    return a|b

def BitAnd(a, b):
    """
    :param a: integer
    :param b: integer
    :return:  integer
    """
    return a&b

def RGBColor(r, g, b):
    """
    :param r: integer
    :param g: integer
    :param b: integer
    :return:  color
    """
    #TODO: implement
    assert False
    return 1

def IntegerQ(x):
    """

    :param x: unum
    :return: boolean
    """
    #TODO: implement
    assert False
    return x in integer

def setenv(e, f):
    """
    :param e:
    :param f:
    :return:
    """
    assert (e in range(0, 4))
    assert (f in range(0, 11))
    global esizesize, fsizesize, esizemax, fsizemax, utagsize, maxubits,\
        ubitmask, fsizemask, esizemask, efsizemask, utagmask,\
        ulpu, smallsubnormalu, smallnormalu, signbigu,\
        posinfu, maxrealu, minrealu, neginfu, negbigu, qNaNu, sNaNu,\
        negopeninfu, posopeninfu, negopenzerou, maxreal, smallsubnormal
    esizesize = e
    fsizesize = f
    esizemax = 2**esizesize
    fsizemax = 2**fsizesize
    utagsize = 1 + f + e
    maxubits = 1 + esizemax + fsizemax + utagsize
    ubitmask = BitShiftLeft(1, utagsize - 1)
    fsizemask = BitShiftLeft(1, f) - 1
    esizemask = (ubitmask - 1) - fsizemask
    efsizemask = BitOr(esizemask, fsizemask)
    utagmask = BitOr(ubitmask, efsizemask)
    ulpu = BitShiftLeft(1, utagsize)
    smallsubnormalu = efsizemask + ulpu
    smallnormalu = efsizemask + BitShiftLeft(1, maxubits - 1 - esizemax)
    signbigu = BitShiftLeft(1, maxubits - 1)
    posinfu = signbigu - 1 - ubitmask
    maxrealu = posinfu - ulpu
    minrealu = maxrealu + signbigu
    neginfu = posinfu + signbigu
    negbigu = neginfu - ulpu
    qNaNu = posinfu + ubitmask
    sNaNu = neginfu + ubitmask

    if utagsize == 1:
        negopeninfu = 0b1101
        posopeninfu = 0b0101
    else:
        negopeninfu = BitShiftLeft(0b1111, utagsize - 1)
        posopeninfu = BitShiftLeft(0b0111, utagsize - 1)
    negopenzerou = BitShiftLeft(0b1001, utagsize - 1)
    maxreal = 2**2**(esizemax - 1)*(2**fsizemax - 1)/2**(fsizemax - 1)
    smallsubnormal = 2**(2 - 2**(esizemax - 1) - fsizemax)


# Make sure values are initialized to something, to start.
setenv(3, 4)

# Local palette definitions. *)
gogreen = RGBColor(0, .75, .625)  # Traffic light color *)
cautionamber = RGBColor(.96, .72, 0)  # Traffic light color *)
stopred = RGBColor(1, .125, 0)  # Traffic light color *)
brightblue = RGBColor(.25, .5, 1)  # Better contrast with black *)
sanegreen = RGBColor(0, .75, 0)  # Better contrast with white *)
paleblue = RGBColor(.9, .9, 1)  # Background color for g-bound tables *)
brightpurple = RGBColor(.75, .5, 1)  # Used in "wrapping problem" *)
brightmagenta = RGBColor(1, .25, 1)  # Prints better than magenta *)
textamber = RGBColor(.75, .5, 0)  # Better contrast with white *)
chartreuse = RGBColor(.875, 1, .5)  # Background for general interval table *)


# View the three fields of a utag as a color-coded binary string. *)

def utagview(u):
    """
    :param u: integer
    :return:
    """
    e = BitShiftRight(BitAnd(u, esizemask), fsizesize)
    f = BitAnd(u, fsizemask)
    i = BitShiftRight(u, utagsize - 1)
    if i == 1:
        ubit_flag = "..."
    else:
        ubit_flag = "\/"  # down arrow
    Grid(((Style(i, Magenta, "Input"),
           Style(IntegerString(e, 2, esizesize), sanegreen, "Input"),
           Style(IntegerString(f, 2, fsizesize), Gray, "Input")),
         (ubit_flag,
          Style(e + 1, "Text"),
          Style(f + 1, "Text"))),
         Frame -> (None, None, {(1, 1) : True, (1, 2) : True, (1, 3) : True}))


def unumQ(x):
    """ Test if a value is a legitimate unum. (Must be integer, and in-range.) *)
    :param x:
    :return boolean:
    """
    if IntegerQ(x):
        if (x >= 0) ^ (x <= sNaNu):
            return True
        else:
            return False
    else:
         return False