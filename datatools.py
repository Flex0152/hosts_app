import pandas as pd


def read_file(path: str) -> pd.DataFrame:
    """Liest die Hosts Datei ein und erstellt das initiale Dataframe."""
    try:
        df = pd.read_csv(
            path, delimiter="\t", 
            header=None, 
            names=["IP Address", "Hostname"])
        
        return df[df.notna()]
    
    except PermissionError:
        return "Lesen nicht möglich! Zugriff verweigert! Bist du Admin?"
    except FileNotFoundError:
        return "Die Datei konnte nicht gefunden werden!"

def new_entry(data: pd.DataFrame, address: str, name: str) -> pd.DataFrame:
    """Erstellt ein DataFrame mit dem neuen Eintrag und gibt das zurück."""
    new_entry_df = pd.DataFrame(
        [{"Hostname": name,
          "IP Address": address}])
    # Wenn der Eintrag noch nicht vorhanden ist
    if data[
        (data["Hostname"] == name) & 
        (data["IP Address"] == address)].empty:

        return pd.concat([data, new_entry_df], ignore_index=True)
    # Wenn der Eintrag schon vorhanden ist, return ursprung
    else:
        return data

def remove_entry_by_name(data: pd.DataFrame, name: str) -> pd.DataFrame:
    """Sucht den Eintrag anhand des Namens. Wird der Eintrag gefunden, wird 
    das DataFrame ohne diesen Eintrag zurückgegeben. Wenn nicht, wird das
    DataFrame im Ursprung zurückgegeben."""
    entry_to_remove = data[data["Hostname"] == name]
    if not entry_to_remove.empty:
        return data.drop(entry_to_remove.index)
    else:
        return data


def write_entry(data: pd.DataFrame, path: str) -> None | str:
    """Schreibt das DataFrame zurück in die Datei"""
    try:
        data.to_csv(path, index=False, sep="\t", header=None)
    except PermissionError:
        return "Zugriff verweigert! Bist du Admin?"
    except FileNotFoundError:
        return "Die Datei konnte nicht gefunden werden!"
    

if __name__ == "__main__":
    file_path = r".\hosts"
    hosts_file = read_file(file_path)
    df = new_entry(hosts_file, "127.0.1.2", "another_example.local")
    write_entry(df, file_path)

    print(df)
    print(remove_entry_by_name(hosts_file, "another_example.flex.local"))
