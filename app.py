import streamlit as st
#MCEQ
import crflux.models as crf
import MCEq.core
import MCEq.particlemanager
import matplotlib.pyplot as plt

def run_mceq(interaction_model, primary_model_name, theta_deg, mag,
             use_muons, use_numu, use_nue, flux_prefixes):

    # Mapeia o nome do modelo primário para o formato esperado pelo MCEq
    if primary_model_name == "H3a":
        primary_model = (crf.HillasGaisser2012, 'H3a')
    elif primary_model_name == "H4a":
        primary_model = (crf.HillasGaisser2012, 'H4a')
    else:
        primary_model = None  # caso "None" esteja selecionado na interface

    if len(flux_prefixes) == 0:
        raise ValueError("Please select at least one flux type (Prompt, Conventional, or Total).")

    mceq = MCEq.core.MCEqRun(
        interaction_model=interaction_model,
        primary_model=primary_model,
        theta_deg=theta_deg
    )

    mceq.solve()
    energies = mceq.e_grid

    fig, ax = plt.subplots()
    ax.set_xscale("log")
    ax.set_yscale("log")

    # ---------------- MUONS ----------------
    if use_muons:
        for prefix in flux_prefixes:
            muon_flux = (
                mceq.get_solution(f"{prefix}mu+", mag) +
                mceq.get_solution(f"{prefix}mu-", mag)
            )
            ax.plot(energies, muon_flux, label=f"{prefix} μ⁺ + μ⁻")

    # ---------------- NU MU ----------------
    if use_numu:
        for prefix in flux_prefixes:
            numu_flux = (
                mceq.get_solution(f"{prefix}numu", mag) +
                mceq.get_solution(f"{prefix}antinumu", mag)
            )
            ax.plot(energies, numu_flux, label=f"{prefix} νμ + ν̄μ")

    # ---------------- NU E ----------------
    if use_nue:
        for prefix in flux_prefixes:
            nue_flux = (
                mceq.get_solution(f"{prefix}nue", mag) +
                mceq.get_solution(f"{prefix}antinue", mag)
            )
            ax.plot(energies, nue_flux, label=f"{prefix} νe + ν̄e")

    ax.set_xlim(1., 1e9)
    ax.set_xlabel("Kinetic energy / GeV")

    ax.set_ylim(1e-6, 1.)
    ax.set_ylabel(r"(E/GeV)$^3$ $\Phi$/(GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$)")

    ax.legend()

    return fig
# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(
    page_title="MCEq Interface",
    layout="wide"
)

# Font Awesome para ícones
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)

# ---------------- CSS ----------------
st.markdown("""
<style>

:root {
    --bg1: #8ee7d8;
    --bg2: #b7d3f0;
    --card-bg: #ffffff;
    --radius: 16px;
    --shadow: 0px 6px 18px rgba(0,0,0,0.10);
    --text-title: #1f2937;
    --text-muted: #4b5563;
    --accent: #3b82f6;
}

/* Fundo geral */
.stApp {
    background: linear-gradient(120deg, var(--bg1), var(--bg2));
    font-family: "Inter", sans-serif;
}

/* Cartões */
.card, .result-card {
    background-color: var(--card-bg);
    padding: 2rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    border: 1px solid rgba(255,255,255,0.4);
}

/* Títulos */
.section-title {
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--text-title);
    margin-bottom: 0.4rem;
}

/* Botão */
.stButton > button {
    background: var(--accent);
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    border: none;
    font-size: 1rem;
    font-weight: 600;
    transition: 0.2s ease-in-out;
}

.stButton > button:hover {
    background: #2563eb;
    transform: translateY(-2px);
}

/* Inputs */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #d1d5db !important;
}

/* Footer */
.footer {
    margin-top: 2.5rem;
    padding: 1.5rem;
    background-color: rgba(255,255,255,0.65);
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.10);
}

.social-icons {
    display: flex;
    justify-content: center;
    gap: 22px;
    margin-bottom: 1rem;
}

.social-link {
    font-size: 28px;
    color: #1f2937;
    transition: 0.2s ease-in-out;
}

.social-link:hover {
    color: #2563eb;
    transform: translateY(-3px);
}

/* Tooltip */
.tooltip-footer {
    position: relative;
    display: inline-block;
}

.tooltiptext-footer {
    visibility: hidden;
    width: 140px;
    background-color: #333;
    color: #fff;
    text-align: center;
    padding: 6px;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
    bottom: 140%;
    left: 50%;
    margin-left: -70px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 0.8rem;
}

.tooltip-footer:hover .tooltiptext-footer {
    visibility: visible;
    opacity: 1;
}

/* Logos */
.footer-logo {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
    gap: 30px;
}

.logo-footer, .logo-footer2 {
    height: 60px;
    opacity: 0.9;
    transition: 0.2s;
}

.logo-footer:hover, .logo-footer2:hover {
    opacity: 1;
}
/*Texto Flutuante*/
.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
}

.tooltiptext {
    visibility: hidden;
    width: 220px;
    background-color: #333;
    color: #fff;
    text-align: left;
    padding: 8px;
    border-radius: 6px;
    position: absolute;
    z-index: 10;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 0.85rem;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
            
</style>
""", unsafe_allow_html=True)

