import json
from .models import StundenAufzeichnung, Firma, Arbeitnehmer, Einstellungen, Rechnungsnummer
from .utils import calculate_stunden, moneyformat
from .pdf import make_pdf
from .forms import StundenAufzeichnungForm, RechnungsForm, UploadFileForm
from .forms import FirmaForm, ArbeitnehmerForm, RechnungsSummeForm
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ValidationError
from django.forms.utils import ErrorList
from django.urls import reverse
from decimal import Decimal
from urllib.parse import quote
from datetime import date, datetime
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist


@login_required
def index(request):
    """
    Der View für die Index Seite.
    Angezeigt wird unteranderem eine Tabelle mit Pagination.
    Login ist notwendig.
    """
    stunden_list = StundenAufzeichnung.objects.all().select_related().order_by(
        "-datum",
        "-startzeit"
    )
    for row in stunden_list:
        row.stunden = calculate_stunden(
            row.startzeit,
            row.endzeit
        )
    paginator = Paginator(stunden_list, 10)
    page = request.GET.get("page")
    try:
        stundenaufzeichnung = paginator.page(page)
    except PageNotAnInteger:
        stundenaufzeichnung = paginator.page(1)
    except EmptyPage:
        stundenaufzeichnung = paginator.page(paginator.num_pages)

    return render(
        request,
        "stunden/index.html",
        {"stundenaufzeichnung": stundenaufzeichnung},
        RequestContext(request)
    )


def log_in(request):
    """
    Der View für den Login.
    """
    error = ""
    username = ""
    if "next" in request.GET.keys():
        next = request.GET["next"]
    else:
        next = reverse("index")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                error = "User ist inakiv."
        else:
            error = "Login fehlgeschlagen. Bitte nochmals versuchen."

    return render(
        request,
        "stunden/login.html",
        {
            "error": error,
            "username": username
        },
        RequestContext(request)
    )


@login_required
def log_out(request):
    """
    Der View für den Logout.
    Leitet auf "/login/" um.
    Login ist notwendig.
    """
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def stundenaufzeichnung(request):
    """
    Der View, um eine Stundenaufzeichnung auszuwählen zum Bearbeiten oder zum Löschen.
    Login ist notwendig.
    """
    stunden_list = StundenAufzeichnung.objects.all().select_related().order_by(
        "-datum",
        "-startzeit"
    )
    paginator = Paginator(stunden_list, 10)
    page = request.GET.get("page")
    try:
        stundenaufzeichnung = paginator.page(page)
    except PageNotAnInteger:
        stundenaufzeichnung = paginator.page(1)
    except EmptyPage:
        stundenaufzeichnung = paginator.page(paginator.num_pages)

    return render(
        request,
        "stunden/stundenaufzeichnung.html",
        {"stundenaufzeichnung": stundenaufzeichnung},
        RequestContext(request)
    )


@login_required
def stundenaufzeichnung_neu(request):
    """
    Der View für einen neuen Eintrag.
    Leitet auf "/" um.
    Login ist notwendig.
    """
    # Falls POST
    if request.method == "POST":
        form = StundenAufzeichnungForm(request.POST)
        if form.is_valid():
            stundenaufzeichnung = StundenAufzeichnungForm(request.POST)
            neuer_eintrag = stundenaufzeichnung.save()
            if neuer_eintrag:
                return HttpResponseRedirect(reverse("index"))

    # Wenn nicht POST dann ein leeres Formular.
    else:
        form = StundenAufzeichnungForm()

    return render(
        request,
        "stunden/stundenaufzeichnung_neu.html",
        {"form": form},
        RequestContext(request)
    )


@login_required
def stundenaufzeichnung_bearbeiten(request, stundenaufzeichnung_id):
    """
    Der View, um eine Stundenaufzeichnung zu bearbeiten, oder zu löschen.
    Login ist notwendig.
    """
    # Request ist POST
    if request.method == "POST":
        # Bearbeiten
        if "stundenaufzeichnung_bearbeiten" in request.POST:
            stundenaufzeichnung = StundenAufzeichnungForm(
                request.POST,
                instance=StundenAufzeichnung.objects.get(pk=stundenaufzeichnung_id)
            )
            stundenaufzeichnung.save()
            return HttpResponseRedirect(reverse("index"))
        # Löschen
        elif "stundenaufzeichnung_loeschen" in request.POST:
            stundenaufzeichnung = StundenAufzeichnung.objects.get(pk=stundenaufzeichnung_id)
            stundenaufzeichnung.delete()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))

    # Request ist nicht POST
    else:
        stundenaufzeichnung = get_object_or_404(
            StundenAufzeichnung,
            pk=stundenaufzeichnung_id
        )
        form = StundenAufzeichnungForm(instance=stundenaufzeichnung)
        return render(
            request,
            "stunden/stundenaufzeichnung_bearbeiten.html",
            {
                "form": form,
                "stundenaufzeichnung_id": stundenaufzeichnung_id
            },
            RequestContext(request)
        )


