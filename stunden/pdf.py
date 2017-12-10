import os
from datetime import date, time
from reportlab.lib.pagesizes import A4, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def make_pdf(data, font_folder="stunden/ubuntu-font-family-0.83/", second_table=True):
    """
    Erstellt PDF Rechnungen.
    Nimmt ein dict als erstes Argument und optional ein Keyword Argument namens
    "font_folder", womit man angeben kann wo sich der Ordner der "Ubuntu"
    Schriftart befindet.

    Verwendungsbeispiel:
    make_pdf({
        "pdf_fileobject": "filename.pdf",  # oder Django HttpResponse Objekt
        "pdf_title": "Rechnung IT-0815",
        "pdf_author": "Martin Fischer",
        "pdf_subject": "Rechnung erstellt von webpystunden3",
        "pdf_creator": "webpystunden3",
        "pdf_keywords": "webpystunden3, Martin, Fischer",
        "sender_address_name": "John Cleese",
        "sender_address_street": "Straße 15",
        "sender_address_city": "Ort",
        "sender_address_zip_city": "5555 Ort",
        "sender_address_country": "Österreich",
        "sender_address_uid": "UID: 123456789",
        "receiver_address_company": "Firma",
        "receiver_address_name": "Eric Idle",
        "receiver_address_street": "Straße 99",
        "receiver_address_zip_city": "9999 Ort",
        "receiver_address_country": "Österreich",
        "receiver_address_uid": "UID: 987654321",
        "rechnungs_nummer": "Rechnung IT-0815",
        "rechnungs_titel": "Rechnung für November",
        "rechnungs_summe_pos1": "60,00",
        "rechnungs_summe_netto": "100,00",
        "rechnungs_stundenlohn": "65",
        "position_2_titel" = "Position 2",
        "position_2_summe" = "222",
        "position_3_titel" = "Position 3",
        "position_3_summe" = "333",
        "einstellungen_ust": "20",
        "rechnungs_summe_ust": "20,00",
        "rechnungs_summe_brutto": "120,00",
        "stunden_rows": [
            [date(2012, 11, 29),
            time(10, 00, 00,),
            time(12, 00, 00,),
            "Das Protokoll Nr. 1",
            "2.00"],
            [date(2012, 11, 30),
            time(13, 00, 00),
            time(16, 30, 00),
            "Das Protokoll Nr. 2",
            "3.50"]
        ],
        "stunden_gesamt_stunden": "5.50",
        "sender_bank_receiver": "John Cleese",
        "sender_bank_name": "The Bank",
        "sender_bank_iban": "AT00000000000000",
        "sender_bank_bic": "XVSGHSVVVVVVVVV",
    }, font_folder="stunden/ubuntu-font-family-0.83/")
    """

    # Registriert die Schriftart Ubuntu.
    pdfmetrics.registerFont(TTFont("Ubuntu", os.path.join(font_folder, "Ubuntu-R.ttf")))
    pdfmetrics.registerFont(TTFont("UbuntuBold", os.path.join(font_folder, "Ubuntu-B.ttf")))
    pdfmetrics.registerFont(TTFont("UbuntuItalic", os.path.join(font_folder, "Ubuntu-RI.ttf")))
    pdfmetrics.registerFontFamily(
        "Ubuntu",
        normal="Ubuntu",
        bold="UbuntuBold",
        italic="UbuntuItalic"
    )

    # Hier werden alles Styles aufgesetzt.
    page_width, page_height = A4
    font_size_p = 11
    font_size_h1 = 14
    color_h1 = colors.HexColor("#16567e")

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="p-left",
        fontName="Ubuntu",
        fontSize=font_size_p,
        leading=font_size_p + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="p-right",
        fontName="Ubuntu",
        fontSize=font_size_p,
        leading=font_size_p + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_RIGHT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="h1_left",
        fontName="Ubuntu",
        fontSize=font_size_h1,
        leading=font_size_h1 + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_h1,
        bulletIndent=0,
        textColor=color_h1,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="table-center-header",
        fontName="Ubuntu",
        fontSize=font_size_p - 2,
        leading=font_size_p + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p,
        bulletIndent=0,
        textColor=colors.white,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="table-center",
        fontName="Ubuntu",
        fontSize=font_size_p,
        leading=font_size_p + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="table-left",
        fontName="Ubuntu",
        fontSize=font_size_p,
        leading=font_size_p + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="table-right",
        fontName="Ubuntu",
        fontSize=font_size_p,
        leading=font_size_p + 2,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_RIGHT,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    styles.add(ParagraphStyle(
        name="table-center-small",
        fontName="Ubuntu",
        fontSize=font_size_p - 2,
        leading=font_size_p,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_CENTER,
        spaceBefore=0,
        spaceAfter=0,
        bulletFontName="Ubuntu",
        bulletFontSize=font_size_p - 2,
        bulletIndent=0,
        textColor=colors.black,
        backColor=None,
        wordWrap=None,
        borderWidth=0,
        borderPadding=0,
        borderColor=None,
        borderRadius=None,
        allowWidows=1,
        allowOrphans=0
    ))

    # So sieht die erste Seite aus.
    def first_page(canvas, doc):
        canvas.saveState()
        canvas.drawImage("stunden/martinfischer.software-briefkopf.jpg", 1 * cm, page_height - 52 - 24, width=page_width - (2 * cm), height=52)
        canvas.setFont("Ubuntu", 8)
        canvas.setFillColor(colors.gray)
        canvas.drawCentredString(page_width / 2.0, 20, "Seite {}".format(doc.page))
        canvas.restoreState()

    # So sehen alle weiter Seiten aus. Identisch zur ersten Seite.
    def further_pages(canvas, doc):
        canvas.saveState()
        canvas.drawImage("stunden/martinfischer.software-briefkopf.jpg", 1 * cm, page_height - 52 - 24, width=page_width - (2 * cm), height=52)
        canvas.setFont("Ubuntu", 8)
        canvas.setFillColor(colors.gray)
        canvas.drawCentredString(page_width / 2.0, 20, "Seite {}".format(doc.page))
        canvas.restoreState()

    # Die Story beginnt hier.
    story = []

    story.append(Spacer(1, font_size_p * 5))

    # Die Daten des Rechnungssenders.
    sender_address_parts = [
        data["sender_address_name"],
        data["sender_address_street"],
        data["sender_address_zip_city"],
        data["sender_address_country"],
        data["sender_address_uid"]
    ]

    for part in sender_address_parts:
        ptext = "<font>{}</font>".format(part)
        story.append(Paragraph(ptext, styles["p-left"]))

    story.append(Spacer(1, font_size_p * 4))

    # Die Daten des Rechnungsempfängers.
    receiver_address_parts = [
        data["receiver_address_company"],
        data["receiver_address_name"],
        data["receiver_address_street"],
        data["receiver_address_zip_city"],
        data["receiver_address_country"],
        data["receiver_address_uid"]
    ]

    for part in receiver_address_parts:
        ptext = "<font>{}</font>".format(part)
        story.append(Paragraph(ptext, styles["p-left"]))

    story.append(Spacer(1, font_size_p))

    # Der Ort und das Datum.
    sender_address_city = data["sender_address_city"]
    today = date.today()
    formated_date = today.strftime("%d.%m.%Y")
    ptext = "<font>{}, {}</font>".format(sender_address_city, formated_date)
    story.append(Paragraph(ptext, styles["p-right"]))

    story.append(Spacer(1, font_size_p * 5))

    # Die Rechnungsnummer.
    ptext = """<font><b>Rechnungsnummer: {}</b></font>""".format(data["rechnungs_nummer"])
    story.append(Paragraph(ptext, styles["h1_left"]))

    story.append(Spacer(1, font_size_p * 3))

    # Die Tabelle mit den Rechnungsdaten.
    # Überschriften.
    table_header_position = Paragraph("<b>Position</b>", styles["table-center-header"])
    table_header_bezeichnung = Paragraph("<b>Bezeichnung</b>", styles["table-center-header"])
    table_header_ust = Paragraph("<b>USt. in %</b>", styles["table-center-header"])
    table_header_summe = Paragraph("<b>Summe</b>", styles["table-center-header"])

    # Reihe 1 - Titel und Summe Stunden.
    table_row1_position = Paragraph("1", styles["table-center"])
    table_row1_bezeichnung = Paragraph("{}".format(
        data["rechnungs_titel"]),
        styles["table-center"]
    )
    table_row1_ust = Paragraph("{}".format(data["einstellungen_ust"]), styles["table-center"])
    table_row1_summe = Paragraph("€ {}".format(
        data["rechnungs_summe_pos1"]),
        styles["table-right"]
    )

    # Reihe 2 - Stundensatz
    table_row2_position = Paragraph("", styles["table-center"])
    table_row2_bezeichnung = Paragraph("(Stundensatz: € {}/h - Stundenaufstellung auf Seite 2)".format(
        data["rechnungs_stundenlohn"]),
        styles["table-center-small"]
    )
    table_row2_ust = Paragraph("", styles["table-center"])
    table_row2_summe = Paragraph("", styles["table-right"])

    # Reihe 4 - Position 2
    if data["position_2_titel"] and data["position_2_summe"]:
        table_row4_position = Paragraph("2", styles["table-center"])
        table_row4_bezeichnung = Paragraph(
            "{}".format(data["position_2_titel"]),styles["table-center"]
        )
        table_row4_ust = Paragraph("{}".format(data["einstellungen_ust"]), styles["table-center"])
        table_row4_summe = Paragraph("€ {}".format(data["position_2_summe"]), styles["table-right"])

    # Reihe 6 - Position 3
    if data["position_3_titel"] and data["position_3_summe"]:
        table_row6_position = Paragraph("3", styles["table-center"])
        table_row6_bezeichnung = Paragraph(
            "{}".format(data["position_3_titel"]),styles["table-center"]
        )
        table_row6_ust = Paragraph("{}".format(data["einstellungen_ust"]), styles["table-center"])
        table_row6_summe = Paragraph("€ {}".format(data["position_3_summe"]), styles["table-right"])

    # Reihe 7 - Ein paar Striche zur Abgrenzung.
    table_row7_position = Paragraph("", styles["table-center"])
    table_row7_bezeichnung = Paragraph("-" * 3, styles["table-right"])
    table_row7_ust = Paragraph("", styles["table-center"])
    table_row7_summe = Paragraph("", styles["table-right"])

    # Reihe 8 - Rechnungsbetrag Netto.
    table_row8_position = Paragraph("", styles["table-center"])
    table_row8_bezeichnung = Paragraph("Rechnungsbetrag netto", styles["table-right"])
    table_row8_ust = Paragraph("", styles["table-center"])
    table_row8_summe = Paragraph("€ {}".format(
        data["rechnungs_summe_netto"]),
        styles["table-right"]
    )

    # Reihe 9 - Summe USt.
    table_row9_position = Paragraph("", styles["table-center"])
    table_row9_bezeichnung = Paragraph("20% Umsatzsteuer von € {}".format(
        data["rechnungs_summe_netto"]),
        styles["table-right"])
    table_row9_ust = Paragraph("", styles["table-center"])
    table_row9_summe = Paragraph("€ {}".format(
        data["rechnungs_summe_ust"]),
        styles["table-right"]
    )

    # Reihe 10 - Ein paar Striche zur Abgrenzung.
    table_row10_position = Paragraph("", styles["table-center"])
    table_row10_bezeichnung = Paragraph("-" * 3, styles["table-right"])
    table_row10_ust = Paragraph("", styles["table-center"])
    table_row10_summe = Paragraph("", styles["table-right"])

    # Reihe 11 - Rechnungsbetrag und Summe Brutto.
    table_row11_position = Paragraph("", styles["table-center"])
    table_row11_bezeichnung = Paragraph(
        "<b>Zu zahlender Rechnungsbetrag brutto inkl. USt.</b>",
        styles["table-right"])
    table_row11_ust = Paragraph("", styles["table-center"])
    table_row11_summe = Paragraph(
        "<b>€ {}</b>".format(
        data["rechnungs_summe_brutto"]),
        styles["table-right"]
    )

    # Die Tabelle als Liste aus Listen. Leer bedeutet eine leere Reihe.
    if second_table:
        data_rechnung = [
            [table_header_position, table_header_bezeichnung, table_header_ust, table_header_summe],
            [table_row1_position, table_row1_bezeichnung, table_row1_ust, table_row1_summe],
            [table_row2_position, table_row2_bezeichnung, table_row2_ust, table_row2_summe],
            [],
            [] if not data["position_2_titel"] and not data["position_2_summe"]
            else [table_row4_position, table_row4_bezeichnung, table_row4_ust, table_row4_summe],
            [],
            [] if not data["position_3_titel"] and not data["position_3_summe"]
            else [table_row6_position, table_row6_bezeichnung, table_row6_ust, table_row6_summe],
            [table_row7_position, table_row7_bezeichnung, table_row7_ust, table_row7_summe],
            [table_row8_position, table_row8_bezeichnung, table_row8_ust, table_row8_summe],
            [table_row9_position, table_row9_bezeichnung, table_row9_ust, table_row9_summe],
            [table_row10_position, table_row10_bezeichnung, table_row10_ust, table_row10_summe],
            [table_row11_position, table_row11_bezeichnung, table_row11_ust, table_row11_summe],
        ]
    else:
        data_rechnung = [
            [table_header_position, table_header_bezeichnung, table_header_ust, table_header_summe],
            [table_row1_position, table_row1_bezeichnung, table_row1_ust, table_row1_summe],
            [],
            [],
            [] if not data["position_2_titel"] and not data["position_2_summe"]
            else [table_row4_position, table_row4_bezeichnung, table_row4_ust, table_row4_summe],
            [],
            [] if not data["position_3_titel"] and not data["position_3_summe"]
            else [table_row6_position, table_row6_bezeichnung, table_row6_ust, table_row6_summe],
            [table_row7_position, table_row7_bezeichnung, table_row7_ust, table_row7_summe],
            [table_row8_position, table_row8_bezeichnung, table_row8_ust, table_row8_summe],
            [table_row9_position, table_row9_bezeichnung, table_row9_ust, table_row9_summe],
            [table_row10_position, table_row10_bezeichnung, table_row10_ust, table_row10_summe],
            [table_row11_position, table_row11_bezeichnung, table_row11_ust, table_row11_summe],
        ]

    # Styles für die Tabelle.
    table_rechnung = Table(data_rechnung, colWidths=[1.7 * cm, 9.5 * cm, 1.8 * cm, 3 * cm])

    table_rechnung.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), "#16567e"),
        ("FONTNAME", (0, 0), (-1, -1), "Ubuntu"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")])
    )

    # Die Story wird um eine Tabelle reicher.
    story.append(table_rechnung)

    story.append(Spacer(1, font_size_p * 3))

    # Dei Bankinformationen.
    ptext = "<font>Bitte den Rechnungsbetrag überweisen an:</font>"
    story.append(Paragraph(ptext, styles["p-left"]))

    story.append(Spacer(1, font_size_p))

    sender_bank_parts = [
        "Empfänger: {}".format(data["sender_bank_receiver"]),
        "Bank: {}".format(data["sender_bank_name"]),
        "IBAN: {}".format(data["sender_bank_iban"]),
        "BIC: {}".format(data["sender_bank_bic"])
    ]

    for part in sender_bank_parts:
        ptext = "<font>{}</font>".format(part)
        story.append(Paragraph(ptext, styles["p-left"]))

    if second_table:
        # Hier wird die erste Seite beendet.
        story.append(PageBreak())

        story.append(Spacer(1, font_size_p * 5))

        # Die Überschrift auf Seite 2.
        ptext = "<font><b>Stundenaufstellung</b></font>"
        story.append(Paragraph(ptext, styles["h1_left"]))

        story.append(Spacer(1, font_size_p * 3))

        # Die Tabelle mit den Stundenaufstellungen.
        stunden_table_data = []
        # Überschriften.
        table_datum_header = Paragraph("<b>Datum</b>", styles["table-center-header"])
        table_startzeit_header = Paragraph("<b>Startzeit</b>", styles["table-center-header"])
        table_endzeit_header = Paragraph("<b>Endzeit</b>", styles["table-center-header"])
        table_protokoll_header = Paragraph("<b>Protokoll</b>", styles["table-center-header"])
        table_stunden_header = Paragraph("<b>Stunden</b>", styles["table-center-header"])

        stunden_table_data_header = [
            table_datum_header,
            table_startzeit_header,
            table_endzeit_header,
            table_protokoll_header,
            table_stunden_header
        ]

        stunden_table_data.append(stunden_table_data_header)

        # Die Reihen mit den Stundendaten.
        stunden_table_data_rows = []
        for stunden_row in data["stunden_rows"]:
            datum = Paragraph("{}".format(
                stunden_row[0].strftime("%d.%m.%Y")),
                styles["table-center"]
            )
            startzeit = Paragraph(u"{}".format(
                stunden_row[1].strftime("%H:%M")),
                styles["table-center"]
            )
            endzeit = Paragraph(
                "{}".format(stunden_row[2].strftime("%H:%M")),
                styles["table-center"]
            )
            protokoll = Paragraph("{}".format(stunden_row[3]), styles["table-left"])
            stunden = Paragraph("{}".format(stunden_row[4]), styles["table-center"])
            row = [datum, startzeit, endzeit, protokoll, stunden]
            stunden_table_data_rows.append(row)

        for row in stunden_table_data_rows:
            stunden_table_data.append(row)

        # Die letzte Reihe mit den Gesamtstunden.
        table_datum_row_last = Paragraph("", styles["table-center"])
        table_startzeit_row_last = Paragraph("", styles["table-center"])
        table_endzeit_row_last = Paragraph("", styles["table-center"])
        table_protokoll_row_last = Paragraph("<b>Gesamtstunden</b>", styles["table-right"])
        table_stunden_row_last = Paragraph(
            "<b>{}</b>".format(
            data["stunden_gesamt_stunden"]),
            styles["table-center"]
        )

        stunden_table_data_row_last = [
            table_datum_row_last,
            table_startzeit_row_last,
            table_endzeit_row_last,
            table_protokoll_row_last,
            table_stunden_row_last
        ]

        stunden_table_data.append(stunden_table_data_row_last)

        # Styles für die Tabelle.
        table_stunden = Table(
            stunden_table_data,
            colWidths=[2.5 * cm, 2.2 * cm, 2.2 * cm, 7 * cm, 2 * cm]
        )

        table_stunden.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), "#16567e"),
            ("FONTNAME", (0, 0), (-1, -1), "Ubuntu"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ])
        )

        # Hier wird die Story um noch eine Tabelle reicher.
        story.append(table_stunden)

    # Das Template für das Dokument wird aufgesetzt.
    doc = SimpleDocTemplate(
        data["pdf_fileobject"],
        pagesize=A4,
        title="{}".format(data["pdf_title"]),
        author="{}".format(data["pdf_author"]),
        subject="{}".format(data["pdf_subject"]),
        creator="{}".format(data["pdf_creator"]),
        keywords="{}".format(data["pdf_keywords"]),
        rightMargin=70,
        leftMargin=70,
        topMargin=20,
        bottomMargin=20
    )

    # Das PDF wird erstellt.
    doc.build(story, onFirstPage=first_page, onLaterPages=further_pages)


