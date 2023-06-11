import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Inicio",
        page_icon="👋",
    )

    st.write("# Visualización de datos de Matrimonio y natalidad en España")

    st.markdown(
        """
        En este proyecto se analizan datos del INE relativos a la demografía de España, concretamente
        datos de matrimonios y nacimientos.

        En la primera página se pueden consultar datos sobre matrimonios por provincia, sexo y año.

        En la segunda paǵina se describen datos de nacimientos por año y estado civil de la madre.
    """
    )


if __name__ == "__main__":
    run()