@login_required
def firma(request):
    """
    Der View, um eine Firma auszuwählen zum Bearbeiten oder zum Löschen.
    Login ist notwendig.
    """
    firmen_list = Firma.objects.all().order_by("firma")
    paginator = Paginator(firmen_list, 10)
    page = request.GET.get("page")
    try:
        firma = paginator.page(page)
    except PageNotAnInteger:
        firma = paginator.page(1)
    except EmptyPage:
        firma = paginator.page(paginator.num_pages)

    return render(
        request,
        "stunden/firma.html",
        {"firma": firma},
        RequestContext(request)
    )


@login_required
def firma_neu(request):
    """
    Der View für einen neuen Firma Eintrag.
    Leitet auf "/" um.
    Login ist notwendig.
    """
    # Falls POST
    if request.method == "POST":
        form = FirmaForm(request.POST)
        if form.is_valid():
            firma = FirmaForm(request.POST)
            neuer_eintrag = firma.save()
            if neuer_eintrag:
                return HttpResponseRedirect(reverse("stundenaufzeichnung_neu"))

    # Wenn nicht POST dann ein leeres Formular.
    else:
        form = FirmaForm()

    return render(
        request,
        "stunden/firma_neu.html",
        {"form": form},
        RequestContext(request)
    )


@login_required
def firma_bearbeiten(request, firma_id):
    """
    Der View, um eine Firma zu bearbeiten, oder zu löschen.
    Login ist notwendig.
    """
    # Request ist POST
    if request.method == "POST":
        # Bearbeiten
        if "firma_bearbeiten" in request.POST:
            firma = FirmaForm(
                request.POST,
                instance=Firma.objects.get(pk=firma_id))
            firma.save()
            return HttpResponseRedirect(reverse("firma"))
        # Löschen
        elif "firma_loeschen" in request.POST:
            firma = Firma.objects.get(pk=firma_id)
            firma.delete()
            return HttpResponseRedirect(reverse("firma"))
        else:
            return HttpResponseRedirect(reverse("firma"))

    # Request ist nicht POST
    else:
        firma = get_object_or_404(Firma, pk=firma_id)
        form = FirmaForm(instance=firma)
        return render(
            request,
            "stunden/firma_bearbeiten.html",
            {
                "form": form,
                "firma_id": firma_id
            },
            RequestContext(request)
        )


@login_required
def arbeitnehmer(request):
    """
    Der View, um eine Arbeitnehmer auszuwählen zum Bearbeiten oder zum Löschen.
    Login ist notwendig.
    """
    arbeitnehmer_list = Arbeitnehmer.objects.all().order_by("name")
    paginator = Paginator(arbeitnehmer_list, 10)
    page = request.GET.get("page")
    try:
        arbeitnehmer = paginator.page(page)
    except PageNotAnInteger:
        arbeitnehmer = paginator.page(1)
    except EmptyPage:
        arbeitnehmer = paginator.page(paginator.num_pages)

    return render(
        request,
        "stunden/arbeitnehmer.html",
        {"arbeitnehmer": arbeitnehmer},
        RequestContext(request)
    )


@login_required
def arbeitnehmer_neu(request):
    """
    Der View für einen neuen Firma Eintrag.
    Leitet auf "/" um.
    Login ist notwendig.
    """
    # Falls POST
    if request.method == "POST":
        form = ArbeitnehmerForm(request.POST)
        if form.is_valid():
            arbeitnehmer = ArbeitnehmerForm(request.POST)
            neuer_eintrag = arbeitnehmer.save()
            if neuer_eintrag:
                return HttpResponseRedirect(reverse("stundenaufzeichnung_neu"))

    # Wenn nicht POST dann ein leeres Formular.
    else:
        form = ArbeitnehmerForm()

    return render(
        request,
        "stunden/arbeitnehmer_neu.html",
        {"form": form},
        RequestContext(request)
    )


