from .models import StundenAufzeichnung, Firma, Arbeitnehmer, Rechnungsnummer
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import AppendedText
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist


class FirmaForm(forms.ModelForm):
    """
    Das Formular für einen neuen Firma Eintrag.
    """

    firma = forms.CharField(
        error_messages={"unique": "Firma mit diesem Firmen Namen existiert bereits."}
    )

    class Meta:
        model = Firma
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-4"
        super(FirmaForm, self).__init__(*args, **kwargs)


class ArbeitnehmerForm(forms.ModelForm):
    """
    Das Formular für einen neuen Arbeitnehmer Eintrag.
    """
    class Meta:
        model = Arbeitnehmer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-4"
        super(ArbeitnehmerForm, self).__init__(*args, **kwargs)


class StundenAufzeichnungForm(forms.ModelForm):
    """
    Das Formular für einen neuen Stunden Eintrag.
    """
    datum = forms.DateField(initial="{}".format(date.today().strftime("%d.%m.%Y")))

    button_firma = """
    <a href="/firma/neu/" class="btn btn-default">
    <i class="glyphicon glyphicon-plus"></i> Neue Firma erstellen</a>
    """

    firma = forms.ModelChoiceField(
        label="Firma",
        queryset=Firma.objects.all(),
        help_text=button_firma,
        required=True,
    )

    startzeit = forms.TimeField(widget=forms.TimeInput(format="%H:%M"), initial="08:00")

    endzeit = forms.TimeField(widget=forms.TimeInput(format="%H:%M"), initial="09:30")

    button_arbeitnehmer = """
    <a href="/arbeitnehmer/neu/" class="btn btn-default">
    <i class="glyphicon glyphicon-plus"></i> Neuen Arbeitnehmer erstellen</a>
    """

    arbeitnehmer = forms.ModelChoiceField(
        label="Arbeitnehmer",
        queryset=Arbeitnehmer.objects.all(),
        help_text=button_arbeitnehmer,
        initial = "1",
        required=True,
    )

    class Meta:
        model = StundenAufzeichnung
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.help_text_inline = True
        self.helper.form_tag = False
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-4"
        self.helper.layout = Layout(
            Field(AppendedText("datum", '<span class="glyphicon glyphicon-calendar"</span>',)),
            Field("firma"),
            Field(AppendedText("startzeit", '<span class="glyphicon glyphicon-time"</span>',)),
            Field(AppendedText("endzeit", '<span class="glyphicon glyphicon-time"</span>',)),
            Field("arbeitnehmer"),
            Field("protokoll"),
            Field("bezahlt"),
        )
        super(StundenAufzeichnungForm, self).__init__(*args, **kwargs)


