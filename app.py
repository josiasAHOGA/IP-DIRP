import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import hashlib
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# DONNÉES EMBARQUÉES
# ══════════════════════════════════════════════════════════════════════════════
CHARGE_JSON    = '[{"Initiale": "IG", "Groupe": "SIEDD", "P": 4, "Co": 4, "R": 6, "Total_sans_R": 8, "Total": 14, "VT": 34, "IC": 18, "ICR": 24.8}, {"Initiale": "SH", "Groupe": "ARN", "P": 4, "Co": 5, "R": 5, "Total_sans_R": 9, "Total": 14, "VT": 34, "IC": 18, "ICR": 24.8}, {"Initiale": "UA", "Groupe": "SIEDD", "P": 5, "Co": 3, "R": 4, "Total_sans_R": 8, "Total": 12, "VT": 38, "IC": 17, "ICR": 24.6}, {"Initiale": "FS", "Groupe": "SIEDD", "P": 5, "Co": 4, "R": 4, "Total_sans_R": 9, "Total": 13, "VT": 32, "IC": 18, "ICR": 24.4}, {"Initiale": "PL", "Groupe": "ARN", "P": 4, "Co": 5, "R": 5, "Total_sans_R": 9, "Total": 14, "VT": 31, "IC": 18, "ICR": 24.2}, {"Initiale": "ED", "Groupe": "SIEDD", "P": 5, "Co": 5, "R": 3, "Total_sans_R": 10, "Total": 13, "VT": 30, "IC": 18, "ICR": 24}, {"Initiale": "CA", "Groupe": "ARN", "P": 5, "Co": 3, "R": 5, "Total_sans_R": 8, "Total": 13, "VT": 30, "IC": 18, "ICR": 24}, {"Initiale": "GN", "Groupe": "ARN", "P": 4, "Co": 4, "R": 6, "Total_sans_R": 8, "Total": 14, "VT": 30, "IC": 18, "ICR": 24}, {"Initiale": "JH", "Groupe": "SIEDD", "P": 4, "Co": 5, "R": 5, "Total_sans_R": 9, "Total": 14, "VT": 30, "IC": 18, "ICR": 24}, {"Initiale": "AP", "Groupe": "SIEDD", "P": 4, "Co": 5, "R": 3, "Total_sans_R": 9, "Total": 12, "VT": 37, "IC": 16, "ICR": 23.4}, {"Initiale": "YM", "Groupe": "SIEDD", "P": 4, "Co": 4, "R": 5, "Total_sans_R": 8, "Total": 13, "VT": 30, "IC": 17, "ICR": 23}, {"Initiale": "MO", "Groupe": "SIEDD", "P": 5, "Co": 3, "R": 4, "Total_sans_R": 8, "Total": 12, "VT": 30, "IC": 17, "ICR": 23}, {"Initiale": "AT", "Groupe": "SIEDD", "P": 3, "Co": 5, "R": 5, "Total_sans_R": 8, "Total": 13, "VT": 34, "IC": 16, "ICR": 22.8}, {"Initiale": "GH", "Groupe": "SIEDD", "P": 3, "Co": 5, "R": 5, "Total_sans_R": 8, "Total": 13, "VT": 34, "IC": 16, "ICR": 22.8}, {"Initiale": "JA", "Groupe": "SIEDD", "P": 5, "Co": 3, "R": 3, "Total_sans_R": 8, "Total": 11, "VT": 32, "IC": 16, "ICR": 22.4}, {"Initiale": "AD", "Groupe": "SIEDD", "P": 4, "Co": 3, "R": 6, "Total_sans_R": 7, "Total": 13, "VT": 27, "IC": 17, "ICR": 22.4}, {"Initiale": "PH", "Groupe": "SIEDD", "P": 7, "Co": 2, "R": 0, "Total_sans_R": 9, "Total": 9, "VT": 31, "IC": 16, "ICR": 22.2}, {"Initiale": "CS", "Groupe": "SIEDD", "P": 3, "Co": 4, "R": 6, "Total_sans_R": 7, "Total": 13, "VT": 31, "IC": 16, "ICR": 22.2}, {"Initiale": "IA", "Groupe": "SIEDD", "P": 3, "Co": 4, "R": 6, "Total_sans_R": 7, "Total": 13, "VT": 30, "IC": 16, "ICR": 22}, {"Initiale": "SB", "Groupe": "ARN", "P": 7, "Co": 1, "R": 0, "Total_sans_R": 8, "Total": 8, "VT": 27, "IC": 15, "ICR": 20.4}, {"Initiale": "JV", "Groupe": "SIEDD", "P": 3, "Co": 3, "R": 7, "Total_sans_R": 6, "Total": 13, "VT": 21, "IC": 16, "ICR": 20.2}, {"Initiale": "OW", "Groupe": "SIEF", "P": 8, "Co": 1, "R": 0, "Total_sans_R": 9, "Total": 9, "VT": 15, "IC": 17, "ICR": 20}, {"Initiale": "EL", "Groupe": "SIEF", "P": 1, "Co": 8, "R": 1, "Total_sans_R": 9, "Total": 10, "VT": 29, "IC": 11, "ICR": 16.8}, {"Initiale": "EK", "Groupe": "SIEF", "P": 2, "Co": 6, "R": 1, "Total_sans_R": 8, "Total": 9, "VT": 27, "IC": 11, "ICR": 16.4}, {"Initiale": "SD", "Groupe": "SIEF", "P": 2, "Co": 5, "R": 3, "Total_sans_R": 7, "Total": 10, "VT": 21, "IC": 12, "ICR": 16.2}, {"Initiale": "JY", "Groupe": "ARN", "P": 0, "Co": 6, "R": 5, "Total_sans_R": 6, "Total": 11, "VT": 22, "IC": 11, "ICR": 15.4}, {"Initiale": "FA", "Groupe": "SIEF", "P": 1, "Co": 7, "R": 2, "Total_sans_R": 8, "Total": 10, "VT": 21, "IC": 11, "ICR": 15.2}, {"Initiale": "TA", "Groupe": "SIEF", "P": 2, "Co": 5, "R": 2, "Total_sans_R": 7, "Total": 9, "VT": 20, "IC": 11, "ICR": 15}, {"Initiale": "RB", "Groupe": "SIEF", "P": 0, "Co": 3, "R": 0, "Total_sans_R": 3, "Total": 3, "VT": 13, "IC": 3, "ICR": 5.6}, {"Initiale": "CY", "Groupe": "ARN", "P": 0, "Co": 2, "R": 0, "Total_sans_R": 2, "Total": 2, "VT": 8, "IC": 2, "ICR": 3.6}]'
MISSIONS_JSON  = '[{"Mois": "AVRIL", "Semaine": "S14", "Periode": "30/03-03/04", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": ""}, {"Mois": "AVRIL", "Semaine": "S14", "Periode": "30/03-03/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S14", "Periode": "30/03-03/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "", "Volume": "", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "06/04-10/04", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Tampon", "Departement": "BOR", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "GN", "Observation": "Rotation Nord"}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "06/04-10/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "4", "Structures": "PH Sainte Rita (Ex Pharmacie de l\'espoir)\\nPH Vie Nouvelle\\nPH Zogbo\\nPH Zongo Nima\\n", "IP": "ED", "Co1": "GH", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "06/04-10/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "OUE", "Volume": "3", "Structures": "H.AAR\\nCHD Oueme\\nHZ Adjohoun", "IP": "AP", "Co1": "MO", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "07/04-09/04", "Zone": "Sud", "Type_Inspection": "BPF locale", "Sous_Type": "Site 1", "Departement": "OUE", "Volume": "1", "Structures": "BIOLYNX", "IP": "OW", "Co1": "TA", "Co2": "", "Co3": "", "Reserve": "IA", "Observation": "Fixe imposée (bIOlYNX)"}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "07/04-10/04", "Zone": "Sud", "Type_Inspection": "BPF locale", "Sous_Type": "Site 2", "Departement": "LIT", "Volume": "1", "Structures": "PHARMAQUICK", "IP": "", "Co1": "SD", "Co2": "FA", "Co3": "", "Reserve": "JV", "Observation": "Fixe imposée (Pharmaquick)"}, {"Mois": "AVRIL", "Semaine": "S16", "Periode": "13/04-17/04", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "4", "Structures": "BWENDORA\\nCarrefour Hubert K.MAGA\\nGanou  (Ex Guéma)\\nCité des Kobourou", "IP": "SH", "Co1": "SB", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Rotation Nord"}, {"Mois": "AVRIL", "Semaine": "S16", "Periode": "13/04-17/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "5", "Structures": "PH Akossombo\\nPH Amen\\nPH De la Paix\\nNouvelle PH Fifadji\\nNouvelle PH Ménontin\\n", "IP": "UA", "Co1": "YM", "Co2": "", "Co3": "", "Reserve": "AT", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S16", "Periode": "13/04-17/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "LIT", "Volume": "4", "Structures": "HZ Menontin\\nCHU-MEL Cotonou\\nCNHU-PPC\\nHopital Bethesda\\n", "IP": "JA", "Co1": "JH", "Co2": "", "Co3": "", "Reserve": "IG", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S16", "Periode": "14/04-16/04", "Zone": "Sud", "Type_Inspection": "BPF locale", "Sous_Type": "Site 3", "Departement": "ATL", "Volume": "1", "Structures": "COPHARBIOTECH", "IP": "", "Co1": "EK", "Co2": "SD", "Co3": "", "Reserve": "", "Observation": "Fixe imposée (Cophar Biotech)"}, {"Mois": "AVRIL", "Semaine": "S17", "Periode": "20/04-24/04", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "BOR", "Volume": "4", "Structures": "HIA Parakou ; HZ Bembèrèkè ; CHD Borgou ; HZ Papane", "IP": "GN", "Co1": "JY", "Co2": "", "Co3": "", "Reserve": "PL", "Observation": "Début PUI Nord"}, {"Mois": "AVRIL", "Semaine": "S17", "Periode": "20/04-24/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "5", "Structures": "PH Renouveau\\nPH Saint Louis\\nPH Sainte Famille\\nPH Le Rocher\\nPH Sainte Philomène\\n", "IP": "IG", "Co1": "CS", "Co2": "", "Co3": "", "Reserve": "FS", "Observation": "Renfort Sud"}, {"Mois": "AVRIL", "Semaine": "S17", "Periode": "20/04-24/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "COU", "Volume": "4", "Structures": "Hôpital APH Gohomey\\nHôpital St Camille Dogbo\\nHZ Aplahoue\\nHZ Klouekanme", "IP": "MO", "Co1": "PH", "Co2": "", "Co3": "", "Reserve": "FA", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S17", "Periode": "20/04-24/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (CAMEVET)", "Departement": "LIT", "Volume": "1", "Structures": "\\nCAMEVET", "IP": "OW", "Co1": "AP", "Co2": "", "Co3": "", "Reserve": "", "Observation": "GR Sud"}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "27/04-01/05", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "DON", "Volume": "3", "Structures": "HZ Bassila ; H. Ordre de malte ; CHD Donga", "IP": "PL", "Co1": "CA", "Co2": "CY", "Co3": "", "Reserve": "SH", "Observation": "Rotation Nord"}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "27/04-01/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "4", "Structures": "PH L\'Eternité\\nPH Le Tamaya\\nNouvelle PH Agontikon\\nPH Palace Plus\\n", "IP": "TA", "Co1": "JA", "Co2": "", "Co3": "", "Reserve": "UA", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "27/04-01/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "MON", "Volume": "3", "Structures": "HZ Lokossa\\nCHD Mono\\nHZ Come", "IP": "JV", "Co1": "AT", "Co2": "", "Co3": "", "Reserve": "IA", "Observation": "Routine Sud"}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "27/04-30/04", "Zone": "Sud", "Type_Inspection": "BPC", "Sous_Type": "Site 1", "Departement": "ZOU", "Volume": "1", "Structures": "PDMC-SL", "IP": "", "Co1": "FS", "Co2": "FA", "Co3": "", "Reserve": "", "Observation": "Fixe imposée (CHD Goho)"}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "29/04-30/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (UBIPHARM)", "Departement": "LIT", "Volume": "1", "Structures": "UBIPHARM", "IP": "YM", "Co1": "JH", "Co2": "", "Co3": "", "Reserve": "", "Observation": "2e GR Avril"}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "27/04-27/04", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "1", "Structures": "Jak Aléjo", "IP": "JH", "Co1": "ED", "Co2": "", "Co3": "", "Reserve": "", "Observation": ""}, {"Mois": "MAI", "Semaine": "S19", "Periode": "05/05-08/05", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Tampon", "Departement": "", "Volume": "0", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "", "Observation": "CVA Ménagé"}, {"Mois": "MAI", "Semaine": "S19", "Periode": "04/05-04/05", "Zone": "Nord", "Type_Inspection": "Exceptionnelle ARN", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "2", "Structures": "PH GOROBANI\\nPH BEYEROU", "IP": "SB", "Co1": "PL", "Co2": "", "Co3": "", "Reserve": "SH", "Observation": "Fixe imposée (incluse dans total Nord)"}, {"Mois": "MAI", "Semaine": "S19", "Periode": "04/05-08/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "5", "Structures": "PH Luli Luli Sarl\\nNouvelle PH Akogbato\\nNouvelle PH Houéyiho\\nNouvelle PH Les Cocotiers\\nPH Océane\\n", "IP": "AP", "Co1": "TA", "Co2": "", "Co3": "", "Reserve": "UA", "Observation": "Routine Sud"}, {"Mois": "MAI", "Semaine": "S19", "Periode": "04/05-08/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "COL", "Volume": "4", "Structures": "HZ Dassa\\nHZ Save\\nHôpital Abbraccio\\nHopital Savalou\\n", "IP": "ED", "Co1": "EK", "Co2": "RB", "Co3": "", "Reserve": "FS", "Observation": "Routine Sud"}, {"Mois": "MAI", "Semaine": "S19", "Periode": "05/05-08/05", "Zone": "Sud", "Type_Inspection": "BPC", "Sous_Type": "Site 2", "Departement": "BOR", "Volume": "1", "Structures": "SMAART-II", "IP": "OW", "Co1": "AD", "Co2": "EL", "Co3": "", "Reserve": "", "Observation": "Fixe imposée (Parakou)"}, {"Mois": "MAI", "Semaine": "S20", "Periode": "11/05-15/05", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "2", "Structures": "Du Campus (Parakou)\\nDu Lycée", "IP": "SB", "Co1": "GN", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "Rotation Nord"}, {"Mois": "MAI", "Semaine": "S20", "Periode": "11/05-15/05", "Zone": "Sud", "Type_Inspection": "Exceptionnelle", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "2", "Structures": "PH LA REFERENCE\\nPH ZOUNDJA SATELLITE", "IP": "PH", "Co1": "MO", "Co2": "JV", "Co3": "", "Reserve": "", "Observation": "Fixe imposée"}, {"Mois": "MAI", "Semaine": "S20", "Periode": "11/05-15/05", "Zone": "Sud", "Type_Inspection": "Exceptionnelle", "Sous_Type": "PUI", "Departement": "ATL", "Volume": "2", "Structures": "CHIC \\nHZ AOMEY CALAVI", "IP": "PH", "Co1": "MO", "Co2": "JV", "Co3": "", "Reserve": "", "Observation": "Fixe imposée"}, {"Mois": "MAI", "Semaine": "S20", "Periode": "11/05-15/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "4", "Structures": "\\nPH Safari Agla \\nPH Saint Etienne d\'Agla \\nPH Les archanges\\nPH Les pylones", "IP": "SD", "Co1": "FA", "Co2": "", "Co3": "", "Reserve": "IG", "Observation": "Charge ajustée"}, {"Mois": "MAI", "Semaine": "S20", "Periode": "11/05-15/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "4", "Structures": "PH Le Nokoué\\nPH Yénawa\\nPH L’Immaculée Adogléta Ex La Colombe\\nPH De l\'Abattoir\\n", "IP": "JH", "Co1": "IA", "Co2": "", "Co3": "", "Reserve": "AT", "Observation": "Routine Sud"}, {"Mois": "MAI", "Semaine": "S21", "Periode": "18/05-22/05", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "4", "Structures": "Confiance\\nDes 3 banques\\nKaaya\\nDon de Dieu (Nikki)", "IP": "SH", "Co1": "JY", "Co2": "CY", "Co3": "", "Reserve": "CA", "Observation": "Rotation Nord"}, {"Mois": "MAI", "Semaine": "S21", "Periode": "18/05-22/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "4", "Structures": "Adanhounsa\\nAttogon\\nAkassato\\nLa Bénédiction", "IP": "EL", "Co1": "YM", "Co2": "", "Co3": "", "Reserve": "GH", "Observation": "Routine Sud"}, {"Mois": "MAI", "Semaine": "S21", "Periode": "18/05-22/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "ZOU", "Volume": "3", "Structures": "HZ Djidja\\nCHD Zou\\nHZ Cove", "IP": "IA", "Co1": "EK", "Co2": "", "Co3": "", "Reserve": "AD", "Observation": "Routine Sud"}, {"Mois": "MAI", "Semaine": "S22", "Periode": "26/05-29/05", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Tampon", "Departement": "", "Volume": "0", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Fériés"}, {"Mois": "MAI", "Semaine": "S22", "Periode": "25/05-29/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "3", "Structures": "Senan Zounga\\nAyessi Godomey\\nCarrefour Gninnin", "IP": "FA", "Co1": "GH", "Co2": "", "Co3": "", "Reserve": "JV", "Observation": "Fin de mois renforcée"}, {"Mois": "MAI", "Semaine": "S22", "Periode": "25/05-29/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "3", "Structures": "PH Saint Gabriel\\nPH Saint Urbain\\nPH Le Remède", "IP": "AT", "Co1": "ED", "Co2": "", "Co3": "", "Reserve": "SD", "Observation": "Routine Sud"}, {"Mois": "MAI", "Semaine": "S22", "Periode": "25/05-29/05", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (UBPHAR Cotonou et Porto Novo)", "Departement": "LIT/OUE", "Volume": "2", "Structures": "UBPHAR COTONOU ET PORTO-NOVO", "IP": "OW", "Co1": "CS", "Co2": "", "Co3": "", "Reserve": "", "Observation": "GR Sud Mai"}, {"Mois": "JUIN", "Semaine": "S23", "Periode": "01/06-05/06", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Tampon", "Departement": "", "Volume": "0", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "SH", "Observation": "Repos CVA"}, {"Mois": "JUIN", "Semaine": "S23", "Periode": "01/06-05/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "5", "Structures": "PHARMACIE DE L\'AIGLE ROYALE\\nPH Esplanade Dantokpa (Ex Des 4 Thérapies)\\nPH Mahuton\\nPH STE FOI\\nNouvelle PH Sainte Victoire\\n\\"", "IP": "AP", "Co1": "JH", "Co2": "", "Co3": "", "Reserve": "AD", "Observation": "Charge réduite (missions ext.)"}, {"Mois": "JUIN", "Semaine": "S23", "Periode": "01/06-05/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Cica Santé Akassato\\nCité Arconville\\nCité de paix (HOUEGBO) (Ex Pharmacie Saint Enfant Jesus de Houegbo)\\nDagbédé de Vassého\\nDe l\'immaculée Conception", "IP": "UA", "Co1": "FS", "Co2": "", "Co3": "", "Reserve": "IA", "Observation": "Charge réduite"}, {"Mois": "JUIN", "Semaine": "S23", "Periode": "01/06-06/06", "Zone": "Extérieur", "Type_Inspection": "BPF extérieure", "Sous_Type": "Inde 1", "Departement": "EXT", "Volume": "1", "Structures": "", "IP": "OW", "Co1": "TA", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Fixe imposée"}, {"Mois": "JUIN", "Semaine": "S23", "Periode": "01/06-06/06", "Zone": "Extérieur", "Type_Inspection": "BPF extérieure", "Sous_Type": "Inde 2", "Departement": "EXT", "Volume": "1", "Structures": "", "IP": "", "Co1": "SD", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Fixe imposée"}, {"Mois": "JUIN", "Semaine": "S24", "Periode": "08/06-12/06", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "4", "Structures": "\\nHoueze Pharma\\nImane\\nOkedama\\nArafat", "IP": "SB", "Co1": "SH", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "Rotation Nord"}, {"Mois": "JUIN", "Semaine": "S24", "Periode": "08/06-12/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes_vétérinaires (GVS)", "Departement": "LIT", "Volume": "1", "Structures": "GVS", "IP": "PH", "Co1": "IG", "Co2": "JH", "Co3": "", "Reserve": "CS", "Observation": "Routine Sud allégée"}, {"Mois": "JUIN", "Semaine": "S24", "Periode": "08/06-12/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "ATL", "Volume": "3", "Structures": "Hôp.La Croix Zinvié\\nHZ Ouidah\\nHZ Allada \\n", "IP": "GH", "Co1": "EL", "Co2": "", "Co3": "", "Reserve": "IA", "Observation": "Routine Sud"}, {"Mois": "JUIN", "Semaine": "S24", "Periode": "08/06-12/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (GAPOB BOHICON)", "Departement": "ZOU", "Volume": "1", "Structures": "GAPOB BOHICON", "IP": "JA", "Co1": "EK", "Co2": "", "Co3": "", "Reserve": "", "Observation": "GR Juin"}, {"Mois": "JUIN", "Semaine": "S25", "Periode": "15/06-19/06", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "4", "Structures": "La Gare\\nLa Grâce (Parakou)\\nN’dali\\nSanté Vitale", "IP": "GN", "Co1": "PL", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Rotation Nord"}, {"Mois": "JUIN", "Semaine": "S25", "Periode": "15/06-19/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "ATL", "Volume": "2", "Structures": "", "IP": "ED", "Co1": "AD", "Co2": "", "Co3": "", "Reserve": "JV", "Observation": "Routine Sud"}, {"Mois": "JUIN", "Semaine": "S25", "Periode": "15/06-19/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "El Béthesda\\nEmmanuel\\nEspace Santé\\nEyitayo de Womey\\nFifamè", "IP": "YM", "Co1": "AT", "Co2": "", "Co3": "", "Reserve": "JH", "Observation": "Routine Sud"}, {"Mois": "JUIN", "Semaine": "S26", "Periode": "22/06-26/06", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "BOR", "Volume": "4", "Structures": "Hôpital Conf Saint Padré Pio\\nHZ Boko\\nHZ Sounon Sero\\nHOPITAL TINRE", "IP": "CA", "Co1": "JY", "Co2": "", "Co3": "", "Reserve": "SH", "Observation": "Rotation Nord PUI"}, {"Mois": "JUIN", "Semaine": "S26", "Periode": "22/06-26/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Fleuve de vie\\nGbèna\\nGodomey Centre\\nGodomey Fignonhou\\nGodomey PK 14", "IP": "FS", "Co1": "FA", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "JUIN", "Semaine": "S26", "Periode": "22/06-26/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Hèdomey Dekoungbe\\nHêvié Sarl\\nHouénoussou\\nIita\\nL’Angelus", "IP": "IA", "Co1": "EK", "Co2": "", "Co3": "", "Reserve": "CS", "Observation": "Routine Sud"}, {"Mois": "JUIN", "Semaine": "S26", "Periode": "22/06-26/06", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (UBPHAR + GAPOB PARAKOU)", "Departement": "BOR", "Volume": "2", "Structures": "UBPHAR ET GAPOB PARAKOU", "IP": "OW", "Co1": "", "Co2": "", "Co3": "", "Reserve": "AT", "Observation": "2e GR Juin"}, {"Mois": "JUIN", "Semaine": "S27", "Periode": "29/06-03/07", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "ALI", "Volume": "4", "Structures": "HZ Malanville-Karimama\\nHZ Kandi\\nHZ Banikoara\\nH. Regina Pacis\\n", "IP": "PL", "Co1": "SH", "Co2": "", "Co3": "", "Reserve": "CA", "Observation": "Clôture bloc Juin Nord"}, {"Mois": "JUIN", "Semaine": "S27", "Periode": "29/06-03/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "La Concorde\\nLa Grâce (Ouidah)\\nMERE ELISABETH NOBRE\\nLa Prunelle de l\'Eternel de PAHOU\\nLa Rose", "IP": "MO", "Co1": "AP", "Co2": "", "Co3": "", "Reserve": "JV", "Observation": "Fin de mois"}, {"Mois": "JUIN", "Semaine": "S27", "Periode": "29/06-03/07", "Zone": "Sud", "Type_Inspection": "BPF locale", "Sous_Type": "Site 4", "Departement": "ZOU", "Volume": "1", "Structures": "", "IP": "", "Co1": "FA", "Co2": "EL", "Co3": "", "Reserve": "", "Observation": "Fixe imposée (API)"}, {"Mois": "JUIN", "Semaine": "S27", "Periode": "29/06-03/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Le Jourdain Togoudo\\nLe Président\\nLe Schilo (Tankpè-Parana)\\nLe Sycomore\\nLes Capucines", "IP": "IG", "Co1": "AD", "Co2": "", "Co3": "", "Reserve": "GH", "Observation": "Fin de mois"}, {"Mois": "JUILLET", "Semaine": "S28", "Periode": "06/07-10/07", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Tampon", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "CY indisponible 01-20/07"}, {"Mois": "JUILLET", "Semaine": "S28", "Periode": "06/07-10/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Les Graces Divines de Ouèdo\\nMagnificat\\nMaria Gléta\\nMitonwè\\nPrincipale de Houéto", "IP": "FS", "Co1": "JA", "Co2": "", "Co3": "", "Reserve": "JV", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S28", "Periode": "06/07-10/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Principale de Tori Bossito\\nSaint Abel Pharmabel de Tankpè\\nSaint Antoine de Padoue\\nSaint Bénoît de Womey\\nSaint Georges", "IP": "UA", "Co1": "CS", "Co2": "", "Co3": "", "Reserve": "YM", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S28", "Periode": "06/07-11/07", "Zone": "Sud", "Type_Inspection": "BPF locale", "Sous_Type": "Site 4", "Departement": "ZOU", "Volume": "1", "Structures": "", "IP": "", "Co1": "FA", "Co2": "EL", "Co3": "", "Reserve": "", "Observation": "Fixe imposée (API)"}, {"Mois": "JUILLET", "Semaine": "", "Periode": "", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Le Jourdain Togoudo\\nLe Président\\nLe Schilo (Tankpè-Parana)\\nLe Sycomore\\nLes Capucines", "IP": "IG", "Co1": "AD", "Co2": "", "Co3": "", "Reserve": "GH", "Observation": "Fin de mois"}, {"Mois": "JUILLET", "Semaine": "S28", "Periode": "06/07-08/07", "Zone": "Sud", "Type_Inspection": "BPF locale", "Sous_Type": "Site 5", "Departement": "OUE", "Volume": "1", "Structures": "", "IP": "OW", "Co1": "TA", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Fixe imposée (SoftCare)"}, {"Mois": "JUILLET", "Semaine": "S29", "Periode": "13/07-17/07", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "4", "Structures": "Tranza\\nVita Plus\\nZongo II\\nNima", "IP": "CA", "Co1": "JY", "Co2": "", "Co3": "", "Reserve": "GN", "Observation": "NA, SB, JH en congé ; CY indispo"}, {"Mois": "JUILLET", "Semaine": "S29", "Periode": "13/07-17/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Saint Gérard de Zoundja\\nSaint Paul\\nSaint PioTokan\\nDe la Centrale Maria-Gleta 2 (Pharmacie Camp Guézo 2)\\nSaint Steve Sarl", "IP": "PH", "Co1": "AT", "Co2": "", "Co3": "", "Reserve": "MO", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S29", "Periode": "13/07-17/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Sainte Adèle de l’Echangeur de Godomey\\nSainte Bernadette\\nSaint Marcellin\\nSainte Marie Elise\\nSainte Trinité de Pahou", "IP": "ED", "Co1": "IG", "Co2": "", "Co3": "", "Reserve": "AP", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S30", "Periode": "20/07-24/07", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR (1)/ALI", "Volume": "4", "Structures": "Saint Benoit de Parakou\\nNasiara\\nMagnolia\\nDHANVANTARI MA\\n", "IP": "SH", "Co1": "GN", "Co2": "", "Co3": "", "Reserve": "PL", "Observation": "CY retour possible après 20/07"}, {"Mois": "JUILLET", "Semaine": "S30", "Periode": "20/07-24/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Sèhouè\\nSos Santé\\nTogoudo\\nToussaint L\'ouverture\\nLe Lotus", "IP": "AP", "Co1": "GH", "Co2": "", "Co3": "", "Reserve": "AD", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S30", "Periode": "20/07-24/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Zinvié\\nZoca\\nZopah Olouwatobi\\nSaint Camille\\nLa Miraculeuse", "IP": "MO", "Co1": "CS", "Co2": "", "Co3": "", "Reserve": "IA", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S30", "Periode": "20/07-24/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (GAPOB COTONOU + LABOREX)", "Departement": "LIT", "Volume": "2", "Structures": "GAPOB COTONOU\\nLABOREX", "IP": "OW", "Co1": "EL", "Co2": "", "Co3": "", "Reserve": "", "Observation": "GR Juillet"}, {"Mois": "JUILLET", "Semaine": "S31", "Periode": "27/07-31/07", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "ATA", "Volume": "2", "Structures": "CHD Atacora ; HZ Saint Jean de Dieu (Tanguiéta)", "IP": "PL", "Co1": "JY", "Co2": "", "Co3": "", "Reserve": "CA", "Observation": "Clôture Nord Juillet"}, {"Mois": "JUILLET", "Semaine": "S31", "Periode": "27/07-31/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Zoé Santé\\nOlouwatoyin de Kpota\\nAlpha Oméga Bazounkpa\\nAlhéri Glodénou\\nSedami", "IP": "AD", "Co1": "SD", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "JUILLET", "Semaine": "S31", "Periode": "27/07-31/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Nouvelle Eve\\nPHARMACIE AÏTCHEDJI SEMINAIRE\\nPHARMACIE VALLEE BERACA\\nZoé d\'Atrokpocodji\\nPahou Capot", "IP": "IA", "Co1": "UA", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Clôture Sud Juillet"}, {"Mois": "JUILLET", "Semaine": "S31", "Periode": "27/07-31/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (SOBAPS PARAKOU + NATITINGOU)", "Departement": "BOR/ATA", "Volume": "2", "Structures": "SOBAPS PARAKOU + NATITINGOU", "IP": "FS", "Co1": "ED", "Co2": "", "Co3": "", "Reserve": "JA", "Observation": "2e GR Juillet"}, {"Mois": "JUILLET", "Semaine": "S31", "Periode": "27/07-31/07", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Grossistes-répartiteurs (Sobaps Cotonou +DG)", "Departement": "LIT", "Volume": "2", "Structures": "SOBAPS COTONOU ET DG", "IP": "PH", "Co1": "IG", "Co2": "", "Co3": "", "Reserve": "JH", "Observation": "SoBAPS Juillet"}, {"Mois": "AOUT", "Semaine": "S32", "Periode": "03/08-07/08", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Tampon", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "PH/ED/YM congés Sud ; NA en congé"}, {"Mois": "AOUT", "Semaine": "S32", "Periode": "03/08-07/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Kpèdétin\\nLa Jouvence Tokpota Dadjrougbe\\nLa Place Kokoye\\nLe Prestige du Pont\\nAdjohoun", "IP": "JH", "Co1": "FA", "Co2": "", "Co3": "", "Reserve": "CS", "Observation": "Routine Sud"}, {"Mois": "AOUT", "Semaine": "S32", "Periode": "03/08-07/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Les Anges\\nLes Chérubins\\nLes Palmiers\\nL\'Harmonie \\nL\'unité", "IP": "AT", "Co1": "GH", "Co2": "", "Co3": "", "Reserve": "JV", "Observation": "Routine Sud"}, {"Mois": "AOUT", "Semaine": "S33", "Periode": "10/08-14/08", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ALI", "Volume": "4", "Structures": "Centrale de Banikoara\\nPharmacie Tawfiq de Sonsoro\\nDara Fari (Ex Capitaine FariI) \\nDu Sahel (décès)", "IP": "SB", "Co1": "CA", "Co2": "", "Co3": "", "Reserve": "GN", "Observation": "Clôture officines Nord"}, {"Mois": "AOUT", "Semaine": "S33", "Periode": "10/08-14/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Malanhoui\\nMetogninsè d\'Anavié S.A.S\\nNotre Dame de l\'Atlantique Akondé\\nNouvel Espoir (Ex victoria)\\nNouvel Horizon", "IP": "JV", "Co1": "PH", "Co2": "", "Co3": "", "Reserve": "FS", "Observation": "IA/JA partiellement indispo"}, {"Mois": "AOUT", "Semaine": "S33", "Periode": "10/08-14/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Nouvelle Pharmacie Du Grand Marché\\nNouvelle Pharmacie Kandévié\\nOganla\\nOlatoundji\\nOlayèmi Guévié", "IP": "CS", "Co1": "UA", "Co2": "", "Co3": "", "Reserve": "IG", "Observation": "Routine Sud"}, {"Mois": "AOUT", "Semaine": "S34", "Periode": "17/08-21/08", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATA", "Volume": "4", "Structures": "La Bienheureuse (Natitingou)\\nTanguiéta\\nTissanta (Décès)\\nNasiara de Kérou", "IP": "GN", "Co1": "PL", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "Progression PUI Nord"}, {"Mois": "AOUT", "Semaine": "S34", "Periode": "17/08-21/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Owodé\\nPlace Bayol\\nSaint Pierre de Sèmè Kpodji\\nSaint Raymond du Marché Agata\\nSainte Marie", "IP": "AD", "Co1": "EL", "Co2": "", "Co3": "", "Reserve": "EK", "Observation": "Routine Sud renforcée"}, {"Mois": "AOUT", "Semaine": "S34", "Periode": "17/08-21/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Suru Léré (Porto - Novo)\\nToffa 1er\\nTohouè\\nTokpota 2 - Davo\\nVakon", "IP": "MO", "Co1": "GH", "Co2": "", "Co3": "", "Reserve": "YM", "Observation": "Routine Sud"}, {"Mois": "AOUT", "Semaine": "S35", "Periode": "24/08-28/08", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "ATA", "Volume": "3", "Structures": "HZ Natitingou\\nHôpital Bakhita\\nHZ Kouande\\n", "IP": "SH", "Co1": "CA", "Co2": "", "Co3": "", "Reserve": "GN", "Observation": "EK en congé dès 26/08"}, {"Mois": "AOUT", "Semaine": "S35", "Periode": "24/08-28/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "4", "Structures": "Val des Graces Sarl\\nSèdjro de Ouanho\\nSanite Anne\\ndu Cinquantenaire Adjakahoué", "IP": "SD", "Co1": "AP", "Co2": "", "Co3": "", "Reserve": "FS", "Observation": "Fin de mois"}, {"Mois": "AOUT", "Semaine": "S35", "Periode": "24/08-28/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "4", "Structures": "Miracle de Tanzoun\\nDJIDJOHO\\nKAYOSSI\\nIFEDE ROUTE DE KETONOU", "IP": "UA", "Co1": "ED", "Co2": "", "Co3": "", "Reserve": "TA", "Observation": "Clôture mois"}, {"Mois": "AOUT", "Semaine": "S35", "Periode": "24/08-28/08", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "4", "Structures": "NOUVELLE PHARMACIE DONA DEÏ\\nPHARMACIE LOUHO\\nAdjarra Docodji UPAO\\nVêkpa", "IP": "YM", "Co1": "AT", "Co2": "", "Co3": "", "Reserve": "", "Observation": "GR Août"}, {"Mois": "SEPTEMBRE", "Semaine": "S36", "Periode": "31/08-04/09", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Nord officines clôturées"}, {"Mois": "SEPTEMBRE", "Semaine": "S36", "Periode": "31/08-04/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Adjibade Sarl\\nAdouni\\nAgata Grace Divine\\nAgblangandan\\nAgbokou\\n", "IP": "CS", "Co1": "FS", "Co2": "", "Co3": "", "Reserve": "IG", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S36", "Periode": "31/08-04/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Badirou de Tchinvié\\nBoladji\\nCarrefour Gbodjè\\nCatchi\\nCentrale d’Adjarra", "IP": "JA", "Co1": "EL", "Co2": "", "Co3": "", "Reserve": "UA", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S37", "Periode": "07/09-11/09", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "DON", "Volume": "4", "Structures": "Ouaké\\nZama Bani\\nCOPARGO\\nCLEMENT", "IP": "PL", "Co1": "SH", "Co2": "", "Co3": "", "Reserve": "GN", "Observation": "Rotation Nord"}, {"Mois": "SEPTEMBRE", "Semaine": "S37", "Periode": "07/09-11/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Centrale Kokoyè\\nCristal Dodji\\nDe la Vallée de l’Ouémé\\nHounsa Rehoboth\\nDjeffa", "IP": "AD", "Co1": "IA", "Co2": "", "Co3": "", "Reserve": "YM", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S37", "Periode": "07/09-11/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Djegan Kpevi\\nDona - Déï\\nDona (Porto - Novo)\\nDowa\\nDowa Gbago Tabita", "IP": "ED", "Co1": "JV", "Co2": "", "Co3": "", "Reserve": "JH", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S37", "Periode": "07/09-12/09", "Zone": "Extérieur", "Type_Inspection": "BPF extérieure", "Sous_Type": "Chine", "Departement": "EXT", "Volume": "1", "Structures": "", "IP": "", "Co1": "FA", "Co2": "", "Co3": "", "Reserve": "AP", "Observation": "Fixe imposée"}, {"Mois": "SEPTEMBRE", "Semaine": "S38", "Periode": "14/09-18/09", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR(01)/ATA", "Volume": "4", "Structures": "Du Plateau\\nEden d\'Ourbouga\\nCité des Bangana\\nDE L\'ATACORA\\n", "IP": "SB", "Co1": "GN", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "Rotation Nord"}, {"Mois": "SEPTEMBRE", "Semaine": "S38", "Periode": "14/09-18/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "OUE", "Volume": "5", "Structures": "Du Boulevard Djassin\\nEkpè\\nFontaine de Jouvence\\nGrande Pharmacie Krake\\nKoutongbé (Ex National)", "IP": "GH", "Co1": "SD", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S38", "Periode": "14/09-18/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COU", "Volume": "4", "Structures": "Gloria Déi de Dogbo Sarl\\nLe Fleuron\\nNouvelle Pharmacie Grace Divine\\nLalo Hlassame", "IP": "JA", "Co1": "IG", "Co2": "", "Co3": "", "Reserve": "CS", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S38", "Periode": "14/09-18/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "MON", "Volume": "4", "Structures": "Sainte Croix (Comè)\\nHôtel de Ville\\nZOUNGBONOU\\nLe Bon Samaritain", "IP": "EK", "Co1": "AP", "Co2": "", "Co3": "", "Reserve": "TA", "Observation": ""}, {"Mois": "SEPTEMBRE", "Semaine": "S39", "Periode": "21/09-25/09", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COL(1)/DON", "Volume": "4", "Structures": "Bantè\\nNouvelle Pharmacie Madina\\nSafari (Bassila)\\nTaifa", "IP": "CA", "Co1": "SH", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S39", "Periode": "21/09-25/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "MON(2)/COU", "Volume": "4", "Structures": "La Nériad\\nSainte Marie Reine\\nRehoboth - P\\nDU CARREFOUR TOVIKLIN", "IP": "MO", "Co1": "YM", "Co2": "", "Co3": "", "Reserve": "EL", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S39", "Periode": "21/09-25/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COU", "Volume": "4", "Structures": "Wezon Aplahoué\\nSaint Marcel (Azovè)\\nSainte Carine\\nSainte Véronique de Djakotomey", "IP": "FS", "Co1": "", "Co2": "", "Co3": "", "Reserve": "AD", "Observation": "Routine Sud"}, {"Mois": "SEPTEMBRE", "Semaine": "S39", "Periode": "22/09-25/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Dèkoungbé\\nDéo Gratias Godomey\\nDu Campus UAC Sarl\\nDu Château d’eau\\nDu Lac", "IP": "PH", "Co1": "ED", "Co2": "", "Co3": "", "Reserve": "", "Observation": ""}, {"Mois": "SEPTEMBRE", "Semaine": "S39", "Periode": "21/09-25/09", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "MON", "Volume": "4", "Structures": "Le Carrefour de Grand-Popo\\nNouvelle Pharmacie  Zogbédji\\nPrincipale de Sè\\nSahouè", "IP": "UA", "Co1": "TA", "Co2": "", "Co3": "", "Reserve": "", "Observation": ""}, {"Mois": "OCTOBRE", "Semaine": "S40", "Periode": "28/09-02/10", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Rotation Nord PUI"}, {"Mois": "OCTOBRE", "Semaine": "S40", "Periode": "28/09-02/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "MON", "Volume": "4", "Structures": "DIVINE MISÉRICORDE DE AKODEHA\\nGrande Pharmacie de Comè Sarl \\nEyram\\nHillacondji Don de Dieu (Ex Notre Dame du perpétuel secours)", "IP": "JH", "Co1": "EL", "Co2": "", "Co3": "", "Reserve": "JA", "Observation": "Routine Sud"}, {"Mois": "OCTOBRE", "Semaine": "S40", "Periode": "28/09-02/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT(3)/ATL", "Volume": "5", "Structures": "PHARMACIE SAINT RAPHAEL\\nPHARMACIE OKPE OLUWA\\nPHARMACIE MATHYS\\nJACK & CIE\\nAITCHEDJI SEMINAIRE", "IP": "AT", "Co1": "OW", "Co2": "", "Co3": "", "Reserve": "IG", "Observation": "Routine Sud"}, {"Mois": "OCTOBRE", "Semaine": "S41", "Periode": "05/10-09/10", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COL", "Volume": "4", "Structures": "Agbado\\nCLEMENT DE TCHETTI\\nDassa Carrefour\\nDe la Savane", "IP": "GN", "Co1": "JY", "Co2": "", "Co3": "", "Reserve": "PL", "Observation": "Rotation Nord"}, {"Mois": "OCTOBRE", "Semaine": "S41", "Periode": "05/10-09/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "PLA", "Volume": "4", "Structures": "Achimi\\nEnoryves\\nAdja-Ouèrè\\nLa Frontière (Igolo)", "IP": "GH", "Co1": "EK", "Co2": "", "Co3": "", "Reserve": "JV", "Observation": "Routine Sud"}, {"Mois": "OCTOBRE", "Semaine": "S41", "Periode": "05/10-09/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "PLA", "Volume": "4", "Structures": "La Grâce Divine Pobè\\nOlabissi\\nPrincipale de Kétou\\nCarrefour Y de Igolo\\n", "IP": "CS", "Co1": "IA", "Co2": "", "Co3": "", "Reserve": "AP", "Observation": "Routine Sud"}, {"Mois": "OCTOBRE", "Semaine": "S42", "Periode": "12/10-16/10", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COL", "Volume": "4", "Structures": "Notre Dame d\'Arigbo\\nPharmacie Le Paraclet\\nDes Collines\\nIreti", "IP": "CA", "Co1": "PL", "Co2": "", "Co3": "", "Reserve": "SH", "Observation": "AT en congé dès 12/10"}, {"Mois": "OCTOBRE", "Semaine": "S42", "Periode": "12/10-16/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ZOU", "Volume": "4", "Structures": "Ave Maria Carrefour Zakpo\\nAzally II\\nAzonnigbo\\nEtoile de Kpokon", "IP": "YM", "Co1": "JA", "Co2": "", "Co3": "", "Reserve": "JH", "Observation": "Routine Sud"}, {"Mois": "OCTOBRE", "Semaine": "S42", "Periode": "12/10-16/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ZOU", "Volume": "4", "Structures": "Du Marché Abomey\\nHouéfa de Sodohoué\\nLayo de Covè\\nMidokpo", "IP": "AD", "Co1": "FS", "Co2": "", "Co3": "", "Reserve": "SD", "Observation": "Routine Sud"}, {"Mois": "OCTOBRE", "Semaine": "S42", "Periode": "12/10-16/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ZOU", "Volume": "4", "Structures": "Nontinmin\\nNouvelle Pharmacie Goho\\nPéniel de Djidja\\nPharmcie Saint Edmond d\'Agbangnizoun\\n", "IP": "TA", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": ""}, {"Mois": "OCTOBRE", "Semaine": "S43", "Periode": "19/10-23/10", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COL", "Volume": "4", "Structures": "Ouesse centre\\nPharmacie ABE DU MARCHE DE SAVE\\nLafia Sarl\\nOluwa Tobi Kilibo", "IP": "SB", "Co1": "SH", "Co2": "", "Co3": "", "Reserve": "GN", "Observation": "Clôture Nord Octobre"}, {"Mois": "OCTOBRE", "Semaine": "S43", "Periode": "19/10-23/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ZOU", "Volume": "4", "Structures": "PHARMACIE PRIELLE DE TINDJI\\nZakpota\\nSaint Henri\\nSaint Luc de Djimè", "IP": "IG", "Co1": "JH", "Co2": "", "Co3": "", "Reserve": "UA", "Observation": "Fin de mois renforcée"}, {"Mois": "OCTOBRE", "Semaine": "S43", "Periode": "19/10-23/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ZOU", "Volume": "4", "Structures": "Sainte Face\\nPHARMACIE SHALOM\\nRoyale d\'Abomey\\nZogbodomey", "IP": "JV", "Co1": "IA", "Co2": "RB", "Co3": "", "Reserve": "FA", "Observation": "Clôture PUI Octobre"}, {"Mois": "OCTOBRE", "Semaine": "S44", "Periode": "26/10-30/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ATL", "Volume": "5", "Structures": "Centrale de Houègbo\\nLYCEE TECHNIQUE D\'AKASSATO\\nLE FIGUIER\\nPharmacie OASIS\\nCENTRALE DE KPOMASSE", "IP": "PH", "Co1": "AP", "Co2": "", "Co3": "", "Reserve": "ED", "Observation": ""}, {"Mois": "OCTOBRE", "Semaine": "S44", "Periode": "26/10-30/10", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Distributeurs en gros", "Departement": "LIT", "Volume": "2", "Structures": "ABMS \\nCentrale d\'approvisionnement des formations sanitaires catholiques (CAFSC)", "IP": "FS", "Co1": "YM", "Co2": "", "Co3": "", "Reserve": "AD", "Observation": ""}, {"Mois": "NOVEMBRE", "Semaine": "S45", "Periode": "02/11-06/11", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "COL", "Volume": "4", "Structures": "Principale Glazoué\\nPriorité Santé (Paouignan)\\nASOVIC DE GOUKA\\nPHARMACIE DONAN DE SAVALOU", "IP": "CA", "Co1": "PL", "Co2": "", "Co3": "", "Reserve": "", "Observation": "JY en congé dès 02/11"}, {"Mois": "NOVEMBRE", "Semaine": "S45", "Periode": "02/11-06/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "ZOU", "Volume": "5", "Structures": "PHARMACIE PÔLE SANTE\\nWahouédon\\nSAINTE VALENTINE\\nDES MUSEES D\'ABOMEY\\nCŒUR D\'OR", "IP": "JA", "Co1": "UA", "Co2": "RB", "Co3": "", "Reserve": "ED", "Observation": "Routine Sud"}, {"Mois": "NOVEMBRE", "Semaine": "S45", "Periode": "02/11-06/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "5", "Structures": "PH MADONE\\nTANTOT LE JOKER\\nPH MARISTES\\nPHARMACIE VIE SACRE AGBATO\\nPH MIDOMBO", "IP": "EK", "Co1": "EL", "Co2": "", "Co3": "", "Reserve": "IG", "Observation": "Routine Sud"}, {"Mois": "NOVEMBRE", "Semaine": "S46", "Periode": "09/11-13/11", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "BOR", "Volume": "4", "Structures": "\\nGorobani\\nLa guérison fin goudron Boni Yayi\\nALAFIA PLUS\\nTIBONA", "IP": "SB", "Co1": "GN", "Co2": "", "Co3": "", "Reserve": "PL", "Observation": "Démarrage Nord Avril ; PL congé dès 03/04, charge limitée"}, {"Mois": "NOVEMBRE", "Semaine": "S46", "Periode": "09/11-13/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "PUI", "Departement": "LIT", "Volume": "5", "Structures": "Cnhu\\nHopital St Jean\\nHopital St Luc\\nPH HAIE VIVE\\nCHUZ SURU-LERE\\n", "IP": "IG", "Co1": "AT", "Co2": "", "Co3": "", "Reserve": "AD", "Observation": "Routine Sud"}, {"Mois": "NOVEMBRE", "Semaine": "S46", "Periode": "09/11-13/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "LIT", "Volume": "0", "Structures": "\\n", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "CS", "Observation": "Routine Sud"}, {"Mois": "NOVEMBRE", "Semaine": "S47", "Periode": "16/11-20/11", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Rotation Nord"}, {"Mois": "NOVEMBRE", "Semaine": "S47", "Periode": "16/11-20/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "GH", "Observation": "Routine Sud"}, {"Mois": "NOVEMBRE", "Semaine": "S47", "Periode": "16/11-20/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "ED", "Observation": "Routine Sud"}, {"Mois": "NOVEMBRE", "Semaine": "S48", "Periode": "23/11-27/11", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "GN en congé dès 27/11"}, {"Mois": "NOVEMBRE", "Semaine": "S48", "Periode": "23/11-27/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "", "Observation": "Fin de mois renforcée"}, {"Mois": "NOVEMBRE", "Semaine": "S48", "Periode": "23/11-27/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "YM", "Observation": "Clôture PUI"}, {"Mois": "NOVEMBRE", "Semaine": "S48", "Periode": "23/11-27/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "MO", "Observation": ""}, {"Mois": "NOVEMBRE", "Semaine": "S48", "Periode": "23/11-27/11", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "0", "Structures": "", "IP": "", "Co1": "", "Co2": "", "Co3": "", "Reserve": "IA", "Observation": "GV Novembre"}, {"Mois": "DECEMBRE", "Semaine": "S49", "Periode": "30/11-04/12", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "CA", "Observation": "Clôture Nord progressive"}, {"Mois": "DECEMBRE", "Semaine": "S49", "Periode": "30/11-04/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "SD", "Observation": "Routine Sud"}, {"Mois": "DECEMBRE", "Semaine": "S49", "Periode": "30/11-04/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "GH", "Observation": "Routine Sud"}, {"Mois": "DECEMBRE", "Semaine": "S50", "Periode": "07/12-11/12", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "PL", "Observation": "Rotation Nord"}, {"Mois": "DECEMBRE", "Semaine": "S50", "Periode": "07/12-11/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "YM", "Observation": "SH indispo dès 10/12 (ARN)"}, {"Mois": "DECEMBRE", "Semaine": "S50", "Periode": "07/12-11/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "MO", "Observation": "Routine Sud"}, {"Mois": "DECEMBRE", "Semaine": "S51", "Periode": "14/12-18/12", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "GN dispo jusqu’au 26/11 ; ici remplacé si besoin"}, {"Mois": "DECEMBRE", "Semaine": "S51", "Periode": "14/12-18/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "GH", "Observation": "Plusieurs congés à venir fin décembre"}, {"Mois": "DECEMBRE", "Semaine": "S51", "Periode": "14/12-18/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "CS", "Observation": "Plusieurs congés à venir fin décembre"}, {"Mois": "DECEMBRE", "Semaine": "S52", "Periode": "21/12-25/12", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "CA", "Observation": "Congés massifs fin décembre, charge réduite"}, {"Mois": "DECEMBRE", "Semaine": "S52", "Periode": "21/12-25/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "AT", "Observation": "Congés massifs fin décembre, charge réduite"}, {"Mois": "DECEMBRE", "Semaine": "S52", "Periode": "21/12-25/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "JA", "Observation": "Pas de PUI cette semaine"}, {"Mois": "DECEMBRE", "Semaine": "S52", "Periode": "21/12-25/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "JH", "Observation": "Pas de PUI cette semaine"}, {"Mois": "DECEMBRE", "Semaine": "S53", "Periode": "28/12-31/12", "Zone": "Nord", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "JY", "Observation": "Clôture annuelle, congés ARN/SIEF"}, {"Mois": "DECEMBRE", "Semaine": "S53", "Periode": "28/12-31/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "AT", "Observation": "Équipe minimale de clôture"}, {"Mois": "DECEMBRE", "Semaine": "S53", "Periode": "28/12-31/12", "Zone": "Sud", "Type_Inspection": "Réglementaire", "Sous_Type": "Officines", "Departement": "", "Volume": "-", "Structures": "", "IP": "-", "Co1": "-", "Co2": "", "Co3": "", "Reserve": "MO", "Observation": ""}]'
CONGES_JSON    = '[{"Mois": "AVRIL", "Initiale": "PL", "Nom_Complet": "Lokoun Fifamè Pulchérie Ella", "Date_Debut": "04/03/2026", "Date_Fin": "04/09/2026", "Duree": "5 jours ouvrés", "Zone_Impact": "ARN / Nord", "Observation": "Indisponible début avril"}, {"Mois": "AVRIL", "Initiale": "GH", "Nom_Complet": "Houndrode Ghisèle Amavi", "Date_Debut": "17/04/2026", "Date_Fin": "05/04/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Impact 2e moitié avril et chevauchement début mai"}, {"Mois": "AVRIL", "Initiale": "AP", "Nom_Complet": "Pokou Aurelle", "Date_Debut": "17/04/2026", "Date_Fin": "05/04/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Impact 2e moitié avril et chevauchement début mai"}, {"Mois": "MAI", "Initiale": "CS", "Nom_Complet": "Segnon Aymone Corinne", "Date_Debut": "05/04/2026", "Date_Fin": "21/05/2026", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud", "Observation": "CRITIQUE : incompatible avec mission exceptionnelle Sud 11–15 mai si maintenue"}, {"Mois": "MAI", "Initiale": "YM", "Nom_Complet": "Madohonan Mawugnon Yasmine", "Date_Debut": "05/11/2026", "Date_Fin": "15/05/2026", "Duree": "5 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-mai"}, {"Mois": "MAI", "Initiale": "UA", "Nom_Complet": "Agossa Ulrich", "Date_Debut": "13/05/2026", "Date_Fin": "26/05/2026", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-mai"}, {"Mois": "MAI", "Initiale": "JA", "Nom_Complet": "Ahoga Josias", "Date_Debut": "15/05/2026", "Date_Fin": "25/05/2026", "Duree": "7 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-mai"}, {"Mois": "MAI", "Initiale": "FS", "Nom_Complet": "Saroukou Farouk Ayindé Antonio", "Date_Debut": "15/05/2026", "Date_Fin": "27/05/2026", "Duree": "9 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-mai"}, {"Mois": "MAI", "Initiale": "PL", "Nom_Complet": "Lokoun Fifamè Pulchérie Ella", "Date_Debut": "18/05/2026", "Date_Fin": "25/05/2026", "Duree": "6 jours ouvrés", "Zone_Impact": "ARN / Nord", "Observation": "Indisponible ARN fin mai"}, {"Mois": "MAI", "Initiale": "IG", "Nom_Complet": "Ganhou Iréné Sènankpon", "Date_Debut": "19/05/2026", "Date_Fin": "25/05/2026", "Duree": "5 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible fin mai"}, {"Mois": "JUIN", "Initiale": "OW", "Nom_Complet": "Whannou de Dravo Kpèdétin Olivia Jute Linda", "Date_Debut": "06/01/2026", "Date_Fin": "18/06/2026", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "NOUVEAU : 1ère partie ajoutée selon précision utilisateur"}, {"Mois": "JUIN", "Initiale": "FA", "Nom_Complet": "Agbo-Ola Adétola Omolara Florisse", "Date_Debut": "06/08/2026", "Date_Fin": "19/06/2026", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Attention à l’appui SIEF en juin"}, {"Mois": "JUILLET", "Initiale": "CY", "Nom_Complet": "Yemoa Charlemagne", "Date_Debut": "07/01/2026", "Date_Fin": "20/07/2026", "Duree": "20 jours calendaires", "Zone_Impact": "Nord uniquement", "Observation": "Ressource Nord indisponible"}, {"Mois": "JUILLET", "Initiale": "JH", "Nom_Complet": "Houngbedji Codjo Joël Onésime", "Date_Debut": "13/07/2026", "Date_Fin": "28/07/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-juillet"}, {"Mois": "JUILLET", "Initiale": "SB", "Nom_Complet": "Bognon Y. Saturnin", "Date_Debut": "13/07/2026", "Date_Fin": "28/07/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "ARN / Nord", "Observation": "Impact ARN mi-juillet"}, {"Mois": "JUILLET", "Initiale": "JV", "Nom_Complet": "Vigan Jean-Paul", "Date_Debut": "15/07/2026", "Date_Fin": "08/03/2026", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement début août"}, {"Mois": "JUILLET", "Initiale": "TA", "Nom_Complet": "Atcheffon Tanguy", "Date_Debut": "27/07/2026", "Date_Fin": "08/11/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement août"}, {"Mois": "AOUT", "Initiale": "PH", "Nom_Complet": "Hade Paterne Déo-Gratias", "Date_Debut": "17/08/2026", "Date_Fin": "09/08/2026", "Duree": "15 jours ouvrés", "Zone_Impact": "Sud", "Observation": "CRITIQUE : senior clé indisponible"}, {"Mois": "AOUT", "Initiale": "ED", "Nom_Complet": "Dagan Midokpè Elodie", "Date_Debut": "08/03/2026", "Date_Fin": "18/08/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible début août"}, {"Mois": "AOUT", "Initiale": "YM", "Nom_Complet": "Madohonan Mawugnon Yasmine", "Date_Debut": "08/03/2026", "Date_Fin": "14/08/2026", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible début août"}, {"Mois": "AOUT", "Initiale": "IA", "Nom_Complet": "Aholoukpe Léonelle Immaculée", "Date_Debut": "08/10/2026", "Date_Fin": "25/08/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-août"}, {"Mois": "AOUT", "Initiale": "JA", "Nom_Complet": "Ahoga Josias", "Date_Debut": "14/08/2026", "Date_Fin": "27/08/2026", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-août"}, {"Mois": "AOUT", "Initiale": "EK", "Nom_Complet": "Kokoye Eole Armanda Luxio", "Date_Debut": "26/08/2026", "Date_Fin": "09/08/2026", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement septembre"}, {"Mois": "OCTOBRE", "Initiale": "AT", "Nom_Complet": "Tamou Sambo Simè Abdias", "Date_Debut": "10/12/2026", "Date_Fin": "29/10/2026", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible mi-octobre"}, {"Mois": "NOVEMBRE", "Initiale": "JY", "Nom_Complet": "Yacoubou Jean", "Date_Debut": "11/02/2026", "Date_Fin": "12/03/2026", "Duree": "24 jours ouvrés", "Zone_Impact": "Nord uniquement", "Observation": "CRITIQUE : ressource Nord indisponible"}, {"Mois": "NOVEMBRE", "Initiale": "GN", "Nom_Complet": "Natonnagnon Geraud", "Date_Debut": "27/11/2026", "Date_Fin": "31/12/2026", "Duree": "Fin d’année", "Zone_Impact": "ARN / Nord", "Observation": "Indisponible fin novembre à décembre"}, {"Mois": "DECEMBRE", "Initiale": "SH", "Nom_Complet": "Houssou Monssèdé Stéphanie", "Date_Debut": "12/10/2026", "Date_Fin": "15/01/2027", "Duree": "Période chevauchante", "Zone_Impact": "ARN / Nord", "Observation": "Indisponible mi-décembre à mi-janvier"}, {"Mois": "DECEMBRE", "Initiale": "IG", "Nom_Complet": "Ganhou Iréné Sènankpon", "Date_Debut": "15/12/2026", "Date_Fin": "31/12/2026", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible fin d’année"}, {"Mois": "DECEMBRE", "Initiale": "JV", "Nom_Complet": "Vigan Jean-Paul", "Date_Debut": "18/12/2026", "Date_Fin": "31/12/2026", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Indisponible fin d’année"}, {"Mois": "DECEMBRE", "Initiale": "PL", "Nom_Complet": "Lokoun Fifamè Pulchérie Ella", "Date_Debut": "18/12/2026", "Date_Fin": "31/12/2026", "Duree": "12 jours ouvrés", "Zone_Impact": "ARN / Nord", "Observation": "Indisponible fin d’année"}, {"Mois": "DECEMBRE", "Initiale": "SD", "Nom_Complet": "Dazoundo Tagnon Cyrille Steeve", "Date_Debut": "18/12/2026", "Date_Fin": "01/06/2027", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "PH", "Nom_Complet": "Hade Paterne Déo-Gratias", "Date_Debut": "21/12/2026", "Date_Fin": "01/08/2027", "Duree": "15 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "UA", "Nom_Complet": "Agossa Ulrich", "Date_Debut": "21/12/2026", "Date_Fin": "01/07/2027", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "IA", "Nom_Complet": "Aholoukpe Léonelle Immaculée", "Date_Debut": "21/12/2026", "Date_Fin": "01/01/2027", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "YM", "Nom_Complet": "Madohonan Mawugnon Yasmine", "Date_Debut": "21/12/2026", "Date_Fin": "01/01/2027", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "SB", "Nom_Complet": "Bognon Y. Saturnin", "Date_Debut": "21/12/2026", "Date_Fin": "01/06/2027", "Duree": "12 jours ouvrés", "Zone_Impact": "ARN / Nord", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "OW", "Nom_Complet": "Whannou de Dravo Kpèdétin Olivia Jute Linda", "Date_Debut": "24/12/2026", "Date_Fin": "26/01/2027", "Duree": "23 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "MIS À JOUR : 2ème partie corrigée selon précision utilisateur"}, {"Mois": "DECEMBRE", "Initiale": "FA", "Nom_Complet": "Agbo-Ola Adétola Omolara Florisse", "Date_Debut": "23/12/2026", "Date_Fin": "13/01/2027", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "EL", "Nom_Complet": "Lokossou Euned Déo-Gracias", "Date_Debut": "23/12/2026", "Date_Fin": "13/01/2027", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "ED", "Nom_Complet": "Dagan Midokpè Elodie", "Date_Debut": "24/12/2026", "Date_Fin": "01/08/2027", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "AP", "Nom_Complet": "Pokou Aurelle", "Date_Debut": "24/12/2026", "Date_Fin": "01/08/2027", "Duree": "12 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "EK", "Nom_Complet": "Kokoye Eole Armanda Luxio", "Date_Debut": "24/12/2026", "Date_Fin": "14/01/2027", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "JA", "Nom_Complet": "Ahoga Josias", "Date_Debut": "28/12/2026", "Date_Fin": "01/05/2027", "Duree": "7 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "CS", "Nom_Complet": "Segnon Aymone Corinne", "Date_Debut": "28/12/2026", "Date_Fin": "01/08/2027", "Duree": "10 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "TA", "Nom_Complet": "Atcheffon Tanguy", "Date_Debut": "28/12/2026", "Date_Fin": "14/01/2027", "Duree": "14 jours ouvrés", "Zone_Impact": "Sud / SIEF", "Observation": "Chevauchement janvier"}, {"Mois": "DECEMBRE", "Initiale": "CA", "Nom_Complet": "Ahouandjinou Corneille", "Date_Debut": "28/12/2026", "Date_Fin": "31/01/2027", "Duree": "Fin janvier 2027", "Zone_Impact": "ARN / Nord", "Observation": "Chevauchement long"}, {"Mois": "DECEMBRE", "Initiale": "AD", "Nom_Complet": "Dassi Bidossessi Aimé", "Date_Debut": "31/12/2026", "Date_Fin": "02/02/2027", "Duree": "24 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Démarrage fin d’année"}, {"Mois": "DECEMBRE", "Initiale": "FS", "Nom_Complet": "Saroukou Farouk Ayindé Antonio", "Date_Debut": "28/12/2026", "Date_Fin": "01/06/2027", "Duree": "7 jours ouvrés", "Zone_Impact": "Sud", "Observation": ""}, {"Mois": "DECEMBRE", "Initiale": "MO", "Nom_Complet": "Olafa Omotayo Mouyinath", "Date_Debut": "31/12/2026", "Date_Fin": "02/02/2027", "Duree": "24 jours ouvrés", "Zone_Impact": "Sud", "Observation": "Démarrage fin d’année"}]'
CONTROLES_JSON = '[{"Mois": "AVRIL", "Semaine": "S15", "Periode": "06/04-10/04", "Equipe": ["GN"]}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "07/04-09/04", "Equipe": ["IA"]}, {"Mois": "AVRIL", "Semaine": "S15", "Periode": "07/04-10/04", "Equipe": ["JV"]}, {"Mois": "AVRIL", "Semaine": "S16", "Periode": "13/04-17/04", "Equipe": ["AT", "IG"]}, {"Mois": "AVRIL", "Semaine": "S17", "Periode": "20/04-24/04", "Equipe": ["FA", "FS", "PL"]}, {"Mois": "AVRIL", "Semaine": "S18", "Periode": "27/04-01/05", "Equipe": ["IA", "SH", "UA"]}, {"Mois": "MAI", "Semaine": "S19", "Periode": "04/05-04/05", "Equipe": ["SH"]}, {"Mois": "MAI", "Semaine": "S19", "Periode": "04/05-08/05", "Equipe": ["FS", "UA"]}, {"Mois": "MAI", "Semaine": "S20", "Periode": "11/05-15/05", "Equipe": ["AT", "IG", "JY"]}, {"Mois": "MAI", "Semaine": "S21", "Periode": "18/05-22/05", "Equipe": ["AD", "CA", "GH"]}, {"Mois": "MAI", "Semaine": "S22", "Periode": "25/05-29/05", "Equipe": ["JV", "SD"]}, {"Mois": "JUIN", "Semaine": "S23", "Periode": "01/06-05/06", "Equipe": ["AD", "IA", "SH"]}, {"Mois": "JUIN", "Semaine": "S24", "Periode": "08/06-12/06", "Equipe": ["CS", "IA", "JY"]}, {"Mois": "JUIN", "Semaine": "S25", "Periode": "15/06-19/06", "Equipe": ["JH", "JV"]}, {"Mois": "JUIN", "Semaine": "S26", "Periode": "22/06-26/06", "Equipe": ["AT", "CS", "SH"]}, {"Mois": "JUIN", "Semaine": "S27", "Periode": "29/06-03/07", "Equipe": ["CA", "GH", "JV"]}, {"Mois": "JUILLET", "Semaine": "S28", "Periode": "06/07-10/07", "Equipe": ["JV", "YM"]}, {"Mois": "JUILLET", "Semaine": "nan", "Periode": "nan", "Equipe": ["GH"]}, {"Mois": "JUILLET", "Semaine": "S29", "Periode": "13/07-17/07", "Equipe": ["AP", "GN", "MO"]}, {"Mois": "JUILLET", "Semaine": "S30", "Periode": "20/07-24/07", "Equipe": ["AD", "IA", "PL"]}, {"Mois": "JUILLET", "Semaine": "S31", "Periode": "27/07-31/07", "Equipe": ["CA", "JA", "JH"]}, {"Mois": "AOUT", "Semaine": "S32", "Periode": "03/08-07/08", "Equipe": ["CS", "JV"]}, {"Mois": "AOUT", "Semaine": "S33", "Periode": "10/08-14/08", "Equipe": ["FS", "GN", "IG"]}, {"Mois": "AOUT", "Semaine": "S34", "Periode": "17/08-21/08", "Equipe": ["EK", "JY", "YM"]}, {"Mois": "AOUT", "Semaine": "S35", "Periode": "24/08-28/08", "Equipe": ["FS", "GN", "TA"]}, {"Mois": "SEPTEMBRE", "Semaine": "S36", "Periode": "31/08-04/09", "Equipe": ["IG", "UA"]}, {"Mois": "SEPTEMBRE", "Semaine": "S37", "Periode": "07/09-11/09", "Equipe": ["GN", "JH", "YM"]}, {"Mois": "SEPTEMBRE", "Semaine": "S37", "Periode": "07/09-12/09", "Equipe": ["AP"]}, {"Mois": "SEPTEMBRE", "Semaine": "S38", "Periode": "14/09-18/09", "Equipe": ["CS", "JY", "TA"]}, {"Mois": "SEPTEMBRE", "Semaine": "S39", "Periode": "21/09-25/09", "Equipe": ["AD", "EL", "JY"]}, {"Mois": "OCTOBRE", "Semaine": "S40", "Periode": "28/09-02/10", "Equipe": ["IG", "JA"]}, {"Mois": "OCTOBRE", "Semaine": "S41", "Periode": "05/10-09/10", "Equipe": ["AP", "JV", "PL"]}, {"Mois": "OCTOBRE", "Semaine": "S42", "Periode": "12/10-16/10", "Equipe": ["JH", "SD", "SH"]}, {"Mois": "OCTOBRE", "Semaine": "S43", "Periode": "19/10-23/10", "Equipe": ["FA", "GN", "UA"]}, {"Mois": "OCTOBRE", "Semaine": "S44", "Periode": "26/10-30/10", "Equipe": ["AD", "ED"]}, {"Mois": "NOVEMBRE", "Semaine": "S45", "Periode": "02/11-06/11", "Equipe": ["ED", "IG"]}, {"Mois": "NOVEMBRE", "Semaine": "S46", "Periode": "09/11-13/11", "Equipe": ["AD", "CS", "PL"]}, {"Mois": "NOVEMBRE", "Semaine": "S47", "Periode": "16/11-20/11", "Equipe": ["ED", "GH"]}, {"Mois": "NOVEMBRE", "Semaine": "S48", "Periode": "23/11-27/11", "Equipe": ["IA", "MO", "YM"]}, {"Mois": "DECEMBRE", "Semaine": "S49", "Periode": "30/11-04/12", "Equipe": ["CA", "GH", "SD"]}, {"Mois": "DECEMBRE", "Semaine": "S50", "Periode": "07/12-11/12", "Equipe": ["MO", "PL", "YM"]}, {"Mois": "DECEMBRE", "Semaine": "S51", "Periode": "14/12-18/12", "Equipe": ["CS", "GH", "JY"]}, {"Mois": "DECEMBRE", "Semaine": "S52", "Periode": "21/12-25/12", "Equipe": ["AT", "CA", "JA", "JH"]}, {"Mois": "DECEMBRE", "Semaine": "S53", "Periode": "28/12-31/12", "Equipe": ["AT", "JY", "MO"]}]'
NAMES_JSON     = '{"PL": "Lokoun Fifamè Pulchérie Ella", "GH": "Houndrode Ghisèle Amavi", "AP": "Pokou Aurelle", "CS": "Segnon Aymone Corinne", "YM": "Madohonan Mawugnon Yasmine", "UA": "Agossa Ulrich", "JA": "Ahoga Josias", "FS": "Saroukou Farouk Ayindé Antonio", "IG": "Ganhou Iréné Sènankpon", "OW": "Whannou de Dravo Kpèdétin Olivia Jute Linda", "FA": "Agbo-Ola Adétola Omolara Florisse", "CY": "Yemoa Charlemagne", "JH": "Houngbedji Codjo Joël Onésime", "SB": "Bognon Y. Saturnin", "JV": "Vigan Jean-Paul", "TA": "Atcheffon Tanguy", "PH": "Hade Paterne Déo-Gratias", "ED": "Dagan Midokpè Elodie", "IA": "Aholoukpe Léonelle Immaculée", "EK": "Kokoye Eole Armanda Luxio", "AT": "Tamou Sambo Simè Abdias", "JY": "Yacoubou Jean", "GN": "Natonnagnon Geraud", "SH": "Houssou Monssèdé Stéphanie", "SD": "Dazoundo Tagnon Cyrille Steeve", "EL": "Lokossou Euned Déo-Gracias", "CA": "Ahouandjinou Corneille", "AD": "Dassi Bidossessi Aimé", "MO": "Olafa Omotayo Mouyinath"}'
LOGO_URI       = 'data:image/png;base64,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'

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ABMed · DIRP – Inspections 2026",
    page_icon="🏥", layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# STYLES  (inspiré DIT — palette ABMed #014955 → #026d7e)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