@login_required
def arbeitnehmer_bearbeiten(request, arbeitnehmer_id):
    """
    Der View, um einen Arbeitnehmer zu bearbeiten, oder zu löschen.
    Login ist notwendig.
    """
    # Request ist POST
    if request.method == "POST":
        # Bearbeiten
        if "arbeitnehmer_bearbeiten" in request.POST:
            arbeitnehmer = ArbeitnehmerForm(
                request.POST,
                instance=Arbeitnehmer.objects.get(pk=arbeitnehmer_id)
            )
            arbeitnehmer.save()
            return HttpResponseRedirect(reverse("arbeitnehmer"))
        # Löschen
        elif "arbeitnehmer_loeschen" in request.POST:
            arbeitnehmer = Arbeitnehmer.objects.get(pk=arbeitnehmer_id)
            arbeitnehmer.delete()
            return HttpResponseRedirect(reverse("arbeitnehmer"))
        else:
            return HttpResponseRedirect(reverse("arbeitnehmer"))

    # Request ist nicht POST
    else:
        arbeitnehmer = get_object_or_404(Arbeitnehmer, pk=arbeitnehmer_id)
        form = ArbeitnehmerForm(instance=arbeitnehmer)
        return render(
            request,
            "stunden/arbeitnehmer_bearbeiten.html",
            {
                "form": form,
                "arbeitnehmer_id": arbeitnehmer_id
            },
            RequestContext(request)
        )


