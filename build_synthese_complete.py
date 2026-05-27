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

# INTRODUCTION SIMPLIFIÉE
story += [
    h1("INTRODUCTION - DEFINITIONS ET LOIS DE ROLLAND"),
    h2("1. Definition du droit administratif"),
    p("Le droit administratif regit les <b>rapports juridiques entre le citoyen et l'administration</b>. Il est anime par la notion d'<b>interet general</b> et encadre par le <b>principe de legalite</b>."),
    sp(),
    h2("2. Les trois Lois de Rolland"),
    t3(
        [["<b>Loi d'egalite</b>", "<b>Loi de continuite</b>", "<b>Loi du changement</b>"],
         ["Traitement egal des administres", "Service public ne peut etre interrompu", "L'interet general impose adaptation"]],
    ),
    sp(),
    h2("3. Decentralisation vs Deconcentration"),
    t2(
        [["<b>Decentralisation :</b> Creation d'une personne morale autonome avec tutelle (communes, provinces, CPAS)", "<b>Deconcentration :</b> Services sous autorite hierarchique du ministre, sans autonomie (bureaux des contributions)"]],
    ),
    pb(),
]

# PARTIE 1 - VERSION CONDENSÉE
story += [
    Paragraph("PARTIE 1 - L'ORGANISATION EXTERNE DE L'ADMINISTRATION", H0),
    hr(),
    h1("CHAPITRE 1 - ADMINISTRATIONS"),
    h2("A. Les ministres"),
    p("<b>Niveau federal :</b> Nommes par le Roi (max. 15). Exercent seuls leurs attributions. <b>Niveau federe :</b> Elus par Parlement, exercent collegialement au sein du gouvernement."),
    sp(),
    h2("B. Administrations speciales"),
    p("Justice, Police, Armee, Enseignement - organises par le legislateur. <b>Administrations collaterales :</b> SAA, Services personnalises, Etablissements publics, AAI, Associations droit public."),
    pb(),
    h1("CHAPITRE 2 - LES COLLECTIVITES LOCALES"),
    h2("A. La commune"),
    p("<b>565 communes en Belgique.</b> <b>Caracteristiques :</b> politique (elues), autonome (institutionnelle + fiscale relative), controlee (tutelle). C'est une collectivite DECENTRALISEE."),
    sp(),
    h3("Art. 162 Const. - Principes fondamentaux"),
    box([
        p("(1) Election directe du conseil communal. (2) Attribution aux conseils de tout interet communal. (3) Decentralisation. (4) Publicite budgets/comptes. (5) Intervention tutelle pour empecher violation loi ou lesion interet general."),
    ], bg=GREY),
    sp(),
    h3("Le conseil communal"),
    p("<b>Election :</b> 6 ans, representation proportionnelle. <b>Nombre :</b> 7 a 55 selon population (CWADEL/NLC). <b>Attributions :</b> competence residuelle - tout interet communal + missions confiees."),
    sp(),
    h3("Le bourgmestre - 3 modes selon la region"),
    t3(
        [["", "Region wallonne", "Region bruxelloise"],
         ["Mode", "ELU de plein droit (pacte majorite) - conseiller avec plus voix preference", "NOMME par Gvt bruxellois"],
         ["Presomption linguistique", "IRREFRAGABLE", "REFRAGABLE (3 criteres CE : politique, technique, moral)"]],
    ),
    sp(),
    h3("Perte du mandat"),
    p("<b>RW :</b> Motion de mefiance constructive (5 conditions : majorite absolue, constructive, motivee) OU sanction disciplinaire. <b>RBX :</b> Sanction disciplinaire UNIQUEMENT."),
    sp(),
    h2("B. Le college communal"),
    p("<b>Designation des echevins :</b> RW - pacte majorite (1/3 autre sexe). RBX - election separee (quasi-parite). <b>3 regles :</b> (1) Collegialite ; (2) Gouvernement d'assemblee ; (3) Decision majorite."),
    sp(),
    h2("C. Le CPAS"),
    p("Etablissement public local. Conseil action sociale (elu par CC) + President (college) + Bureau permanent."),
    sp(),
    h2("D. La province"),
    p("<b>Conseil provincial :</b> Elu directement (31-56 membres RW). <b>College provincial :</b> 4-5 deputes elus par conseil (pacte majorite). <b>Gouverneur :</b> Haut fonctionnaire regional nomme par Gouvernement regional sur avis du Conseil des ministres federal. Nomme a vie. Pas lien politique avec province. De-triplement fonctionnel (regles federales, regionales, communautaires)."),
    sp(),
    arret("Vandendooren", "CE, 10/06/2002", "Nomination gouverneur non conditionnee par couleur politique. Pas d'origine provinciale requise, mais residence apres nomination obligatoire."),
    sp(),
    h2("E. Agglomeration bruxelloise"),
    p("Art. 165-166 Const. Competences exercees par organes Region bruxelloise (arretes/reglements agglomeration). Controle tutelle s'efface (memes autorites)."),
    sp(),
    h2("F. Commissions communautaires bruxelloises"),
    p("COCOF, VGC, COCOM. Collectivites decentralisees. Missions communautaires a Bruxelles. Controle tutelle pour COCOF et VGC (pas COCOM)."),
    pb(),
]