if __name__ == '__main__':
    make_pdf({
        "pdf_fileobject": "filename.pdf",  # oder Django HttpResponse Objekt
        "pdf_title": "Rechnung IT-0815",
        "pdf_author": "Martin Fischer",
        "pdf_subject": "Rechnung erstellt von webpystunden3",
        "pdf_creator": "webpystunden3",
        "pdf_keywords": "webpystunden3, Martin, Fischer",
        "sender_address_name": "John Cleese",
        "sender_address_street": "Straße 15",
        "sender_address_city": "Ort",
        "sender_address_zip_city": "5555 Ort",
        "sender_address_country": "Österreich",
        "sender_address_uid": "UID: 123456789",
        "receiver_address_company": "Firma",
        "receiver_address_name": "Eric Idle",
        "receiver_address_street": "Straße 99",
        "receiver_address_zip_city": "9999 Ort",
        "receiver_address_country": "Österreich",
        "receiver_address_uid": "UID: 987654321",
        "rechnungs_nummer": "Rechnung IT-0815",
        "rechnungs_titel": "Rechnung für November",
        "rechnungs_stundenlohn": "65",
        "position_2_titel": "Position 2",
        "position_2_summe": "222",
        "position_3_titel": "Position 3",
        "position_3_summe": "333",
        "rechnungs_summe_netto": "100,00",
        "rechnungs_summe_pos1": "60,00",
        "einstellungen_ust": "20",
        "rechnungs_summe_ust": "20,00",
        "rechnungs_summe_brutto": "120,00",
        "stunden_rows": [
            [date(2012, 11, 29),
                time(10, 00, 00,),
                time(12, 00, 00,),
                "Das Protokoll Nr. 1",
                "2.00"],
            [date(2012, 11, 30),
                time(13, 00, 00),
                time(16, 30, 00),
                "Das Protokoll Nr. 2",
                "3.50"]
        ],
        "stunden_gesamt_stunden": "5.50",
        "sender_bank_receiver": "John Cleese",
        "sender_bank_name": "The Bank",
        "sender_bank_iban": "AT00000000000000",
        "sender_bank_bic": "XVSGHSVVVVVVVVV",
    }, font_folder="stunden/ubuntu-font-family-0.83/", second_table=True)