@login_required
def rechnung(request):
    """
    Der View für die Rechnung.
    Bei einem GET Request wird ein Formular angezeigt und eine Tabelle mit
    Einträgen, die unbezahlt markiert sind.
    Bei einem POST Request wird das Formular überprüft und wenn alles richtig
    scheint wird eine PDF Rechnung mit Hilfe von pdf.make_pdf() erstellt.
    Login ist notwendig.
    """
    # Holt alle unbezahlten Einträge aus der db.
    stunden_not_payed = StundenAufzeichnung.objects.select_related().filter(
        bezahlt=False).order_by("-datum", "-startzeit")

    # Rechnet die Stunden aus.
    for row in stunden_not_payed:
        row.stunden = calculate_stunden(row.startzeit, row.endzeit)

    # Eine Liste der markierten Checkboxen bei einem POST Request.
    stunden_ids = []

    if request.method == "POST":
        form = RechnungsForm(request.POST)
        stunden_ids = request.POST.getlist("checks[]")
        stunden_ids = [int(id) for id in stunden_ids]
        custom_error = "Bitte mindestens einen Eintrag unten auswählen"

        # Einträge als bezahlt markieren, update in der db.
        if "bezahlt_markieren" in request.POST and stunden_ids:
            queryset = StundenAufzeichnung.objects.filter(pk__in=stunden_ids)
            queryset.update(bezahlt=True)
            return HttpResponseRedirect(reverse("index"))

        # Formular nicht valid, keine Einträge gewählt, nicht bezahlt_markieren
        if not form.is_valid() and not stunden_ids and not "bezahlt_markieren" in request.POST:
            return render(
                request,
                "stunden/rechnung.html",
                {
                    "stunden_not_payed": stunden_not_payed,
                    "form": form,
                    "custom_error": custom_error
                },
                RequestContext(request)
            )

        # Formular nicht valid, keine Einträge gewählt, bezahlt_markieren.
        elif not form.is_valid() and not stunden_ids and "bezahlt_markieren" in request.POST:
            form = RechnungsForm()
            return render(
                request,
                "stunden/rechnung.html",
                {
                    "stunden_not_payed": stunden_not_payed,
                    "form": form,
                    "custom_error": custom_error
                },
                RequestContext(request)
            )

        # Formular ist valid.
        if form.is_valid():
            # Keine Einträge gewählt.
            if not stunden_ids:
                return render(
                    request,
                    "stunden/rechnung.html",
                    {
                        "stunden_not_payed": stunden_not_payed,
                        "form": form,
                        "custom_error": custom_error
                    },
                    RequestContext(request)
                )

            # Die Daten aus dem POST Request
            receiver_address_company = form.cleaned_data["firma"].firma
            receiver_address_name = form.cleaned_data["firma"].name
            receiver_address_street = form.cleaned_data["firma"].adresse
            receiver_address_zip = form.cleaned_data["firma"].plz
            receiver_address_city = form.cleaned_data["firma"].ort
            receiver_address_zip_city = receiver_address_zip + " " + receiver_address_city
            receiver_address_country = form.cleaned_data["firma"].land
            receiver_address_uid = form.cleaned_data["firma"].uid
            rechnungs_nummer = form.cleaned_data["rechnungs_nummer"]
            rechnungs_titel = form.cleaned_data["rechnungs_titel"]
            rechnungs_stundenlohn = form.cleaned_data["rechnungs_stundenlohn"]
            position_2_titel = form.cleaned_data["position_2_titel"]
            position_2_summe = form.cleaned_data["position_2_summe"]
            position_3_titel = form.cleaned_data["position_3_titel"]
            position_3_summe = form.cleaned_data["position_3_summe"]
            sender_address_name = form.cleaned_data["meine_daten"].name
            sender_address_street = form.cleaned_data["meine_daten"].adresse
            sender_address_zip = form.cleaned_data["meine_daten"].plz
            sender_address_city = form.cleaned_data["meine_daten"].ort
            sender_address_zip_city = sender_address_zip + " " + sender_address_city
            sender_address_country = form.cleaned_data["meine_daten"].land
            sender_address_uid = form.cleaned_data["meine_daten"].uid
            sender_bank_receiver = sender_address_name
            sender_bank_name = form.cleaned_data["meine_daten"].bank_name
            sender_bank_iban = form.cleaned_data["meine_daten"].bank_iban
            sender_bank_bic = form.cleaned_data["meine_daten"].bank_bic

            # Die Stundenreihen werden erstellt.
            stunden_rows = []
            stunden_gesamt_stunden = 0
            for id in stunden_ids:
                entry = StundenAufzeichnung.objects.get(pk=id)
                if entry.firma.firma == receiver_address_company:
                    stunden = Decimal(calculate_stunden(entry.startzeit, entry.endzeit))
                    stunden_gesamt_stunden += stunden
                    row = [
                        entry.datum,
                        entry.startzeit,
                        entry.endzeit,
                        entry.protokoll,
                        stunden,
                    ]
                    stunden_rows.append(row)

            # Fehler, wenn kein gewählter Eintrag zum Rechnungsempfänger passt.
            if not stunden_rows:
                custom_error = """Es wurde kein Eintrag für den oben
                    ausgewählten Rechnungsempfänger ausgewählt."""
                return render(
                    request,
                    "stunden/rechnung.html",
                    {
                        "stunden_not_payed": stunden_not_payed,
                         "form": form,
                         "stunden_ids": stunden_ids,
                         "custom_error": custom_error
                     },
                    RequestContext(request)
                )

            # Fehler, wenn Position 3 aber nicht Position 2 existiert.
            if not position_2_summe and position_3_summe:
                custom_error = "Bitte zuerst Position 2 ausfüllen."
                return render(
                    request,
                    "stunden/rechnung.html",
                    {
                        "stunden_not_payed": stunden_not_payed,
                         "form": form,
                         "stunden_ids": stunden_ids,
                         "custom_error": custom_error
                     },
                    RequestContext(request)
                )

            # Fehler, wenn nur ein Teil einer Position ausgefüllt wurde.
            if position_2_titel and not position_2_summe or \
            not position_2_titel and position_2_summe or \
            position_3_titel and not position_3_summe or \
            not position_3_titel and position_3_summe:
                custom_error = "Bitte beide Teile einer Position ausfüllen."
                return render(
                    request,
                    "stunden/rechnung.html",
                    {
                        "stunden_not_payed": stunden_not_payed,
                         "form": form,
                         "stunden_ids": stunden_ids,
                         "custom_error": custom_error
                     },
                    RequestContext(request)
                )

            # Die Rechnungssummen werden ausgerechnet.
            try:
                einstellungen = Einstellungen.objects.get(pk=1)
                einstellungen_ust = einstellungen.ust
            except ObjectDoesNotExist:
                einstellungen_ust = 20

            rechnungs_summe_pos1 = stunden_gesamt_stunden * rechnungs_stundenlohn
            if not position_2_summe and not position_3_summe:
                rechnungs_summe_netto = rechnungs_summe_pos1
            elif position_2_summe and not position_3_summe:
                rechnungs_summe_netto = rechnungs_summe_pos1 + position_2_summe
            elif position_2_summe and position_3_summe:
                rechnungs_summe_netto = rechnungs_summe_pos1 + position_2_summe + position_3_summe
            rechnungs_summe_ust = rechnungs_summe_netto / Decimal(100) * Decimal(einstellungen_ust)
            rechnungs_summe_brutto = rechnungs_summe_netto + rechnungs_summe_ust

            rechnungs_summe_pos1_formated = moneyformat(rechnungs_summe_pos1)
            rechnungs_summe_netto_formated = moneyformat(rechnungs_summe_netto)
            if position_2_summe:
                position_2_summe_formated = moneyformat(position_2_summe)
            if position_3_summe:
                position_3_summe_formated = moneyformat(position_3_summe)
            rechnungs_summe_ust_formated = moneyformat(rechnungs_summe_ust)
            rechnungs_summe_brutto_formated = moneyformat(rechnungs_summe_brutto)

            #Das file Objekt zur PDF erstellung wird erstellt.
            response = HttpResponse(content_type="application/pdf")
            filename = rechnungs_nummer.encode("utf-8")
            filename = quote(filename)
            url = "attachment; filename=\"Rechnung_{}_mfs_{}.pdf\"".format(
                filename,
                date.today().isoformat()
            )
            response["Content-Disposition"] = url

            # Die Daten fürs PDF.
            data = {
                "pdf_fileobject": response,
                "pdf_title": "Rechnung {} mfs {}".format(
                    rechnungs_nummer,
                    date.today().isoformat()
                ),
                "pdf_author": "Martin Fischer",
                "pdf_subject": "Rechnung erstellt von webpystunden3",
                "pdf_creator": "webpystunden3",
                "pdf_keywords": "webpystunden3, Martin, Fischer",
                "sender_address_name": sender_address_name,
                "sender_address_street": sender_address_street,
                "sender_address_city": sender_address_city,
                "sender_address_zip_city": sender_address_zip_city,
                "sender_address_country": sender_address_country,
                "sender_address_uid": sender_address_uid,
                "receiver_address_company": receiver_address_company,
                "receiver_address_name": receiver_address_name,
                "receiver_address_street": receiver_address_street,
                "receiver_address_zip_city": receiver_address_zip_city,
                "receiver_address_country": receiver_address_country,
                "receiver_address_uid": receiver_address_uid,
                "rechnungs_nummer": rechnungs_nummer,
                "rechnungs_titel": rechnungs_titel,
                "rechnungs_summe_pos1": rechnungs_summe_pos1_formated,
                "rechnungs_summe_netto": rechnungs_summe_netto_formated,
                "rechnungs_stundenlohn": rechnungs_stundenlohn,
                "position_2_titel": position_2_titel,
                "position_2_summe":
                    position_2_summe_formated if position_2_summe else position_2_summe,
                "position_3_titel": position_3_titel,
                "position_3_summe":
                    position_3_summe_formated if position_3_summe else position_3_summe,
                "einstellungen_ust": str(einstellungen_ust),
                "rechnungs_summe_ust": rechnungs_summe_ust_formated,
                "rechnungs_summe_brutto": rechnungs_summe_brutto_formated,
                "stunden_rows": stunden_rows,
                "stunden_gesamt_stunden": stunden_gesamt_stunden,
                "sender_bank_receiver": sender_bank_receiver,
                "sender_bank_name": sender_bank_name,
                "sender_bank_iban": sender_bank_iban,
                "sender_bank_bic": sender_bank_bic,
            }

            # Das PDF wird erstellt.
            make_pdf(data)

            # Speichern der Rechnungsnummer
            rechnungsnummer = Rechnungsnummer(rechnungsnummer=rechnungs_nummer)
            rechnungsnummer.save()

            # Das PDF wird an den Browser zum Herunterladen geschickt.
            return response

    # Falls kein POST Request.
    else:
        form = RechnungsForm()

    return render(
        request,
        "stunden/rechnung.html",
        {
            "stunden_not_payed": stunden_not_payed,
            "form": form,
            "stunden_ids": stunden_ids,
        },
        RequestContext(request)
    )


