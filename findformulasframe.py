import tkinter as tk
from tkinter import ttk

import constants
import utility
import pyperclip

from constants import *


class FindFormulaFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid), )

        # create StringVar
        self.unit_price_var = tk.StringVar()
        self.basis_value_var = tk.StringVar()
        self.decimals_var = tk.StringVar()

        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()

        self.unit_price_entry = ttk.Entry(self)
        self.basis_value_entry = ttk.Entry(self)
        self.decimals_combo = ttk.Combobox(self)

        self.multiplier_display = ttk.Entry(self)
        self.discount_display = ttk.Entry(self)
        self.markup_display = ttk.Entry(self)
        self.gross_profit_display = ttk.Entry(self)

        self.multiplier_copy_button = ttk.Button(self)
        self.discount_copy_button = ttk.Button(self)
        self.markup_copy_button = ttk.Button(self)
        self.gross_profit_copy_button = ttk.Button(self)

        self.place_widgets()
        self.configure_widgets(ivcmd, vcmd)
        self.setup_traces()

    def setup_traces(self):
        self.unit_price_var.trace('w', self.update_formulas)
        self.basis_value_var.trace('w', self.update_formulas)

    def configure_widgets(self, ivcmd, vcmd):
        # create the widgets
        self.unit_price_entry.config(
            validate='key',
            textvariable=self.unit_price_var,
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.basis_value_entry.config(
            validate='key',
            textvariable=self.basis_value_var,
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.decimals_combo.config(
            values=constants.DECIMALS_VALUES,
            textvariable=self.decimals_var,
        )
        self.decimals_combo.set('Auto')
        self.decimals_combo.bind('<<ComboboxSelected>>', self.update_formulas)
        self.multiplier_display.config(
            textvariable=self.multiplier_var,
            state='readonly'
        )
        self.discount_display.config(
            textvariable=self.discount_var,
            state='readonly'
        )
        self.markup_display.config(
            textvariable=self.markup_var,
            state='readonly'
        )
        self.gross_profit_display.config(
            textvariable=self.gross_profit_var,
            state='readonly'
        )
        self.multiplier_copy_button.config(
            text='Copy',
            command=lambda: self.copy_formula(self.multiplier_var.get())
        )
        self.discount_copy_button.config(
            text='Copy',
            command=lambda: self.copy_formula(self.discount_var.get())
        )
        self.markup_copy_button.config(
            text='Copy',
            command=lambda: self.copy_formula(self.markup_var.get())
        )
        self.gross_profit_copy_button.config(
            text='Copy',
            command=lambda: self.copy_formula(self.gross_profit_var.get())
        )

    def place_widgets(self):
        ttk.Label(self, text=UNIT_PRICE).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self, text=BASIS_VALUE).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self, text=DECIMALS).grid(row=2, column=0, sticky=tk.W)

        self.unit_price_entry.grid(row=0, column=1, sticky=tk.EW)
        self.basis_value_entry.grid(row=1, column=1, sticky=tk.EW)
        self.decimals_combo.grid(row=2, column=1, sticky=tk.EW)

        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, rowspan=4, padx=5, sticky=tk.NS)

        ttk.Label(self, text=MULTIPLIER).grid(row=0, column=3, sticky=tk.W)
        ttk.Label(self, text=DISCOUNT).grid(row=1, column=3, sticky=tk.W)
        ttk.Label(self, text=MARKUP).grid(row=2, column=3, sticky=tk.W)
        ttk.Label(self, text=GROSS_PROFIT).grid(row=3, column=3, sticky=tk.W)

        self.multiplier_display.grid(row=0, column=4, sticky=tk.EW)
        self.discount_display.grid(row=1, column=4, sticky=tk.EW)
        self.markup_display.grid(row=2, column=4, sticky=tk.EW)
        self.gross_profit_display.grid(row=3, column=4, sticky=tk.EW)

        self.multiplier_copy_button.grid(row=0, column=5)
        self.discount_copy_button.grid(row=1, column=5)
        self.markup_copy_button.grid(row=2, column=5)
        self.gross_profit_copy_button.grid(row=3, column=5)

    def update_formulas(self, *_):

        decimals = self.decimals_var.get()

        if not self.unit_price_var.get() or not self.basis_value_var.get():
            self.clear_formulas()
            return

        if float(self.unit_price_var.get()) == 0 or float(self.basis_value_var.get()) == 0:
            self.clear_formulas()
            return

        unit_price = float(self.unit_price_var.get())
        basis_value = float(self.basis_value_var.get())
        # if decimals == 'Auto':
        #     multiplier = utility.smallestMultiplier(basis_value, unit_price)
        # else:
        #     gm = 1-basis_value/unit_price
        #     multiplier = 1 / (1-gm)
        gm = 1-basis_value/unit_price
        multiplier = 1 / (1-gm)
        print("----------------")
        print(f'Unit: {unit_price}')
        print(f'Basis: {basis_value}')
        print(f'GrossMargin: {1-basis_value/unit_price}')
        print(f'Multipler: {1/(1-gm)}')
        print("----------------")

        multiplier_formula = utility.find_multiplier_formula(multiplier,  decimals)
        discount_formula = utility.find_discount_formula(multiplier, decimals)
        markup_formula = utility.find_markup_formula(multiplier, decimals)
        gross_profit_formula = utility.find_gross_profit_formula(multiplier, decimals)

        self.multiplier_var.set(multiplier_formula)
        self.discount_var.set(discount_formula)
        self.markup_var.set(markup_formula)
        self.gross_profit_var.set(gross_profit_formula)

    @staticmethod
    def validate(value) -> bool:
        if value == '':
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def copy_formula(formula):
        pyperclip.copy(formula)

    def clear_formulas(self):
        self.multiplier_var.set('')
        self.discount_var.set('')
        self.markup_var.set('')
        self.gross_profit_var.set('')

    def on_invalid(self):
        pass


if __name__ == '__main__':
    app = tk.Tk()

    app.title(FIND_FORMULAS)

    frame = FindFormulaFrame(app)
    frame.pack()

    app.mainloop()
