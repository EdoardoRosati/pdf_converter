import sys
import os
import pdfplumber
import pandas as pd

# Verifica che sia stato passato un file come argomento
if len(sys.argv) < 2:
    print("Uso corretto: python ScriptPDF.py <nome_file.pdf>")
    sys.exit(1)  # Esce con errore

# Ottieni il percorso del file PDF dall'argomento della riga di comando
pdf_path = sys.argv[1]

# Controlla se il file esiste
if not os.path.exists(pdf_path):
    print(f"Errore: il file '{pdf_path}' non esiste.")
    sys.exit(1)

# Nome di output
output_text_path = "estratto_testo.txt"
output_csv_path = "estratto_tabelle.csv"

try:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        tables = []
        
        for page in pdf.pages:
            # Estrarre il testo
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
            
            # Estrarre le tabelle
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                df = pd.DataFrame(table)  # Converti la tabella in DataFrame
                tables.append(df)

    # Salvare il testo estratto
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    # Salvare le tabelle estratte
    if tables:
        df_combined = pd.concat(tables, ignore_index=True)
        df_combined.to_csv(output_csv_path, index=False, encoding="utf-8")

    print(f"✅ Estrazione completata!\n- Testo salvato in: {output_text_path}\n- Tabelle salvate in: {output_csv_path}")

except Exception as e:
    print(f"❌ Errore durante l'elaborazione del file: {e}")
