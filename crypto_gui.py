"""
Module GUI pour l'outil de cryptographie.

Fournit une interface graphique moderne utilisant CustomTkinter pour chiffrer
et déchiffrer du texte, avec un guide utilisateur intégré.
"""
import sys
import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk
import markdown
from tkhtmlview import HTMLLabel

import crypto_utils

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def get_resource_path(relative_path: str) -> str:
    """
    Obtient le chemin absolu vers une ressource, compatible avec PyInstaller.

    Args:
        relative_path: Le chemin relatif du fichier ressource.

    Returns:
        Le chemin absolu vers la ressource.
    """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


class CryptoGUI(ctk.CTk):
    """
    Fenêtre principale de l'application de cryptographie.
    """

    def __init__(self) -> None:
        """Initialise la fenêtre principale et configure l'interface."""
        super().__init__()
        
        self.title("Outil Crypto - Interface Graphique")
        self.geometry("900x700")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Crypto Prog", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.tool_button = ctk.CTkButton(
            self.sidebar_frame, text="Outil de Chiffrement", command=self.show_tool_frame
        )
        self.tool_button.grid(row=1, column=0, padx=20, pady=10)

        self.guide_button = ctk.CTkButton(
            self.sidebar_frame, text="Guide Utilisateur", command=self.show_guide_frame
        )
        self.guide_button.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Thème:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- Main Frame Containers ---
        self.tool_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.guide_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.setup_tool_ui()
        self.setup_guide_ui()

        # Show default frame
        self.show_tool_frame()

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        """Change le thème de l'application."""
        ctk.set_appearance_mode(new_appearance_mode)

    def show_tool_frame(self) -> None:
        """Affiche le frame principal de l'outil de cryptographie."""
        self.guide_frame.grid_forget()
        self.tool_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.tool_frame.grid_columnconfigure(0, weight=1)
        self.tool_frame.grid_rowconfigure(2, weight=1)
        self.tool_frame.grid_rowconfigure(4, weight=1)

    def show_guide_frame(self) -> None:
        """Affiche le frame du guide utilisateur."""
        self.tool_frame.grid_forget()
        self.guide_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.guide_frame.grid_columnconfigure(0, weight=1)
        self.guide_frame.grid_rowconfigure(1, weight=1)

    def setup_tool_ui(self) -> None:
        """Configure les éléments d'interface de l'outil de chiffrement."""
        # Algorithm Selection
        self.algo_frame = ctk.CTkFrame(self.tool_frame)
        self.algo_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.algo_frame.grid_columnconfigure(0, weight=1)

        algo_label = ctk.CTkLabel(
            self.algo_frame, text="1. Choisissez l'algorithme", font=ctk.CTkFont(weight="bold")
        )
        algo_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.algo_var = tk.StringVar(value="caesar")
        
        radio_frame = ctk.CTkFrame(self.algo_frame, fg_color="transparent")
        radio_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        algorithms = [
            ("César", "caesar"),
            ("Affine", "affine"),
            ("Vigenère", "vigenere"),
            ("RSA", "rsa"),
            ("DES", "des"),
            ("AES", "aes"),
        ]

        for i, (text, val) in enumerate(algorithms):
            rb = ctk.CTkRadioButton(
                radio_frame,
                text=text,
                variable=self.algo_var,
                value=val,
                command=self.update_parameters_visibility,
            )
            rb.grid(row=0, column=i, padx=10, pady=5)

        # Parameters Frame
        self.params_frame = ctk.CTkFrame(self.tool_frame)
        self.params_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.params_frame.grid_columnconfigure(0, weight=1)
        
        param_label = ctk.CTkLabel(
            self.params_frame, text="2. Paramètres", font=ctk.CTkFont(weight="bold")
        )
        param_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.params_container = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.params_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Caesar
        self.caesar_frame = ctk.CTkFrame(self.params_container, fg_color="transparent")
        ctk.CTkLabel(self.caesar_frame, text="Décalage (Shift):").pack(side="left", padx=5)
        self.shift_entry = ctk.CTkEntry(self.caesar_frame, width=80)
        self.shift_entry.pack(side="left", padx=5)

        # Affine
        self.affine_frame = ctk.CTkFrame(self.params_container, fg_color="transparent")
        ctk.CTkLabel(self.affine_frame, text="Coefficient a:").pack(side="left", padx=5)
        self.a_entry = ctk.CTkEntry(self.affine_frame, width=80)
        self.a_entry.pack(side="left", padx=5)
        ctk.CTkLabel(self.affine_frame, text="Coefficient b:").pack(side="left", padx=5)
        self.b_entry = ctk.CTkEntry(self.affine_frame, width=80)
        self.b_entry.pack(side="left", padx=5)

        # Key (Vigenere, AES, DES)
        self.key_frame = ctk.CTkFrame(self.params_container, fg_color="transparent")
        ctk.CTkLabel(self.key_frame, text="Clé:").pack(side="left", padx=5)
        self.key_entry = ctk.CTkEntry(self.key_frame, width=250)
        self.key_entry.pack(side="left", padx=5)

        # RSA
        self.rsa_frame = ctk.CTkFrame(self.params_container, fg_color="transparent")
        ctk.CTkButton(
            self.rsa_frame, text="Générer Clés", command=self.generate_rsa_keys, width=100
        ).pack(side="left", padx=5)
        self.pub_path_var = tk.StringVar()
        ctk.CTkButton(
            self.rsa_frame,
            text="Clé Publique",
            command=lambda: self.select_file(self.pub_path_var),
            width=100,
        ).pack(side="left", padx=5)
        ctk.CTkEntry(self.rsa_frame, textvariable=self.pub_path_var, width=150).pack(
            side="left", padx=5
        )
        self.priv_path_var = tk.StringVar()
        ctk.CTkButton(
            self.rsa_frame,
            text="Clé Privée",
            command=lambda: self.select_file(self.priv_path_var),
            width=100,
        ).pack(side="left", padx=5)
        ctk.CTkEntry(self.rsa_frame, textvariable=self.priv_path_var, width=150).pack(
            side="left", padx=5
        )

        self.update_parameters_visibility()

        # Input Frame
        self.input_frame = ctk.CTkFrame(self.tool_frame)
        self.input_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)

        input_header = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        input_header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        ctk.CTkLabel(
            input_header, text="3. Entrée (Texte ou Fichier)", font=ctk.CTkFont(weight="bold")
        ).pack(side="left")
        ctk.CTkButton(
            input_header, text="Charger Fichier", command=self.load_input_file, width=120
        ).pack(side="right")

        self.text_input = ctk.CTkTextbox(self.input_frame)
        self.text_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Actions
        self.action_frame = ctk.CTkFrame(self.tool_frame, fg_color="transparent")
        self.action_frame.grid(row=3, column=0, pady=(0, 15))
        
        ctk.CTkButton(
            self.action_frame,
            text="CHIFFRER",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=lambda: self.process_action("encrypt"),
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            self.action_frame,
            text="DÉCHIFFRER",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=lambda: self.process_action("decrypt"),
        ).pack(side="left", padx=10)

        # Output Frame
        self.output_frame = ctk.CTkFrame(self.tool_frame)
        self.output_frame.grid(row=4, column=0, sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)

        output_header = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        output_header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        ctk.CTkLabel(output_header, text="4. Résultat", font=ctk.CTkFont(weight="bold")).pack(
            side="left"
        )
        ctk.CTkButton(
            output_header, text="Sauvegarder", command=self.save_output_file, width=120
        ).pack(side="right")

        self.text_output = ctk.CTkTextbox(self.output_frame)
        self.text_output.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def setup_guide_ui(self) -> None:
        """Configure l'interface pour afficher le guide utilisateur."""
        guide_label = ctk.CTkLabel(
            self.guide_frame, text="Guide Utilisateur", font=ctk.CTkFont(size=24, weight="bold")
        )
        guide_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Frame for HTML Label
        self.html_frame = ctk.CTkFrame(self.guide_frame)
        self.html_frame.grid(row=1, column=0, sticky="nsew")
        
        self.html_label = HTMLLabel(self.html_frame, html="<h1>Chargement...</h1>", background="white")
        self.html_label.pack(fill="both", expand=True, padx=2, pady=2)

        self.load_user_guide()

    def load_user_guide(self) -> None:
        """Charge le guide utilisateur depuis le fichier Markdown."""
        try:
            guide_path = get_resource_path("USER_GUIDE.md")
            if os.path.exists(guide_path):
                with open(guide_path, "r", encoding="utf-8") as f:
                    md_content = f.read()
                # Convert markdown to HTML
                html_content = markdown.markdown(md_content)
                self.html_label.set_html(html_content)
            else:
                self.html_label.set_html("<h1>Erreur</h1><p>USER_GUIDE.md non trouvé.</p>")
        except Exception as e:
            self.html_label.set_html(f"<h1>Erreur</h1><p>Impossible de lire le guide: {e}</p>")

    def update_parameters_visibility(self) -> None:
        """Affiche ou cache les paramètres en fonction de l'algorithme sélectionné."""
        for frame in [self.caesar_frame, self.affine_frame, self.key_frame, self.rsa_frame]:
            frame.pack_forget()

        algo = self.algo_var.get()
        if algo == "caesar":
            self.caesar_frame.pack(anchor="w")
        elif algo == "affine":
            self.affine_frame.pack(anchor="w")
        elif algo in ["vigenere", "des", "aes"]:
            self.key_frame.pack(anchor="w")
        elif algo == "rsa":
            self.rsa_frame.pack(anchor="w")

    def select_file(self, string_var: tk.StringVar) -> None:
        """Ouvre une boîte de dialogue pour sélectionner un fichier et met à jour la variable."""
        path = filedialog.askopenfilename()
        if path:
            string_var.set(path)

    def load_input_file(self) -> None:
        """Charge le contenu d'un fichier texte dans la zone d'entrée."""
        path = filedialog.askopenfilename()
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.text_input.delete("1.0", tk.END)
                    self.text_input.insert(tk.END, content)
            except OSError as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier:\n{e}")
            except Exception as e:
                messagebox.showerror("Erreur inattendue", f"Une erreur s'est produite:\n{e}")

    def save_output_file(self) -> None:
        """Sauvegarde le contenu de la zone de résultat dans un fichier texte."""
        content = self.text_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Attention", "Il n'y a aucun résultat à sauvegarder.")
            return
            
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Succès", "Fichier sauvegardé avec succès.")
            except OSError as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier:\n{e}")
            except Exception as e:
                messagebox.showerror("Erreur inattendue", f"Une erreur s'est produite:\n{e}")

    def generate_rsa_keys(self) -> None:
        """Génère une paire de clés RSA et les sauvegarde dans des fichiers."""
        try:
            priv, pub = crypto_utils.generate_rsa_keys()
            base = filedialog.asksaveasfilename(
                title="Base du nom des fichiers de clés", initialfile="id_rsa"
            )
            if base:
                with open(base, "wb") as f:
                    f.write(priv)
                with open(base + ".pub", "wb") as f:
                    f.write(pub)
                messagebox.showinfo("RSA", f"Clés générées :\n{base}\n{base}.pub")
        except OSError as e:
             messagebox.showerror("Erreur d'écriture", f"Impossible de sauvegarder les clés:\n{e}")
        except Exception as e:
            messagebox.showerror("Erreur RSA", f"Une erreur s'est produite:\n{e}")

    def _prepare_aes_key(self, key_str: str) -> bytes:
        """Prépare la clé AES (tronque ou hash pour obtenir 32 bytes si nécessaire)."""
        key_bytes = key_str.encode("utf-8")
        if len(key_bytes) not in (16, 24, 32):
            key_bytes = hashlib.sha256(key_bytes).digest()
        return key_bytes
        
    def _prepare_des_key(self, key_str: str) -> bytes:
        """Prépare la clé DES (tronque ou hash pour obtenir 24 bytes si nécessaire)."""
        key_bytes = key_str.encode("utf-8")
        if len(key_bytes) != 8:
            key_bytes = hashlib.sha256(key_bytes).digest()[:24]
        return key_bytes

    def process_action(self, action: str) -> None:
        """
        Exécute le chiffrement ou déchiffrement sélectionné.

        Args:
            action: L'action à exécuter ("encrypt" ou "decrypt").
        """
        algo = self.algo_var.get()
        content = self.text_input.get("1.0", tk.END).strip()
        
        if not content:
            messagebox.showwarning("Attention", "Veuillez entrer du texte ou charger un fichier.")
            return

        try:
            result = ""
            if algo == "caesar":
                try:
                    shift_val = self.shift_entry.get().strip()
                    if not shift_val:
                        raise ValueError("Le décalage est manquant.")
                    shift = int(shift_val)
                except ValueError:
                    raise ValueError("Le décalage doit être un nombre entier valide.")
                
                if action == "encrypt":
                    result = crypto_utils.caesar_encrypt(content, shift)
                else:
                    result = crypto_utils.caesar_decrypt(content, shift)

            elif algo == "affine":
                try:
                    a_val = self.a_entry.get().strip()
                    b_val = self.b_entry.get().strip()
                    if not a_val or not b_val:
                        raise ValueError("Les deux coefficients sont requis.")
                    a = int(a_val)
                    b = int(b_val)
                except ValueError as e:
                    raise ValueError(f"Les coefficients a et b doivent être des nombres entiers valides.\nDétails: {e}")
                
                if action == "encrypt":
                    result = crypto_utils.affine_encrypt(content, a, b)
                else:
                    result = crypto_utils.affine_decrypt(content, a, b)

            elif algo == "vigenere":
                key = self.key_entry.get().strip()
                if not key:
                    raise ValueError("Veuillez fournir une clé de chiffrement.")
                if action == "encrypt":
                    result = crypto_utils.vigenere_encrypt(content, key)
                else:
                    result = crypto_utils.vigenere_decrypt(content, key)

            elif algo == "aes":
                key = self.key_entry.get().strip()
                if not key:
                    raise ValueError("Veuillez fournir une clé AES.")
                key_bytes = self._prepare_aes_key(key)

                if action == "encrypt":
                    result = crypto_utils.aes_encrypt(content, key_bytes).hex()
                else:
                    try:
                        data_bytes = bytes.fromhex(content)
                    except ValueError:
                        raise ValueError("Le texte d'entrée doit être en hexadécimal pour le déchiffrement AES.")
                    result = crypto_utils.aes_decrypt(data_bytes, key_bytes)

            elif algo == "des":
                key = self.key_entry.get().strip()
                if not key:
                    raise ValueError("Veuillez fournir une clé DES.")
                key_bytes = self._prepare_des_key(key)

                if action == "encrypt":
                    result = crypto_utils.des_encrypt(content, key_bytes).hex()
                else:
                    try:
                        data_bytes = bytes.fromhex(content)
                    except ValueError:
                        raise ValueError("Le texte d'entrée doit être en hexadécimal pour le déchiffrement DES.")
                    result = crypto_utils.des_decrypt(data_bytes, key_bytes)

            elif algo == "rsa":
                if action == "encrypt":
                    pub_path = self.pub_path_var.get().strip()
                    if not pub_path:
                        raise ValueError("Veuillez sélectionner un fichier de clé publique.")
                    try:
                        with open(pub_path, "rb") as f:
                            pub_key = f.read()
                    except OSError as e:
                        raise ValueError(f"Impossible de lire la clé publique:\n{e}")
                    
                    result = crypto_utils.rsa_encrypt(content, pub_key).hex()
                else:
                    priv_path = self.priv_path_var.get().strip()
                    if not priv_path:
                        raise ValueError("Veuillez sélectionner un fichier de clé privée.")
                    try:
                        with open(priv_path, "rb") as f:
                            priv_key = f.read()
                    except OSError as e:
                        raise ValueError(f"Impossible de lire la clé privée:\n{e}")
                    
                    try:
                        data_bytes = bytes.fromhex(content)
                    except ValueError:
                        raise ValueError("Le texte d'entrée doit être en hexadécimal pour le déchiffrement RSA.")
                    
                    result = crypto_utils.rsa_decrypt(data_bytes, priv_key)

            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, result)

        except ValueError as e:
            messagebox.showwarning("Paramètres incorrects", str(e))
        except Exception as e:
            messagebox.showerror("Erreur inattendue", f"Une erreur s'est produite lors du traitement:\n{e}")


if __name__ == "__main__":
    app = CryptoGUI()
    app.mainloop()
