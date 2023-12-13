import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# Etape 1
# définition de la fonction List
def List(texte):
    words = texte.split()
    occurs = []
# Remplissage de la liste occurs
    for word in words:
        occurs.append(words.count(word))
# création d'une list à partir d'un dictionnaire
    dual = list(zip(words, occurs))
# Triage de couple selon l'ordre décroissant des ocurrences
    dual.sort(key=lambda i: i[1], reverse=True)
# affichage des listes words, occurs et dual
    print(dual)
    return (dual)


# Etape 2
def cleaner(dual, parasites):
    cleared = [tup for tup in dual if not ((set(parasites) & set(tup)))]
    print(cleared)
    return (cleared)


# Etape 3
def getparasites():
    parasite = open(r"C:\L3\Cours_de_python\Projets\parasite.csv")
    vision = csv.reader(parasite)
    for row in vision:
        print(row)
    return (row)


# Etape 5
def remove_balise(text_html):
    txt = BeautifulSoup(text_html, 'html.parser')
    newtxt = txt.get_text(separator="", strip=True)
    print(newtxt)
    return (newtxt)


# Etape 6
def balise(text_html, tagname, attributes):
    content = []
    soup = BeautifulSoup(text_html, 'html.parser')
    tags = soup.find_all(tagname)
    for tag in tags:
        value = tag.get(attributes)
        if value:
            content.append(value)
    return (content)


# Etape 8
def getdomain(url):
    try:
        parsed_url = urlparse(url)
        return (parsed_url).netloc
    except Exception as e:
        print(f"Erreur : {e}")
        return (None)


# Etape 9
def checkdomain(urls, domain):
    in_domain = []
    out_domain = []
    for url in urls:
        v = getdomain(url)
        if v == domain:
            in_domain.append(url)
        else:
            out_domain.append(url)
    print(in_domain)
    print(out_domain)
    return (in_domain, out_domain)


# Etape 10
def get_html(url):
    try:
        r = requests.get(url)
        print("HTML:\n", r.text)
        return (r)
    except:
        print("Invalid URL or some error occured while making the GET request to the specified URL")
        return (None)


# Etape 11
def checkdomain_11(urls, domain):
    in_domain = 0
    out_domain = 0
    for url in urls:
        v = getdomain(url)
        if v == domain:
            in_domain += 1
        else:
            out_domain += 1
    print(in_domain)
    print(out_domain)
    return (in_domain, out_domain)


# Etape 11
def url_control(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            return (True)
        else:
            return (False)
    except:
        return (False)


# variables stockant le texte
x = "I'm only happy when it's rains I'm only happy when it's rains rains"
y = ["le", "la", "les", "only"]
z = "<Title> Hello Abdelkrim </Title>"
url = "https://esiee-it.blackboard.com/"
fakes = "https://esiee-it.blackboard.fr/", "https://www.youtube.com/watch?v=MOItX2aKTGc&t=15s", "https://web.whatsapp.com/"
domain = "www.youtube.com"
tagbalise = "a"
attributs = "href"
html_doc = """

<Html>
<Body>
    <a href="https://www.google.com">Google</a>
    <a href="https://www.python.org">Python</a>
    <a> no href </a>
</Body>
</Html>
"""
# appel des fonctions
# parasites = getparasites()
# cleared_texte = cleaner(result, y)
# without_balise = remove_balise(z)
# liste = balise(html_doc, tagbalise, attributs)
domain_name = getdomain(url)
print(f"Nom de domaine extrait : {domain_name}" if domain_name else "impossible d'afficher le nom de domaine")
filtre_domain = checkdomain(fakes, domain)

a = input("veuillez saisir une url : ")
checkurl = url_control(a)
html = get_html(a)
# result = List(html)
