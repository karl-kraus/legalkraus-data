# legalkraus-data

Ordnerstruktur:
- in "collections" befinden sich XML/TEI-Dokumente mit Metadaten zu den Fällen
- in "indices" befinden sich sieben Register in XML/TEI (Personen, Institutionen, Orte, Werke, juristische Texte, Fackel-Texte, Dokumente aus Rechtsakten)
- in "objects" befinden sich die annotierten XML/TEI-Dokumente, welche die Grundlage der digitalen Edition bilden (im Unterschied zu "collections" nicht Fälle/Sammlungen, sondern einzelne 
Dateinamen:
- z. B. "C_000001.xml" -> "C" = collection, Ziffer = Fallnummer
- z. B. "I_000001.xml" -> "I" = index, Ziffer = Nummer des Registers (1 = Personen, 2 = Institutionen, 3 = Orte, 4 = Werke, 5 = Gesetzestexte, 6 = Fackel, 7 = Dokumente aus Rechtsakten)
- z. B. "D_000001-001-000.xml" -> "D" = document, erste Ziffer(n) = Fallnummer, zweite Ziffer(n) = Dokumentnummer, ggf. dritte Ziffer(n) = Beilage