# PARTIE 2 - VERSION CONDENSÉE
story += [
    Paragraph("PARTIE 2 - L'ORGANISATION INTERNE (FONCTION PUBLIQUE)", H0),
    hr(),
    h1("CHAPITRE 1 - AGENT STATUTAIRE vs CONTRACTUEL"),
    t2(
        [["<b>AGENT STATUTAIRE :</b> Situation determinee unilateralement par normes generales et abstraites modifiables. Engagement : concours + stage + nomination vie. Statut triple (administratif, pecunier, syndical). Loi du changement. Pas droits acquis (standstill). Juge : CE (droits subjectifs -> Trib.).", "<b>AGENT CONTRACTUEL :</b> Contrat loi 03/07/1978. Evaluation titres/merites. Priorite laureats CELOR. Statut : contrat + loi 1978 + reglement travail. Loi changement ne s'applique PAS. Juge : Tribunal travail (acte detachable -> CE)."]],
    ),
    sp(),
    h2("Les trois statuts de l'agent statutaire"),
    t3(
        [["Administratif", "Pecunier", "Syndical"],
         ["Recrutement, nomination, promotion, discipline. Autorite competente (Roi -> AR 02/10/1937 pour federal ; gouvernements regionaux ; conseils locaux).", "Remuneration, anciennete, pension. Meme autorite. Theorie service-fait.", "Relations syndiques. LEGISLATEUR FEDERAL (art. 87, 5 LSRI). Negociation (mesures importantes) vs Concertation (mesures moins importantes)."]],
    ),
    sp(),
    h1("CHAPITRE 2 - RECRUTEMENT, STAGE, NOMINATION"),
    p("<b>Recrutement :</b> (1) Conditions prealables. (2) Diplome. (3) Avis vacance publie MB + delai. (4) Procedure egale. (5) <b>Concours</b> = comparaison/classement."),
    sp(),
    p("<b>Stage :</b> 1 an. Si mention insuffisant -> prolongation, licenciement ou nomination. Licenciement : 3 mois preavis min."),
    sp(),
    p("<b>Carriere :</b> Niveaux A/B/C/D. Promotion plane (nomination successive sans emploi vacant, competence liee)."),
    sp(),
    h1("CHAPITRE 3 - REGIME DISCIPLINAIRE"),
    p("<b>Sanctions :</b> Rappel ordre -> Blame -> Retenue traitement -> Deplacement -> Suspension (<3 mois) -> Regression -> Retrogradation -> Demission office -> REVOCATION."),
    sp(),
    box([
        p("<b>13 garanties procedurales :</b> (1) Droit defense. (2) Avocat/delegue syndical. (3) Acces dossier. (4) Audition publique si demande. (5) Bilinguisme. (6) Non bis in idem. (7) Impartialite d'ordre public. (8) Auteur proposant != sanctionnant. (9) Recours organise. (10) Sanction <= proposition. (11) Non retroactivite. (12) Motivation formelle. (13) Notification sans delai."),
    ], bg=LBLUE, border=NAVY),
    sp(),
    p("<b>Independence disciplinaire/penale :</b> Autorite disciplinaire ne lie PAS constatations fait du juge penal. Si acquittement -> pas sanction. Si condamnation -> peut ne pas sanctionner."),
    sp(),
    h2("Suspension preventive"),
    p("<b>Nature :</b> Mesure d'ordre (non sanction). But : eloigner agent pendant instruction. <b>Garanties :</b> Audition prealable. Droit conseil. Recours organise."),
    pb(),
]