@login_required
def rechnung_summe(request):
    """
    Der View für die Rechnung mit einer Gesamtsumme.
    Bei einem GET Request wird ein Formular angezeigt und eine Tabelle mit
    Einträgen, die unbezahlt markiert sind.
    Bei einem POST Request wird das Formular überprüft und wenn alles richtig
    scheint wird eine PDF Rechnung mit Hilfe von pdf.make_pdf() erstellt.
    Login ist notwendig.
    """
    if request.method == "POST":
        form = RechnungsSummeForm(request.POST)

        # Formular nicht valid
        if not form.is_valid():
            return render(
                request,
                "stunden/rechnungsumme.html",
                {"form": form,},
                RequestContext(request)
            )

        # Formular ist valid.
        if form.is_valid():
            # Die Daten aus dem POST Request
            receiver_address_company = form.cleaned_data["firma"].firma
            receiver_address_name = form.cleaned_data["firma"].name
            receiver_address_street = form.cleaned_data["firma"].adresse
            receiver_address_zip = form.cleaned_data["firma"].plz
            receiver_address_city = form.cleaned_data["firma"].ort
            receiver_address_zip_city = receiver_address_zip + " " + receiver_address_city
            receiver_address_country = form.cleaned_data["firma"].land
            receiver_address_uid = form.cleaned_data["firma"].uid
            rechnungs_nummer = form.cleaned_data["rechnungs_nummer"]
            rechnungs_titel = form.cleaned_data["rechnungs_titel"]
            rechnungs_summe = form.cleaned_data["rechnungs_summe"]
            position_2_titel = form.cleaned_data["position_2_titel"]
            position_2_summe = form.cleaned_data["position_2_summe"]
            position_3_titel = form.cleaned_data["position_3_titel"]
            position_3_summe = form.cleaned_data["position_3_summe"]
            sender_address_name = form.cleaned_data["meine_daten"].name
            sender_address_street = form.cleaned_data["meine_daten"].adresse
            sender_address_zip = form.cleaned_data["meine_daten"].plz
            sender_address_city = form.cleaned_data["meine_daten"].ort
            sender_address_zip_city = sender_address_zip + " " + sender_address_city
            sender_address_country = form.cleaned_data["meine_daten"].land
            sender_address_uid = form.cleaned_data["meine_daten"].uid
            sender_bank_receiver = sender_address_name
            sender_bank_name = form.cleaned_data["meine_daten"].bank_name
            sender_bank_iban = form.cleaned_data["meine_daten"].bank_iban
            sender_bank_bic = form.cleaned_data["meine_daten"].bank_bic

            # Fehler, wenn Position 3 aber nicht Position 2 existiert.
            if not position_2_summe and position_3_summe:
                custom_error = "Bitte zuerst Position 2 ausfüllen."
                return render(
                    request,
                    "stunden/rechnungsumme.html",
                    {
                         "form": form,
                         "custom_error": custom_error
                     },
                    RequestContext(request)
                )

            # Fehler, wenn nur ein Teil einer Position ausgefüllt wurde.
            if position_2_titel and not position_2_summe or \
            not position_2_titel and position_2_summe or \
            position_3_titel and not position_3_summe or \
            not position_3_titel and position_3_summe:
                custom_error = "Bitte beide Teile einer Position ausfüllen."
                return render(
                    request,
                    "stunden/rechnungsumme.html",
                    {
                         "form": form,
                         "custom_error": custom_error
                     },
                    RequestContext(request)
                )

            # Die Rechnungssummen werden ausgerechnet.
            try:
                einstellungen = Einstellungen.objects.get(pk=1)
                einstellungen_ust = einstellungen.ust
            except ObjectDoesNotExist:
                einstellungen_ust = 20

            rechnungs_summe_pos1 = rechnungs_summe
            if not position_2_summe and not position_3_summe:
                rechnungs_summe_netto = rechnungs_summe_pos1
            elif position_2_summe and not position_3_summe:
                rechnungs_summe_netto = rechnungs_summe_pos1 + position_2_summe
            elif position_2_summe and position_3_summe:
                rechnungs_summe_netto = rechnungs_summe_pos1 + position_2_summe + position_3_summe

            rechnungs_summe_ust = rechnungs_summe_netto / Decimal(100) * Decimal(einstellungen_ust)
            rechnungs_summe_brutto = rechnungs_summe_netto + rechnungs_summe_ust

            if position_2_summe:
                position_2_summe_formated = moneyformat(position_2_summe)
            if position_3_summe:
                position_3_summe_formated = moneyformat(position_3_summe)
            rechnungs_summe_pos1_formated = moneyformat(rechnungs_summe_pos1)

            rechnungs_summe_netto_formated = moneyformat(rechnungs_summe_netto)
            rechnungs_summe_ust_formated = moneyformat(rechnungs_summe_ust)
            rechnungs_summe_brutto_formated = moneyformat(rechnungs_summe_brutto)

            #Das file Objekt zur PDF erstellung wird erstellt.
            response = HttpResponse(content_type="application/pdf")
            filename = rechnungs_nummer.encode("utf-8")
            filename = quote(filename)
            url = "attachment; filename=\"Rechnung_{}_mfs_{}.pdf\"".format(
                filename,
                date.today().isoformat()
            )
            response["Content-Disposition"] = url

            # Die Daten fürs PDF.
            data = {
                "pdf_fileobject": response,
                "pdf_title": "Rechnung {} mfs {}".format(
                    rechnungs_nummer,
                    date.today().isoformat()
                ),
                "pdf_author": "Martin Fischer",
                "pdf_subject": "Rechnung erstellt von webpystunden3",
                "pdf_creator": "webpystunden3",
                "pdf_keywords": "webpystunden3, Martin, Fischer",
                "sender_address_name": sender_address_name,
                "sender_address_street": sender_address_street,
                "sender_address_city": sender_address_city,
                "sender_address_zip_city": sender_address_zip_city,
                "sender_address_country": sender_address_country,
                "sender_address_uid": sender_address_uid,
                "receiver_address_company": receiver_address_company,
                "receiver_address_name": receiver_address_name,
                "receiver_address_street": receiver_address_street,
                "receiver_address_zip_city": receiver_address_zip_city,
                "receiver_address_country": receiver_address_country,
                "receiver_address_uid": receiver_address_uid,
                "rechnungs_nummer": rechnungs_nummer,
                "rechnungs_titel": rechnungs_titel,
                "rechnungs_summe_pos1": rechnungs_summe_pos1_formated,
                "rechnungs_summe_netto": rechnungs_summe_netto_formated,
                "rechnungs_stundenlohn": "",
                "position_2_titel": position_2_titel,
                "position_2_summe":
                    position_2_summe_formated if position_2_summe else position_2_summe,
                "position_3_titel": position_3_titel,
                "position_3_summe":
                    position_3_summe_formated if position_3_summe else position_3_summe,
                "einstellungen_ust": str(einstellungen_ust),
                "rechnungs_summe_ust": rechnungs_summe_ust_formated,
                "rechnungs_summe_brutto": rechnungs_summe_brutto_formated,
                "sender_bank_receiver": sender_bank_receiver,
                "sender_bank_name": sender_bank_name,
                "sender_bank_iban": sender_bank_iban,
                "sender_bank_bic": sender_bank_bic,
            }

            # Das PDF wird erstellt.
            make_pdf(data, second_table=False)

            # Speichern der Rechnungsnummer
            rechnungsnummer = Rechnungsnummer(rechnungsnummer=rechnungs_nummer)
            rechnungsnummer.save()

            # Das PDF wird an den Browser zum Herunterladen geschickt.
            return response

    # Falls kein POST Request.
    else:
        form = RechnungsSummeForm()

    return render(
        request,
        "stunden/rechnungsumme.html",
        {"form": form,},
        RequestContext(request)
    )


