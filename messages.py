import customtkinter

class Error(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("System")

        self.label = customtkinter.CTkLabel(self, text="Es ist ein Fehler aufgetreten")
        self.label.pack(padx=20, pady=20)


class Succes(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("System")

        self.label = customtkinter.CTkLabel(self, text="Der Download wurde gestartet")
        self.label.pack(padx=20, pady=20)

class Finished(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("System")

        self.label = customtkinter.CTkLabel(self, text="Der Download wurde fertiggestellt")
        self.label.pack(padx=20, pady=20)