__author__ = 'reynolds12'
""" File unum_computing.py implements unum from John Gustafson
"""

import fractions
import math
import numbers

# The functions below replace the corresponding built-in Mathematica functions.

def Abs(x):
    return abs(x)

def BitAnd(x, y):
    return x & y

def BitOr(x, y):
    return x | y

def BitShiftLeft(b, s):
    return b << s

def BitShiftRight(b, s):
    return b >> s

def BitXor(b, s):
    return b ^ s

def Boole(x):
    """ Explicitly turn a boolean into an integer.
    """
    return 1 if x else 0

def Ceiling(x):
    return math.ceil(x)

def Denominator(x):
    """ Extract denominator of a rational number
    """
    return fractions.Fraction(x).Denomiator

def Floor(x):
    return math.floor(x)

def IntegerQ(x):
    return isinstance(x, int)
    #    if x == Infinity or x == NegInfinity or x == NaN, Mathematica returns False

def Log(b, x):
    return math.log(x, b)

def Max(a, b):
    return max(a, b)

def NumericQ(x):
    return isinstance(x, int) or isinstance(x, float) or isinstance(x, long) or isinstance(x, complex)
    #    if x == Infinity or x == NegInfinity or x == NaN, Mathematica returns False

# Not implemented:
def ne(x):
    # Defined later in Mathematica:
    raise NotImplementedError

def RGBColor(RGB_triplet):
    raise NotImplementedError

def Style(a,b,c=None):
    raise NotImplementedError

def IntegerString(a,b,c):
    raise NotImplementedError

def Grid(string_style_blocks, Frame):
    raise NotImplementedError

def Row (string_style_blocks):
    raise NotImplementedError

Bold = None
Gray = None
Magenta = None
Red = None

Infinity = float("inf")
NegInfinity = float("-inf")
NaN = float("nan")

# END functions replacing built-in Mathematica functions.

def setenv(e, f):
    """ Set the environment variables based on the esizesize and
    fsizesize. In this prototype, the maximum esizesize is 4 and the
    maximum fsizesize is 11.
    """
    assert e in range(0, 4)
    assert f in range(0,11)
    global esizesize, fsizesize
    global esizemax, fsizemax
    global utagsize
    global maxubits
    global ubitmask
    global fsizemask
    global esizemask
    global efsizemask
    global utagmask
    global ulpu
    global smallsubnormalu
    global smallnormalu
    global signbigu
    global posinfu
    global maxrealu
    global minrealu
    global neginfu
    global negbigu
    global qNaNu
    global sNaNu
    global negopeninfu
    global posopeninfu
    global negopenzerou
    global maxreal
    global smallsubnormal

    esizesize, fsizesize = e, f
    esizemax, fsizemax = 2**e, 2**f
    utagsize = 1 + f + e
    maxubits = 1 + esizemax + fsizemax + utagsize
    ubitmask = BitShiftLeft(1, (utagsize - 1))
    fsizemask = (1 << f) - 1
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
    negopeninfu = 0b1101 if utagsize == 1 else BitShiftLeft(0b1111, utagsize - 1)
    posopeninfu = 0b0101 if utagsize == 1 else  BitShiftLeft(0b0111, utagsize - 1)
    negopenzerou = BitShiftLeft(0b1001, utagsize - 1)
    maxreal = 2**2**(esizemax - 1) * (2**fsizemax - 1)/2**(fsizemax - 1)
    smallsubnormal = 2**(2 - 2**(esizemax - 1) - fsizemax)

# Make sure values are initialized to something, to start.
setenv(3, 4)

# Local palette definitions.
gogreen = RGBColor((0, .75, .625)) # Traffic light color
cautionamber = RGBColor((.96, .72, 0))  # Traffic light color
stopred = RGBColor((1, .125, 0)) # Traffic light color
brightblue = RGBColor((.25, .5, 1)) # Better contrast with black
sanegreen = RGBColor((0, .75, 0)) # Better contrast with white
paleblue = RGBColor((.9, .9, 1)) # Background color for g-bound tables
brightpurple = RGBColor((.75, .5, 1))# Used in "wrapping problem"
brightmagenta = RGBColor((1, .25, 1))# Prints better than magenta
textamber = RGBColor((.75, .5, 0)) # Better contrast with white
chartreuse = RGBColor((.875, 1, .5)) # Background for general interval table

# View the three fields of a utag as a color-coded binary string. 

