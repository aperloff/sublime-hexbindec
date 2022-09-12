import re

import sublime
import sublime_plugin

# ============================================================================
# CONFIGURATION DESCRIPTION
#
# Each TextCommand uses the view.settings() object to look for custom format
# patterns. That's why it is possible to define a hex/bin for each type of
# source with the help of language specific settings files.
#
# If no setting is found the following patterns are used by default to extract
# the hex/bin value from the selected text and format the output of the
# converted value.
#
# REMARKS
#     A hex/bin value can be single quoted.
#
# EXAMPLE CONFIGURATION
#
#    // Binaries look like 'B101110'
#    "convert_src_bin": "'B([01]+)'",
#    // After convertion to binary format the output as follows
#    "convert_dst_bin": "'B{0:b}'",
#
#    // Hexadecimals look like 'H1AF23'
#    "convert_src_hex": "'H([0-9A-Z]+)'",
#    // After convertion to hexadecimal format the output as follows
#    "convert_dst_hex": "'H{0:X}'",
#
#    // Exponential decimals look like 1.42EX-5
#    "convert_src_exp": "\\b([1-9]\\.\\d+)EX([-+]?\\d+)\\b",
#    "convert_dst_exp": "EX",
# ============================================================================
# Default binary destination format
_CONVERT_DST_BIN_DFLT = '{0:b}'
# Default hexadecimal destination format
_CONVERT_DST_HEX_DFLT = '{0:#x}'
# Default exponential destination format
_CONVERT_DST_EXP_DFLT = r'e'
# Default binary (int) search pattern
_CONVERT_SRC_BIN_DFLT = r'\b(?:0b)?([01]+)\b'
# Default binary (ufixed) search pattern
_CONVERT_SRC_FXD_DFLT = r'\b(?:0b)?(?P<int>[01]+)([.])(?P<frac>[01]+)\b'
# Default hexadecimal search pattern
_CONVERT_SRC_HEX_DFLT = r'\b(?:0x)?([0-9a-fA-F]+)h?\b'
# Default exponential search pattern
_CONVERT_SRC_EXP_DFLT = r'\b(\d+\.\d+)[e,E]([-+]?\d+)\b'
# ============================================================================


def load_pattern(view, name, default):
    try:
        return re.compile(view.settings().get(name, default))
    except:
        return re.compile(default)


class BinToDecCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        r = load_pattern(view, 'convert_src_bin', _CONVERT_SRC_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                match = r.match(view.substr(sel))
                view.replace(edit, sel, str(int(match.group(1), 2)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid binary value(s)!" % num_skip)


class BinToHexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_hex', _CONVERT_DST_HEX_DFLT)
        r = load_pattern(view, 'convert_src_bin', _CONVERT_SRC_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                match = r.match(view.substr(sel))
                view.replace(edit, sel, dst_format.format(int(match.group(1), 2)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid binary value(s)!" % num_skip)


class DecToBinCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_bin', _CONVERT_DST_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)

                dec = view.substr(sel).strip()
                view.replace(edit, sel, dst_format.format(int(dec)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid decimal value(s)!" % num_skip)


class DecToHexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_hex', _CONVERT_DST_HEX_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)

                dec = int(view.substr(sel).strip())
                view.replace(edit, sel, dst_format.format(dec))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid decimal value(s)!" % num_skip)


class HexToBinCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_bin', _CONVERT_DST_BIN_DFLT)
        r = load_pattern(view, 'convert_src_hex', _CONVERT_SRC_HEX_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                # valid hex: 10 , 0x10 , 0x10h , 10h, h10
                match = r.match(view.substr(sel))
                view.replace(edit, sel, dst_format.format(int(match.group(1), 16)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid hexadecimal value(s)!" % num_skip)


class HexToDecCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        r = load_pattern(view, 'convert_src_hex', _CONVERT_SRC_HEX_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                # validate selection
                match = r.match(view.substr(sel))
                # replace selection with the result
                view.replace(edit, sel, str(int(match.group(1), 16)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid hexadecimal value(s)!" % num_skip)


class ExpToDecCommand(sublime_plugin.TextCommand):
    """
    Convert real values with exponent to normal decimal.
    Minimum: 9.0e-4
    Maximum: 9.0e15
    EXAMPLE:
        1.42e3  ->  1420
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        r = load_pattern(view, 'convert_src_exp', _CONVERT_SRC_EXP_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    while view.substr(sel.a - 1) in "0123456789.eExX-":
                        sel.a -= 1
                    while view.substr(sel.b) in "0123456789.eExX-":
                        sel.b += 1

                # validate selection
                match = r.match(view.substr(sel))
                # convert the match and round by 18 digits after comma
                result = round(float(match.group(1)) * 10 ** float(match.group(2)), 18)
                # replace selection with the formated result
                view.replace(edit, sel, str(result).rstrip('0').rstrip('.'))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid exponential value(s)!" % num_skip)


class DecToExpCommand(sublime_plugin.TextCommand):
    """
    Convert a real value to exponential format.
    Minimum: 9.0e-4
    Maximum: 9.0e15
    EXAMPLE:
        1420  ->  1.42e3
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_pattern = view.settings().get('convert_dst_exp', _CONVERT_DST_EXP_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    while view.substr(sel.a - 1) in "0123456789.":
                        sel.a -= 1
                    while view.substr(sel.b) in "0123456789.":
                        sel.b += 1

                # convert the value
                base = float(view.substr(sel))
                exp = 0
                while base > 10:
                    base /= 10
                    exp += 1
                while base < 1:
                    base *= 10
                    exp -= 1

                # convert base to string
                base = str(base).rstrip('0').rstrip('.')
                # replace selection with the formated result
                view.replace(edit, sel, base + dst_pattern + str(exp))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid decimal value(s)!" % num_skip)


def UFixedToDecimal(matches):
    from decimal import Decimal, getcontext
    getcontext().prec = 128
    integer_portion = int(matches['int'], 2)
    value = Decimal(0.0)
    for i, digit in enumerate(matches['frac']):
        if digit == "1":
            value += (Decimal(2) ** Decimal(-int(i) - 1))
    fractional_portion = value
    return integer_portion + fractional_portion


class UfxToDecCommand(sublime_plugin.TextCommand):
    """
    Convert an unsigned fixed point binary number into decimal format.
    Precision: 128 digits
    EXAMPLE:
        0x101.110  ->  5.75
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        r = load_pattern(view, 'convert_src_fxd', _CONVERT_SRC_FXD_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    while view.substr(sel.a - 1) in "01.":
                        sel.a -= 1
                    while view.substr(sel.b) in "01.":
                        sel.b += 1

                # validate selection
                match = r.match(view.substr(sel))
                if match is None:
                    raise Exception("Did not match")

                view.replace(edit, sel, str(UFixedToDecimal(match.groupdict())))
            except:
                num_skip += 1

        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid fixed point value(s)!" % num_skip)


def FixedToDecimal(matches):
    from decimal import Decimal, getcontext
    getcontext().prec = 128
    sign = matches['int'][0]
    if sign == '0':
        return UFixedToDecimal(matches)
    else:
        power = len(matches['int']) - 1
        start = -(Decimal(2) ** Decimal(power))
        matches['int'] = '0' + matches['int'][1:]
        add = UFixedToDecimal(matches)
        value = start + add
    return value


class SfxToDecCommand(sublime_plugin.TextCommand):
    """
    Convert a 2s complement fixed point binary number into decimal format.
    Precision: 128 digits
    EXAMPLE:
        0x101.110  ->  -2.25
        0x1.011    ->  -0.625
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        r = load_pattern(view, 'convert_src_fxd', _CONVERT_SRC_FXD_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    while view.substr(sel.a - 1) in "01.":
                        sel.a -= 1
                    while view.substr(sel.b) in "01.":
                        sel.b += 1

                # validate selection
                match = r.match(view.substr(sel))
                if match is None:
                    raise Exception("Did not match")

                view.replace(edit, sel, str(FixedToDecimal(match.groupdict())))
            except:
                num_skip += 1

        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid fixed point value(s)!" % num_skip)


def twos_complement(value, nbits, base):
    """Compute the 2's complement of int value val"""
    val = int(value, base)
    if val < 0:
        val = (1 << nbits) + val
    else:
        if (val & (1 << (nbits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << nbits)        # compute negative value.
    return val                              # return positive value as is

class SbinToDecCommand(sublime_plugin.TextCommand):
    """
    Convert a 2s complement integer binary number into decimal format.
    EXAMPLE:
        0x101  ->  -3
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        r = load_pattern(view, 'convert_src_bin', _CONVERT_SRC_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                match = r.match(view.substr(sel))
                view.replace(edit, sel, str(twos_complement(match.group(1), len(match.group(1)), 2)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid binary value(s)!" % num_skip)


class SbinToHexCommand(sublime_plugin.TextCommand):
    """
    Convert a 2s complement integer binary number into hexadecimal format.
    EXAMPLE:
        0x101  ->  -0x3
    """

    def run(self, edit):
        num_skip = 0
        view = self.view
        # read settings
        dst_format = view.settings().get('convert_dst_hex', _CONVERT_DST_HEX_DFLT)
        r = load_pattern(view, 'convert_src_bin', _CONVERT_SRC_BIN_DFLT)
        # convert all selected numbers
        for sel in view.sel():
            try:
                # expand selection to word
                if sel.empty():
                    sel = view.word(sel)
                    # if source is single quoted, expand selection
                    # by one more character before and after the word.
                    if r.pattern[0] == '\'':
                        sel.a -= 1
                        sel.b += 1

                match = r.match(view.substr(sel))
                view.replace(edit, sel, dst_format.format(twos_complement(match.group(1), len(match.group(1)), 2)))

            except:
                num_skip += 1

        # show number of invalid values
        if num_skip > 0:
            sublime.status_message(
                "Skipped %d invalid binary value(s)!" % num_skip)