# ---------------- LAYOUT PRINCIPAL ----------------
left, right = st.columns([1.1, 1])

# ================== PAINEL ESQUERDO ==================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("MCEq Interface")

    st.markdown("""
<div class="tooltip">
    <span class="section-title">Interation Model</span>
    <span class="tooltiptext">
        Defines the hadronic interaction model used to simulate cosmic ray collisions with atmospheric nuclei. Different models apply various physics approximations and parameterizations, impacting the secondary particle distributions.
    </span>
</div>
""", unsafe_allow_html=True)
    interaction_model = st.radio(
        "",
        [
            "SIBYLL-2.3c", "SIBYLL-2.3", "SIBYLL-2.1",
            "EPOS-LHC", "QGSJet-II-04", "QGSJet-II-03",
            "QGSJet-01c", "DPMJET-III-3.0.6",
            "DPMJET-III-19.1", "SIBYLL-2.3c_pp"
        ]
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
<div class="tooltip">
    <span class="section-title">Primary Model</span>
    <span class="tooltiptext">
        Selects the cosmic-ray primary flux model used in the simulation.
        Options like H3a and H4a represent different parameterizations of
        the cosmic-ray spectrum.
    </span>
</div>
""", unsafe_allow_html=True)

        primary_model = st.radio("", ["None", "H3a", "H4a"])
    with col2:
        
        st.markdown("""
<div class="tooltip">
    <span class="section-title">Direction</span>
    <span class="tooltiptext">
        Magnitude: Represents the energy power with which the flux is multiplied, that is, it is used to highlight features of the spectrum, which is normally very steep.
        Angle: Specifies the zenith angle of incoming cosmic rays relative to the vertical. An angle of 0° is vertical (straight down), and 90° is horizontal (parallel to the ground). Affects the atmospheric depth traveled.                        
    </span>
</div>
""", unsafe_allow_html=True)
        
        magnitude = st.text_input("Magnitude")
        angle = st.text_input("Angle (°)")

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
<div class="tooltip">
    <span class="section-title">Particle</span>
    <span class="tooltiptext">
        Selects the types of secondary particles to track in the simulation. Options typically include muons and different types of neutrinos, which are produced during cosmic ray interactions.                                                
    </span>
</div>
""", unsafe_allow_html=True)
        muons = st.checkbox("Muons")
        muon_neutrinos = st.checkbox("Muon Neutrinos")
        electron_neutrinos = st.checkbox("Electron Neutrinos")
    with col4:
        st.markdown("""
<div class="tooltip">
    <span class="section-title">Flux</span>
    <span class="tooltiptext">
        Determines the component of atmospheric particle flux to consider. Conventional flux comes from pion and kaon decays, while prompt flux originates from heavier charm meson decays. The total flux includes both contributions.                                                
    </span>
</div>
""", unsafe_allow_html=True)
        conventional = st.checkbox("Conventional")
        prompt = st.checkbox("Prompt")
        total = st.checkbox("Total")

    st.markdown("<br>", unsafe_allow_html=True)
    simulate = st.button("Simulate", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Lista de fluxos selecionados
flux_prefixes = []

if prompt:
    flux_prefixes.append("pr_")

if conventional:
    flux_prefixes.append("conv_")

if total:
    flux_prefixes.append("total_")


# ================== PAINEL DIREITO MCEQ ==================
with right:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    st.subheader("Simulation Output")

    output_area = st.empty()

    if simulate:
        with output_area:

            # -------- VALIDAÇÃO DOS CAMPOS --------
            if angle.strip() == "":
                st.error("Please enter a value for the angle (θ).")
                st.stop()

            if magnitude.strip() == "":
                st.error("Please enter a value for the magnitude.")
                st.stop()

            # Validação numérica do ângulo
            try:
                theta_val = float(angle)
            except ValueError:
                st.error("Angle must be a valid number.")
                st.stop()

            # Validação numérica da magnitude
            try:
                mag = int(magnitude)
            except ValueError:
                st.error("Magnitude must be an integer.")
                st.stop()

            # -------- SE PASSAR NAS VALIDAÇÕES, RODA O MCEQ --------
            st.info("Running MCEq simulation...")

            fig = run_mceq(
                interaction_model=interaction_model,
                primary_model_name=primary_model,
                theta_deg=theta_val,
                mag=mag,
                use_muons=muons,
                use_numu=muon_neutrinos,
                use_nue=electron_neutrinos,
                flux_prefixes=flux_prefixes
)

            st.success("Simulation finished successfully!")
            st.pyplot(fig)

    else:
        with output_area:
            st.info("Run a simulation to display results here.")
            st.image(
                "https://dummyimage.com/450x300/cccccc/000000&text=Waiting+for+Simulation",
                caption="Results will appear here"
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- RODAPÉ ----------------
with st.container():
    st.markdown('<div class="footer">', unsafe_allow_html=True)

    # Ícones sociais (HTML)
    st.markdown(
"""<div class="social-icons">

<div class="tooltip-footer">
    <a href="https://mceq.readthedocs.io/en/latest/index.html" target="_blank" class="social-link">
        <i class="fas fa-file-alt"></i>
    </a>
    <span class="tooltiptext-footer">MCEq Documentation</span>
</div>

<div class="tooltip-footer">
    <a href="https://wp.ufpel.edu.br/game/" target="_blank" class="social-link">
        <i class="fas fa-globe"></i>
    </a>
    <span class="tooltiptext-footer">GAME Site</span>
</div>

<div class="tooltip-footer">
    <a href="mailto:game.ufpel@protonmail.com" class="social-link">
        <i class="fas fa-envelope"></i>
    </a>
    <span class="tooltiptext-footer">Email Us</span>
</div>

<div class="tooltip-footer">
    <a href="https://instagram.com" target="_blank" class="social-link">
        <i class="fab fa-instagram"></i>
    </a>
    <span class="tooltiptext-footer">Instagram</span>
</div>

<div class="tooltip-footer">
    <a href="https://linkedin.com" target="_blank" class="social-link">
        <i class="fab fa-linkedin"></i>
    </a>
    <span class="tooltiptext-footer">LinkedIn</span>
</div>

</div>

<div class="footer-logo">
</div>
""",
        unsafe_allow_html=True
    )

    # Logos carregadas pelo Streamlit (funciona 100%)
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # coluna central
    st.image("identidadeufpel.png", width=80)

with col3:
    st.image("identidadegame.png", width=120)

    st.markdown('</div>', unsafe_allow_html=True)
