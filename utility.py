import constants


def calculate_multiplier(formula: str) -> float:
    """
    Converts a string formula to a float multiplier

    :param formula:
    :return:
    :raises ValueError: when the formula cannot be converted into a multiplier
    """
    # if the formula is left blank it defaults to *1
    if formula == '':
        formula = '*1'

    formula = formula.upper()

    # discount formula
    if formula[0] in '+-':
        return 1 + float(formula) / 100

    # markup formula
    if formula[0] == 'D':
        return 1 / float(formula[1:])

    # gross profit formula
    if formula.startswith('GP'):
        number = float(formula[2:])
        # GP100 is not a valid formula in eclipse
        if number > 99.99:
            raise ValueError(f'GP Formulas must be below 100: {formula}')
        multiplier = 1 / (1 - float(formula[2:]) / 100)
        return multiplier

    # multiplier formula
    if formula[0] in '*X':
        return float(formula[1:])

    raise ValueError(f'{formula} is not a valid formula')


def find_multiplier_formula(multiplier, decimals):
    if decimals == 'Auto':
        return f'*{multiplier}'
    else:
        return f'*{multiplier:0.{int(decimals)}f}'


def find_markup_formula(multiplier, decimals):
    if decimals == 'Auto':
        return f'D{1/multiplier}'
    else:
        return f'D{1/multiplier:0.{int(decimals)}f}'


def find_discount_formula(multiplier, decimals):
    print(multiplier)
    if decimals == 'Auto':
        return f'{(multiplier - 1)*100:+}'
    else:
        temp1 = (multiplier - 1)
        temp2 = temp1 * 100.0
        temp3 = int(decimals)
        temp4 = f'{temp2:+0.{temp3}f}'
        return f'{temp4}'


def find_gross_profit_formula(multiplier, decimals):
    # was having problems with different values from the f-string and rounding the number

    numeric_part = (1-1/multiplier) * 100
    if decimals == 'Auto':
        return f'GP{numeric_part}' if abs(numeric_part) < 100 else ''
    else:
        return f'GP{numeric_part:0.{int(decimals)}f}' if abs(numeric_part) < 100 else ''


def valid_formula(formula):
    if formula is None:
        return False
    formula = formula.upper()
    if formula == '':
        return True
    if formula[0] in ['*', 'X', 'D']:
        try:
            return True if float(formula[1:]) != 0 else False
        except ValueError:
            return False
    if formula[0] in ['-', '+']:
        try:
            return True if float(formula[1:]) != 0 else False
        except ValueError:
            return False
    if formula.startswith('GP'):
        try:
            return True if (float(formula[2:]) != 0) and (float(formula[2:]) < 100) else False
        except ValueError:
            return False
    return False


def smallestMultiplier(basis, unit):
    decimals = constants.MAX_DECIMALS
    while decimals >= 0:
        gm = basis/unit
        multiplier = round(1/(1-gm), decimals)
        if round(basis * multiplier, 3) != unit:
            break
        else:
            decimals = decimals - 1
    multiplier = round(unit / basis, decimals + 1)
    return multiplier
