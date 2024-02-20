import tkinter as tk
from tkinter import ttk
import utility
import pyperclip
import re
from constants import *


class FindBasisValueFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.multiplier = 0

        float_vcmd = (self.register(self.validate_float), '%P')
        formula_vcmd = (self.register(self.validate_formula), '%P')
        ivcmd = (self.register(self.on_invalid), )

        self.unit_price_var = tk.StringVar()
        self.formula_var = tk.StringVar()
        self.basis_price_var = tk.StringVar()

        self.copy_button = ttk.Button(self)
        self.unit_price_entry = ttk.Entry(self)
        self.formula_entry = ttk.Entry(self)
        self.calculated_basis_entry = ttk.Entry(self)

        self.configure_widgets(float_vcmd, formula_vcmd, ivcmd)
        self.place_widgets()
        self.setup_traces()

    def setup_traces(self):
        self.unit_price_var.trace_add('write', self.update_basis_price)
        self.formula_var.trace_add('write', self.update_basis_price)

    def configure_widgets(self, float_vcmd, formula_vcmd, ivcmd):
        self.copy_button = ttk.Button(self, text='Copy', command=self.copy_basis_price)
        self.unit_price_entry = ttk.Entry(
            self,
            textvariable=self.unit_price_var,
            validate='key',
            validatecommand=float_vcmd,
            invalidcommand=ivcmd,
        )
        self.formula_entry = ttk.Entry(
            self,
            textvariable=self.formula_var,
            validate='key',
            validatecommand=formula_vcmd,
            invalidcommand=ivcmd,
        )
        self.calculated_basis_entry = ttk.Entry(
            self,
            state='readonly',
            textvariable=self.basis_price_var
        )

    def place_widgets(self):
        ttk.Label(self, text=UNIT_PRICE).grid(row=0, column=0, sticky=tk.W)
        self.unit_price_entry.grid(row=0, column=1, sticky=tk.EW)

        ttk.Label(self, text=FORMULA).grid(row=1, column=0, sticky=tk.W)
        self.formula_entry.grid(row=1, column=1, sticky=tk.EW)

        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, rowspan=3, padx=5, sticky=tk.NS)

        ttk.Label(self, text=BASIS_VALUE).grid(row=0, column=4, sticky=tk.W)
        self.calculated_basis_entry.grid(row=0, column=5, sticky=tk.EW)
        self.copy_button.grid(row=0, column=6, sticky=tk.EW)

    @staticmethod
    def validate_float(value):
        if value == '':
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_formula(value):
        if value == '':
            return True
        value = value.upper()
        if re.search(r'^[*XD][-+]?\d*\.?\d*$', value):
            return True
        if re.search(r'^[-+]\d*\.?\d*$', value):
            return True
        if value == 'G' or re.search(r'^GP[-+]?\d*\.?\d*$', value):
            return True
        return False

    def update_basis_price(self, *_):
        self.formula_var.set(self.formula_var.get().upper())
        if not utility.valid_formula(self.formula_var.get()):
            self.clear_basis()
            return
        if self.unit_price_var.get() == '' or self.formula_var.get() == '':
            self.clear_basis()
            return
        multiplier = utility.calculate_multiplier(self.formula_var.get())
        if self.multiplier == 0:
            self.clear_basis()
            return
        basis = float(self.unit_price_var.get()) / multiplier
        self.basis_price_var.set(f'{basis:.3}')

    def clear_basis(self):
        self.basis_price_var.set('')

    def on_invalid(self):
        pass

    def copy_basis_price(self):
        pyperclip.copy(self.basis_price_var.get())


if __name__ == '__main__':
    app = tk.Tk()

    app.title(FIND_BASIS_VALUE)

    frame = FindBasisValueFrame(app)
    frame.pack()

    app.mainloop()

