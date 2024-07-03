import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listStato = []

    def fillDD(self):
        self._listYear = self._model.get_anni()
        for a in self._listYear:
            num = self._model.get_num_apparizioni(a)
            self._view.ddyear.options.append(ft.dropdown.Option(str(a) + " --> " + str(num[0])))

    def fillDDstato(self):
        self._listStato = self._model.get_stati()
        for s in self._listStato:
            self._view.ddstato.options.append(ft.dropdown.Option(key=s.id, text=s.Name))

    def handle_graph(self, e):
        anno = self._view.ddyear.value.split(" ")[0]
        if anno is not None:
            self._view.txt_result.controls.clear()
            self._view.update_page()
            self._model.crea_grafo(anno)
            num_nodi = self._model.num_nodi()
            num_archi = self._model.num_archi()
            self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {num_nodi}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero archi: {num_archi}"))
            # aggiungere disabled
            self._view.ddstato.disabled = False
            self._view.btn_analizza.disabled = False
            self._view.btn_sequenza_avvistamenti.disabled = False
            self.fillDDstato()
            self._view.update_page()

        else:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare campo anno. ")
            self._view.update_page()


    def handle_analizza(self, e):
        stato = self._view.ddstato.value
        if stato is not None:
            self._view.txt_result.controls.clear()
            self._view.update_page()
            succ, pred, visitabili = self._model.analizza_grafo(stato)
            self._view.txt_result.controls.append(ft.Text("Successori:"))
            for n in succ:
                self._view.txt_result.controls.append(ft.Text(f"- {n.Name}"))
            self._view.txt_result.controls.append(ft.Text("Predecessori:"))
            for n in pred:
                self._view.txt_result.controls.append(ft.Text(f"- {n.Name}"))
            self._view.txt_result.controls.append(ft.Text("Nodi visitabili:"))
            for n in visitabili:
                self._view.txt_result.controls.append(ft.Text(f"- {n.Name}"))
            self._view.update_page()
        else:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare campo stato. ")
            self._view.update_page()
    def handle_path(self, e):
        stato = self._view.ddstato.value
        if stato is not None:
            self._view.txtOut2.controls.clear()
            costo, lista = self._model.get_ciclo_max(stato)
            self._view.txtOut2.controls.append(ft.Text(f"Archi attraversati: {costo}"))
            for n in lista:
                self._view.txtOut2.controls.append(ft.Text(f"{n[0]} --> {n[1]}"))
            self._view.update_page()
        else:
            self._view.txtOut2.controls.clear()
            self._view.create_alert("Selezionare campo stato. ")
            self._view.update_page()
