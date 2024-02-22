import tkinter as tk

import findbasisvalueframe
import formulaconverterframe
import findformulasframe

from constants import *


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.current_frame = None

        self.find_basis_value_frame = findbasisvalueframe.FindBasisValueFrame(self)
        self.find_formulas_frame = findformulasframe.FindFormulaFrame(self)
        self.formula_converter_frame = formulaconverterframe.FormulaConverterFrame(self)

        menubar = tk.Menu()
        self.config(menu=menubar)

        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(
            label=FIND_BASIS_VALUE,
            command=self.load_find_basis_value_frame,
        )
        view_menu.add_command(
            label=FIND_FORMULAS,
            command=self.load_find_formulas_frame,
        )
        view_menu.add_command(
            label=FORMULA_CONVERTER,
            command=self.load_formula_converter_frame,
        )

        menubar.add_cascade(
            label='View',
            menu=view_menu,
            underline=0
        )

        self.load_find_formulas_frame()

    def load_find_formulas_frame(self):
        if self.current_frame is not None:
            self.current_frame.forget()
        self.current_frame = self.find_formulas_frame
        self.current_frame.pack(padx=10, pady=10)
        self.title(APPLICATION_TITLE + " - " + FIND_FORMULAS)

    def load_find_basis_value_frame(self):
        if self.current_frame is not None:
            self.current_frame.forget()
        self.current_frame = self.find_basis_value_frame
        self.current_frame.pack(padx=10, pady=10)
        self.title(APPLICATION_TITLE + " - " + FIND_BASIS_VALUE)

    def load_formula_converter_frame(self):
        if self.current_frame is not None:
            self.current_frame.forget()
        self.current_frame = self.formula_converter_frame
        self.current_frame.pack(padx=10, pady=10)
        self.title(APPLICATION_TITLE + " - " + FORMULA_CONVERTER)


if __name__ == '__main__':
    app = App()

    app.mainloop()
