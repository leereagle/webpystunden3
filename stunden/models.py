from .utils import calculate_stunden
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Firma(models.Model):
    """
    Das ORM Model für Firma.
    """
    firma = models.CharField(max_length=200, blank=False, unique=True)
    name = models.CharField(max_length=200, blank=True)
    adresse = models.CharField(max_length=200, blank=True)
    plz = models.CharField(max_length=20, blank=True)
    ort = models.CharField(max_length=200, blank=True)
    land = models.CharField(max_length=200, blank=True)
    uid = models.CharField(max_length=20, blank=True, verbose_name="UID")
    stundensatz = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.firma

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmen"


class Arbeitnehmer(models.Model):
    """
    Das ORM Model für Arbeitnehmer.
    """
    name = models.CharField(max_length=200, blank=False, unique=True)
    adresse = models.CharField(max_length=200, blank=True)
    plz = models.CharField(max_length=20, blank=True)
    ort = models.CharField(max_length=200, blank=True)
    land = models.CharField(max_length=200, blank=True)
    uid = models.CharField(max_length=20, blank=True, verbose_name="UID")
    bank_name = models.CharField(max_length=200, blank=True, verbose_name="Bank")
    bank_iban = models.CharField(max_length=200, blank=True, verbose_name="IBAN")
    bank_bic = models.CharField(max_length=200, blank=True, verbose_name="BIC")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Arbeitnehmer"
        verbose_name_plural = "Arbeitnehmer"


class StundenAufzeichnung(models.Model):
    """
    Das ORM Model für StundenAufzeichnung.
    """
    datum = models.DateField(blank=False)
    firma = models.ForeignKey("Firma", on_delete=models.CASCADE)
    startzeit = models.TimeField(blank=False)
    endzeit = models.TimeField(blank=False)
    arbeitnehmer = models.ForeignKey("Arbeitnehmer", on_delete=models.CASCADE)
    protokoll = models.TextField(blank=False)
    bezahlt = models.BooleanField(blank=False)

    def stunden(self):
        """
        Rechnet den Zeitunterschied aus.
        """
        return calculate_stunden(self.startzeit, self.endzeit)

    def clean(self):
        """
        Ein Validator, der prüft, ob die Startzeit vor der Endzeit liegt.
        Die geringste Auflösung laut calculate_stunden ist 18 Sekunden.
        """
        if self.startzeit and self.endzeit:
            if float(self.stunden()) <= 0.00:
                raise ValidationError("Die Endzeit muss nach der Startzeit liegen!")

    def __str__(self):
        return str(self.firma)

    class Meta:
        verbose_name = "Stunden Aufzeichnung"
        verbose_name_plural = "Stunden Aufzeichnungen"


class Einstellungen(models.Model):
    """
    Das ORM Model für Einstellungen.
    """
    ust = models.IntegerField(blank=False, default=20)

    def __str__(self):
        return str(self.ust)

    class Meta:
        verbose_name = "Einstellungen"
        verbose_name_plural = "Einstellungen"


class Rechnungsnummer(models.Model):
    """
    Das ORM Model für Einstellungen.
    """
    rechnungsnummer = models.CharField(max_length=200, blank=True)
    rechnungsnummer_datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rechnungsnummer)

    class Meta:
        verbose_name = "Rechnungsnummer"
        verbose_name_plural = "Rechnungsnummern"
