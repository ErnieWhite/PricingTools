"""

"""
import tkinter as tk
from tkinter import ttk
import re
import pyperclip

import constants
import utility
from constants import *


class FormulaConverterFrame(ttk.Frame):
    """

    """
    def __init__(self, container):
        """

        :param container:
        """
        super().__init__(container)
        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid),)

        # create the formula StringVar
        self.formula_var = tk.StringVar()

        # create the StringVars
        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()
        self.decimals_var = tk.StringVar()

        # create the entries
        self.formula_entry = ttk.Entry(
            self,
            validate='key',
            textvariable=self.formula_var,
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.decimals_combo = ttk.Combobox(self, values=constants.DECIMALS_VALUES, textvariable=self.decimals_var)
        self.decimals_combo.set('Auto')
        self.decimals_combo.bind('<<ComboboxSelected>>', self.handle_formula_change_event)

        self.multiplier_display = ttk.Entry(self, textvariable=self.multiplier_var, state='readonly')
        self.discount_display = ttk.Entry(self, textvariable=self.discount_var, state='readonly')
        self.markup_display = ttk.Entry(self, textvariable=self.markup_var, state='readonly')
        self.gross_profit_display = ttk.Entry(self, textvariable=self.gross_profit_var, state='readonly')


        # create the copy buttons
        self.multiplier_formula_button = ttk.Button(
            self,
            text="Copy",
            command=lambda: self.copy_formula(self.multiplier_var.get()),
        )
        self.discount_formula_button = ttk.Button(
            self, text="Copy",
            command=lambda: self.copy_formula(self.discount_var.get()),
        )
        self.markup_formula_button = ttk.Button(
            self,
            text="Copy",
            command=lambda: self.copy_formula(self.markup_var.get()),
        )
        self.gross_profit_formula_button = ttk.Button(
            self,
            text="Copy",
            command=lambda: self.copy_formula(self.gross_profit_var.get()),
        )

        self.place_widgets()
        self.setup_traces()

    def place_widgets(self):
        """

        :return:
        """
        # place the current widget
        ttk.Label(self, text=FORMULA).grid(row=0, column=0, sticky=tk.W)
        self.formula_entry.grid(column=1, row=0, sticky=tk.EW)

        ttk.Label(self, text=DECIMALS).grid(column=0, row=1, sticky=tk.W)
        self.decimals_combo.grid(column=1, row=1, sticky=tk.EW)

        # place the separator
        ttk.Separator(self, orient=tk.VERTICAL).grid(column=2, row=0, rowspan=4, padx=5, sticky=tk.NS)

        # place the multiplier widgets
        ttk.Label(self, text=MULTIPLIER).grid(column=4, row=0, sticky=tk.W)
        self.multiplier_display.grid(column=5, row=0)
        self.multiplier_formula_button.grid(column=6, row=0)

        # place the discount widgets
        tk.Label(self, text=DISCOUNT).grid(column=4, row=1, sticky=tk.W)
        self.discount_display.grid(column=5, row=1)
        self.discount_formula_button.grid(column=6, row=1)

        # place the markup widget
        ttk.Label(self, text=MARKUP).grid(column=4, row=2, sticky=tk.W)
        self.markup_display.grid(column=5, row=2)
        self.markup_formula_button.grid(column=6, row=2)

        # place the gross profit widgets
        ttk.Label(self, text=GROSS_PROFIT).grid(column=4, row=3, sticky=tk.W)
        self.gross_profit_display.grid(column=5, row=3)
        self.gross_profit_formula_button.grid(column=6, row=3)

    def setup_traces(self):
        """

        :return:
        """
        # self.formula_entry.bind('<Return>', self.handle_formula_change_event)
        self.formula_var.trace('w', self.handle_formula_change_event)

    def handle_formula_change_event(self, *_):
        value = self.formula_var.get()
        value = value.upper()
        self.formula_var.set(value)
        decimals = self.decimals_var.get()

        if utility.valid_formula(value) and value != '':
            multiplier = utility.calculate_multiplier(value)
            self.multiplier_var.set(utility.find_multiplier_formula(multiplier, decimals))
            self.discount_var.set(utility.find_discount_formula(multiplier, decimals))
            self.markup_var.set(utility.find_markup_formula(multiplier, decimals))
            self.gross_profit_var.set(utility.find_gross_profit_formula(multiplier, decimals))
        else:
            self.clear_calculated_formulas()

    def clear_calculated_formulas(self):
        self.multiplier_var.set('')
        self.discount_var.set('')
        self.markup_var.set('')
        self.gross_profit_var.set('')

    @staticmethod
    def copy_formula(formula):
        pyperclip.copy(formula)

    @staticmethod
    def validate(value) -> bool:
        if value == '':
            return True
        value = value.upper()
        if re.search(r'^[*XD][-,+]?\d*\.?\d*$', value):
            return True
        if re.search(r'^[-+]\d*\.?\d*$', value):
            return True
        if value == 'G' or re.search(r'^GP[-+]?\d*\.?\d*$', value):
            return True
        return False

    @staticmethod
    def on_invalid():
        pass


if __name__ == '__main__':
    app = tk.Tk()

    app.title(FORMULA_CONVERTER)

    frame = FormulaConverterFrame(app)
    frame.pack()

    app.mainloop()

