# webpystunden3
webpystunden3 ist eine Python3 - Django (2.0) Webapp zum Aufzeichnen von Stunden und zur
automatischen PDF Rechnungs Erstellung. Besonders geeignet für IT Freelancer, Selbstständige
und kleinere Betriebe.

## Features

* Erstellung von Stundenaufzeichnungen, Firmen und Arbeitnehmern
* Erstellung von PDF Rechnungen mit eingebetteter Stundentabelle
* JSON Daten Export
* JSON Daten Import
* Tests vorhanden

## Verwendete Technologien

* Python
* Django
* Reportlab
* jQuery
* Bootstrap

## Installation

In einem Linux Terminal mit Python 3.5.x, virtualenv und git installiert:
```
mkdir webpystunden3
cd webpystunden3
virtualenv -p python3 webpystunden3

cd webpystunden3
source bin/activate

git clone https://github.com/martinfischer/webpystunden3.git

cd webpystunden3
pip install -r requirements.txt

mv webpystunden3/example-settings.py webpystunden3/settings.py
nano webpystunden3/settings.py
(Folgende Einstellungen zuerst entkommentieren und ändern: ADMINS und SECRET_KEY)

python manage.py makemigrations stunden
python manage.py migrate

python manage.py createsuperuser
(Hier einen Superuser erstellen!)

python manage.py test stunden
python manage.py runserver

http://127.0.0.1:8000/ öffnen und mit Superuser einloggen.
```

## Screenshots

![webpystunden3 login](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_01.png)
---
![webpystunden3 index](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_02.png)
---
![webpystunden3 neu mit datepicker](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_03.png)
---
![webpystunden3 neu mit timepicker](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_04.png)
---
![webpystunden3 rechnung](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_05.png)
---
![webpystunden3 json export](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_06.png)
---
![webpystunden3 json import](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_07.png)
---
![webpystunden3 einstellungen](https://raw.github.com/martinfischer/webpystunden3/master/screenshots/webpystunden3_screenshot_08.png)

## Lizenz

MIT