@login_required
def jsonexport(request):
    """
    Der View für den JSON Export.
    Login ist notwendig.
    """
    # Wenn POST Request.
    if request.method == "POST":
        # Radio-Button Wert
        json_export_select = request.POST.get("json_export_select")
        # File Objekt wird erstellt.
        response = HttpResponse(content_type="application/json")
        jetzt = datetime.now()

        filename = ""

        if json_export_select == "json_export_select_stundenaufzeichnung":
            filename = "webpystunden3-export--stundenaufzeichnung--{}".format(
                jetzt.strftime("%Y-%m-%d--%H-%M")
            )
            data = serializers.serialize(
                "json",
                StundenAufzeichnung.objects.all(),
                stream=response
            )

        if json_export_select == "json_export_select_firma":
            filename = "webpystunden3-export--firma--{}".format(jetzt.strftime("%Y-%m-%d--%H-%M"))
            data = serializers.serialize("json", Firma.objects.all(), stream=response)

        if json_export_select == "json_export_select_arbeitnehmer":
            filename = "webpystunden3-export--arbeitnehmer--{}".format(
                jetzt.strftime("%Y-%m-%d--%H-%M")
            )
            data = serializers.serialize("json", Arbeitnehmer.objects.all(), stream=response)

        if json_export_select == "json_export_select_rechnungsnummer":
            filename = "webpystunden3-export--rechnungsnummer--{}".format(
                jetzt.strftime("%Y-%m-%d--%H-%M")
            )
            data = serializers.serialize("json", Rechnungsnummer.objects.all(), stream=response)

        response["Content-Disposition"] = "attachment; filename={}.json".format(filename)
        return response

    # Falls nicht POST Request.
    else:
        # Hole alle Daten.
        stundenaufzeichnungen = StundenAufzeichnung.objects.all().select_related()
        return render(
            request,
            "stunden/jsonexport.html",
            {"stundenaufzeichnungen": stundenaufzeichnungen},
            RequestContext(request)
        )


