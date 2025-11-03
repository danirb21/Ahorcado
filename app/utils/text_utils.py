import unicodedata

def quitar_tildes(texto: str) -> str:
    """Elimina las tildes y otros diacríticos del texto."""
    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(
        c for c in texto_normalizado if unicodedata.category(c) != "Mn"
    )
