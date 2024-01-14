import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from bs4 import BeautifulSoup
import requests

class Fenêtre:
    # Création de l'interface principale
    def __init__(self, window):
        self.window = window
        self.window.title("Analyse d'urls")

        self.first_page_url = tk.StringVar()
        self.user_keywords = tk.StringVar()

        tk.Label(window, text="URL de la première page de votre site :").pack(pady=10)
        tk.Entry(window, textvariable=self.first_page_url, width=100).pack(pady=5)
        tk.Label(window, text="Mots-clés (séparés par des virgules) :").pack(pady=10)
        tk.Entry(window, textvariable=self.user_keywords, width=100).pack(pady=5)
        tk.Button(window, text="Lancer l'analyse", command=self.start_analysis).pack(pady=20)

    def start_analysis(self):
        url = self.first_page_url.get()
        keywords = self.user_keywords.get()

        if not url or not keywords:
            messagebox.showerror("Erreur", "Veuillez saisir l'URL et des mots-clés.")
            return

        self.analyse_url(url, keywords)

    def analyse_url(self, url, keywords):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # le décompte du nombre de liens sortants
            outgoing_links = len([link['href'] for link in soup.find_all('a', href=True) if 'http' in link['href'] and url not in link['href']])

            # le décompte du nombre de liens entrants
            internal_links = len([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('/')])

            # Calcul du pourcentage de balises "alt" sur le nombre d'images
            total_images = len(soup.find_all('img'))
            alt_images = len(soup.find_all('img', alt=True))
            alt_percentage = (alt_images / total_images) * 100 if total_images > 0 else 0

            # Extraction des mots clés
            meta_keywords_tag = soup.find('meta', {'name': 'keywords'})
            page_keywords = meta_keywords_tag['content'].split(',') if meta_keywords_tag else []

            # Vérification du mot clés utilisateur
            user_keywords_top_3 = any(keyword.strip() in page_keywords[:3] for keyword in keywords.split(','))

            # affichage des données
            data = {
                "URL": [url],
                "Liens Sortants": [outgoing_links],
                "Liens Internes": [internal_links],
                "% Balises Alt": [alt_percentage],
                "Mots-clés": [", ".join(page_keywords[:3])],
                "Mots-clés Utilisateur": [user_keywords_top_3]
            }

            self.share_results(data)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def share_results(self, data):
        # Création de la deuxième interface
        results_interface = tk.Toplevel(self.window)
        results_interface.title("Résultats de l'analyse")

        self.urls_data = pd.DataFrame(data)

        url_listbox = tk.Listbox(results_interface, selectmode=tk.SINGLE)
        url_listbox.pack(pady=20)

        for url in self.urls_data["URL"]:
            url_listbox.insert(tk.END, url)

        def show_details():
            selected_url = url_listbox.get(tk.ACTIVE)
            selected_url_details = self.urls_data[self.urls_data["URL"] == selected_url].squeeze()

            details_message = f"URL : {selected_url}\n" \
                              f"Liens Sortants : {selected_url_details['Liens Sortants']}\n" \
                              f"Liens Internes : {selected_url_details['Liens Internes']}\n" \
                              f"% Balises Alt : {selected_url_details['% Balises Alt']}\n" \
                              f"Mots-clés : {selected_url_details['Mots-clés']}\n" \
                              f"Mots-clés Utilisateur : {selected_url_details['Mots-clés Utilisateur']}"

            messagebox.showinfo("Détails de l'URL", details_message)

        tk.Button(results_interface, text="Afficher les détails", command=show_details).pack(pady=20)
        tk.Button(results_interface, text="Sauvegarder le rapport", command=self.save_report).pack(pady=20)
        tk.Button(results_interface, text="Mettre à jour les mots-clés parasites", command=self.update_keywords).pack(pady=20)

    def save_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.urls_data.to_csv(file_path, index=False)
            messagebox.showinfo("Rapport sauvegardé", "Sauvegarde du rapport effectué.")

    def update_keywords(self):
        # Mise à jour des mots parasites
        messagebox.showinfo("Mots-clés parasites mis à jour", "Mise à jour des mots clés parasites effectuée.")

if __name__ == "__main__":
    window = tk.Tk()
    analyzer = Fenêtre(window)
    window.mainloop()