def utagview(u): 
    e = BitShiftRight(BitAnd(u, esizemask), fsizesize)
    f = BitAnd(u, fsizemask)
    i = BitShiftRight(u, utagsize - 1)

    Grid(
        (
            (Style(i, Magenta, "Input"),
             Style(IntegerString(e, 2, esizesize), sanegreen, "Input"),
             Style(IntegerString(f, 2, fsizesize), Gray, "Input")
             ),
            (("\(NegativeThinSpace)\(CenterEllipsis)"
             if i == 1 else
             "\(DownArrow)"),
             Style(e + 1, "Text"),
             Style(f + 1, "Text")
             )
        ),
        Frame=(None,
               None,
               {(1, 1): True,
                (1, 2): True,
                (1, 3): True}
               )
    )

# Test if a value is a legitimate unum. (Must be integer, and in-range.)
def unumQ(x):
    return isinstance(x, int) and 0 <= x <= sNaNu


# Values and bit masks for taking apart a unum bit string.
# Independent of the contents of the utag.
def fsizeminus1(u):
    assert unumQ(u)
    return BitAnd(u, fsizemask)

def fsize(u):
    assert unumQ(u)
    return 1 + fsizeminus1(u)

def esizeminus1(u):
    assert unumQ(u)
    return BitShiftRight(BitAnd(u, esizemask), fsizesize)

def esize(u):
    assert unumQ(u)
    return 1 + esizeminus1(u)

def utag(esize, fsize):
    assert isinstance(esize, int)
    assert 1 <= esize <= esizemax
    assert isinstance(fsize, int)
    assert 1 <= fsize <= fsizemax
    return BitOr(fsize - 1, BitShiftLeft(esize - 1, fsizesize))

def numbits(u):
    assert unumQ(u)
    return 1 + esize(u) + fsize(u) + utagsize

def signmask(u):
    assert unumQ(u)
    return BitShiftLeft(1, numbits(u) - 1)

def hiddenmask(u):
    assert unumQ(u)
    return BitShiftLeft(1, fsize(u) + utagsize)

def fracmask(u):
    assert unumQ(u)
    return BitShiftLeft(BitShiftLeft(1, fsize(u)) - 1, utagsize)

def expomask(u):
    assert unumQ(u)
    return BitShiftLeft(BitShiftLeft(1, esize(u)) - 1, fsize(u) + utagsize)

def floatmask(u):
    assert unumQ(u)
    return signmask(u) + expomask(u) + fracmask(u)


# Values and bit masks that depend on what is stored in the utag. 
def bias(u):
    assert unumQ(u)
    return 2^esizeminus1(u) - 1

def sign(u):
    assert unumQ(u)
    return Boole(BitAnd(u, signmask(u)) > 0)

def expo(u):
    assert unumQ(u)
    return BitShiftRight(BitAnd(u, expomask(u)), utagsize + fsize(u))

def hidden(u):
    assert unumQ(u)
    return Boole(expo(u) > 0)

def frac(u):
    assert unumQ(u)
    return BitShiftRight(BitAnd(u, fracmask(u)), utagsize)

def inexQ(u):
    assert unumQ(u)
    return BitAnd(ubitmask, u) > 0

def exQ(u):
    assert unumQ(u)
    return BitAnd(ubitmask, u) == 0

def exact(u):
    assert unumQ(u)
    return BitXor(u, ubitmask) if inexQ(u) else u

def colorcode(u):
    """Display the six fields of a unum bit string, color-coded and spaced.
    """
    assert unumQ(u)
    return Row(
        (Style(sign(u), Red, Bold),
         " ",
         Style(IntegerString(expo(u), 2, esize(u)), brightblue, Bold),
         " ",
         Style(IntegerString(frac(u), 2, fsize(u)), Bold),
         " ",
         Style(Boole(inexQ(u)), Magenta),
         " ",
         Style(IntegerString(esizeminus1(u), 2, esizesize), sanegreen),
         " ",
         Style(IntegerString(fsizeminus1(u), 2, fsizesize), Gray)))

# Numerical value meant by exponent bits; helper function for u2f:
def expovalue(u):
    assert unumQ(u)
    return expo(u) - bias(u) + 1 - hidden(u)

