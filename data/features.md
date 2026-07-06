# Spaltenbeschreibung des Datensatzes

Der Datensatz enthält Informationen zu Lachgasemissionen (`N2O flux`) aus afrikanischen Wald-, Plantagen-, Grünland- und Ackerstandorten. Neben der Zielvariable sind räumliche Informationen, Zeitinformationen, Landnutzung, Düngung, Wetterdaten, Bodenfeuchte, Bodentemperatur und modellierte Features enthalten. Die ursprünglichen Daten stammen aus PANGAEA; meteorologische und bodenbezogene Variablen sind als ERA5-Reanalysedaten gekennzeichnet.

> Hinweis: Die Spalten `year`, `month` und `day_of_year` sind keine ursprünglichen Messspalten, sondern aus `Date/Time` abgeleitete Zeitfeatures.

## Übersicht der Spalten

| Spalte | Bedeutung | Einheit / Datentyp | Kategorie | Relevanz für Machine Learning |
|---|---|---:|---|---|
| `Event` | Ereignis-, Standort- oder Beobachtungslabel. Dient zur Identifikation einzelner Messkontexte. | kategorial | Identifikation | Kann Standort- oder Ereigniseffekte enthalten. Wichtig für gruppierte Analysen und potenziell für Group-Splits. |
| `Latitude` | Breitengrad des Messstandortes. | Dezimalgrad | Räumliches Feature | Bildet geografische Lage ab und kann indirekt Klima- oder Standortbedingungen repräsentieren. |
| `Longitude` | Längengrad des Messstandortes. | Dezimalgrad | Räumliches Feature | Ergänzt `Latitude` zur räumlichen Verortung. Kann räumliche Muster im Modell erklärbar machen. |
| `Date/Time` | Datum bzw. Zeitpunkt der Beobachtung. | Datum / Zeit | Zeitfeature | Grundlage für saisonale Features wie `year`, `month`, `day_of_year` oder Sinus-/Cosinus-Transformationen. |
| `Land use` | Landnutzung am Standort, z. B. Wald, Plantage, Ackerland oder Grünland. | kategorial | Standort / Management | Wichtige erklärende Variable, da Landnutzung Vegetation, Bodenmanagement und Nährstoffkreisläufe beeinflusst. |
| `Fert N [kg/ha] (Recorded at time of application)` | Ausgebrachte Stickstoffmenge zum Zeitpunkt der Düngerapplikation. | kg/ha | Management | Sehr relevantes Feature, da Stickstoffeintrag ein zentraler Treiber für N₂O-Emissionen ist. |
| `TTT day m [°C] (ERA5 reanalyses)` | Tagesmittel der Lufttemperatur. | °C | Wetter | Beeinflusst mikrobielle Aktivität, Nitrifikation und Denitrifikation. |
| `TxTxTx day max [°C] (ERA5 reanalyses)` | Tagesmaximum der Lufttemperatur. | °C | Wetter | Beschreibt Hitzebedingungen und Temperaturspitzen am Messtag. |
| `TnTnTn day min [°C] (ERA5 reanalyses)` | Tagesminimum der Lufttemperatur. | °C | Wetter | Beschreibt nächtliche bzw. minimale Temperaturbedingungen. |
| `Precip day total [mm/day] (ERA5 reanalyses)` | Tägliche Niederschlagssumme. | mm/day | Wetter / Hydrologie | Beeinflusst Bodenfeuchte, Sauerstoffverfügbarkeit und Denitrifikationsprozesse. |
| `Soil moisture [m**3/m**3] (Content at 0-7 cm depth, ERA5...)` | Volumetrischer Bodenwassergehalt in der obersten Bodenschicht. | m³/m³ | Boden | Sehr wichtig für N₂O, da Bodenwassergehalt Gasdiffusion und mikrobielle Prozesse steuert. |
| `Soil moisture [m**3/m**3] (ERA5 reanalyses)` | Weitere ERA5-Bodenfeuchtevariable. Wahrscheinlich tiefere Bodenschicht. | m³/m³ | Boden | Kann Feuchtebedingungen unterhalb der Oberfläche abbilden. Vermutlich Layer 2, also 7–28 cm. |
| `Soil moisture [m**3/m**3] (ERA5 reanalyses).1` | Weitere ERA5-Bodenfeuchtevariable. Wahrscheinlich tiefere Bodenschicht. | m³/m³ | Boden | Kann Wurzelzonen- oder Speicherfeuchte repräsentieren. Vermutlich Layer 3, also 28–100 cm. |
| `T soil day m [°C] (ERA5 reanalyses)` | Tagesmittel der Bodentemperatur. Wahrscheinlich oberste Bodenschicht. | °C | Boden | Prozessnahes Temperaturfeature, da mikrobielle Umsetzungen direkt von Bodentemperatur abhängen. Vermutlich Layer 1, also 0–7 cm. |
| `T soil day m [°C] (ERA5 reanalyses).1` | Weitere Bodentemperaturvariable aus ERA5. Wahrscheinlich tiefere Bodenschicht. | °C | Boden | Repräsentiert stabilere thermische Bedingungen unterhalb der Oberfläche. Vermutlich Layer 2, also 7–28 cm. |
| `T soil day m [°C] (ERA5 reanalyses).2` | Weitere Bodentemperaturvariable aus ERA5. Wahrscheinlich tiefere Bodenschicht. | °C | Boden | Repräsentiert trägere Bodentemperaturbedingungen. Vermutlich Layer 3, also 28–100 cm. |
| `Cloud cov [%] (ERA5 reanalyses)` | Bewölkungsgrad. | % | Wetter / Strahlung | Beeinflusst Strahlung, Temperatur, Verdunstung und Energiehaushalt. |
| `VPD day m [kPa] (ERA5 reanalyses)` | Tagesmittel des Vapour Pressure Deficit, also Wasserdampfdruckdefizit der Luft. | kPa | Atmosphäre | Beschreibt atmosphärischen Trockenheits- bzw. Verdunstungsdruck. |
| `PPPP day m [hPa] (ERA5 reanalyses)` | Tagesmittel des atmosphärischen Luftdrucks. | hPa | Atmosphäre | Kann mit Höhenlage, Wetterlage und allgemeinen atmosphärischen Bedingungen zusammenhängen. |
| `SWD day m [W/m**2] (ERA5 reanalyses)` | Tagesmittel der abwärtsgerichteten kurzwelligen Strahlung. | W/m² | Strahlung | Beeinflusst Energieeintrag, Bodentemperatur, Verdunstung und Pflanzenaktivität. |
| `PPFD day m [µmol/m**2/s] (ERA5 reanalyses)` | Tagesmittel der Photosynthetic Photon Flux Density. | µmol/m²/s | Strahlung / Vegetation | Beschreibt die photosynthetisch nutzbare Lichtmenge pro Fläche und Zeit. |
| `Duration [days] (Since last precipitation even...)` | Anzahl der Tage seit dem letzten Niederschlagsereignis. | Tage | Lag-/Recency-Feature | Beschreibt Trockenperioden und kann Bodenfeuchte- sowie Emissionsdynamiken erklären. |
| `Duration [days] (Since last fertiliser applica...)` | Anzahl der Tage seit der letzten Düngerapplikation. | Tage | Lag-/Management-Feature | Wichtig, da N₂O-Emissionen zeitlich verzögert nach Düngung auftreten können. |
| `Fert N dec adj exp [kg/ha] (Exponential decay model (k=0.05))` | Modellierte, exponentiell abklingende Stickstoffwirkung nach Düngung. | kg/ha | Modelliertes Management-Feature | Bildet ab, dass der Effekt einer Düngerapplikation mit der Zeit abnimmt. |
| `Transformation S (Modeled)` | Sinus-Transformation einer zyklischen Zeitkomponente. | dimensionslos | Modelliertes Zeitfeature | Kodiert Saisonalität ohne künstlichen Bruch zwischen Jahresende und Jahresanfang. |
| `Transformation C (Modeled)` | Cosinus-Transformation einer zyklischen Zeitkomponente. | dimensionslos | Modelliertes Zeitfeature | Ergänzt `Transformation S`; beide zusammen beschreiben zyklische Zeitpositionen. |
| `N2O flux [µg/m**2/h] (From soil surface, Modeled)` | Lachgasfluss von der Bodenoberfläche. | µg/m²/h | Zielvariable | Regressionsziel des Modells. Beschreibt die vorherzusagende N₂O-Emission. |
| `year` | Jahr, abgeleitet aus `Date/Time`. | Integer | Abgeleitetes Zeitfeature | Kann langfristige Trends, Messjahre oder zeitliche Splits unterstützen. |
| `month` | Monat, abgeleitet aus `Date/Time`. | Integer, 1–12 | Abgeleitetes Zeitfeature | Einfach interpretierbares saisonales Feature. |
| `day_of_year` | Tag des Jahres, abgeleitet aus `Date/Time`. | Integer, 1–365/366 | Abgeleitetes Zeitfeature | Gut geeignet für saisonale Muster und als Basis für zyklisches Encoding. |

