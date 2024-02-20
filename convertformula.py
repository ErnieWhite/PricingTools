import re
import tkinter as tk
from tkinter import ttk

import pyperclip

import utility


class ConvertFormula(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.title = 'Convert Formula'

        self.vcmd = (self.register(self.validate), '%P')
        self.ivcmd = (self.register(self.on_invalid),)

        # create the StringVars
        self.formula_string_var = tk.StringVar()
        self.decimals_var = tk.StringVar()
        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()

        # create the entries
        self.current_formula_entry = ttk.Entry(self)
        self.multiplier_formula_display = ttk.Entry(self)
        self.discount_formula_display = ttk.Entry(self)
        self.markup_formula_display = ttk.Entry(self)
        self.gross_profit_formula_display = ttk.Entry(self)

        # create the combobox
        self.decimals = ttk.Combobox(self)

        # create the copy buttons
        self.multiplier_copy_button = ttk.Button(self)
        self.discount_copy_button = ttk.Button(self)
        self.markup_copy_button = ttk.Button(self)
        self.gross_profit_copy_button = ttk.Button(self)

        self.configure_widgets()
        self.place_widgets()
        self.setup_bindings()

    def configure_widgets(self):

        combo_items = ('Auto', '0', '1', '2', '3', '4', '5', '6')

        entry_options = {'validate': 'key', 'validatecommand': self.vcmd, 'invalidcommand': self.ivcmd}
        display_options = {'state': 'readonly', 'takefocus': False}
        combobox_options = {'values': combo_items, 'state': 'readonly'}

        self.current_formula_entry.configure(textvariable=self.formula_string_var, **entry_options)
        self.multiplier_formula_display.configure(textvariable=self.multiplier_var, **display_options)
        self.discount_formula_display.configure(textvariable=self.discount_var, **display_options)
        self.markup_formula_display.configure(textvariable=self.markup_var, **display_options)
        self.gross_profit_formula_display.configure(textvariable=self.gross_profit_var, **display_options)

        # create the combobox
        self.decimals.configure(textvariable=self.decimals_var, **combobox_options)
        self.decimals.current(0)

        # create the copy buttons
        # TODO: Replace the text with an image
        self.multiplier_copy_button.configure(text="Copy", command=lambda: self.copy_formula(self.multiplier_var))
        self.discount_copy_button.configure(text="Copy", command=lambda: self.copy_formula(self.discount_var))
        self.markup_copy_button.configure(text="Copy", command=lambda: self.copy_formula(self.markup_var))
        self.gross_profit_copy_button.configure(text="Copy", command=lambda: self.copy_formula(self.gross_profit_var))

    def place_widgets(self) -> None:

        label_options = {'sticky': tk.W, 'padx': 2, 'pady': 2}
        entry_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        combobox_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        separator_options = {'rowspan': 4, 'sticky': tk.NS, 'padx': 2, 'pady': 2}
        display_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        button_options = {'padx': 2, 'pady': 2}

        ttk.Label(self, text='Formula').grid(column=0, row=0, **label_options)
        ttk.Label(self, text='Decimals').grid(column=0, row=1, **label_options)

        self.current_formula_entry.grid(column=1, row=0, **entry_options)

        self.decimals.grid(column=1, row=1, **combobox_options)

        ttk.Separator(self, orient=tk.VERTICAL).grid(column=2, row=0, **separator_options)

        ttk.Label(self, text='Multiplier').grid(column=3, row=0, **label_options)
        ttk.Label(self, text='Discount').grid(column=3, row=1, **label_options)
        ttk.Label(self, text='Markup').grid(column=3, row=2, **label_options)
        ttk.Label(self, text='Gross Profit').grid(column=3, row=3, **label_options)

        self.multiplier_formula_display.grid(column=4, row=0, **display_options)
        self.discount_formula_display.grid(column=4, row=1, **display_options)
        self.markup_formula_display.grid(column=4, row=2, **display_options)
        self.gross_profit_formula_display.grid(column=4, row=3, **display_options)

        self.multiplier_copy_button.grid(column=5, row=0, **button_options)
        self.discount_copy_button.grid(column=5, row=1, **button_options)
        self.markup_copy_button.grid(column=5, row=2, **button_options)
        self.gross_profit_copy_button.grid(column=5, row=3, **button_options)

    def setup_bindings(self) -> None:
        self.formula_string_var.trace_add('write', self.handle_formula_change_event)
        self.decimals_var.trace_add('write', self.handle_formula_change_event)

    def handle_formula_change_event(self, *_) -> None:
        value = self.formula_string_var.get().upper()
        decimals = self.decimals_var.get()

        self.formula_string_var.set(value)
        self.clear_calculated_formulas()

        if utility.valid_formula(value):
            multiplier = utility.calculate_multiplier(value)

            formula = utility.find_multiplier_formula(multiplier, decimals)
            self.multiplier_var.set(formula)

            formula = utility.find_discount_formula(multiplier, decimals)
            self.discount_var.set(formula)

            formula = utility.find_markup_formula(multiplier, decimals)
            self.markup_var.set(formula)

            formula = utility.find_gross_profit_formula(multiplier, decimals)
            self.gross_profit_var.set(formula)

    def clear_calculated_formulas(self) -> None:
        self.multiplier_var.set('')
        self.discount_var.set('')
        self.markup_var.set('')
        self.gross_profit_var.set('')

    @staticmethod
    def copy_formula(var: tk.StringVar) -> None:
        pyperclip.copy(var.get())

    @staticmethod
    def validate(value: str) -> bool:
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
    def on_invalid() -> None:
        beepy.beep(sound=1)


if __name__ == '__main__':
    app = tk.Tk()

    frame = ConvertFormula(app)
    frame.pack()
    app.title(frame.title)

    app.mainloop()