# Convert an exact unum to its float value.
def u2f(u):
    assert unumQ(u)
    assert exQ(u)
    if u == posinfu:
        return Infinity
    elif u == neginfu:
        return NegInfinity
    else:
        return (-1)**sign(u) * 2**expovalue(u) * (hidden(u) + frac(u)/2**fsize(u))

# Biggest unum possible with identical utag contents.
def bigu(u):
    assert unumQ(u)
    return expomask(u) + fracmask(u) + BitAnd(efsizemask, u) \
        - ulpu * Boole(BitAnd(u, efsizemask) == efsizemask)

# Biggest numerical value representable with identical utag contents.
def big(u):
    assert unumQ(u)
    return u2f(bigu(u))

# Some synonyms.
open, closed = True, False

# Test if x is representable as a float. (Including exception values.)
def floatQ(x):
    if NumericQ(x):
        return not isinstance(x, complex)
    else:
        # These return False from NumericQ non-numeric, but are representable:
        if x == Infinity or x == NegInfinity or x == NaN:
            return True
        else:
            return False

def gQ(x):
    """Test for a value being in the form of a general bound.
    """
    # Changed indexes to zero-based:
    def is2x2(x):
        return (isinstance(x, (list, tuple)) and
            len(x) == 2 and
            isinstance(x[0], (list, tuple)) and
            len(x[0]) == 2 and
            isinstance(x[1], (list, tuple)) and
            len(x[1]) == 2)

    def is_2_float_bool_pairs(x):
        return (is2x2(x) and
            type(x[1, 0]) is bool and
            type(x[1, 0]) is bool and
            floatQ(x[0, 0]) and
            floatQ(x[0, 1]))

    def contains_NaN(x):
        return (x[0, 0] == NaN or x[0, 1] == NaN)

    def equal_endpoints(x):
        return (x[0, 0] == x[0, 1] and not x[1, 0] and not x[1, 1])

    def lower_higher_endpoints(x):
        return x[0, 0] < x[0, 1]

    return is_2_float_bool_pairs(x) and (contains_NaN(x) or equal_endpoints(x) or lower_higher_endpoints(x))

def uboundQ(x):
    """ Test for a value being in the form of a ubound, with one or two unums. 
    """
    def is_1_or_2_list(x):
        return (isinstance(x, (list, tuple)) and len(x)in (1, 2))

    if is_1_or_2_list(x):
        xL = x[0]
        xR = x[-1]
        if (unumQ(xL) and unumQ(xR)):
            gL, gR = unum2g(xL), unum2g(xR)
            return ((len(x) == 1 or xL == qNaNu or xL == sNaNu or xR == qNaNu or xR == sNaNu) or
                (gL[0, 0] < gR[0, 1] or (gL[0, 0] == gR[0, 1] and exQ(xL) and exQ(xR))))
        else:
            return False
    else:
        return False

def uboundpairQ(x):
    """ Test for a value being in the form of a ubound with two unums.
    """
    return (uboundQ(x) and len(x) == 2)

def uQ(x):
    """ Test for a value being in the u-layer: unum or ubound.
    """
    return (unumQ(x) or uboundQ(x))

def f2g(x):
    """Trivial expression of a floatable value in the form of a general interval.
    """
    assert floatQ(x)
    if x == NaN:
        return [[NaN, NaN],
                [open, open]]
    else:
        return [[x, x],
                [closed, closed]]

def unum2g(u):
    """ Conversion of a unum to a general interval.
    """
    assert unumQ(u)
    if u == qNaNu or u == sNaNu:
        return [[NaN, NaN],
                [open, open]]
    else:
        x = u2f(exact(u))
        y = u2f(exact(u) + ulpu)
        if exQ(u):
            return [[x, x],
                    [closed, closed]]
        elif u == bigu(u) + ubitmask:
            return [[big(u), Infinity],
                    [open, open]]
        elif u == signmask(u) + bigu(u) + ubitmask:
            return [[NegInfinity, -big(u)],
                    [open, open]]
        elif sign(u) == 1:
            return [[y, x],
                    [open, open]]
        else:
            # If negative, the left endpoint is the one farther from zero.
            return [[x, y],
                    [open, open]]

def ubound2g(ub):
    """ Conversion of a ubound to a general interval.
    """
    assert uboundQ(ub)
    uL = ub[0]
    uR = ub[-1]
    if uL == qNaNu or uL == sNaNu or uR == qNaNu or uR == sNaNu:
        return [[NaN, NaN],
                [open, open]]
    else:
        gL, gR = (unum2g(uL), unum2g(uR))
        return [[gL[0,0], gR[0,1]],
                [gL[1,0], gR[1,1]]]