:root {
  --abm:#014955; --abm-l:#026d7e; --abm-xl:#03899e; --abm-bg:#e8f4f6;
  --navy:#0f172a; --navy-l:#1e293b; --white:#fff; --light:#f7fafa;
  --muted:#7c9a9e; --border:#d5e3e5;
  --danger:#dc2626; --danger-bg:#fef2f2;
  --success:#059669; --success-bg:#ecfdf5;
  --amber:#d97706; --amber-bg:#fffbeb;
  --ctrl:#92400e; --ctrl-bg:#fef3c7;
  --radius:12px;
  --shadow:0 1px 3px rgba(1,73,85,.08);
  --shadow-lg:0 12px 32px rgba(1,73,85,.12);
  --font:'Plus Jakarta Sans',system-ui,sans-serif;
}
*, html, body { font-family:var(--font) !important; }
[data-testid="stAppViewContainer"] { background:var(--light) !important; }
[data-testid="stSidebar"] > div:first-child {
    background:var(--white) !important;
    border-right:1.5px solid var(--border) !important;
    padding:0 !important;
}
[data-testid="stSidebar"] * { color:var(--navy) !important; }
[data-testid="stSidebarContent"] { padding:0 !important; }
.stRadio > label { display:none; }
.stRadio [data-baseweb="radio"] { gap:2px !important; }
div[data-testid="stVerticalBlock"] { gap:0 !important; }
.block-container { padding-top:1.5rem !important; padding-bottom:3rem !important; }
button[kind="primary"] { background:var(--abm) !important; border-color:var(--abm) !important; font-family:var(--font) !important; }
button[kind="primary"]:hover { background:var(--abm-l) !important; }
div[data-testid="stTextInput"] input { border-radius:10px !important; border:1.5px solid var(--border) !important; font-family:var(--font) !important; }
div[data-testid="stSelectbox"] > div { border-radius:10px !important; }