@login_required
def jsonimport(request):
    """
    Der View für den JSON Import.
    Login ist notwendig.
    """
    # Fehler wenn der Dateiname nicht zum ausgewählten Bereich passt
    def validate_acceptable_filename(json_file, acceptable_filename):
        if not str(json_file).startswith(acceptable_filename):
            errors = form._errors.setdefault("json_file", ErrorList())
            errors.append("Bitte wähle die richtige Datei für den richtigen Bereich aus!")
            raise ValidationError()

    # Wenn der Request POST ist.
    if request.method == "POST":
        # Radio-Button Wert
        json_import_select = request.POST.get("json_import_select")
        # File Objekt wird erstellt.
        response = HttpResponse(content_type="application/json")
        jetzt = datetime.now()

        # Hol die Datei.
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Die Datei.
                json_file = request.FILES["json_file"]
                count_import = 0

                # Stundenaufzeichnung
                if json_import_select == "json_import_select_stundenaufzeichnung":
                    acceptable_filename = "webpystunden3-export--stundenaufzeichnung"
                    validate_acceptable_filename(json_file, acceptable_filename)
                    for deserialized_object in serializers.json.Deserializer(json_file):
                        count_import += 1
                        deserialized_object.save()

                # Firma
                if json_import_select == "json_import_select_firma":
                    acceptable_filename = "webpystunden3-export--firma"
                    validate_acceptable_filename(json_file, acceptable_filename)
                    for deserialized_object in serializers.json.Deserializer(json_file):
                        count_import += 1
                        deserialized_object.save()

                # Arbeitnehmer
                if json_import_select == "json_import_select_arbeitnehmer":
                    acceptable_filename = "webpystunden3-export--arbeitnehmer"
                    validate_acceptable_filename(json_file, acceptable_filename)
                    for deserialized_object in serializers.json.Deserializer(json_file):
                        count_import += 1
                        deserialized_object.save()

                # Rechnungsnummer
                if json_import_select == "json_import_select_rechnungsnummer":
                    acceptable_filename = "webpystunden3-export--rechnungsnummer"
                    validate_acceptable_filename(json_file, acceptable_filename)
                    for deserialized_object in serializers.json.Deserializer(json_file):
                        count_import += 1
                        deserialized_object.save()

            except:
                return render(
                    request,
                    "stunden/jsonimport.html",
                    {"form": form},
                    RequestContext(request)
                )

            # Leitet auf eine success Seite um und schickt die Anzahlen mit.
            return HttpResponseRedirect(
                reverse("jsonimport_success",
                kwargs={"count_import": count_import})
            )

    # Falls der Request nicht POST ist.
    else:
        form = UploadFileForm()

    return render(
        request,
        "stunden/jsonimport.html",
        {"form": form},
        RequestContext(request)
    )