def u2g(u):
    """ Conversion of a unum or ubound to a general interval.
    """
    assert uQ(u)
    if unumQ(u):
        return unum2g(u)
        return unum2g(u)
    else:
        return ubound2g(u)

def x2u(x):
    """ Conversion of a floatable real to a unum. Same as the "^" 
    annotation. Most of the complexity stems from seeking the shortest 
    possible bit string. 
    """
    assert floatQ(x)
    # Exceptional nonnumeric values:
    if x == NaN:
        return qNaNu
    elif x == Infinity:
        return posinfu
    elif x == NegInfinity:
        return neginfu
    # Magnitudes too large to represent:
    elif Abs(x) > maxreal:
        return maxrealu + ubitmask + (signbigu if x < 0 else 0)
    # Zero is a special case. The smallest unum for it is just 0:
    elif x == 0:
        return 0
    # Magnitudes too small to represent become
    # "inexact zero" with the maximum exponent and fraction field sizes:
    elif Abs(x) < smallsubnormal:
        return utagmask + (signbigu if x < 0 else 0)
    # For subnormal numbers, divide by the ULP value to get the fractional part.
    # The While loop strips off trailing bits.
    elif Abs(x) < u2f(smallnormalu):
        y = Abs(x)/smallsubnormal
        y = ((signbigu if x < 0 else 0) + efsizemask +
             (ubitmask if y != Floor(y) else 0) +
             BitShiftLeft (Floor(y), utagsize))
        while BitAnd(BitShiftLeft(3, utagsize - 1), y) == 0:
            y = (y - BitAnd(efsizemask, y)) / 2 + BitAnd(efsizemask, y) - 1
        return y

    # All remaining cases are in the normalized range.
    else:
        y = Abs(x)/2**scale(x)
        n = 0
        while Floor(y) != y and n < fsizemax:
            n += 1
            y *= 2
        if y == Floor(y):
            # then the value is representable exactly.
            # Fill in fields from right to left:
            # Size of fraction field, fits in the rightmost fsizesize bits...
            y = (n - Boole(n > 0)
                # Size of exponent field minus 1, fits in the esizesize bits...
                + BitShiftLeft(ne(x) - 1, fsizesize)
                # Significant bits after hidden bit, fits left of the unum tag bits...
                + (0 if n == 0 else BitShiftLeft(Floor(y) - 2**scale(y), utagsize))
                # Value of exponent bits, adjusted for bias...
                + BitShiftLeft(scale(x) + 2**(ne(x) - 1) - 1,
                               utagsize + n + Boole(n == 0))
                # If negative, add the sign bit
                + (BitShiftLeft(1, utagsize + n + Boole(n == 0) + ne(x)) if x < 0 else 0))
            # If a number is more concise as a subnormal, make it one.
            z = Log(2, 1 - Log(2, Abs(x)))
            if IntegerQ(z) and z >= 0:
                return (BitShiftLeft(z, fsizesize) + ulpu +
                        Boole(x < 0) * signmask(BitShiftLeft(z, fsizesize)))
            else:
                return y
        else:
            # else inexact. Use all available fraction bits.
            z = (Ceiling(Abs(x)/2**(scale(x) - fsizemax)) *
                 2**(scale(x) - fsizemax))
            n = Max(ne(x), ne(z))
            # All bits on for the fraction size, since we're using the maximum
            y = (fsizemask
                # Store the exponent size minus 1 in the exponent size field
                + BitShiftLeft(n - 1, fsizesize)
                # Back off by one ULP and make it inexact
                + ubitmask - ulpu
                # Fraction bits are the ones to the left of the binary point
                # after removing hidden bit and scaling
                + BitShiftLeft(Floor(z/2**scale(z) - 1) * 2**fsizemax, utagsize)
                # Exponent value goes in the exponent field
                + BitShiftLeft(scale(z) + 2**(n - 1) - 1, utagsize + fsizemax))
            # If x is negative, set the sign bit in the unum.
            if x < 0:
                y += signmask(y)
            return y

# Assign the x2u function to the "^" notation. *)
OverHat = x2u