## Fachliche Gruppierung der Features

| Feature-Gruppe | Spalten | Bedeutung |
|---|---|---|
| Identifikation | `Event` | Identifiziert Beobachtungskontexte, Standorte oder Ereignisse. |
| Räumliche Features | `Latitude`, `Longitude` | Beschreiben die geografische Lage der Messpunkte. |
| Zeitfeatures | `Date/Time`, `year`, `month`, `day_of_year`, `Transformation S`, `Transformation C` | Beschreiben Zeitpunkt, Jahr, Saison und zyklische zeitliche Muster. |
| Landnutzung und Management | `Land use`, `Fert N`, `Duration since last fertiliser application`, `Fert N dec adj exp` | Beschreiben menschliche Bewirtschaftung und Stickstoffeintrag. |
| Wetter und Atmosphäre | Temperatur, Niederschlag, Bewölkung, VPD, Luftdruck | Beschreiben meteorologische Rahmenbedingungen. |
| Strahlung | `SWD`, `PPFD` | Beschreiben Energieeintrag und photosynthetisch relevante Lichtverhältnisse. |
| Bodenbedingungen | Bodenfeuchte, Bodentemperatur | Prozessnahe Einflussgrößen für mikrobielle N₂O-Bildung. |
| Zielvariable | `N2O flux` | Vorherzusagende Lachgasemission. |

