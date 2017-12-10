from .models import StundenAufzeichnung, Firma, Arbeitnehmer, Einstellungen, Rechnungsnummer
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site


# Deregistriert das Site Model
admin.site.unregister(Site)

# Deregistriert das Group Model
admin.site.unregister(Group)


class StundenAufzeichnungAdmin(admin.ModelAdmin):
    """
    Das Admin Model für StundenAufzeichnung.
    Fügt die mark_bezahlt und mark_unbezahlt Admin Aktionen hinzu.
    """
    list_display = (
        "datum",
        "firma",
        "startzeit",
        "endzeit",
        "arbeitnehmer",
        "protokoll",
        "stunden",
        "bezahlt"
    )
    list_filter = ["datum", "firma", "bezahlt"]
    date_hierarchy = "datum"
    ordering = ["-datum", "-startzeit"]

    def mark_bezahlt(self, request, queryset):
        """
        Admin Aktion, die Einträge als bezahlt markiert.
        """
        rows_updated = queryset.update(bezahlt=True)
        if rows_updated == 1:
            result = "1 Eintrag wurde"
        else:
            result = "{} Einträge wurden".format(rows_updated)
        self.message_user(request, "{} erfolgreich als bezahlt markiert.".format(result))
    mark_bezahlt.short_description = "Bezahlt markieren"

    def mark_unbezahlt(self, request, queryset):
        """
        Admin Aktion, die Einträge als unbezahlt markiert.
        """
        rows_updated = queryset.update(bezahlt=False)
        if rows_updated == 1:
            result = "1 Eintrag wurde"
        else:
            result = "{} Einträge wurden".format(rows_updated)
        self.message_user(request, "{} erfolgreich als unbezahlt markiert.".format(result))
    mark_unbezahlt.short_description = "Unbezahlt markieren"

    # Fügt die Admin Aktionen hinzu.
    actions = [mark_bezahlt, mark_unbezahlt]

admin.site.register(StundenAufzeichnung, StundenAufzeichnungAdmin)


class FirmaAdmin(admin.ModelAdmin):
    """
    Das Admin Model für Firma.
    """
    list_display = (
        "firma",
        "name",
        "adresse",
        "plz",
        "ort",
        "land",
        "uid",
    )
    ordering = ["firma"]

admin.site.register(Firma, FirmaAdmin)


class ArbeitnehmerAdmin(admin.ModelAdmin):
    """
    Das Admin Model für Arbeitnehmer.
    """
    list_display = (
        "name",
        "adresse",
        "plz",
        "ort",
        "land",
        "uid",
        "bank_name",
        "bank_iban",
        "bank_bic",
    )

admin.site.register(Arbeitnehmer, ArbeitnehmerAdmin)


class EinstellungenAdmin(admin.ModelAdmin):
    """
    Das Admin Model für Einstellungen.
    """
    list_display = (
        "ust",
    )

admin.site.register(Einstellungen, EinstellungenAdmin)


class RechnungsnummerAdmin(admin.ModelAdmin):
    """
    Das Admin Model für Rechnungsnummer.
    """
    list_display = (
        "rechnungsnummer",
        "rechnungsnummer_datum",
    )

admin.site.register(Rechnungsnummer, RechnungsnummerAdmin)