def autoN(x):
    """ View a float as a decimal, using as many digits as needed to be exact.
    """
    if x == NaN or x == 0 or x == Infinity:
        return x
    elif x < 0:
        return Row(("-", autoN(-x)))
    else:
        y = Log(2, Denominator(x))
        if y == 0:
            return IntegerString(x, 10, 1 + Floor(Log(10, x)))
        if isinstance(x, numbers.Rational) and y == Floor(y):
           y = x - Floor(x)
           z = Floor(Log(2, Denominator(y)))
           return Row((Floor(x), ".", IntegerString(y*10^z, 10, z)))
        else:
            return "?"

# def unumview(u):
#     """ Display a unum with color-coding and annotation. Warning: there are some negative spaces in the StringForm
#     expressions.
#     """
#     e = expo(u)
#     es = esizeminus1(u)
#     f = frac(u)
#     fs = fsizeminus1(u)
#     g = u2g(u)
#     i = inexQ(u)
#     NaNQ = (u == sNaNu || u == qNaNu)
#     s = sign(u)
#     specQ = (u == sNaNu || u == qNaNu || u == posinfu || u == neginfu)
#
#     return Grid(
#         (
#             (
#                 Item(Style(s, Red, "Input"), Frame -> True, Alignment -> "Left"),
#                 Item(Style(IntegerString(e, 2, esize(u), brightblue, "Input"), Frame -> True),
#                 " ",
#                 Item(Style(IntegerString(f, 2, fsize(u), "Input"), Frame -> "True"),
#                 Item(Style(Boole(i), Magenta, "Input", Plain), Frame -> "True"),
#                 Item(Style(IntegerString(es, 2, esizesize), sanegreen, "Input", Plain), Frame -> True),
#                 Item(Style(IntegerString(fs, 2, fsizesize), FontColor -> Gray, "Input", Plain), Frame -> True),
#                 " ",
#                 if(not NaNQ and not i and u2f(u) != Floor(u2f(u),
#                     u2f(u),
#                     Row((
#                         Item(
#                             Which(
#                                 specQ,
#                                     Style("special case string", Italic),
#                                 (g[1, 1] == Floor(g[1, 1]) and g[1, 2] == Floor(g[1, 2])),
#                                     " ",
#                                 True,
#                                     StringForm(If(g[2, 1], "(``,", "[``,"), g[1, 1])
#                             )
#                         ),
#                         Item(
#                             If(NaNQ ||  (g[1, 1] == Floor(g[1, 1]) and g[1, 2] == Floor(g[1, 2])),
#                                 " ",
#                                 StringForm(If(g[2, 2], "``)", "``]"), g[1, 2])
#                             )
#                         )
#                     )
#                     )
#                 )
#             ),
#             (
#                 Style(If(s == 0, "+", "-"), Red),
#                 Style(StringForm("``\[Times]", Superscript(2, expovalue(u))), brightblue),
#                 Style(StringForm("\[NegativeThickSpace]``+\[NegativeThickSpace]\\[NegativeThickSpace]", hidden(u))),
#                 DisplayForm(FractionBox(f, 2^(fs + 1))),
#                 Style(If(i, "\[CenterEllipsis]", "\[DownArrow]"), Magenta),
#                 Style(es + 1, sanegreen),
#                 Style(fs + 1, Gray),
#                 " ",
#                 If(not NaNQ and  not i,
#                     Row((If(not specQ, "= "),
#                     autoN(g[1, 1])),
#                 Row((
#                     Item(If(NaNQ,
#                         " ",
#                         StringForm(If(g[2, 1],
#                             "= (``,", "= [``,"),
#                             autoN(g[1, 1]))),
#                     Item(If(NaNQ,
#                         "NaN",
#                         StringForm(If(g[2, 2],
#                             "``)",
#                             "``]"),
#                         autoN(g[1, 2])),
#                         Alignment -> Left))))
#             )
#         ),
#         ItemStyle -> (Automatic,
#                       2 -> ("Text", 12),
#                       (1, 9) -> "Text"))






# later:
def scale (x):
    """ Helper function for conversion; find the scale factor, with exceptions.
    """
    assert floatQ(x) and x != Infinity and x != NaN
    return (0 if x == 0 else Floor(Log(2, Abs(x))))

def ne(x):
    """ Find a concise number of exponent bits, accounting for subnormals.
    """
    assert floatQ(x) and x != Infinity and x != NaN
    return (1 if x == 0 or scale(x) == 1 else
            Ceiling(Log(2, 1 + Abs(scale(x) - 1))) + 1)

