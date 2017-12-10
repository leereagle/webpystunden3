from django.urls import re_path, include
from django.contrib import admin
from stunden import views as stunden_views


# Die Admin Seite.
admin.autodiscover()


urlpatterns = [
    # 'stunden.views',
    # Home
    re_path(r'^$', stunden_views.index, name="index"),

    # Login und Logout
    re_path(r'^login/$', stunden_views.log_in, name="login"),
    re_path(r'^logout/$', stunden_views.log_out, name="logout"),

    # Rechnungen
    re_path(r'^rechnung/$', stunden_views.rechnung, name="rechnung"),
    re_path(r'^rechnungsumme/$', stunden_views.rechnung_summe, name="rechnungsumme"),

    # JSON Export
    re_path(r'^jsonexport/$', stunden_views.jsonexport, name="jsonexport"),

    # JSON Import und Success Seite
    re_path(r'^jsonimport/$', stunden_views.jsonimport, name="jsonimport"),
    re_path(
        r'^jsonimport/success/(?P<count_import>\d+)/$',
        stunden_views.jsonimport_success,
        name="jsonimport_success"
    ),

    # Stundenaufzeichnung, neu und bearbeiten
    re_path(r'^stundenaufzeichnung/$', stunden_views.stundenaufzeichnung, name="stundenaufzeichnung"),
    re_path(
        r'^stundenaufzeichnung/neu/$',
        stunden_views.stundenaufzeichnung_neu,
        name="stundenaufzeichnung_neu"
    ),
    re_path(
        r'^stundenaufzeichnung/(?P<stundenaufzeichnung_id>\d+)/$',
        stunden_views.stundenaufzeichnung_bearbeiten,
        name="stundenaufzeichnung_bearbeiten"
    ),

    # Firma, neu und bearbeiten
    re_path(r'^firma/$', stunden_views.firma, name="firma"),
    re_path(r'^firma/neu/$', stunden_views.firma_neu, name="firma_neu"),
    re_path(r'^firma/(?P<firma_id>\d+)/$', stunden_views.firma_bearbeiten, name="firma_bearbeiten"),

    # Arbeitnehmer, neu und bearbeiten
    re_path(r'^arbeitnehmer/$', stunden_views.arbeitnehmer, name="arbeitnehmer"),
    re_path(r'^arbeitnehmer/neu/$', stunden_views.arbeitnehmer_neu, name="arbeitnehmer_neu"),
    re_path(
        r'^arbeitnehmer/(?P<arbeitnehmer_id>\d+)/$',
        stunden_views.arbeitnehmer_bearbeiten,
        name="arbeitnehmer_bearbeiten"
    ),

    # Einstellungen
    re_path(r'^einstellungen/$', stunden_views.einstellungen, name="einstellungen"),

    # Rechnung Firma-Checkbox-Auswahl Stundensatz Eintrag
    re_path(
        r'^get_firma_stundensatz/(?P<selected_firma_id>\d+)/$',
        stunden_views.get_firma_stundensatz,
        name="get_firma_stundensatz"
    ),

    # Einstellungen
    re_path(r'^rechnungsnummer/$', stunden_views.rechnungsnummer, name="rechnungsnummer"),

    # Admin
    re_path(r'^admin/', admin.site.urls),
]
