import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self._max_anni=None
        self._max_ore=None
        self._nerc=None


    def handleWorstCase(self, e):
        soluzioni=self._model.worstCase(self._nerc, self.get_y(), self.get_x())
        for soluzione in soluzioni:
            self._view._txtOut.controls.append(ft.Text(soluzione))
        self._view._page.update()
        return

    def fillDD(self):
        nercList = self._model.listNerc
        #self._view._ddNerc.options.clear()

        for n in nercList:
            self._view._ddNerc.options.append(
                ft.dropdown.Option(key=n.value, data=n)
            )

        self._view._ddNerc.on_change = self.getNerc
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v



    def getNerc(self, e):
        selected_key = e.control.value
        self._nerc = self._idMap[selected_key]

        #print("NERC selezionato:", self._nerc)

    def get_x(self):
        value = (self._view._txtYears.value)
        if value == "":
            return None
        self._max_anni=int(value)
        return self._max_anni

    def get_y(self):
        value = (self._view._txtHours.value)
        if value == "":
            return None
        self._max_ore=float(value)
        return self._max_ore


