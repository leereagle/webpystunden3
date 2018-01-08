import json
from .models import StundenAufzeichnung, Firma, Arbeitnehmer
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, time, datetime


class TestIndex(TestCase):
    """
    Testet den index View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_redirect_status_code_when_not_loged_in(self):
        """
        Testet den Redirect Status Code, wenn der User nicht
        angemeldet ist.
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)

    def test_redirect_url_when_not_loged_in(self):
        """
        Testet den Redirect auf "/login/?next=/", wenn der User nicht
        angemeldet ist.
        """
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, reverse("login") + "?next=/")

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_response_context(self):
        """
        Testet ob der Context aufrufbar ist und ob die Daten stimmen.
        Die Daten kommen aus den Fixtures.
        """
        # Login und Request.
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("index"))

        # "stunden" muss im Context sein.
        self.assertTrue("stundenaufzeichnung" in response.context)

        # Laut Fixtures müssen 5 Primary Keys im Context sein.
        pk = [stunden.pk for stunden in response.context["stundenaufzeichnung"]]
        self.assertEqual(pk, [5, 4, 3, 2, 1])

        # Laut Fixtures müssen diese 2 Firmen im Context sein.
        firma = set([stunden.firma.firma for stunden in response.context["stundenaufzeichnung"]])
        firma_expected = set(["Monty Python", "Monty Python Music"])
        self.assertEqual(firma, firma_expected)

        # Laut Fixtures muss ein Arbeitnehmer im Context sein.
        arbeitnehmer = set(
            [stunden.arbeitnehmer.name for stunden in response.context["stundenaufzeichnung"]]
        )
        self.assertEqual(arbeitnehmer, set(["Michael Palin"]))

        # Laut Fixture müssen insgesamt 15 Stunden im Context sein.
        stunden = sum([float(stunden.stunden) for stunden in
                       response.context["stundenaufzeichnung"]])
        self.assertEqual(stunden, 15)


class TestLogIn(TestCase):
    """
    Testet den log_in View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """
        Testet den Login per POST Request.
        """
        # Einloggen und überprüfen, ob die Umleitung zum index funktioniert
        username_password = {"username": "admin", "password": "admin"}
        response = self.client.post(reverse("login"), username_password)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

        # "/jsonimport/" aufrufen versuchen
        response = self.client.get(reverse("jsonimport"))
        self.assertEqual(response.status_code, 200)

    def test_login_bad_credentials(self):
        """
        Testet den Login mit falschem Passwort.
        """
        # Falsches Passwort. Kein Redirect und ein Fehler wird angezeigt.
        username_password = {"username": "admin", "password": "istfalsch"}
        response = self.client.post(reverse("login"), username_password)
        self.assertEqual(response.status_code, 200)
        error_message = "Login fehlgeschlagen. Bitte nochmals versuchen."
        self.assertEqual(error_message, response.context["error"])

        # "/jsonimport/" aufrufen versuchen. Redirect muss passieren.
        response = self.client.get(reverse("jsonimport"))
        self.assertEqual(response.status_code, 302)
        next = reverse("login") + "?next=" + reverse("jsonimport")
        self.assertRedirects(response, next)


class TestLogOut(TestCase):
    """
    Testet den log_out View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_logout(self):
        """
        Testet den Login per POST Request.
        """
        # Einloggen
        username_password = {"username": "admin", "password": "admin"}
        response = self.client.post(reverse("login"), username_password)

        # "/jsonimport/" aufrufen versuchen
        response = self.client.get(reverse("jsonimport"))
        self.assertEqual(response.status_code, 200)

        # Ausloggen und überprüfen, ob die Umleitung funktioniert
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        next = reverse("login")
        self.assertRedirects(response, next)