/* ── Sidebar brand ── */
.sb-brand {
    padding:20px 18px; border-bottom:1px solid var(--border);
    display:flex; align-items:center; gap:12px;
}
.sb-brand-text h1 { font-size:13px; font-weight:700; color:var(--navy); line-height:1.2; margin:0; }
.sb-brand-text span { font-size:9px; font-weight:700; color:var(--abm); text-transform:uppercase; letter-spacing:1.5px; }

/* ── Nav items ── */
.nav-section { font-size:10px; font-weight:700; color:var(--muted);
    text-transform:uppercase; letter-spacing:1.5px; padding:16px 18px 6px; }
.nav-item {
    display:flex; align-items:center; gap:12px; padding:10px 18px;
    color:#5a7a7e; font-size:13px; font-weight:500; border-radius:8px;
    margin:1px 8px; cursor:pointer; transition:all .2s; text-decoration:none;
    border:none; background:transparent; width:calc(100% - 16px); text-align:left;
}
.nav-item:hover { color:var(--navy); background:var(--abm-bg); }
.nav-item.active { color:var(--abm) !important; background:var(--abm-bg) !important; font-weight:600; }
.nav-item svg { flex-shrink:0; width:18px; height:18px; }
.nav-badge { margin-left:auto; background:var(--danger); color:white !important;
    font-size:10px; font-weight:700; padding:2px 7px; border-radius:10px; }

