import tkinter as tk
from tkinter import ttk

import pyperclip


class AdjustFormula(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title = 'Adjust Formula'

        # create the tk vars
        self.unit_price_var = tk.StringVar()
        self.basis_value_var = tk.StringVar()
        self.unit_cost_var = tk.StringVar()

        self.spinner_value = tk.DoubleVar(value=0)

        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()

        # create the entry widgets
        self.unit_price_entry = ttk.Entry(self)
        self.basis_value_entry = ttk.Entry(self)
        self.unit_cost_entry = ttk.Entry(self)

        # create the margin spinner
        self.margin_spinner = ttk.Spinbox(self, textvariable=self.spinner_value)

        # create the decimals combobox
        item_list = ("Auto", "1", "2", "3", "4", "5", "6")
        self.decimals_combo = ttk.Combobox(self, values=item_list)

        # create the formula display widgets
        self.multiplier_display = ttk.Entry(self, state="readonly")
        self.discount_display = ttk.Entry(self, state="readonly")
        self.markup_display = ttk.Entry(self, state="readonly")
        self.gross_profit_display = ttk.Entry(self, state="readonly")

        self.multiplier_copy_button = ttk.Button(self, text='Copy')
        self.discount_copy_button = ttk.Button(self, text='Copy')
        self.markup_copy_button = ttk.Button(self, text='Copy')
        self.gross_profit_copy_button = ttk.Button(self, text='Copy')

        self.place_widgets()
        self.configure_widgets()

    def configure_widgets(self) -> None:
        item_list = ("Auto", "1", "2", "3", "4", "5", "6")

        # create the entry widgets
        self.unit_price_entry.configure(textvariable=self.unit_price_var)
        self.basis_value_entry.configure(textvariable=self.basis_value_var)
        self.unit_cost_entry.configure(textvariable=self.unit_cost_var)

        # create the margin spinner
        self.margin_spinner.configure(textvariable=self.spinner_value)

        # create the decimals combobox
        self.decimals_combo.configure(values=item_list)
        self.decimals_combo.current(0)

        # create the formula display widgets
        self.multiplier_display.configure(state="readonly")
        self.discount_display.configure(state="readonly")
        self.markup_display.configure(state="readonly")
        self.gross_profit_display.configure(state="readonly")

        self.multiplier_copy_button.configure(text='Copy', command=lambda: self.copy_formula(self.multiplier_var))
        self.discount_copy_button.configure(text='Copy', command=lambda: self.copy_formula(self.discount_var))
        self.markup_copy_button.configure(text='Copy', command=lambda: self.copy_formula(self.markup_var))
        self.gross_profit_copy_button.configure(text='Copy', command=lambda: self.copy_formula(self.gross_profit_var))

    def place_widgets(self):
        label_options = {'sticky': tk.W, 'padx': 2, 'pady': 2}
        entry_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        separator_options = {'rowspan': 5, 'sticky': tk.NS, 'padx': 2, 'pady': 2}
        display_options = {'sticky': tk.EW, 'padx': 2, 'pady': 2}
        copy_options = {'sticky': tk.E, 'padx': 2, 'pady': 2}

        ttk.Label(self, text="Unit Price").grid(row=0, column=0, **label_options)
        ttk.Label(self, text="Unit Cost").grid(row=1, column=0, **label_options)
        ttk.Label(self, text="Basis Value").grid(row=2, column=0, **label_options)
        ttk.Label(self, text="Decimals").grid(row=3, column=0, **label_options)
        ttk.Label(self, text="GM Adjustment").grid(row=4, column=0, **label_options)

        self.unit_price_entry.grid(row=0, column=1, **entry_options)
        self.unit_cost_entry.grid(row=1, column=1, **entry_options)
        self.basis_value_entry.grid(row=2, column=1, **entry_options)
        self.decimals_combo.grid(row=3, column=1, **entry_options)
        self.margin_spinner.grid(row=4, column=1, **entry_options)

        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, **separator_options)

        ttk.Label(self, text="Multiplier").grid(row=0, column=3, **label_options)
        ttk.Label(self, text="Discount").grid(row=1, column=3, **label_options)
        ttk.Label(self, text="Markup").grid(row=2, column=3, **label_options)
        ttk.Label(self, text="Gross Profit").grid(row=3, column=3, **label_options)

        self.multiplier_display.grid(row=0, column=4, **display_options)
        self.discount_display.grid(row=1, column=4, **display_options)
        self.markup_display.grid(row=2, column=4, **display_options)
        self.gross_profit_display.grid(row=3, column=4, **display_options)

        self.multiplier_copy_button.grid(row=0, column=5, **copy_options)
        self.discount_copy_button.grid(row=1, column=5, **copy_options)
        self.markup_copy_button.grid(row=2, column=5, **copy_options)
        self.gross_profit_copy_button.grid(row=3, column=5, **copy_options)

    @staticmethod
    def copy_formula(var: tk.StringVar) -> None:
        pyperclip.copy(var.get())


if __name__ == "__main__":
    app = tk.Tk()
    frame = AdjustFormula(app)
    frame.pack()
    app.title(frame.title)
    app.mainloop()
