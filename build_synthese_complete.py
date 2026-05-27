from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, 
                                 PageBreak, Table, TableStyle, HRFlowable,
                                 KeepTogether, ListFlowable, ListItem)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

# ─── STYLES ───────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1a2c5b")
BLUE   = colors.HexColor("#2e5fa3")
LBLUE  = colors.HexColor("#dce8f7")
GREEN  = colors.HexColor("#1a6b3a")
LGREEN = colors.HexColor("#d4edda")
RED    = colors.HexColor("#8b0000")
LRED   = colors.HexColor("#fde8e8")
ORANGE = colors.HexColor("#c85a00")
LORANG = colors.HexColor("#fff3e0")
GREY   = colors.HexColor("#f0f4f8")
LGREY  = colors.HexColor("#e8edf2")
DGREY  = colors.HexColor("#4a5568")
BLACK  = colors.black
YELLOW = colors.HexColor("#fff9c4")
WHITE  = colors.white

W = A4[0] - 4*cm

def st(name, **kw): return ParagraphStyle(name, **kw)

H0  = st("H0",  fontSize=20, textColor=NAVY,  spaceBefore=20, spaceAfter=8,  fontName="Helvetica-Bold", alignment=TA_CENTER)
H1  = st("H1",  fontSize=14, textColor=WHITE, spaceBefore=18, spaceAfter=5, fontName="Helvetica-Bold", backColor=NAVY, leftIndent=-5, rightIndent=-5, borderPad=6)
H2  = st("H2",  fontSize=12, textColor=NAVY,  spaceBefore=14, spaceAfter=4,  fontName="Helvetica-Bold", leftIndent=0, borderPad=3, backColor=LBLUE)
H3  = st("H3",  fontSize=11, textColor=BLUE,  spaceBefore=10, spaceAfter=3,  fontName="Helvetica-Bold")
H4  = st("H4",  fontSize=10, textColor=BLUE,  spaceBefore=7,  spaceAfter=2,  fontName="Helvetica-BoldOblique")
H5  = st("H5",  fontSize=9.5, textColor=DGREY, spaceBefore=5, spaceAfter=2,  fontName="Helvetica-Bold")
BODY = st("BODY", fontSize=9.2, textColor=BLACK, spaceBefore=3, spaceAfter=3, fontName="Helvetica", leading=14, alignment=TA_JUSTIFY)
BOLD = st("BOLD", fontSize=9.2, textColor=BLACK, spaceBefore=3, spaceAfter=3, fontName="Helvetica-Bold", leading=14)
ITAL = st("ITAL", fontSize=9, textColor=DGREY, spaceBefore=2, spaceAfter=2,   fontName="Helvetica-Oblique", leading=13)
NOTE = st("NOTE", fontSize=8.5, textColor=DGREY, spaceBefore=2, spaceAfter=2, fontName="Helvetica-Oblique", leading=13, leftIndent=10)
CITE = st("CITE", fontSize=9, textColor=colors.HexColor("#2c3e50"), spaceBefore=3, spaceAfter=3, fontName="Helvetica-Oblique", leading=14, leftIndent=15, borderPad=2)

def p(text, style=BODY): return Paragraph(text, style)
def h1(text): return Paragraph(f"<font color='white'> ■  {text}</font>", H1)
def h2(text): return Paragraph(f"<font color='#1a2c5b'>{text}</font>", H2)
def h3(text): return Paragraph(text, H3)
def h4(text): return Paragraph(text, H4)
def h5(text): return Paragraph(text, H5)
def sp(n=4): return Spacer(1, n)
def hr(): return HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=4, spaceBefore=4)
def hr2(): return HRFlowable(width="100%", thickness=0.4, color=BLUE, spaceAfter=2, spaceBefore=2)
def pb(): return PageBreak()

def box(items, bg=GREY, border=BLUE, padding=8):
    inner = [p(i) if isinstance(i, str) else i for i in items]
    tbl = Table([[inner]], colWidths=[W])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1),1,border),
        ("TOPPADDING",(0,0),(-1,-1),padding),
        ("BOTTOMPADDING",(0,0),(-1,-1),padding),
        ("LEFTPADDING",(0,0),(-1,-1),padding),
        ("RIGHTPADDING",(0,0),(-1,-1),padding),
    ]))
    return tbl

def warn(text): return box([p(f"<b>&#9888; ATTENTION EXAMEN :</b> {text}", BODY)], bg=LRED, border=RED)
def tip(text):  return box([p(f"<b>&#9733; Question frequente :</b> {text}", BODY)], bg=LGREEN, border=GREEN)
def arret(nom, date, texte): 
    return box([p(f"<b>Arret {nom} ({date}) :</b> {texte}", BODY)], bg=YELLOW, border=ORANGE)