## Hinweise zu mehrfach vorkommenden Spaltennamen

Einige Spaltennamen kommen im Ursprungsdatensatz offenbar mehrfach oder sehr ähnlich vor. Beim Einlesen mit pandas wurden deshalb automatische Suffixe wie `.1` oder `.2` angehängt.

Beispiele:

- `Soil moisture [m**3/m**3] (ERA5 reanalyses)`
- `Soil moisture [m**3/m**3] (ERA5 reanalyses).1`
- `T soil day m [°C] (ERA5 reanalyses).1`
- `T soil day m [°C] (ERA5 reanalyses).2`

Diese Suffixe stammen nicht fachlich aus dem Datensatz, sondern entstehen durch pandas, wenn mehrere Spalten denselben Namen besitzen. Fachlich ist wahrscheinlich, dass diese Spalten unterschiedliche ERA5-Bodenschichten repräsentieren.

ERA5-Land verwendet für Bodenvariablen typischerweise folgende Schichten:

| Layer | Tiefe |
|---:|---:|
| Layer 1 | 0–7 cm |
| Layer 2 | 7–28 cm |
| Layer 3 | 28–100 cm |
| Layer 4 | 100–289 cm |

Da in den aktuellen Spaltennamen nicht jede Tiefe explizit enthalten ist, sollte die genaue Zuordnung der `.1`- und `.2`-Spalten geprüft werden, bevor sie endgültig umbenannt werden.

## Mögliche saubere Spaltennamen

Für die spätere Modellierung könnten die Spalten in ein einheitliches `snake_case`-Format überführt werden:

| Originalspalte | Vorschlag für neuen Spaltennamen |
|---|---|
| `Event` | `event` |
| `Latitude` | `latitude` |
| `Longitude` | `longitude` |
| `Date/Time` | `date_time` |
| `Land use` | `land_use` |
| `Fert N [kg/ha] (Recorded at time of application)` | `fert_n_kg_ha` |
| `TTT day m [°C] (ERA5 reanalyses)` | `air_temp_mean_c` |
| `TxTxTx day max [°C] (ERA5 reanalyses)` | `air_temp_max_c` |
| `TnTnTn day min [°C] (ERA5 reanalyses)` | `air_temp_min_c` |
| `Precip day total [mm/day] (ERA5 reanalyses)` | `precip_total_mm_day` |
| `Soil moisture [m**3/m**3] (Content at 0-7 cm depth, ERA5...)` | `soil_moisture_0_7cm_m3_m3` |
| `Soil moisture [m**3/m**3] (ERA5 reanalyses)` | `soil_moisture_7_28cm_m3_m3` |
| `Soil moisture [m**3/m**3] (ERA5 reanalyses).1` | `soil_moisture_28_100cm_m3_m3` |
| `T soil day m [°C] (ERA5 reanalyses)` | `soil_temp_0_7cm_c` |
| `T soil day m [°C] (ERA5 reanalyses).1` | `soil_temp_7_28cm_c` |
| `T soil day m [°C] (ERA5 reanalyses).2` | `soil_temp_28_100cm_c` |
| `Cloud cov [%] (ERA5 reanalyses)` | `cloud_cover_percent` |
| `VPD day m [kPa] (ERA5 reanalyses)` | `vpd_mean_kpa` |
| `PPPP day m [hPa] (ERA5 reanalyses)` | `air_pressure_mean_hpa` |
| `SWD day m [W/m**2] (ERA5 reanalyses)` | `shortwave_downward_radiation_w_m2` |
| `PPFD day m [µmol/m**2/s] (ERA5 reanalyses)` | `ppfd_mean_umol_m2_s` |
| `Duration [days] (Since last precipitation even...)` | `days_since_last_precip` |
| `Duration [days] (Since last fertiliser applica...)` | `days_since_last_fertiliser` |
| `Fert N dec adj exp [kg/ha] (Exponential decay model (k=0.05))` | `fert_n_decay_adjusted_kg_ha` |
| `Transformation S (Modeled)` | `season_sin` |
| `Transformation C (Modeled)` | `season_cos` |
| `N2O flux [µg/m**2/h] (From soil surface, Modeled)` | `n2o_flux_ug_m2_h` |
| `year` | `year` |
| `month` | `month` |
| `day_of_year` | `day_of_year` |

## Quellen

- PANGAEA-Datensatz: *Nitrous oxide emissions from African Forests and Plantations*.
- Copernicus / ECMWF ERA5-Land-Dokumentation für ERA5-Land-Reanalysevariablen und Bodenschichten.