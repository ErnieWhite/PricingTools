import tkinter as tk
from tkinter import ttk

import pyperclip

import utility


class CalculateFormulas(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title = 'Calculate Formulas'

        self.vcmd = (self.register(self.validate), '%P')
        self.ivcmd = (self.register(self.on_invalid),)

        # create StringVar
        self.unit_price_var = tk.StringVar()
        self.basis_value_var = tk.StringVar()
        self.decimals_var = tk.StringVar()

        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()

        # create the widgets

        self.unit_price_entry = ttk.Entry(self)
        self.basis_value_entry = ttk.Entry(self)
        self.decimals_combo = ttk.Combobox(self)

        self.multiplier_formula_display = ttk.Entry(self)
        self.discount_formula_display = ttk.Entry(self)
        self.markup_formula_display = ttk.Entry(self)
        self.gross_profit_formula_display = ttk.Entry(self)

        self.multiplier_formula_copy_button = ttk.Button(self)
        self.discount_formula_copy_button = ttk.Button(self)
        self.markup_formula_copy_button = ttk.Button(self)
        self.gross_profit_formula_copy_button = ttk.Button(self)

        self.configure_widgets()
        self.place_widgets()
        self.set_up_traces()

    def configure_widgets(self):

        combo_items = ('Auto', '0', '1', '2', '4', '5', '6')
        entry_options = {'validate': 'key', 'validatecommand': self.vcmd, 'invalidcommand': self.ivcmd}

        self.unit_price_entry.configure(textvariable=self.unit_price_var, **entry_options)
        self.basis_value_entry.configure(textvariable=self.basis_value_var, **entry_options)
        self.decimals_combo.configure(values=combo_items, textvariable=self.decimals_var, state='readonly', )
        self.decimals_combo.current(0)

        self.multiplier_formula_display.configure(textvariable=self.multiplier_var, state='readonly')
        self.discount_formula_display.configure(textvariable=self.discount_var, state='readonly')
        self.markup_formula_display.configure(textvariable=self.markup_var, state='readonly')
        self.gross_profit_formula_display.configure(textvariable=self.gross_profit_var, state='readonly')

        self.multiplier_formula_copy_button.configure(text='Copy',
                                                      command=lambda: self.copy_formula(self.multiplier_var))
        self.discount_formula_copy_button.configure(text='Copy', command=lambda: self.copy_formula(self.discount_var))
        self.markup_formula_copy_button.configure(text='Copy', command=lambda: self.copy_formula(self.markup_var))
        self.gross_profit_formula_copy_button.configure(text='Copy',
                                                        command=lambda: self.copy_formula(self.gross_profit_var))

    def place_widgets(self):
        label_options = {'sticky': tk.W, 'padx': 2, 'pady': 2}
        entry_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        display_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        button_options = {'padx': 2, 'pady': 2}
        combobox_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        separator_options = {'rowspan': 4, 'sticky': tk.NS, 'padx': 2, 'pady': 2}

        ttk.Label(self, text='Unit Price').grid(row=0, column=0, **label_options)
        ttk.Label(self, text='Basis Value').grid(row=1, column=0, **label_options)
        ttk.Label(self, text='Decimals').grid(row=2, column=0, **label_options)

        self.unit_price_entry.grid(row=0, column=1, **entry_options)
        self.basis_value_entry.grid(row=1, column=1, **entry_options)
        self.decimals_combo.grid(row=2, column=1, **combobox_options)

        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, **separator_options)

        ttk.Label(self, text='Multiplier').grid(row=0, column=3, **label_options)
        ttk.Label(self, text='Discount').grid(row=1, column=3, **label_options)
        ttk.Label(self, text='Markup').grid(row=2, column=3, **label_options)
        ttk.Label(self, text='Gross Profit').grid(row=3, column=3, **label_options)

        self.multiplier_formula_display.grid(row=0, column=4, **display_options)
        self.discount_formula_display.grid(row=1, column=4, **display_options)
        self.markup_formula_display.grid(row=2, column=4, **display_options)
        self.gross_profit_formula_display.grid(row=3, column=4, **display_options)

        self.multiplier_formula_copy_button.grid(row=0, column=5, **button_options)
        self.discount_formula_copy_button.grid(row=1, column=5, **button_options)
        self.markup_formula_copy_button.grid(row=2, column=5, **button_options)
        self.gross_profit_formula_copy_button.grid(row=3, column=5, **button_options)

    def set_up_traces(self):
        self.unit_price_var.trace_add('write', self.update_formulas)
        self.basis_value_var.trace_add('write', self.update_formulas)
        self.decimals_var.trace_add('write', self.update_formulas)

    def update_formulas(self, *_):
        if not self.unit_price_var.get() or not self.basis_value_var.get():
            self.clear_formulas()
            return
        if float(self.unit_price_var.get()) == 0 or float(self.basis_value_var.get()) == 0:
            self.clear_formulas()
            return
        decimals = self.decimals_var.get()
        multiplier = float(self.unit_price_var.get()) / float(self.basis_value_var.get())
        multiplier_formula = utility.find_multiplier_formula(multiplier, decimals)
        print(multiplier_formula)
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
    def copy_formula(var: tk.StringVar) -> None:
        print('copy')
        pyperclip.copy(var.get())

    def clear_formulas(self):
        self.multiplier_var.set('')
        self.discount_var.set('')
        self.markup_var.set('')
        self.gross_profit_var.set('')

    @staticmethod
    def on_invalid():
        print('\a')


if __name__ == '__main__':
    app = tk.Tk()

    frame = CalculateFormulas(app)
    frame.pack()
    app.title(frame.title)

    app.mainloop()