@login_required
def jsonimport_success(request, count_import):
    """
    Der View für die JSON Import Success Seite.
    Holt sich die Anzahlen der db Imports aus der URL.
    Login ist notwendig.
    """

    return render(
        request,
        "stunden/jsonimport_success.html",
        {"count_import": count_import},
        RequestContext(request)
    )


@login_required
def einstellungen(request):
    """
    Der View für die Einstellungen.
    Login ist notwendig.
    """
    # Request ist POST
    if request.method == "POST":
        # Bearbeiten
        if "einstellungen_bearbeiten" in request.POST:
            input_ust = request.POST["input_ust"]
            try:
                einstellungen = Einstellungen.objects.get(pk=1)
                einstellungen.ust = input_ust
                einstellungen.save()
            except ObjectDoesNotExist:
                einstellungen = Einstellungen(ust=input_ust)
                einstellungen.save()
            return HttpResponseRedirect(reverse("einstellungen"))

    # Request ist nicht POST
    else:
        try:
            einstellungen = Einstellungen.objects.get(pk=1)
            return render(
                request,
                "stunden/einstellungen.html",
                {"einstellungen": einstellungen},
                RequestContext(request)
            )
        except ObjectDoesNotExist:
            return render(
                request,
                "stunden/einstellungen.html",
                {},
                RequestContext(request)
            )


@login_required
def get_firma_stundensatz(request, selected_firma_id):
    """
    Der View für den Rechnung Firma-Checkbox-Auswahl Stundensatz Eintrag.
    Login ist notwendig.
    """
    firma = Firma.objects.get(pk=selected_firma_id)
    data = {"firma_stundensatz": firma.stundensatz}

    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def rechnungsnummer(request):
    """
    Der View für die Rechnungsnummer Seite.
    Login ist notwendig.
    """
    rechnungsnummern = Rechnungsnummer.objects.all().order_by("-rechnungsnummer")

    return render(
        request,
        "stunden/rechnungsnummer.html",
        {"rechnungsnummern": rechnungsnummern},
        RequestContext(request)
    )
