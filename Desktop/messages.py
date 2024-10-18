import customtkinter

class Error(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Du hast keinen Youtube Link eingegeben!")
        self.label.pack(padx=20, pady=20)

class Success(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Der Download wurde gestartet")
        self.label.pack(padx=20, pady=20)

class Finished(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Das Video wurde erfolgreich runtergeladen")
        self.label.pack(padx=20, pady=20)