/* ── Sidebar footer ── */
.sb-footer { padding:16px 18px; border-top:1px solid var(--border); }
.user-info { display:flex; align-items:center; gap:10px; }
.user-avatar { width:36px; height:36px; border-radius:50%; background:var(--abm);
    color:white !important; display:flex; align-items:center; justify-content:center;
    font-size:13px; font-weight:700; flex-shrink:0; }
.user-name { font-size:13px; font-weight:600; color:var(--navy); }
.user-role-lbl { font-size:11px; color:var(--muted); }

/* ── Hero ── */
.hero {
    background:linear-gradient(135deg,var(--abm) 0%,var(--abm-l) 50%,var(--abm-xl) 100%);
    background-size:200% 200%; border-radius:16px; padding:32px 28px;
    color:white; margin-bottom:20px; position:relative; overflow:hidden;
}
.hero::before { content:''; position:absolute; top:-60%; right:-15%;
    width:400px; height:400px;
    background:radial-gradient(circle,rgba(255,255,255,.08) 0%,transparent 70%);
    pointer-events:none; }
.hero h2 { font-size:22px; font-weight:700; margin-bottom:6px; }
.hero p  { font-size:13px; opacity:.8; max-width:500px; line-height:1.6; }
.hero-date { margin-top:10px; font-size:10px; opacity:.5;
    text-transform:uppercase; letter-spacing:1px; }