def art(ref, texte):
    return box([p(f"<b>{ref} :</b> {texte}", BODY)], bg=LGREY, border=BLUE)

def tbl_base_style():
    return [
        ("GRID",(0,0),(-1,-1),0.4,BLUE),
        ("BACKGROUND",(0,0),(-1,0),LBLUE),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]

def t2(rows, headers=None, w1=None, w2=None):
    data = []
    if headers:
        data.append([p(f"<b>{headers[0]}</b>", BOLD), p(f"<b>{headers[1]}</b>", BOLD)])
    for r in rows:
        data.append([p(r[0], BODY), p(r[1], BODY)])
    tbl = Table(data, colWidths=[w1 or W/2-0.1*cm, w2 or W/2-0.1*cm])
    tbl.setStyle(TableStyle(tbl_base_style()))
    return tbl

def t3(rows, headers=None):
    data = []
    if headers:
        data.append([p(f"<b>{h}</b>", BOLD) for h in headers])
    for r in rows:
        data.append([p(c, BODY) for c in r])
    cw = W/3-0.05*cm
    tbl = Table(data, colWidths=[cw,cw,cw])
    tbl.setStyle(TableStyle(tbl_base_style()))
    return tbl

def t4(rows, headers=None):
    data = []
    if headers:
        data.append([p(f"<b>{h}</b>", BOLD) for h in headers])
    for r in rows:
        data.append([p(c, BODY) for c in r])
    cw = W/4-0.03*cm
    tbl = Table(data, colWidths=[cw]*4)
    tbl.setStyle(TableStyle(tbl_base_style()))
    return tbl

def multi_col(coldata, widths=None):
    n = len(coldata)
    inner = [[p(c, BODY) if isinstance(c, str) else c for c in col] for col in coldata]
    ww = widths or [W/n-0.05*cm]*n
    tbl = Table([inner], colWidths=ww)
    tbl.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
    ]))
    return tbl

# ══════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    "Synthese_DA_COMPLETE_BAC3.pdf",
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    title="Synthese COMPLETE - Droit Administratif (LDROI1305) - Pr. Renders",
    author="Synthese basee sur les notes de cours Victoria Oblin 2024-2025"
)

story = []

# PAGE DE TITRE
story += [
    sp(30),
    Paragraph("SYNTHESE COMPLETE", st("TT1",fontSize=24,fontName="Helvetica-Bold",textColor=NAVY,alignment=TA_CENTER)),
    sp(8),
    Paragraph("DROIT ADMINISTRATIF", st("TT2",fontSize=20,fontName="Helvetica-Bold",textColor=BLUE,alignment=TA_CENTER)),
    Paragraph("LDROI1305", st("TT3",fontSize=14,fontName="Helvetica",textColor=BLUE,alignment=TA_CENTER)),
    sp(10),
    Paragraph("Pr. David Renders - UCLouvain - 2024-2025", st("TT4",fontSize=12,fontName="Helvetica-Oblique",textColor=DGREY,alignment=TA_CENTER)),
    Paragraph("Notes de cours : Victoria Oblin", st("TT4b",fontSize=11,fontName="Helvetica-Oblique",textColor=DGREY,alignment=TA_CENTER)),
    sp(20),
    box([
        p("<b>Ce document couvre :</b> L'organisation de l'administration (externe + interne/fonction publique) · L'acte administratif unilateral (notion, classification, regime juridique, retrait) · L'acte administratif bilateral (concession domaniale, marches publics) · Les controles (tutelle, CADA, ombudsman, juridictions) · Le Conseil d'Etat (annulation, suspension, indemnite) · Article 159 Const.", BODY),
        sp(4),
        p("<b>Bases legales fondamentales :</b> Constitution (art. 7, 33, 41, 144-145, 159, 162, 163, 165-166, 170) · LCCE (art. 14, 14bis, 17, 19) · Loi 17/06/2016 (marches publics) · Loi 17/06/2013 (recours MP) · Loi 29/07/1991 (motivation formelle) · AR 02/10/1937 (statut Camu) · AR 14/01/2013 (execution MP) · CWADEL · NLC · Loi 11/04/1994 (CADA federale)", BODY),
    ], bg=LBLUE, border=NAVY),
    pb(),
]

