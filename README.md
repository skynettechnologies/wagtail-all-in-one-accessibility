# All in One Accessibility
-   All in One Accessibility widget improves wagtail website ADA compliance and browser experience for WCAG 2.1, ATAG 2.0, ADA, Section 508, Australian DDA, European EAA EN 301 549, UK Equality Act (EA), Israeli Standard 5568, and California Unruh standards.
-   2 Minute installation
-   Screen Reader, dynamic widget color and position, supports multiple languages (40 languages)
-   Reduces the risk of time-consuming accessibility lawsuits.
-   Use apps to connect to external services and manage data flows

It uses the accessibility interface which handles UI and design related adjustments. All in One Accessibility app enhances your wagtail website accessibility to people with hearing or vision impairments, motor impaired, color blind, dyslexia, cognitive & learning impairments, seizure and epileptic, and ADHD problems. It uses the accessibility interface which handles UI and design related adjustments.

### Supported Languages (140+ Languages):

English (USA), English (UK), English (Australian), English (Canadian), English (South Africa), Español, Español (Mexicano), Deutsch, عربى, Português, Português (Brazil), 日本語, Français, Italiano, Polski, Pусский, 中文, 中文 (Traditional), עִברִית, Magyar, Slovenčina, Suomenkieli, Türkçe, Ελληνικά, Latinus, Български, Català, Čeština, Dansk, Nederlands, हिंदी, Bahasa Indonesia, 한국인, Lietuvių, Bahasa Melayu, Norsk, Română, Slovenščina, Svenska, แบบไทย, Українська, Việt Nam, বাঙালি, සිංහල, አማርኛ, Hmoob, မြန်မာ, Eesti keel, latviešu, Cрпски, Hrvatski, ქართული, ʻŌlelo Hawaiʻi, Cymraeg, Cebuano, Samoa, Kreyòl ayisyen, Føroyskt, Crnogorski, Azerbaijani, Euskara, Tagalog, Galego, Norsk Bokmål, فارسی, ਪੰਜਾਬੀ, shqiptare, Hայերեն, অসমীয়া, Aymara, Bamanankan, беларускі, bosanski, Corsu, ދިވެހި, Esperanto, Eʋegbe, Frisian, guarani, ગુજરાતી, Hausa, íslenskur, Igbo, Gaeilge, basa jawa, ಕನ್ನಡ, қазақ, ខ្មែរ, Kinyarwanda, Kurdî, Кыргызча, ພາສາລາວ, Lingala, Luganda, lëtzebuergesch, македонски, Malagasy, മലയാളം, Malti, Maori, मराठी, Монгол, नेपाली, Sea, ଓଡିଆ, Afaan Oromoo, پښتو, Runasimi, संस्कृत, Gàidhlig na h-Alba, Sesotho, Shona, سنڌي, Soomaali, basa Sunda, kiswahili, тоҷикӣ, தமிழ், Татар, తెలుగు, ትግሪኛ, Tsonga, Türkmenler, Ride, اردو, ئۇيغۇر, o'zbek, isiXhosa, יידיש, Yoruba, Zulu, भोजपुरी, डोगरी, कोंकणी, Kurdî, Krio, मैथिली, Meiteilon, Mizo tawng, Sepedi, Ilocano.

[`all-in-one-accessibility-introduction`](https://www.youtube.com/watch?v=PPQMWSzroAA) - introduction of All in One Accessibility widget .

---

## Installation
-   Run `pip install wagtail-all-in-one-accessibility`
-   Add `wagtail.contrib.modeladmin` in `settings.INSTALLED_APPS`
-   Add `wagtail_all_in_one_accessibility` in `settings.INSTALLED_APPS`
-   Add `wagtail_all_in_one_accessibility.context_processors.admin_AIOA` in `settings.TEMPLATES context_processors`
-   Add `<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>`put this line in your base.html footer
-   Run `python manage.py migrate`
-   Run `python manage.py runserver` for Restart your application server

---

## Usage

---

### Settings.INSTALLED_APPS
Just add `wagtail_all_in_one_accessibility` and `wagtail.contrib.modeladmin,` in to your setting.INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wagtail.contrib.modeladmin',
    'wagtail_all_in_one_accessibility',
]
```

### Settings.TEMPLATES
Just add `wagtail_all_in_one_accessibility.context_processors.admin_AIOA` in your setting.TEMPLATES:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'wagtail_all_in_one_accessibility.context_processors.admin_AIOA',
            ],
        },
    },
]
```

### Base.html
Just add this tag in your base.html footer(your main template of django website) `<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>`:
```python
  <footer>
    <script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>
  </footer>
```

### Migrate
Migrate your app
```python
python manage.py migrate

```

### Restart 
Restart your app server with this command and check the admin panel the model is ready to use
```python
python manage.py runserver
```

