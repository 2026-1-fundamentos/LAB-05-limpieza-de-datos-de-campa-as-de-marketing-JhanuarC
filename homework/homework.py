"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    from pathlib import Path
    import pandas as pd 
    import zipfile
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months

    

    Plan de accion
    -Como acceder a los .zip
    -Crear los csv con los formatos requeridos
    """
    ruta_csv = Path("files/input")
    lista_csv = []

    for archivo in ruta_csv.rglob("*.zip"):
       with zipfile.ZipFile(archivo, "r") as z:
            #Nombre del csv
            nombre_csv = z.namelist()[0]

            with z.open(nombre_csv) as f:
                df = pd.read_csv(f)
                lista_csv.append(df)

    df_csv = pd.concat(lista_csv,ignore_index=True)#df con todos los datos


    client_df = df_csv[[
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage",
    ]].copy()

    #Limpieza de datos de client_df
    client_df["job"] = client_df["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client_df["education"] = client_df["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client_df["credit_default"] = (client_df["credit_default"] == "yes").astype(int)
    client_df["mortgage"] = (client_df["mortgage"] == "yes").astype(int)  

    campaign_df = df_csv[[
        "client_id", 
        "number_contacts", 
        "contact_duration", 
        "previous_campaign_contacts", 
        "previous_outcome", 
        "campaign_outcome", 
        "day", 
        "month",
    ]].copy()

    #Limpieza de datos de campaign_df
    campaign_df["previous_outcome"] = (campaign_df["previous_outcome"] == "success").astype(int)
    campaign_df["campaign_outcome"] = (campaign_df["campaign_outcome"] == "yes").astype(int)
    campaign_df["last_contact_date"] = pd.to_datetime(
        campaign_df["day"].astype(str) + "-" + campaign_df["month"].astype(str) + "-2022", 
        format="%d-%b-%Y"
    ).dt.strftime("%Y-%m-%d")
    campaign_df.drop(columns=["day", "month"], inplace=True)

    economics_df = df_csv[[
        "client_id", 
        "cons_price_idx", 
        "euribor_three_months",
    ]].copy()

    #Exportar los dataframes a csv
    output_path = Path("files/output")
    #Crear la carpeta si no existe
    output_path.mkdir(parents=True, exist_ok=True)

    client_df.to_csv(output_path / "client.csv", index=False)
    campaign_df.to_csv(output_path / "campaign.csv", index=False)
    economics_df.to_csv(output_path / "economics.csv", index=False)


if __name__ == "__main__":
    clean_campaign_data()