# SOMMAIRE
story += [
    Paragraph("TABLE DES MATIERES", st("TDM",fontSize=14,fontName="Helvetica-Bold",textColor=NAVY,alignment=TA_CENTER,spaceBefore=10,spaceAfter=10)),
    hr(),
]
toc_items = [
    "INTRODUCTION - Definitions fondamentales & lois de Rolland",
    "PARTIE 1 - ORGANISATION EXTERNE DE L'ADMINISTRATION",
    "  Chap. 1 - Administrations federales, regionales et communautaires",
    "  Chap. 2 - Les collectivites locales",
    "    A. La commune (bourgmestre, college, conseil)",
    "    B. La province (conseil, college, gouverneur)",
    "    C. Agglomeration bruxelloise, commissions communautaires, CPAS",
    "PARTIE 2 - ORGANISATION INTERNE (FONCTION PUBLIQUE)",
    "  Chap. 1 - Agent statutaire vs agent contractuel",
    "  Chap. 2 - Recrutement, stage, nomination, carriere",
    "  Chap. 3 - Regime disciplinaire et suspension preventive",
    "PARTIE 3 - L'ACTE ADMINISTRATIF UNILATERAL (AAU)",
    "  Chap. 1 - Notion, contours, classification (reglementaire/individuel)",
    "  Chap. 2 - Regime juridique : legalite externe (competence, delegation, formes)",
    "  Chap. 3 - Regime juridique : legalite interne (objet, motifs, but)",
    "  Chap. 4 - Motivation formelle (loi 29/07/1991)",
    "  Chap. 5 - Caractere obligatoire, entree en vigueur, mutabilite",
    "  Chap. 6 - Theorie du retrait d'acte (4 hypotheses)",
    "  Chap. 7 - Privilege du prealable et execution d'office",
    "PARTIE 4 - L'ACTE ADMINISTRATIF BILATERAL (CONTRATS)",
    "  Chap. 1 - Contrat de l'administration vs contrat administratif",
    "  Chap. 2 - La concession domaniale (domaine, regime, contentieux)",
    "  Chap. 3 - Le marche public (champ, procedures, criteres, contentieux)",
    "PARTIE 5 - LE CONTROLE DE L'ADMINISTRATION",
    "  Chap. 1 - Recours administratifs (inorganise/organise)",
    "  Chap. 2 - Controle de tutelle (ordinaire/specifique/concours)",
    "  Chap. 3 - CADA et acces aux documents administratifs",
    "  Chap. 4 - L'ombudsman",
    "  Chap. 5 - Controle juridictionnel (juge judiciaire + Conseil d'Etat)",
    "  Chap. 6 - Article 159 de la Constitution",
    "FICHES RECAPITULATIVES - Questions phares d'examen",
]
for text in toc_items:
    story.append(p(text, BODY))
story.append(pb())

# INTRODUCTION
story += [
    h1("INTRODUCTION - DEFINITIONS ET LOIS DE ROLLAND"),
    h2("1. Definition du droit administratif"),
    p("Le droit administratif regit les <b>rapports juridiques entre le citoyen et l'administration</b>. "
      "Il est anime par la notion d'<b>interet general</b> : parce que les citoyens ne peuvent pas endosser certaines missions collectives, "
      "des personnes morales de droit public en sont chargees. Ces personnes disposent de <b>pouvoirs exorbitants</b> "
      "(pouvoir de commandement, privilege du prealable, execution d'office) strictement encadres par le "
      "<b>principe de legalite</b> (art. 33 Const. : 'Tous les pouvoirs emanent de la nation. Ils sont exerces de la maniere etablie par la Constitution')."),
    sp(),
    h2("2. Les trois Lois de Rolland (lois du service public)"),
    t3(
        [["<b>Loi d'egalite</b>",
          "<b>Loi de continuite</b>",
          "<b>Loi du changement</b>"],
         ["L'administration traite tous les administres de facon egale dans l'accomplissement de ses missions. Fonde le principe de non-discrimination.",
          "Le service public ne peut etre interrompu. Fonde la limitation du droit de greve dans les services essentiels. Justifie le privilege du prealable.",
          "L'interet general impose a l'administration de s'adapter. Fonde la mutabilite des statuts et des reglements sans droits acquis pour l'avenir. Justifie la loi du changement en fonction publique."]],
    ),
    sp(),
    h2("3. Notions fondamentales"),
    t2(
        [["<b>Decentralisation</b><br/>Technique institutionnelle par laquelle une personne morale de droit public cree une autre personne morale de droit public, lui confie des responsabilites autonomes et exerce a son egard un controle de <b>tutelle</b> (legalite + interet general). Ex : communes, provinces, CPAS, etablissements publics.",
          "<b>Deconcentration</b><br/>Technique qui place des services en dehors de la capitale tout en les maintenant sous l'autorite <b>hierarchique</b> du ministre. Aucune autonomie, aucune tutelle, aucune personnalite juridique propre. Ex : bureaux des contributions, guichets communaux pour CI ou demandes de pension."]],
        headers=["DECENTRALISATION","DECONCENTRATION"]
    ),
    sp(),
    tip("'La commune est-elle deconcentree ?' NON : decentralisee (personnalite juridique + autonomie + tutelle). Elle peut exercer certaines missions en deconcentration (ex : delivrance CI)."),
    pb(),
]

doc.build(story)
print("✅ PDF genere avec succes : Synthese_DA_COMPLETE_BAC3.pdf")
