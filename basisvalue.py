import re
import tkinter as tk
from tkinter import ttk

import pyperclip

import utility


class BasisValue(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        # Tacked onto the window title
        self.title = 'Basis Value'

        # Set up data validation call backs
        self.float_vcmd = (self.register(self.validate_float), '%P')
        self.formula_vcmd = (self.register(self.validate_formula), '%P')
        self.ivcmd = (self.register(self.on_invalid),)

        self.unit_price_var = tk.StringVar()
        self.formula_var = tk.StringVar()
        self.basis_price_var = tk.StringVar()
        self.decimals_var = tk.StringVar()

        self.unit_price_entry = ttk.Entry(self)
        self.formula_entry = ttk.Entry(self)
        self.calculated_basis_entry = ttk.Entry(self)

        self.decimals_combobox = ttk.Combobox(self)

        self.copy_button = ttk.Button(self)

        self.set_up_traces()
        self.configure_widgets()
        self.place_widgets()

    def configure_widgets(self):
        # create the widgets

        self.unit_price_entry.configure(
            textvariable=self.unit_price_var,
            validate='key',
            validatecommand=self.float_vcmd,
            invalidcommand=self.ivcmd,
        )

        self.formula_entry.configure(
            textvariable=self.formula_var,
            validate='key',
            validatecommand=self.formula_vcmd,
            invalidcommand=self.ivcmd,
        )

        self.calculated_basis_entry.configure(
            state='readonly',
            textvariable=self.basis_price_var
        )

        combo_values = ('Auto', '0', '1', '2', '3', '4')
        self.decimals_combobox.configure(
            textvariable=self.decimals_var,
            state='readonly',
            values=combo_values,
        )
        self.decimals_combobox.current(0)

        self.copy_button.configure(text='Copy', command=self.copy_basis_price)

    def place_widgets(self):
        label_options = {'sticky': 'w', 'padx': 2, 'pady': 2}
        entry_options = {'sticky': 'we', 'padx': 2, 'pady': 2}
        separator_options = {'rowspan': 3, 'sticky': 'ns', 'padx': 2, 'pady': 2}
        ttk.Label(self, text='Unit Price').grid(row=0, column=0, **label_options)
        self.unit_price_entry.grid(row=0, column=1, **entry_options)

        ttk.Label(self, text='Formula').grid(row=1, column=0, **label_options)
        self.formula_entry.grid(row=1, column=1, **entry_options)

        ttk.Label(self, text='Decimals').grid(row=2, column=0, **label_options)
        self.decimals_combobox.grid(row=2, column=1, **entry_options)

        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, **separator_options)

        ttk.Label(self, text='Basis Value').grid(row=0, column=3, **label_options)
        self.calculated_basis_entry.grid(row=0, column=4, **entry_options)

        self.copy_button.grid(row=0, column=5, sticky='e', padx=2, pady=2)

    def set_up_traces(self):
        self.unit_price_var.trace_add('write', self.update_basis_price)
        self.formula_var.trace_add('write', self.update_basis_price)
        self.decimals_var.trace_add('write', self.update_basis_price)

    @staticmethod
    def validate_float(value):
        if re.search(r'^[-+]?\d*\.?\d*$', value):
            return True
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
        if self.unit_price_var.get() == '.':
            self.clear_basis()
            return
        if not utility.valid_formula(self.formula_var.get()):
            self.clear_basis()
            return
        if self.unit_price_var.get() == '' or self.formula_var.get() == '':
            self.clear_basis()
            return
        multiplier = utility.calculate_multiplier(self.formula_var.get())
        if multiplier == 0:
            self.clear_basis()
            return
        specifier = utility.create_specifier(self.decimals_var.get())
        basis_price = float(self.unit_price_var.get()) / multiplier
        self.basis_price_var.set(f'{basis_price:{specifier}}')

    def clear_basis(self):
        self.basis_price_var.set('')

    @staticmethod
    def on_invalid():
        beepy.beep(sound=1)

    def copy_basis_price(self):
        pyperclip.copy(self.basis_price_var.get())


if __name__ == '__main__':
    app = tk.Tk()

    frame = BasisValue(app)
    frame.pack()

    app.title(frame.title)

    app.mainloop()
