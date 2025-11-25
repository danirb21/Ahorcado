class WindowPosition:
    last_x = None
    last_y = None

    @staticmethod
    def store(window):
        try:
            window.update_idletasks()
            WindowPosition.last_x = window.winfo_x()
            WindowPosition.last_y = window.winfo_y()
        except:
            pass

    @staticmethod
    def apply(window):
        try:
            if WindowPosition.last_x is not None and WindowPosition.last_y is not None:
                window.geometry(f"+{WindowPosition.last_x}+{WindowPosition.last_y}")
        except:
            pass