class RechnungsForm(forms.Form):
    """
    Das Formular für die Rechnung.
    """
    last_month = date.today() + relativedelta(months=-1)
    last_month_formated = last_month.strftime("%m-%Y")

    firma = forms.ModelChoiceField(
        label="Rechnungsempfänger",
        queryset=Firma.objects.all(),
        required=True,
    )

    rechnungs_nummer = forms.CharField(
        label="Rechnungsnummer",
        max_length=50,
        initial="",
        help_text="(Die Rechnungsnummer benennt auch das PDF)",
        required=True,
    )

    rechnungs_titel = forms.CharField(
        label="Rechnungstitel",
        max_length=100,
        initial="Wartungsarbeiten {}".format(last_month_formated),
        help_text="(Ein Titel mit letztem Monat wurde automatisch eingetragen)",
        required=True,
    )

    rechnungs_stundenlohn = forms.DecimalField(
        label="Stundensatz ohne USt.",
        help_text="(Zulässig sind Werte wie: 50, 50.5 oder 50,55)",
        localize=True,
        max_digits=5,
        decimal_places=2,
        required=True,
    )

    position_2_titel = forms.CharField(
        label="Position 2 Titel",
        required=False,
    )

    position_2_summe = forms.DecimalField(
        label="Summe Pos. 2 ohne USt.",
        help_text="(Zulässig sind Werte wie: 50, 50.5 oder 50,55)",
        localize=True,
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    position_3_titel = forms.CharField(
        label="Position 3 Titel",
        required=False,
    )

    position_3_summe = forms.DecimalField(
        label="Summe Pos. 3 ohne USt.",
        help_text="(Zulässig sind Werte wie: 50, 50.5 oder 50,55)",
        localize=True,
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    meine_daten = forms.ModelChoiceField(
    label="Arbeitnehmer",
    queryset=Arbeitnehmer.objects.all(),
    initial = "1",
    required=True,
    )

    def __init__(self, *args, **kwargs):
        """
        Fügt Feldern CSS und Bootstrap Styling hinzu.
        """
        try:
            letzte_rechnungsnummer = Rechnungsnummer.objects.latest(
                "rechnungsnummer_datum").rechnungsnummer
            neue_rechnungsnummer = "IT-{}".format(int(letzte_rechnungsnummer.split("-")[-1]) + 1)
        except:
            neue_rechnungsnummer = ""
        kwargs.update(initial={
            "rechnungs_nummer": neue_rechnungsnummer,
        })
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.label_class = "col-lg-3"
        self.helper.field_class = "col-lg-3"
        self.helper.layout = Layout(
            Field("firma"),
            Field("rechnungs_nummer"),
            Field("rechnungs_titel"),
            Field(AppendedText("rechnungs_stundenlohn", "€",)),
            Field("position_2_titel"),
            Field(AppendedText("position_2_summe", "€",)),
            Field("position_3_titel"),
            Field(AppendedText("position_3_summe", "€",)),
            Field("meine_daten"),
        )
        super(RechnungsForm, self).__init__(*args, **kwargs)


class RechnungsSummeForm(forms.Form):
    """
    Das Formular für die Rechnung.
    """

    firma = forms.ModelChoiceField(
        label="Rechnungsempfänger",
        queryset=Firma.objects.all(),
        required=True,
    )

    rechnungs_nummer = forms.CharField(
        label="Rechnungsnummer",
        max_length=50,
        initial="",
        help_text="(Die Rechnungsnummer benennt auch das PDF)",
        required=True,
    )

    rechnungs_titel = forms.CharField(
        label="Position 1 Titel",
        max_length=100,
        initial="Erstellung ...",
        required=True,
    )

    rechnungs_summe = forms.DecimalField(
        label="Summe Pos. 1 excl. USt.",
        help_text="(Inklusiv Summe / 1.2)",
        localize=True,
        max_digits=10,
        decimal_places=2,
        required=True,
    )

    position_2_titel = forms.CharField(
        label="Position 2 Titel",
        required=False,
    )

    position_2_summe = forms.DecimalField(
        label="Summe Pos. 2 excl. USt.",
        help_text="(Inklusiv Summe / 1.2)",
        localize=True,
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    position_3_titel = forms.CharField(
        label="Position 3 Titel",
        required=False,
    )

    position_3_summe = forms.DecimalField(
        label="Summe Pos. 3 excl. USt.",
        help_text="(Inklusiv Summe / 1.2)",
        localize=True,
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    meine_daten = forms.ModelChoiceField(
        label="Arbeitnehmer",
        queryset=Arbeitnehmer.objects.all(),
        initial = "1",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        """
        Fügt Feldern CSS und Bootstrap Styling hinzu.
        """
        try:
            letzte_rechnungsnummer = Rechnungsnummer.objects.latest(
                "rechnungsnummer_datum").rechnungsnummer
            neue_rechnungsnummer = "IT-{}".format(int(letzte_rechnungsnummer.split("-")[-1]) + 1)
        except:
            neue_rechnungsnummer = ""
        kwargs.update(initial={
            "rechnungs_nummer": neue_rechnungsnummer,
        })
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.help_text_inline = True
        self.helper.label_class = "col-lg-3"
        self.helper.field_class = "col-lg-3"
        self.helper.layout = Layout(
            Field("firma"),
            Field("rechnungs_nummer"),
            Field("rechnungs_titel"),
            Field(AppendedText("rechnungs_summe", "€",)),
            Field("position_2_titel"),
            Field(AppendedText("position_2_summe", "€",)),
            Field("position_3_titel"),
            Field(AppendedText("position_3_summe", "€",)),
            Field("meine_daten"),
        )
        super(RechnungsSummeForm, self).__init__(*args, **kwargs)


class UploadFileForm(forms.Form):
    """
    Das Formular für den File Upload auf JSON Import.
    """
    json_file = forms.FileField(
        label="JSON Datei",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "col-lg-3"
        self.helper.field_class = "col-lg-9"
        super(UploadFileForm, self).__init__(*args, **kwargs)

    def clean_json_file(self):
        """
        Ein Validator, der prüft, ob die Dateiendung ".json" lautet.
        """
        data = self.cleaned_data["json_file"]
        if str(data).split(".")[-1] != "json":
            raise forms.ValidationError("Das ist keine JSON Datei!")
        return data