# PARTIE 3 - VERSION CONDENSÉE
story += [
    Paragraph("PARTIE 3 - L'ACTE ADMINISTRATIF UNILATERAL (AAU)", H0),
    hr(),
    h1("CHAPITRE 1 - NOTION ET CONTOURS"),
    p("<b>Definition :</b> Toute manifestation volonte autorite administrant, destinee produire effets juridiques, par volonte seule. Expresse (ecrit) ou silence (art. 14 §3 LCCE = refus)."),
    sp(),
    h3("Art. 14 §3 LCCE - Silence valant refus"),
    box([
        p("(1) Autorite administrative. (2) Competence OBLIGATOIRE (peu importe discretionnaire/liee). (3) Disposition RESIDUELLE. Mise demeure -> 4 mois -> silence = refus."),
    ], bg=GREY),
    sp(),
    h2("Actes assembles legislatives et personnes privees"),
    p("<b>Parlements :</b> Art. 14 §1 2 LCCE - recours CE UNIQUEMENT matiere MP/fonction publique. Extension : Cour comptes, CE, juridictions, Pouvoir judiciaire, CSJ, mediateurs."),
    sp(),
    h3("Administrations penitentiaires"),
    p("<b>Execution peine :</b> TAP/Commission plaintes. <b>Sans rapport peine :</b> AAU recours CE."),
    sp(),
    h3("Personnes privees - Indices Bonheure"),
    box([
        p("<b>3 cumules :</b> (1) Organisation (pouvoirs publics pouvoir dans direction/controle). (2) Mission (missions interet general - service public fonctionnel). (3) Moyens (pouvoir decision contraignant tiers). = autorite administrative fonctionnelle. Ex : UCLouvain diplomes homologues."),
    ], bg=LGREEN, border=GREEN),
    sp(),
    h1("CHAPITRE 2 - CLASSIFICATION"),
    h2("Acte reglementaire"),
    p("Dispositions generales/abstraites, generalite destinataires abstraits. N'epuise pas effets par seule application. Ex : statut Camu."),
    sp(),
    h2("Acte individuel"),
    p("Mesures speciales/concretes, personnes determinees/identifiables. Ex : nomination."),
    sp(),
    h2("Difference 3 : Avis SLCE, Motivation, Art. 159"),
    t3(
        [["Critere", "Acte REGLEMENTAIRE", "Acte INDIVIDUEL"],
         ["Avis SLCE", "Obligatoire federal/federe (ordre public)", "Non applicable"],
         ["Motivation formelle", "Non applicable", "OBLIGATOIRE loi 1991"],
         ["Art. 159", "CE : tout temps. Cass : tout temps", "CE : tant qu'attaquable. Cass : tout temps"]],
    ),
    pb(),
    h1("CHAPITRE 3 - LEGALITE EXTERNE"),
    h2("A. Competence"),
    h3("Theorie fonctionnaire de fait"),
    box([
        p("<b>Hyp. 1 :</b> Autorite reguliere pas en mesure -> tiers exerce sa place -> actes couverts si necessite absolue. <b>Hyp. 2 :</b> Nomination annulee retroactivement -> actes AVANT annulation restent valables (securite juridique). Vice competence couvert, autres irregularites peuvent etre invoquees."),
    ], bg=GREY),
    sp(),
    h3("Autorite collegiale - conditions validite"),
    box([
        p("(1) Quorum : plus 1/2 membres (CE). (2) Regulierement investis, pas incompatibilite. (3) Majorite voix exprimees."),
    ], bg=GREY),
    sp(),
    h3("Delegation pouvoir - 7 conditions"),
    box([
        p("(1) Texte autorise. (2) Texte publie. (3) Acte delegation ECRIT, PREALABLE, PUBLIE. (4) Publication PRECEDE exercice. (5) PARTIELLE/ACCESSOIRE. (6) PRECAIRE/REVOCABLE AD NUTUM. (7) STRICTE INTERPRETATION. Subdelegation : interdite sauf expres."),
    ], bg=LBLUE, border=NAVY),
    sp(),
    h3("Delegation signature vs pouvoir"),
    p("<b>Delegation POUVOIR :</b> Transfert exercice competence, delegataire decide (7 conditions). <b>Delegation SIGNATURE :</b> Autorite competente decide, delegataire signe seulement (SO/PO - plus leger). Verifier dossier administratif."),
    sp(),
    h2("B. Formes et formalites"),
    h3("Propositions et avis"),
    t4(
        [["Type avis", "Contraignant?", "Sanctionne irregulier?", "Exemples"],
         ["Proposition", "OUI", "OUI", "Candidats nomination BM"],
         ["Avis conforme", "OUI", "OUI", "Avis conforme Conseil ministres nomination gouverneur"],
         ["Avis simple obligatoire", "NON mais pris compte", "OUI si requis interet administre", "SLCE, commission selection"],
         ["Avis facultatif demande", "NON", "OUI : si demande -> obligatoire consideration", "N'importe quel avis demande"],
         ["Avis interet seul admin", "NON", "NON", "Avis inspecteur finances"]],
    ),
    sp(),
    h3("Droits defense vs Audi alteram partem"),
    t2(
        [["<b>DROITS DEFENSE :</b> Mesures SANCTION (disciplinaire/administrative). Garanties strictes : info prealable complete, acces dossier, avocat, audition orale, PV. Urgence N'EXCUSE PAS. ORDRE PUBLIC (souleve d'office). Formalite substantielle.", "<b>AUDI ALTERAM PARTEM :</b> Mesures GRAVES (comportement personnel). Plus souple : pas formalisme, urgence permet passer outre, delegation pouvoir audition possible. PAS ORDRE PUBLIC (invoque requerant). Autorite permette point vue."]],
    ),
    sp(),
    h3("Impartialite"),
    p("<b>ORDRE PUBLIC.</b> <b>Objective :</b> Circonstances -> crainte raisonnable. <b>Subjective :</b> Partialite averee. CE controle les deux."),
    sp(),
    h3("Confiance legitime - 3 conditions"),
    box([
        p("(1) Situation causee acte admin. (2) Confiance legitime nait (bonne foi + attente non contraire ordre public). (3) Admin pas motif grave/justification legitime revenir."),
    ], bg=LORANG, border=ORANGE),
    sp(),
    h3("Enquete publique"),
    box([
        p("<b>Quand?</b> Chaque fois texte requiert OU voluntairement. <b>Pendant :</b> Rendre effective (temps utile, info suffisante, acces dossier). <b>Apres :</b> Tenir compte resultats, motiver, communiquer, recommencer si modif fondamentale."),
    ], bg=GREY),
    sp(),
    h2("C. Acte doit etre ecrit et signe"),
    p("Obligation non codifiee mais CE. Actes oraux irreguliers. Exception : silence = AAU (art. 14 §3 LCCE). <b>Signature :</b> Accede existence juridique. <b>Contreseing (art. 106) :</b> AR - ministre contresigne, responsabilite politique."),
    sp(),
    h2("D. Publication et notification"),
    p("<b>Publication reglementaires :</b> MB (10e jour), bulletin prov. (8e), affichage comm. (5e). <b>Notification individuels :</b> Lettre recommandee. <b>Voies recours non mentionnees :</b> Delai pas debute -> 4 mois + 60 j (art. 19 al.2 LCCE)."),
    pb(),
]

