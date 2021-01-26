import pickle
import base64
import sys

sys.path.append('/Users/ovsannikovaleksandr/Desktop/предпроф/back')
import render_storage

import requests


class BackendTalker:

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.adr = "http://" + self.host + ":" + str(self.port)

    def get_list_of_all(self):
        resp = requests.get(self.adr + "/get_list_of_all")
        unbased = base64.b64decode(resp.text.encode())
        return pickle.loads(unbased)

    def get_scheme(self):
        resp = requests.get(self.adr + "/get_scheme")
        return resp.text

    def get_cell(self, cell_name):
        resp = requests.get(self.adr + "/get_cell", params={"cell_name": cell_name})
        unbased = base64.b64decode(resp.text.encode())
        try:
            if unbased.decode() == "Not":
                return "Неправильная ячейка"
        except:
            return pickle.loads(unbased)

    def get_data_to_search_by_item(self, uuid):
        resp = requests.get(self.adr + "/get_data_from_item_search", params={"uuid": uuid})
        unbased = base64.b64decode(resp.text.encode())
        try:
            if unbased.decode() == "Not":
                return "Неправильный uuid"
        except:
            return pickle.loads(unbased)

    def get(self, cell_name):
        if len(cell_name) == 2:
            resp = requests.get(self.adr + "/get_item_from_storage", params={"cell_name": cell_name})
        else:
            resp = requests.get(self.adr + "/get_item_from_storage", params={"uuid": cell_name})

        return resp.text

    def put(self, xls_file):
        based = base64.b64encode(xls_file)
        resp = requests.post(self.adr + "/put_items_to_storage", data=based)
        return resp

    def get_remote(self):
        resp = requests.get(self.adr+"/remote")
        data_splitted = resp.text.split("<p>")
        data_splitted.pop(0)
        text = "".join(data_splitted)
        data_splitted = text.split("</p>")
        data_splitted.pop(-1)
        text = "".join(data_splitted).replace("<br/>", "\n").replace("                ", " ").replace("            ", " ")
        return text

    def get_main_pdf(self):
        resp = requests.get(self.adr+"/get_pdf_main")
        with open("Отчет о добавлении товаров на склад.pdf", "wb") as f:
            f.write(resp.content)

    def get_remote_pdf(self):
        resp = requests.get(self.adr+"/get_pdf_remote")
        with open("Отчет о добавлении товаров на удаленный склад.pdf", "wb") as f:
            f.write(resp.content)
