from textual.app import App, ComposeResult
from textual.widgets import Label, DataTable, Input, Button
from textual.containers import Horizontal

from datatools import read_file, new_entry, write_entry, remove_entry_by_name


class HostsApplication(App):

    DEFAULT_CSS="""
      /*Screen {layout: grid; grid-size: 4}*/
      DataTable {padding: 1; margin: 1; height: 100%;}
      Button {margin: 1;}
      .btn {display: block; height: 4;}
      #tab {height: 10;}
      Input {margin: 1;}
    """
    
    file_path = r"C:\Windows\System32\drivers\etc\hosts"
    data = read_file(file_path)
    row_selected = []

    def compose(self) -> ComposeResult:
        yield Label()
        yield Input(placeholder="Hostname", id="hostname")
        yield Input(placeholder="IP Adresse", id="ipaddress")
        with Horizontal(classes="btn"):
            yield Button("Hinzufügen", id="add")
            yield Button("Löschen", id="remove")
        yield DataTable(id="tab")

    def add_rows_to_table(self, table):
        """Fügt der übergebenden Tabelle die Datensätze hinzu, falls vorhanden."""
        if len(self.data) > 0:
            table.add_rows(
                [
                    [item['IP Address'], item['Hostname']]
                    for _, item in self.data.iterrows()
                ]
            )

    def refresh_table(self) -> None:
        """Holt sich die vorhandene DataTable. Löscht alle Einträge
        und baut sie komplett neu auf."""
        table = self.query_one(DataTable)
        table.clear()
        self.data = read_file(self.file_path)
        self.add_rows_to_table(table)

    def on_mount(self):
        """Initiales erstellen der Tabelle"""
        table = self.query_one(DataTable)
        if not isinstance(self.data, str):
            table.add_columns(*tuple(self.data.columns.values))
            self.add_rows_to_table(table)
            table.cursor_type = "row"
        else:
            self.query_one(Label).update(self.data)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(Label).update("")
        if event.button.id == "add":
            hostname = self.query_one("#hostname", Input)
            ipaddress = self.query_one("#ipaddress", Input)
            if hostname.value == "" or ipaddress.value == "":
                self.query_one(Label).update("Einer der beiden Werte scheint leer zu sein!")
            else:
                self.data = new_entry(self.data, ipaddress.value, hostname.value)
                result = write_entry(self.data, self.file_path)
                self.refresh_table()
                if isinstance(result, str):
                    self.query_one(Label).update(result)
                
        if event.button.id == "remove":
            if len(self.row_selected) > 0:
                self.data = remove_entry_by_name(self.data, self.row_selected[1])
                result = write_entry(self.data, self.file_path)
                self.refresh_table()
                if isinstance(result, str):
                    self.query_one(Label).update(result)
            else:
                self.query_one(Label).update("[!] Es wurde nichts ausgewählt!")


    def on_data_table_row_selected(self, event:DataTable.RowSelected) -> list:
        """Ob gebraucht oder nicht, wird eine Zeile gewählt wird die
        Zeile in die Klassenvariable geschrieben."""
        table = self.query_one(DataTable)
        self.row_selected = table.get_row(event.row_key)


if __name__ == "__main__":
    app = HostsApplication()
    app.run()