class TestStundenAufzeichnung(TestCase):
    """
    Testet den stundenaufzeichnung View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("stundenaufzeichnung"))
        self.assertEqual(response.status_code, 200)

    def test_response_context(self):
        """
        Testet ob der Context aufrufbar ist und ob die Daten stimmen.
        Die Daten kommen aus den Fixtures.
        """
        # Login und Request.
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("stundenaufzeichnung"))

        # "stundenaufzeichnung" muss im Context sein.
        self.assertTrue("stundenaufzeichnung" in response.context)

        # Laut Fixtures müssen 5 Primary Keys im Context sein.
        pk = [stunden.pk for stunden in response.context["stundenaufzeichnung"]]
        self.assertEqual(pk, [5, 4, 3, 2, 1])

        # Laut Fixtures müssen diese 2 Firmen im Context sein.
        firma = set([stunden.firma.firma for stunden in response.context["stundenaufzeichnung"]])
        firma_expected = set(["Monty Python", "Monty Python Music"])
        self.assertEqual(firma, firma_expected)

        # Laut Fixtures muss ein Arbeitnehmer im Context sein.
        arbeitnehmer = set(
            [stunden.arbeitnehmer.name for stunden in response.context["stundenaufzeichnung"]]
        )
        self.assertEqual(arbeitnehmer, set(["Michael Palin"]))


class TestStundenAufzeichnungNeu(TestCase):
    """
    Testet den stundenaufzeichnung_neu View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("stundenaufzeichnung_neu"))
        self.assertEqual(response.status_code, 200)

    def test_post_new_entry(self):
        """
        Testet einen neuen Eintrag per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Post data
        data = {
            "datum": "29.09.2012",
            "firma": "1",
            "startzeit": "10:00",
            "endzeit": "14:30",
            "arbeitnehmer": "1",
            "protokoll": "Das ist ein Test Protokoll.",
            "bezahlt": "False",
        }
        response = self.client.post(reverse("stundenaufzeichnung_neu"), data)
        # Prüft redirect auf Index
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))
        # Prüft Daten
        stundenaufzeichnungen = StundenAufzeichnung.objects.all()
        self.assertEqual(len(stundenaufzeichnungen), 6)
        neu = StundenAufzeichnung.objects.get(pk=6)
        self.assertEqual(neu.datum, date(2012, 9, 29))
        self.assertEqual(neu.firma.firma, "Monty Python")
        self.assertEqual(neu.startzeit, time(10))
        self.assertEqual(neu.endzeit, time(14, 30))
        self.assertEqual(neu.arbeitnehmer.name, "Michael Palin")
        self.assertEqual(neu.protokoll, "Das ist ein Test Protokoll.")
        self.assertEqual(neu.bezahlt, False)

    def test_post_validation_empty_data(self):
        """
        Testet die Validation mit falschen Daten per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Post empty_data
        empty_data = {
            "datum": "",
            "firma": "",
            "startzeit": "",
            "endzeit": "",
            "arbeitnehmer": "",
            "protokoll": "",
            "bezahlt": "",
        }
        response = self.client.post(reverse("stundenaufzeichnung_neu"), empty_data)
        # Prüft Status Code, darf kein Redirect sein.
        self.assertEqual(response.status_code, 200)
        # Prüft Daten
        stundenaufzeichnungen = StundenAufzeichnung.objects.all()
        self.assertEqual(len(stundenaufzeichnungen), 5)
        self.assertFormError(
            response,
            "form",
            "datum",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(
            response,
            "form",
            "firma",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(
            response,
            "form",
            "startzeit",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(
            response,
            "form",
            "endzeit",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(
            response,
            "form",
            "arbeitnehmer",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(
            response,
            "form",
            "protokoll",
            ["Dieses Feld ist zwingend erforderlich."]
        )

    def test_post_validation_bad_data(self):
        """
        Testet die Validation mit falschen Daten per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Prüft bad_data
        bad_data = {
            "datum": "42.42.4242",
            "firma": "42",
            "startzeit": "42:42",
            "endzeit": "Forty:Two",
            "arbeitnehmer": "42",
            "protokoll": "",
            "bezahlt": "True",
        }
        response = self.client.post(reverse("stundenaufzeichnung_neu"), bad_data)
        # Prüft Status Code, darf kein Redirect sein.
        self.assertEqual(response.status_code, 200)
        # Prüft Daten
        stundenaufzeichnungen = StundenAufzeichnung.objects.all()
        self.assertEqual(len(stundenaufzeichnungen), 5)
        self.assertFormError(response, "form", "datum", ["Bitte ein gültiges Datum eingeben."])
        self.assertFormError(
            response,
            "form",
            "firma",
            ["Bitte eine gültige Auswahl treffen. Dies ist keine gültige Auswahl."]
        )
        self.assertFormError(
            response,
            "form",
            "startzeit",
            ["Bitte eine gültige Uhrzeit eingeben."]
        )
        self.assertFormError(
            response,
            "form",
            "endzeit",
            ["Bitte eine gültige Uhrzeit eingeben."]
        )
        self.assertFormError(
            response,
            "form",
            "arbeitnehmer",
            ["Bitte eine gültige Auswahl treffen. Dies ist keine gültige Auswahl."]
        )
        self.assertFormError(
            response,
            "form",
            "protokoll",
            ["Dieses Feld ist zwingend erforderlich."]
        )


class TestStundenAufzeichnungBearbeiten(TestCase):
    """
    Testet den stundenaufzeichnung_bearbeiten View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse("stundenaufzeichnung_bearbeiten",
            kwargs={"stundenaufzeichnung_id": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_data_in_context(self):
        """
        Testet das Bearbeiten eines fixture Eintrages.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Hole den Eintrag mit ID 1
        response = self.client.get(
            reverse("stundenaufzeichnung_bearbeiten",
            kwargs={"stundenaufzeichnung_id": 1})
        )
        # Status Code OK
        self.assertEqual(response.status_code, 200)
        # Überprüfe, ob die Daten aus den Fixtures im Context sind.
        self.assertTrue("Protokoll 1" in str(response.context["form"]["protokoll"]))
        self.assertTrue("10:00" in str(response.context["form"]["startzeit"]))
        self.assertTrue("12:00" in str(response.context["form"]["endzeit"]))
        self.assertTrue("22.09.2012" in str(response.context["form"]["datum"]))


class TestFirma(TestCase):
    """
    Testet den firma View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("firma"))
        self.assertEqual(response.status_code, 200)

    def test_response_context(self):
        """
        Testet ob der Context aufrufbar ist und ob die Daten stimmen.
        Die Daten kommen aus den Fixtures.
        """
        # Login und Request.
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("firma"))

        # "firma" muss im Context sein.
        self.assertTrue("firma" in response.context)

        # Laut Fixtures müssen 2 Primary Keys im Context sein.
        pk = [firma.pk for firma in
              response.context["firma"]]
        self.assertEqual(pk, [1, 2])

        # Laut Fixtures müssen diese 2 Firmen im Context sein.
        firma = set([firma.firma for firma in response.context["firma"]])
        firma_expected = set(["Monty Python", "Monty Python Music"])
        self.assertEqual(firma, firma_expected)


class TestFirmaNeu(TestCase):
    """
    Testet den firma_neu View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("stundenaufzeichnung_neu"))
        self.assertEqual(response.status_code, 200)

    def test_post_new_entry(self):
        """
        Testet einen neuen Eintrag per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Post data
        data = {
            "firma": "Monty Python Movies",
            "name": "Graham Chapman",
            "adresse": "Luxery Jacht Nr. 5",
            "plz": "08150",
            "ort": "Mongrove",
            "land": "England",
            "uid": "UID: 15423672882",
        }
        response = self.client.post(reverse("firma_neu"), data)
        # Prüft redirect auf stundenaufzeichnung_neu
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("stundenaufzeichnung_neu"))
        # Prüft Daten
        firma = Firma.objects.all()
        self.assertEqual(len(firma), 3)
        neu = Firma.objects.get(pk=3)
        self.assertEqual(neu.firma, "Monty Python Movies")
        self.assertEqual(neu.name, "Graham Chapman")
        self.assertEqual(neu.adresse, "Luxery Jacht Nr. 5")
        self.assertEqual(neu.plz, "08150")
        self.assertEqual(neu.ort, "Mongrove")
        self.assertEqual(neu.land, "England")
        self.assertEqual(neu.uid, "UID: 15423672882")

    def test_post_validation_empty_data(self):
        """
        Testet die Validation mit falschen Daten per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Post empty_data
        empty_data = {
            "firma": "",
            "name": "",
            "adresse": "",
            "plz": "",
            "ort": "",
            "land": "",
            "uid": "",
        }
        response = self.client.post(reverse("firma_neu"), empty_data)
        # Prüft Status Code, darf kein Redirect sein.
        self.assertEqual(response.status_code, 200)
        # Prüft Daten
        stundenaufzeichnungen = Firma.objects.all()
        self.assertEqual(len(stundenaufzeichnungen), 2)
        self.assertFormError(
            response,
            "form",
            "firma",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(response, "form", "name", None)
        self.assertFormError(response, "form", "adresse", None)
        self.assertFormError(response, "form", "plz", None)
        self.assertFormError(response, "form", "ort", None)
        self.assertFormError(response, "form", "land", None)
        self.assertFormError(response, "form", "uid", None)

    def test_post_validation_bad_data(self):
        """
        Testet die Validation mit falschen Daten per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Prüft bad_data
        bad_data = {
            "firma": "Monty Python",
            "name": "",
            "adresse": "",
            "plz": "",
            "ort": "",
            "land": "",
            "uid": "",
        }
        response = self.client.post(reverse("firma_neu"), bad_data)
        # Prüft Status Code, darf kein Redirect sein.
        self.assertEqual(response.status_code, 200)
        # Prüft Daten
        firma = Firma.objects.all()
        self.assertEqual(len(firma), 2)
        self.assertFormError(
            response,
            "form",
            "firma",
            ["Firma mit diesem Firmen Namen existiert bereits."]
        )
        self.assertFormError(response, "form", "name", None)
        self.assertFormError(response, "form", "adresse", None)
        self.assertFormError(response, "form", "plz", None)
        self.assertFormError(response, "form", "ort", None)
        self.assertFormError(response, "form", "land", None)
        self.assertFormError(response, "form", "uid", None)


class TestFirmaBearbeiten(TestCase):
    """
    Testet den firma_bearbeiten View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("firma_bearbeiten", kwargs={"firma_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_data_in_context(self):
        """
        Testet das Bearbeiten eines fixture Eintrages.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Hole den Eintrag mit ID 1
        response = self.client.get(reverse("firma_bearbeiten", kwargs={"firma_id": 1}))
        # Status Code OK
        self.assertEqual(response.status_code, 200)
        # Überprüfe, ob die Daten aus den Fixtures im Context sind.
        self.assertTrue("Great Britain" in str(response.context["form"]["land"]))
        self.assertTrue("John Cleese" in str(response.context["form"]["name"]))
        self.assertTrue("Silly Walk Street 42" in str(response.context["form"]["adresse"]))
        self.assertTrue("Monty Python" in str(response.context["form"]["firma"]))


class TestArbeitnehmer(TestCase):
    """
    Testet den arbeitnehmer View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("arbeitnehmer"))
        self.assertEqual(response.status_code, 200)

    def test_response_context(self):
        """
        Testet ob der Context aufrufbar ist und ob die Daten stimmen.
        Die Daten kommen aus den Fixtures.
        """
        # Login und Request.
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("arbeitnehmer"))

        # "arbeitnehmer" muss im Context sein.
        self.assertTrue("arbeitnehmer" in response.context)

        # Laut Fixtures muss 1 Primary Key im Context sein.
        pk = [arbeitnehmer.pk for arbeitnehmer in response.context["arbeitnehmer"]]
        self.assertEqual(pk, [1])

        # Laut Fixtures müssen diese 2 Firmen im Context sein.
        arbeitnehmer = set(
            [arbeitnehmer.name for arbeitnehmer in response.context["arbeitnehmer"]]
        )
        arbeitnehmer_expected = set(["Michael Palin"])
        self.assertEqual(arbeitnehmer, arbeitnehmer_expected)


class TestArbeitnehmerNeu(TestCase):
    """
    Testet den arbeitnehmer_neu View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("arbeitnehmer_neu"))
        self.assertEqual(response.status_code, 200)

    def test_post_new_entry(self):
        """
        Testet einen neuen Eintrag per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Post data
        data = {
            "name": "Graham Chapman",
            "adresse": "Luxery Jacht Nr. 5",
            "plz": "08150",
            "ort": "Mongrove",
            "land": "England",
            "uid": "UID: 15423672882",
            "bank_name": "Bank of Banks",
            "bank_iban": "AT000000000000000",
            "bank_bic": "XXXXXXXXXXX",
        }
        response = self.client.post(reverse("arbeitnehmer_neu"), data)
        # Prüft redirect auf stundenaufzeichnung_neu
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("stundenaufzeichnung_neu"))
        # Prüft Daten
        arbeitnehmer = Arbeitnehmer.objects.all()
        self.assertEqual(len(arbeitnehmer), 2)
        neu = Arbeitnehmer.objects.get(pk=2)
        self.assertEqual(neu.name, "Graham Chapman")
        self.assertEqual(neu.adresse, "Luxery Jacht Nr. 5")
        self.assertEqual(neu.plz, "08150")
        self.assertEqual(neu.ort, "Mongrove")
        self.assertEqual(neu.land, "England")
        self.assertEqual(neu.uid, "UID: 15423672882")
        self.assertEqual(neu.bank_name, "Bank of Banks")
        self.assertEqual(neu.bank_iban, "AT000000000000000")
        self.assertEqual(neu.bank_bic, "XXXXXXXXXXX")

    def test_post_validation_empty_data(self):
        """
        Testet die Validation mit falschen Daten per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Post empty_data
        empty_data = {
            "name": "",
            "adresse": "",
            "plz": "",
            "ort": "",
            "land": "",
            "uid": "",
            "bank_name": "",
            "bank_iban": "",
            "bank_bic": "",
        }
        response = self.client.post(
            reverse("arbeitnehmer_neu"),
            empty_data
        )
        # Prüft Status Code, darf kein Redirect sein.
        self.assertEqual(response.status_code, 200)
        # Prüft Daten
        stundenaufzeichnungen = Arbeitnehmer.objects.all()
        self.assertEqual(len(stundenaufzeichnungen), 1)
        self.assertFormError(
            response,
            "form",
            "name",
            ["Dieses Feld ist zwingend erforderlich."]
        )
        self.assertFormError(response, "form", "adresse", None)
        self.assertFormError(response, "form", "plz", None)
        self.assertFormError(response, "form", "ort", None)
        self.assertFormError(response, "form", "land", None)
        self.assertFormError(response, "form", "uid", None)
        self.assertFormError(response, "form", "bank_name", None)
        self.assertFormError(response, "form", "bank_iban", None)
        self.assertFormError(response, "form", "bank_bic", None)

    def test_post_validation_bad_data(self):
        """
        Testet die Validation mit falschen Daten per POST Request.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Prüft bad_data
        bad_data = {
            "name": "Michael Palin",
            "adresse": "Luxery Jacht Nr. 5",
            "plz": "08150",
            "ort": "Mongrove",
            "land": "England",
            "uid": "UID: 15423672882",
            "bank_name": "Bank of Banks",
            "bank_iban": "AT000000000000000",
            "bank_bic": "XXXXXXXXXXX",
        }
        response = self.client.post(reverse("arbeitnehmer_neu"), bad_data)
        # Prüft Status Code, darf kein Redirect sein.
        self.assertEqual(response.status_code, 200)
        # Prüft Daten
        arbeitnehmer = Arbeitnehmer.objects.all()
        self.assertEqual(len(arbeitnehmer), 1)
        self.assertFormError(
            response,
            "form",
            "name",
            ["Arbeitnehmer mit diesem Name existiert bereits."]
        )
        self.assertFormError(response, "form", "adresse", None)
        self.assertFormError(response, "form", "plz", None)
        self.assertFormError(response, "form", "ort", None)
        self.assertFormError(response, "form", "land", None)
        self.assertFormError(response, "form", "uid", None)
        self.assertFormError(response, "form", "bank_name", None)
        self.assertFormError(response, "form", "bank_iban", None)
        self.assertFormError(response, "form", "bank_bic", None)


class TestArbeitnehmerBearbeiten(TestCase):
    """
    Testet den arbeitnehmer_bearbeiten View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            reverse("arbeitnehmer_bearbeiten",
            kwargs={"arbeitnehmer_id": 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_data_in_context(self):
        """
        Testet das Bearbeiten eines fixture Eintrages.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # Hole den Eintrag mit ID 1
        response = self.client.get(
            reverse("arbeitnehmer_bearbeiten",
            kwargs={"arbeitnehmer_id": 1})
        )
        # Status Code OK
        self.assertEqual(response.status_code, 200)
        # Überprüfe, ob die Daten aus den Fixtures im Context sind.
        self.assertTrue("Österreich" in str(response.context["form"]["land"]))
        self.assertTrue("Michael Palin" in str(response.context["form"]["name"]))
        self.assertTrue("Innsbruckerstraße 42" in str(response.context["form"]["adresse"]))
        self.assertTrue("AT000000000000000000" in str(response.context["form"]["bank_iban"]))


class TestRechnung(TestCase):
    """
    Testet den rechnung View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("rechnung"))
        self.assertEqual(response.status_code, 200)

    def test_unbezahlt_im_context(self):
        """
        Testet, ob die unbezahlten Einträge im Context sind.
        """
        # Login und Request
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("rechnung"))

        # Überprüfe, ob die unbezahlten Daten aus den Fixtures im Context sind.
        self.assertTrue("stunden_not_payed" in response.context)

        # Laut Fixtures müssen 3 Primary Keys im Context sein.
        pk = [stunden.pk for stunden in response.context["stunden_not_payed"]]
        self.assertEqual(pk, [5, 3, 2])

        # Laut Fixtures müssen diese 3 Firmen im Context sein.
        protokoll = [stunden.protokoll for stunden in response.context["stunden_not_payed"]]
        protokoll_expected = ["Protokoll 5", "Protokoll 3", "Protokoll 2"]
        self.assertEqual(protokoll, protokoll_expected)

    def test_post_data(self):
        """
        Testet mit POST data und schaut, ob das PDF erstellt wurde.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # POST
        data = {
            "checks[]": [5, 3, 2],
            "firma": 1,
            "rechnungs_nummer": "IT-0815",
            "rechnungs_titel": "Programmierung November",
            "rechnungs_stundenlohn": 50,
            "meine_daten": 1
        }
        response = self.client.post(reverse("rechnung"), data)
        self.assertEqual(response.status_code, 200)
        # Prüft, ob ein PDF attachment mit dem richtigem filename existiert.

        self.assertEqual(
            response.get("Content-Disposition"),
            'attachment; filename="Rechnung_IT-0815_mfs_{}.pdf"'.format(date.today().isoformat())
        )


class TestRechnungSumme(TestCase):
    """
    Testet den rechnung_summe View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("rechnungsumme"))
        self.assertEqual(response.status_code, 200)

    def test_post_data(self):
        """
        Testet mit POST data und schaut, ob das PDF erstellt wurde.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # POST
        data = {
            "firma": 1,
            "rechnungs_nummer": "IT-0815",
            "rechnungs_titel": "Programmierung November",
            "rechnungs_summe": 1000,
            "meine_daten": 1
        }
        response = self.client.post(reverse("rechnungsumme"), data)
        self.assertEqual(response.status_code, 200)
        # Prüft, ob ein PDF attachment mit dem richtigem filename existiert.
        self.assertEqual(
            response.get("Content-Disposition"),
            'attachment; filename="Rechnung_IT-0815_mfs_{}.pdf"'.format(date.today().isoformat())
        )


class TestJSONExport(TestCase):
    """
    Testet den jsonexport View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("jsonexport"))
        self.assertEqual(response.status_code, 200)

    def test_post_data(self):
        """
        Testet mit POST data und schaut, ob das PDF erstellt wurde.
        """
        # Login
        self.client.login(username="admin", password="admin")
        # POST
        response = self.client.post(reverse(
            "jsonexport"),
            {"json_export_select": "json_export_select_stundenaufzeichnung"}
        )
        self.assertEqual(response.status_code, 200)
        jetzt = datetime.now().strftime("%Y-%m-%d--%H-%M")
        # Prüft, ob ein JSON attachment mit dem richtigem filename existiert.
        self.assertEqual(
            response.get("Content-Disposition"),
            'attachment; filename=webpystunden3-export--stundenaufzeichnung--{}.json'.format(jetzt)
        )


class TestJSONImport(TestCase):
    """
    Testet den jsonimport View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("jsonimport"))
        self.assertEqual(response.status_code, 200)


class TestJSONImportSuccess(TestCase):
    """
    Testet den jsonimport_success View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        data = {"count_import": 3,}
        response = self.client.get(reverse("jsonimport_success", kwargs=data))
        self.assertEqual(response.status_code, 200)


class TestEinstellungen(TestCase):
    """
    Testet den Einstellungen View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("einstellungen"))
        self.assertEqual(response.status_code, 200)


class TestGetFirmaStundensatz(TestCase):
    """
    Testet den get_firma_stundensatz View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("get_firma_stundensatz", args=["1"]))
        self.assertEqual(response.status_code, 200)


class TestRechnungsnummer(TestCase):
    """
    Testet den Rechnungsnummer View.
    """

    fixtures = ["webpystunden3_testdata.json"]

    def setUp(self):
        """
        Das setUp läuft vor den Tests.
        """
        admin = User.objects.create_user("admin", "admin@admin.com", "admin")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

    def test_response_status_code(self):
        """
        Testet den Status Code.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("rechnungsnummer"))
        self.assertEqual(response.status_code, 200)