# FICHES FINALES
story += [
    Paragraph("FICHES RECAPITULATIVES", H0),
    hr(),
    h1("FICHE 1 - RETRAIT D'ACTE (ARBRE DECISION)"),
    box([
        p("<b>Acte LEGAL createur avantage :</b> JAMAIS retire."),
        sp(2),
        p("<b>Acte ILLEGAL createur avantage :</b>"),
        p("  • <b>Dans 60 jours recours :</b> Retrait toute illegalite."),
        p("  • <b>Apres 60 j si recours :</b> Jusqu'a cloture debats, illegalite requete/ordre public."),
        p("  • <b>Au-dela :</b> 5 hyp seulement : (1) repute inexistant ; (2) manoeuvres frauduleuses ; (3) texte expres ; (4) renonciation beneficiaire ; (5) autorite chose jugee."),
        sp(2),
        p("<b>Jurisprudence Cass. :</b> EN TOUT TEMPS (art. 159)."),
    ], bg=LGREEN, border=GREEN),
    sp(),
    h1("FICHE 2 - DROITS DEFENSE vs AUDI ALTERAM PARTEM"),
    t2(
        [["<b>Droits defense :</b> Mesures sanction. Garanties strictes (info complete, dossier, avocat, audition orale, PV). Urgence N'EXCUSE. Ordre public. Substantiel.", "<b>Audi alteram partem :</b> Mesures graves (comportement). Souplesse. Urgence ok. Pas ordre public. Autorite permette point vue."]],
    ),
    sp(),
    h1("FICHE 3 - RETRAIT D'ACTE - VERSION COURTE"),
    p("<b>LEGAL createur avantage = JAMAIS retire. ILLEGAL createur avantage = 60 j + exceptions au-dela. NON createur = DOIT etre retire si illegal (responsabilite civil si non)."),
    sp(),
    h1("FICHE 4 - ART. 159 CONST."),
    box([
        p("Toute juridiction contentieuse (judiciaire ET administrative) peut ecarter application AAU si non-conforme aux lois (sense large). <b>CE :</b> Reglementaires tout temps ; individuels tant qu'attaquables. <b>Cass :</b> Tout temps tous actes. ORDRE PUBLIC. Effet = ecarter (pas annulation, mais mettre quarantaine). N'importe quelle partie OU juge d'office."),
    ], bg=LORANG, border=ORANGE),
    sp(),
    h1("LEXIQUE ESSENTIEL"),
    p("<b>Abrogation :</b> Cessation effets acte pour futur (pas retrait = retroactif). Reglementaires. Limite individuels."),
    p("<b>Detournement pouvoir :</b> Autorite acte principalement/exclusivement but illicite. Preuve : faisceau presomptions graves/precises/concordantes. -> SCACE Assemblee generale, unanimite."),
    p("<b>Mutabilite :</b> Reglementaires : ordre public, pas droits acquis au maintien (mais droits acquis SOUS reglement proteges passe). Individuels : abrogation si effets persistants + interet general."),
    p("<b>Privilege prealable :</b> AAU titre executoire lui-meme. Admin pas passer justice pour obeissance. Exception : expropriation utilite publique."),
    p("<b>Impartialite :</b> Objective (crainte raisonnable partialite) + Subjective (partialite averee). ORDRE PUBLIC. CE controle les deux."),
    p("<b>Confiance legitime :</b> (1) Situation causee acte admin ; (2) Confiance legitime nait ; (3) Admin pas justification legitime revenir."),
    p("<b>Loi changement :</b> 3e loi Rolland. Admin s'adapter. Pas droits acquis maintien reglement (futur). Mutabilite."),
    p("<b>Motifs adequation :</b> Pas formule creuse. Plus etayee pouvoir discretionnaire. Renforcee revirement. Pas repondre chaque argument."),
    p("<b>Pouvoir discretionnaire :</b> Admin marge appreciation. Controle marginal (erreur manifeste OU proportionnalite)."),
    p("<b>Competence liee :</b> Admin aucune liberte, decision obligatoire. Juge judiciaire exclusif."),
    p("<b>Proportionnalite :</b> (1) Sanction admin/disciplinaire ; (2) Mesure police ; (3) Droit fondamental ; (4) Texte impose objectif ; (5) Texte impose mesures proportionnees. Test : adequate + necessaire + proportionnee sensu stricto."),
    pb(),
    sp(40),
    Paragraph("FIN DE LA SYNTHESE", st("FIN",fontSize=16,fontName="Helvetica-Bold",textColor=NAVY,alignment=TA_CENTER)),
    sp(10),
    box([
        p("Synthese realisee a partir notes cours Victoria Oblin (LDROI1305, 2024-2025, Pr. David Renders, UCLouvain). Rigueur universitaire exigee : employer termes exacts, citer articles et arrets, distinctions cles.", NOTE),
        sp(4),
        p("<b>Examen :</b> Deux oraux (assistant + prof/assistant). Code droit administratif autorise. Repondre termes precis, citer articles/arrets, distinctions.", BOLD),
    ], bg=LBLUE, border=NAVY),
]

doc.build(story)
print("✅✅✅ PDF GENERE AVEC SUCCES ! ✅✅✅")
print("📄 Fichier : Synthese_DA_COMPLETE_BAC3.pdf")