/* ── Stats grid ── */
.stats-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:20px; }
.stat-card { background:white; border-radius:var(--radius); padding:18px;
    border:1.5px solid var(--border); cursor:pointer; transition:all .25s; }
.stat-card:hover { transform:translateY(-2px); box-shadow:var(--shadow-lg); border-color:var(--abm-l); }
.stat-icon { width:36px; height:36px; border-radius:10px; display:flex;
    align-items:center; justify-content:center; margin-bottom:10px; }
.ic-abm  { background:var(--abm-bg);    color:var(--abm); }
.ic-green{ background:var(--success-bg); color:var(--success); }
.ic-amber{ background:var(--amber-bg);   color:var(--amber); }
.ic-red  { background:var(--danger-bg);  color:var(--danger); }
.ic-ctrl { background:var(--ctrl-bg);    color:var(--ctrl); }
.stat-label { font-size:10px; font-weight:600; color:var(--muted);
    text-transform:uppercase; letter-spacing:.8px; }
.stat-value { font-size:26px; font-weight:800; color:var(--navy); margin-top:2px; }

/* ── Section title ── */
.stitle { font-size:11px; font-weight:700; color:var(--muted);
    text-transform:uppercase; letter-spacing:.07em; margin:16px 0 8px;
    padding-bottom:6px; border-bottom:1px solid var(--border); }

/* ── Cards ── */
.card { background:white; border-radius:var(--radius); border:1.5px solid var(--border); overflow:hidden; margin-bottom:14px; }
.card-header { padding:14px 18px; border-bottom:1px solid var(--border);
    display:flex; align-items:center; justify-content:space-between; }
.card-header h3 { font-size:14px; font-weight:700; color:var(--navy); margin:0; }

/* ── Mission card ── */
.mc { background:white; border-radius:12px; padding:14px 16px;
    margin-bottom:8px; border-left:4px solid var(--abm);
    border:1.5px solid var(--border); border-left:4px solid var(--abm); }
.mc.ctrl { border-left-color:var(--amber); background:var(--amber-bg); }
.mc.bpf  { border-left-color:var(--success); background:var(--success-bg); }
.mc-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.mc-title { font-weight:700; font-size:13px; color:var(--navy); }
.mc-meta  { display:flex; gap:20px; font-size:12px; color:#64748b; flex-wrap:wrap; margin-bottom:6px; }
.mc-structs { font-size:11px; color:#475569; background:#f8fafc;
    border-radius:8px; padding:6px 10px; line-height:1.5; }
.mc-obs { font-size:11px; color:#94a3b8; font-style:italic; margin-top:4px; }

/* ── Tags ── */
.tag { display:inline-flex; align-items:center; gap:4px; padding:2px 9px;
    border-radius:20px; font-size:11px; font-weight:600; }
.tag-insp  { background:#dbeafe; color:#1d4ed8; }
.tag-co    { background:#ede9fe; color:#6d28d9; }
.tag-ctrl  { background:var(--ctrl-bg); color:var(--ctrl); }
.tag-bpf   { background:var(--success-bg); color:#065f46; }

/* ── Equipe chips ── */
.eq-chip { display:inline-block; background:var(--abm); color:white !important;
    border-radius:6px; padding:3px 10px; font-size:12px; font-weight:600; margin:2px; }
.eq-chip.ctrl { background:var(--amber); }
.eq-chip.vous { background:var(--success); }

/* ── Congé item ── */
.cg-item { background:var(--amber-bg); border-left:4px solid var(--amber);
    border-radius:8px; padding:8px 12px; margin-bottom:6px; font-size:13px; }

/* ── Login page ── */
.login-page { min-height:100vh; display:flex; align-items:center; justify-content:center;
    background:linear-gradient(160deg,var(--abm) 0%,#02313a 40%,#011e23 100%);
    padding:40px 24px; }
.login-brand h1 { font-size:22px; font-weight:800; color:white; line-height:1.3; margin-bottom:8px; }
.login-brand h1 span { color:#03899e; }
.login-brand p { font-size:12px; color:rgba(255,255,255,.6); line-height:1.7; }
.login-card { background:white; border-radius:16px; padding:32px 28px; box-shadow:var(--shadow-lg); }
.login-card h2 { font-size:18px; font-weight:700; color:var(--navy); margin-bottom:4px; }
.login-card p  { font-size:12px; color:var(--muted); margin-bottom:16px; }
.form-lbl { display:block; font-size:10px; font-weight:700; color:var(--navy-l);
    margin-bottom:5px; text-transform:uppercase; letter-spacing:.5px; }
.alert { padding:10px 14px; border-radius:8px; font-size:12px; margin-bottom:12px; }
.alert-err { background:var(--danger-bg); color:var(--danger); }
.alert-ok  { background:var(--success-bg); color:var(--success); }

/* ── Table ── */
.tbl { width:100%; border-collapse:collapse; font-size:12px; }
.tbl thead tr { background:var(--light); }
.tbl thead th { text-align:left; padding:8px 14px; font-size:10px; font-weight:700;
    letter-spacing:.8px; text-transform:uppercase; color:var(--muted); }
.tbl tbody tr { border-top:1px solid var(--border); transition:background .15s; }
.tbl tbody tr:hover { background:var(--abm-bg); }
.tbl tbody td { padding:10px 14px; color:var(--navy); }

/* ── Badge ── */
.bdg { display:inline-flex; align-items:center; gap:4px; padding:3px 8px;
    border-radius:20px; font-size:10px; font-weight:600; }
.bdg-dot { width:5px; height:5px; border-radius:50%; flex-shrink:0; }
.bdg-green { background:var(--success-bg); color:var(--success); }
.bdg-green .bdg-dot { background:var(--success); }
.bdg-amber { background:var(--amber-bg); color:var(--amber); }
.bdg-amber .bdg-dot { background:var(--amber); }
.bdg-abm { background:var(--abm-bg); color:var(--abm); }
.bdg-abm .bdg-dot { background:var(--abm); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load():
    insp  = pd.DataFrame(json.loads(CHARGE_JSON))
    miss  = pd.DataFrame(json.loads(MISSIONS_JSON))
    cong  = pd.DataFrame(json.loads(CONGES_JSON))
    ctrl  = pd.DataFrame(json.loads(CONTROLES_JSON))
    nms   = json.loads(NAMES_JSON)
    return insp, miss, cong, ctrl, nms

inspdf, missdf, congdf, ctrldf, NAMES = load()
VALIDES = set(inspdf["Initiale"].dropna().str.strip().str.upper())
ORDRE   = ["AVRIL","MAI","JUIN","JUILLET","AOUT","SEPTEMBRE","OCTOBRE","NOVEMBRE","DECEMBRE"]

def get_nom(init):
    return NAMES.get(init.upper(), init)

def get_charge(init):
    r = inspdf[inspdf["Initiale"].str.strip().str.upper() == init]
    return r.iloc[0] if not r.empty else None

def get_missions(init):
    rows = []
    for _, row in missdf.iterrows():
        role = None
        for col,r in [("IP","Principal"),("Co1","Co-inspecteur"),("Co2","Co-inspecteur"),("Co3","Co-inspecteur")]:
            if col in row and str(row[col]).strip().upper() == init:
                role = r; break
        if not role and "Reserve" in row and str(row["Reserve"]).strip().upper() == init:
            role = "Contrôle-poste"
        if role:
            d = row.to_dict(); d["Mon_Role"] = role; rows.append(d)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def get_controles(init):
    res = []
    for _, row in ctrldf.iterrows():
        eq = row.get("Equipe",[])
        if isinstance(eq, list) and init in eq:
            res.append(row.to_dict())
    return pd.DataFrame(res) if res else pd.DataFrame()

def get_conges(init):
    return congdf[congdf["Initiale"].str.strip().str.upper() == init].copy()

def safe_int(v):
    try: return int(float(v))
    except: return "—"

def shash(s):
    return hashlib.sha256(s.encode()).hexdigest()[:8]

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k,v in [("logged_in",False),("initiale",""),("page","dashboard"),
            ("passwords", {}), ("must_change_pw", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# Default passwords = sha256(initiale lowercase)
def check_pw(init, pw):
    stored = st.session_state.passwords.get(init)
    if stored is None:
        # Default password = initiales en minuscules
        return shash(init.lower()) == shash(pw) or pw == init.lower()
    return stored == shash(pw)

def set_pw(init, pw):
    st.session_state.passwords[init] = shash(pw)

# ══════════════════════════════════════════════════════════════════════════════
# SVG ICONS
# ══════════════════════════════════════════════════════════════════════════════
ICONS = {
"dashboard": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>''',
"calendar": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="14" x2="8" y2="14"/><line x1="12" y1="14" x2="12" y2="14"/><line x1="16" y1="14" x2="16" y2="14"/></svg>''',
"shield": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>''',
"sun": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/></svg>''',
"globe": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10A15.3 15.3 0 0112 2z"/></svg>''',
"users": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>''',
"logout": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>''',
"key": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="7.5" cy="15.5" r="5.5"/><path d="M21 2l-9.6 9.6"/><path d="M15.5 7.5l3 3L22 7l-3-3"/></svg>''',
"chart": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>''',
"warning": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>''',
}

def icon(name, size=18, color="currentColor"):
    svg = ICONS.get(name,"")
    return f'''<span style="width:{size}px;height:{size}px;display:inline-flex;align-items:center;color:{color}">{svg}</span>'''

def nav_item(label, page_key, icon_name, badge=None):
    active = st.session_state.page == page_key
    cls = "nav-item active" if active else "nav-item"
    bdg = f'<span class="nav-badge">{badge}</span>' if badge else ""
    ico = f'<span style="width:18px;height:18px;display:flex;align-items:center">{ICONS[icon_name]}</span>'
    html = f'<div class="{cls}" onclick="void(0)">{ico}<span>{label}</span>{bdg}</div>'
    st.markdown(html, unsafe_allow_html=True)
    if st.button(label, key=f"nav_{page_key}", use_container_width=True,
                 help=label, label_visibility="collapsed"):
        st.session_state.page = page_key
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def page_login():
    st.markdown('''
    <style>
    [data-testid="stAppViewContainer"] { background:linear-gradient(160deg,#014955 0%,#02313a 40%,#011e23 100%) !important; }
    .block-container { max-width:900px !important; padding-top:6rem !important; }
    </style>
    ''', unsafe_allow_html=True)

    col_brand, col_card = st.columns([1, 1.1], gap="large")

    with col_brand:
        st.markdown(f'''
        <div style="padding-top:1rem;">
            <img src="{LOGO_URI}" style="width:120px;border-radius:14px;margin-bottom:20px;background:white;padding:10px"/>
            <h1 style="font-size:24px;font-weight:800;color:white;line-height:1.3;margin-bottom:10px;">
                Plateforme de<br><span style="color:#03899e;">Programmation<br>des Inspections</span>
            </h1>
            <p style="font-size:13px;color:rgba(255,255,255,.6);line-height:1.7;">
                DIRP / Agence Béninoise du Médicament<br>
                Gestion des missions d'inspection 2026
            </p>
        </div>
        ''', unsafe_allow_html=True)

    with col_card:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h2>Connexion</h2><p>Identifiez-vous avec vos initiales et votre mot de passe.</p>', unsafe_allow_html=True)

        init_input = st.text_input("Initiales", placeholder="Ex : JA, IG, SH…",
                                   max_chars=4, label_visibility="visible").strip().upper()
        pw_input = st.text_input("Mot de passe", type="password",
                                 placeholder="Votre mot de passe",
                                 help="Par défaut : vos initiales en minuscules (ex : ja)")

        if "login_err" in st.session_state and st.session_state.login_err:
            st.markdown(f'<div class="alert alert-err">{st.session_state.login_err}</div>',
                        unsafe_allow_html=True)

        if st.button("Se connecter →", type="primary", use_container_width=True):
            if init_input not in VALIDES:
                st.session_state.login_err = "Initiales non reconnues dans le système."
                st.rerun()
            elif not check_pw(init_input, pw_input):
                st.session_state.login_err = "Mot de passe incorrect."
                st.rerun()
            else:
                st.session_state.logged_in = True
                st.session_state.initiale = init_input
                st.session_state.page = "dashboard"
                st.session_state.login_err = ""
                # Check if still using default password
                st.session_state.must_change_pw = (
                    init_input not in st.session_state.passwords
                )
                st.rerun()

        st.markdown('<div style="margin-top:12px;font-size:11px;color:#94a3b8;text-align:center;">Mot de passe par défaut : vos initiales en minuscules<br>Ex : initiales JA → mot de passe <strong>ja</strong></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar(init):
    charge = get_charge(init)
    groupe = charge["Groupe"] if charge is not None else "—"
    nom = get_nom(init)
    init_parts = init[:2]

    ctrl_count = len(get_controles(init))

    with st.sidebar:
        # Brand
        st.markdown(f'''
        <div class="sb-brand">
            <img src="{LOGO_URI}" style="width:42px;border-radius:8px;background:white;padding:4px"/>
            <div class="sb-brand-text">
                <h1>ABMed · DIRP</h1>
                <span>Inspections 2026</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)
        nav_item("Tableau de bord", "dashboard", "dashboard")

        st.markdown('<div class="nav-section">Mes missions</div>', unsafe_allow_html=True)
        nav_item("Mes inspections", "missions", "calendar")
        nav_item("Contrôles-poste", "controles", "shield",
                 badge=ctrl_count if ctrl_count > 0 else None)
        nav_item("Mes congés", "conges", "sun")

        st.markdown('<div class="nav-section">Statistiques</div>', unsafe_allow_html=True)
        nav_item("Vue globale", "globale", "globe")
        nav_item("Équipe", "equipe", "users")

        st.markdown('<div class="nav-section">Compte</div>', unsafe_allow_html=True)
        nav_item("Changer mot de passe", "password", "key")

        # Footer
        st.markdown(f'''
        <div class="sb-footer">
            <div class="user-info">
                <div class="user-avatar">{init_parts}</div>
                <div>
                    <div class="user-name">{nom[:22] + "…" if len(nom) > 22 else nom}</div>
                    <div class="user-role-lbl">Groupe {groupe}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        if st.button(f"Déconnexion", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.initiale = ""
            st.session_state.page = "dashboard"
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard(init):
    charge  = get_charge(init)
    missions = get_missions(init)
    conges  = get_conges(init)
    controles = get_controles(init)
    groupe  = charge["Groupe"] if charge is not None else "—"
    nom     = get_nom(init)
    today   = datetime.now().strftime("%A %d %B %Y").capitalize()

    # Alerte mot de passe par défaut
    if st.session_state.must_change_pw:
        st.warning(f"⚠️ Vous utilisez le mot de passe par défaut. Veuillez le changer dans **Compte → Changer mot de passe**.")

    # Hero
    st.markdown(f'''
    <div class="hero">
        <h2>Bienvenue, {nom.split()[0] if nom else init} !</h2>
        <p>Groupe <strong>{groupe}</strong> · Agence Béninoise du Médicament · DIRP</p>
        <div class="hero-date">{today}</div>
    </div>
    ''', unsafe_allow_html=True)

    # Stats
    total_m = safe_int(charge["Total"]) if charge is not None else "—"
    p_val   = safe_int(charge["P"]) if charge is not None else "—"
    co_val  = safe_int(charge["Co"]) if charge is not None else "—"
    r_val   = safe_int(charge["R"]) if charge is not None else "—"
    icr_val = f'{float(charge["ICR"]):.1f}' if charge is not None and str(charge.get("ICR","")) not in ["","nan"] else "—"

    st.markdown(f'''
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon ic-abm">{ICONS["calendar"]}</div>
            <div class="stat-label">Total missions</div>
            <div class="stat-value">{total_m}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon ic-green">{ICONS["chart"]}</div>
            <div class="stat-label">En principal</div>
            <div class="stat-value">{p_val}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon ic-abm" style="background:#ede9fe;color:#6d28d9">{ICONS["users"]}</div>
            <div class="stat-label">Co-inspecteur</div>
            <div class="stat-value">{co_val}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon ic-ctrl">{ICONS["shield"]}</div>
            <div class="stat-label">Contrôles-poste</div>
            <div class="stat-value">{r_val}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon ic-amber">{ICONS["chart"]}</div>
            <div class="stat-label">ICR</div>
            <div class="stat-value">{icr_val}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Prochaines missions
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="stitle">Mes prochaines missions</div>', unsafe_allow_html=True)
        if not missions.empty:
            df_insp = missions[missions["Mon_Role"] != "Contrôle-poste"].head(5)
            for _, row in df_insp.iterrows():
                role = row.get("Mon_Role","")
                cls = "bpf" if "BPF" in str(row.get("Type_Inspection","")).upper() else ""
                tag_cls = "tag-insp" if role=="Principal" else "tag-co"
                mois = str(row.get("Mois","")).strip()
                sem  = str(row.get("Semaine","")).strip()
                per  = str(row.get("Periode","")).strip()
                zone = str(row.get("Zone","")).strip()
                stype= str(row.get("Sous_Type","")).strip()
                st.markdown(f'''
                <div class="mc {cls}">
                    <div class="mc-head">
                        <span class="mc-title">{mois} · {sem} ({per})</span>
                        <span class="tag {tag_cls}">{role}</span>
                    </div>
                    <div class="mc-meta">
                        <span>📍 {zone}</span>
                        <span>🏷 {stype}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("Aucune mission trouvée.")

    with col2:
        st.markdown('<div class="stitle">Mes contrôles-poste</div>', unsafe_allow_html=True)
        if not controles.empty:
            for _, row in controles.iterrows():
                mois = str(row.get("Mois","")).strip()
                sem  = str(row.get("Semaine","")).strip()
                per  = str(row.get("Periode","")).strip()
                equipe = row.get("Equipe",[])
                chips = "".join([f'<span class="eq-chip {"vous" if m==init else "ctrl"}">{m}</span>' for m in equipe])
                st.markdown(f'''
                <div class="mc ctrl">
                    <div class="mc-head">
                        <span class="mc-title">{mois} · {sem}</span>
                        <span class="tag tag-ctrl">Contrôle-poste</span>
                    </div>
                    <div style="margin-top:4px;font-size:11px;color:#92400e;font-weight:500;">Équipe :</div>
                    <div>{chips}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("Aucun contrôle-poste.")

        if not conges.empty:
            st.markdown('<div class="stitle">Mes congés</div>', unsafe_allow_html=True)
            for _, row in conges.iterrows():
                mois  = str(row.get("Mois","")).strip()
                debut = str(row.get("Date_Debut","")).strip()
                fin   = str(row.get("Date_Fin","")).strip()
                duree = str(row.get("Duree","")).strip()
                st.markdown(f'''
                <div class="cg-item">
                    <strong>{mois}</strong> · {debut} → {fin}
                    <span style="color:var(--amber);font-size:11px;"> ({duree})</span>
                </div>
                ''', unsafe_allow_html=True)


def page_missions(init):
    missions = get_missions(init)
    st.markdown('<div class="stitle">Mes missions d\'inspection</div>', unsafe_allow_html=True)

    df = missions[missions["Mon_Role"] != "Contrôle-poste"].copy() if not missions.empty else pd.DataFrame()

    if df.empty:
        st.info("Aucune mission d'inspection enregistrée.")
        return

    col1,col2,col3 = st.columns(3)
    with col1:
        mois_l = ["Tous"] + [m for m in ORDRE if m in df["Mois"].str.upper().values]
        fm = st.selectbox("Mois", mois_l)
    with col2:
        fr = st.selectbox("Rôle", ["Tous"] + df["Mon_Role"].unique().tolist())
    with col3:
        zones = ["Toutes"] + df["Zone"].dropna().unique().tolist() if "Zone" in df.columns else ["Toutes"]
        fz = st.selectbox("Zone", zones)

    if fm != "Tous": df = df[df["Mois"].str.upper() == fm]
    if fr != "Tous": df = df[df["Mon_Role"] == fr]
    if fz != "Toutes": df = df[df["Zone"] == fz]

    st.caption(f"{len(df)} mission(s) affichée(s)")
    for _, row in df.iterrows():
        role  = row.get("Mon_Role","")
        mois  = str(row.get("Mois","")).strip()
        sem   = str(row.get("Semaine","")).strip()
        per   = str(row.get("Periode","")).strip()
        zone  = str(row.get("Zone","")).strip()
        stype = str(row.get("Sous_Type","")).strip()
        dept  = str(row.get("Departement","")).strip()
        vol   = str(row.get("Volume","")).strip()
        structs = str(row.get("Structures","")).replace("\\n","<br>").strip()
        obs   = str(row.get("Observation","")).strip()

        cls = "bpf" if "BPF" in str(row.get("Type_Inspection","")).upper() else ""
        tag_cls = "tag-insp" if role=="Principal" else "tag-co"
        vol_d   = vol if vol not in ["","nan","None","0.0","0"] else "—"
        dept_d  = dept if dept not in ["","nan","None"] else "—"
        str_d   = structs if structs not in ["","nan","None"] else "—"
        obs_d   = f'<div class="mc-obs">💬 {obs}</div>' if obs not in ["","nan","None"] else ""

        st.markdown(f'''
        <div class="mc {cls}">
            <div class="mc-head">
                <span class="mc-title">{mois} · {sem} ({per})</span>
                <span class="tag {tag_cls}">{role}</span>
            </div>
            <div class="mc-meta">
                <span>📍 {zone}</span>
                <span>🏷 {stype}</span>
                <span>🗺 {dept_d}</span>
                <span>🔢 {vol_d} structure(s)</span>
            </div>
            <div class="mc-structs">{str_d}</div>
            {obs_d}
        </div>
        ''', unsafe_allow_html=True)


def page_controles(init):
    controles = get_controles(init)
    st.markdown('<div class="stitle">Mes missions de contrôle-poste d\'enlèvement</div>', unsafe_allow_html=True)
    st.markdown('''
    <div style="background:#fef3c7;border:1.5px solid #fcd34d;border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#92400e;">
        <strong>ℹ️ Contrôle-poste d'enlèvement :</strong> chaque semaine, les inspecteurs en réserve forment
        l'équipe chargée de cette mission de contrôle. Votre puce apparaît en <span style="background:#059669;color:white;padding:1px 7px;border-radius:4px;font-size:11px;">vert</span>.
    </div>
    ''', unsafe_allow_html=True)

    if controles.empty:
        st.success("Aucun contrôle-poste programmé pour vous.")
        return

    for _, row in controles.iterrows():
        mois   = str(row.get("Mois","")).strip()
        sem    = str(row.get("Semaine","")).strip()
        per    = str(row.get("Periode","")).strip()
        equipe = row.get("Equipe",[])
        chips  = "".join([f'<span class="eq-chip {"vous" if m==init else "ctrl"}">{m} {" (vous)" if m==init else ""}</span>' for m in equipe])
        noms   = " · ".join([get_nom(m) for m in equipe])
        st.markdown(f'''
        <div class="mc ctrl">
            <div class="mc-head">
                <span class="mc-title">{mois} · {sem} &nbsp;({per})</span>
                <span class="tag tag-ctrl">Contrôle-poste d'enlèvement</span>
            </div>
            <div style="margin-top:8px;">
                <span style="font-size:11px;color:#92400e;font-weight:600;">Équipe complète :</span><br>
                {chips}
            </div>
            <div style="font-size:11px;color:#64748b;margin-top:4px;">{noms}</div>
        </div>
        ''', unsafe_allow_html=True)


def page_conges(init):
    conges = get_conges(init)
    st.markdown('<div class="stitle">Mes périodes de congé</div>', unsafe_allow_html=True)
    if conges.empty:
        st.success("✅ Aucun congé enregistré.")
        return
    cols = [c for c in ["Mois","Date_Debut","Date_Fin","Duree","Zone_Impact","Observation"] if c in conges.columns]
    st.dataframe(conges[cols].reset_index(drop=True), use_container_width=True)


def page_globale():
    st.markdown('<div class="stitle">Vue globale des inspections 2026</div>', unsafe_allow_html=True)
    df = missdf.copy()
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0)

    c1,c2,c3,c4 = st.columns(4)
    for col, val, lbl, icn, clr in [
        (c1, len(df), "Missions totales", "calendar", "ic-abm"),
        (c2, int(df["Volume"].sum()), "Structures inspectées", "chart", "ic-green"),
        (c3, len(ctrldf), "Contrôles-poste", "shield", "ic-ctrl"),
        (c4, len(VALIDES), "Inspecteurs", "users", "ic-amber"),
    ]:
        with col:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-icon {clr}">{ICONS[icn]}</div>
                <div class="stat-label">{lbl}</div>
                <div class="stat-value">{val}</div>
            </div>
            ''', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        by_mois = df.groupby("Mois")["Volume"].sum().reset_index()
        by_mois["O"] = by_mois["Mois"].str.upper().apply(lambda x: ORDRE.index(x) if x in ORDRE else 99)
        by_mois = by_mois.sort_values("O")
        fig = px.bar(by_mois, x="Mois", y="Volume", color_discrete_sequence=["#014955"],
                     title="Volume mensuel d'inspections")
        fig.update_layout(height=280, margin=dict(t=30,b=5), plot_bgcolor="white",
                          xaxis=dict(gridcolor="#f1f5f9"), yaxis=dict(gridcolor="#f1f5f9"))
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        if "Sous_Type" in df.columns:
            tc = df["Sous_Type"].value_counts().reset_index()
            fig2 = px.pie(tc, names="Sous_Type", values="count", hole=0.4,
                          color_discrete_sequence=["#014955","#026d7e","#03899e","#d97706","#dc2626"],
                          title="Répartition par type")
            fig2.update_layout(height=280, margin=dict(t=30,b=5),
                               legend=dict(font=dict(size=10)))
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="stitle">Contrôles-poste — équipes</div>', unsafe_allow_html=True)
    ctrl_d = ctrldf.copy()
    ctrl_d["Équipe"] = ctrl_d["Equipe"].apply(
        lambda x: " · ".join(x) if isinstance(x,list) else str(x))
    st.dataframe(ctrl_d[["Mois","Semaine","Periode","Équipe"]].reset_index(drop=True),
                 use_container_width=True, height=300)


def page_equipe(init_courant):
    st.markdown('<div class="stitle">Charge de l\'équipe — classement ICR</div>', unsafe_allow_html=True)
    df = inspdf.copy()
    df["ICR_n"] = pd.to_numeric(df["ICR"], errors="coerce")
    df["Nom"] = df["Initiale"].apply(lambda x: get_nom(str(x).strip().upper()))
    df[""] = df["Initiale"].apply(lambda x: "⬅ vous" if str(x).strip().upper() == init_courant else "")
    cols = [c for c in ["Initiale","Nom","Groupe","P","Co","R","Total","IC","ICR",""] if c in df.columns]
    st.dataframe(df[cols].sort_values("ICR", ascending=False).reset_index(drop=True),
                 use_container_width=True, height=460)

    st.markdown('<div class="stitle">Comparaison ICR</div>', unsafe_allow_html=True)
    s = df.sort_values("ICR_n", ascending=True)
    colors = ["#059669" if str(x).strip().upper() == init_courant else "#014955" for x in s["Initiale"]]
    fig = go.Figure(go.Bar(x=s["ICR_n"], y=s["Initiale"], orientation="h",
                           marker_color=colors, text=s["ICR_n"].round(1), textposition="outside"))
    fig.update_layout(height=max(340,len(df)*24), margin=dict(l=5,r=50,t=5,b=5),
                      plot_bgcolor="white", xaxis=dict(gridcolor="#f1f5f9"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="stitle">Congés de l\'équipe</div>', unsafe_allow_html=True)
    cols_cg = [c for c in ["Mois","Initiale","Nom_Complet","Date_Debut","Date_Fin","Duree","Zone_Impact"] if c in congdf.columns]
    st.dataframe(congdf[cols_cg].reset_index(drop=True), use_container_width=True, height=260)


def page_password(init):
    st.markdown('<div class="stitle">Changer mon mot de passe</div>', unsafe_allow_html=True)

    if st.session_state.must_change_pw:
        st.warning("Vous utilisez encore le mot de passe par défaut. Veuillez le changer maintenant.")

    with st.form("change_pw"):
        old_pw  = st.text_input("Mot de passe actuel", type="password")
        new_pw  = st.text_input("Nouveau mot de passe", type="password",
                                help="Minimum 4 caractères")
        new_pw2 = st.text_input("Confirmer le nouveau mot de passe", type="password")
        submitted = st.form_submit_button("Enregistrer", type="primary")

        if submitted:
            if not check_pw(init, old_pw):
                st.error("Mot de passe actuel incorrect.")
            elif len(new_pw) < 4:
                st.error("Le nouveau mot de passe doit contenir au moins 4 caractères.")
            elif new_pw != new_pw2:
                st.error("Les deux mots de passe ne correspondent pas.")
            else:
                set_pw(init, new_pw)
                st.session_state.must_change_pw = False
                st.success("✅ Mot de passe mis à jour avec succès !")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ROUTING
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    page_login()
else:
    init = st.session_state.initiale
    render_sidebar(init)

    pg = st.session_state.page
    if pg == "dashboard":  page_dashboard(init)
    elif pg == "missions": page_missions(init)
    elif pg == "controles":page_controles(init)
    elif pg == "conges":   page_conges(init)
    elif pg == "globale":  page_globale()
    elif pg == "equipe":   page_equipe(init)
    elif pg == "password": page_password(init)
