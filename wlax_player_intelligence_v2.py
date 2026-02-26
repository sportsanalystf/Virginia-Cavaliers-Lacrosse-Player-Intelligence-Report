import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Virginia WLAX Player Intelligence",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════
# UVA OFFICIAL BRAND COLORS
# ═══════════════════════════════════════════════
UVA_BLUE = "#232D4B"
UVA_ORANGE = "#E57200"
CAV_ORANGE = "#F84C1E"       # Athletics-specific orange
UVA_CYAN = "#009FDF"
UVA_YELLOW = "#FDDA24"
UVA_TEAL = "#25CAD3"
UVA_GREEN = "#62BB46"
UVA_MAGENTA = "#EF3F6B"
LIGHT_GRAY = "#F1F1EF"
MED_GRAY = "#DADADA"
TEXT_GRAY = "#666666"
WHITE = "#FFFFFF"
UVA_BLUE_25 = "#C8CBD2"
UVA_ORANGE_25 = "#F9DCBF"

# Tier colors
TIER_COLORS = {1: CAV_ORANGE, 2: UVA_CYAN, 3: UVA_GREEN, 4: MED_GRAY}
# Flag colors
FLAG_COLORS = {"positive": UVA_GREEN, "negative": UVA_MAGENTA, "warning": UVA_YELLOW, "info": UVA_CYAN}

# ─── CUSTOM CSS (LIGHT THEME) ───
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&family=Bebas+Neue&display=swap');

:root {{
    --uva-blue: {UVA_BLUE};
    --uva-orange: {UVA_ORANGE};
    --cav-orange: {CAV_ORANGE};
}}

.stApp {{
    background-color: {LIGHT_GRAY};
    font-family: 'DM Sans', sans-serif;
    color: {UVA_BLUE};
}}

h1, h2, h3 {{
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 1.5px;
    color: {UVA_BLUE} !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {UVA_BLUE} !important;
}}
section[data-testid="stSidebar"] * {{
    color: white !important;
}}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown h4 {{
    color: white !important;
}}

/* Main Header */
.main-header {{
    background: linear-gradient(135deg, {UVA_BLUE} 0%, #1a2238 50%, {UVA_ORANGE} 100%);
    padding: 1.5rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}}
.main-header h1 {{
    color: white !important;
    font-size: 2.5rem;
    margin: 0;
    font-family: 'Bebas Neue', sans-serif !important;
    line-height: 1;
}}
.main-header p {{
    color: rgba(255,255,255,0.75);
    font-size: 0.95rem;
    margin: 0.25rem 0 0 0;
}}

/* Player Card */
.player-card {{
    background: {WHITE};
    border: 1px solid {MED_GRAY};
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(35,45,75,0.06);
    transition: all 0.25s ease;
    border-left: 5px solid {UVA_ORANGE};
}}
.player-card:hover {{
    box-shadow: 0 4px 24px rgba(35,45,75,0.12);
    border-left-color: {CAV_ORANGE};
}}

.player-name {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: {UVA_BLUE};
    letter-spacing: 2px;
    margin: 0;
    line-height: 1.1;
}}
.player-meta {{
    color: {UVA_ORANGE};
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 3px;
}}

/* Impact score box */
.impact-score-box {{
    background: linear-gradient(135deg, {UVA_ORANGE} 0%, {CAV_ORANGE} 100%);
    border-radius: 14px;
    padding: 1rem 0.8rem;
    text-align: center;
    min-width: 90px;
}}
.impact-score-num {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: white;
    line-height: 1;
}}
.impact-score-label {{
    color: rgba(255,255,255,0.9);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
}}

/* Stat boxes */
.stat-box {{
    background: {WHITE};
    border: 1px solid {MED_GRAY};
    border-radius: 12px;
    padding: 0.8rem;
    text-align: center;
}}
.stat-val {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    line-height: 1;
}}
.stat-label {{
    font-size: 0.65rem;
    color: {TEXT_GRAY};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-top: 4px;
}}

/* Tier badges */
.tier-badge {{
    display: inline-block;
    padding: 3px 14px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: white;
    vertical-align: middle;
    margin-left: 8px;
}}
.tier-1 {{ background: {CAV_ORANGE}; }}
.tier-2 {{ background: {UVA_CYAN}; }}
.tier-3 {{ background: {UVA_GREEN}; }}
.tier-4 {{ background: {MED_GRAY}; color: {UVA_BLUE}; }}

/* Flag tags */
.flag-tag {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 3px 4px;
    letter-spacing: 0.5px;
}}
.flag-positive {{ background: #E8F5E9; color: #2E7D32; border: 1px solid #A5D6A7; }}
.flag-negative {{ background: #FCE4EC; color: #C62828; border: 1px solid #EF9A9A; }}
.flag-warning {{ background: #FFF8E1; color: #E65100; border: 1px solid #FFE082; }}
.flag-info {{ background: #E3F2FD; color: #1565C0; border: 1px solid #90CAF9; }}

/* Coaching notes */
.coaching-notes {{
    background: #F8F8FC;
    border-left: 4px solid {UVA_BLUE};
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    font-size: 0.88rem;
    color: {UVA_BLUE};
    line-height: 1.65;
    margin-top: 0.8rem;
}}

/* Recommendation box */
.rec-box {{
    background: linear-gradient(135deg, #FFF3E0 0%, #FFF8E1 100%);
    border-left: 4px solid {UVA_ORANGE};
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    font-size: 0.88rem;
    color: {UVA_BLUE};
    line-height: 1.65;
    margin-top: 0.5rem;
}}
.rec-box strong {{ color: {CAV_ORANGE}; }}

.section-divider {{
    border: none;
    border-top: 1px solid {MED_GRAY};
    margin: 1rem 0;
}}

/* Headshot */
.headshot-circle {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid {UVA_ORANGE};
    background: {LIGHT_GRAY};
}}

/* Metric cards */
div[data-testid="stMetric"] {{
    background: {WHITE};
    border: 1px solid {MED_GRAY};
    border-radius: 10px;
    padding: 0.6rem;
}}
div[data-testid="stMetric"] label {{
    color: {TEXT_GRAY} !important;
}}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
    color: {UVA_BLUE} !important;
}}

/* Dataframe */
.stDataFrame {{ border-radius: 10px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# DATA LAYER
# ═══════════════════════════════════════════════

# Player headshot URLs from virginiasports.com (manually mapped)
HEADSHOT_URLS = {
    "Madison Alaimo": "https://virginiasports.com/imgproxy/pYMb3-v9_Iw05OEJEvS-VLV-PkXLxFnbK2dnVLNGX2o/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvYm9JU25aRzgycFVLbFVqTjc3c3daUkRwV0JOWkdpVDQ2UG0zSUVCQy5qcGc.jpg",
    "Jenna Dinardo": "https://virginiasports.com/imgproxy/M-EqJX8pcAsMqHLqjB7zcRq0P-nR7bKVTQ8i_D86R_4/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvaUpmMjVsZWtZazlNZzRRYWxoTWlCZmhSNldUZjBxZnBTdW1kbENRYi5qcGc.jpg",
    "Addi Foster": "https://virginiasports.com/imgproxy/a-B08gK1VEOXrp9J_Bq82N_9xdFa-xpzxKphIiuuPcg/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvRGdrQ1czdnJKTnRJcGRvZjJuOWRjSHBZMGJnbjRTeWZ3amFWRlFOOS5qcGc.jpg",
    "Kate Galica": "https://virginiasports.com/imgproxy/Z4W8fnWOqaA8_rvVBt7EqYIeGP5hJuEhM3yBq62nGYU/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvdmFpYXp5MlVkMXBRMThGVFJxemZ3V2hyb3ZkUjl4MEIzbTN5UHdaYi5qcGc.jpg",
    "Cady Flaherty": "https://virginiasports.com/imgproxy/K-T-B3xpQl-aDjFqBq_Y80c5ZE8x4l5H8MbR7AqGnOE/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvN2xzcFN0THhFbnMwZFBPNk1mTUt2V1M5VUt3S01VVlZPdkVzNWltdi5qcGc.jpg",
    "Gabby Laverghetta": "https://virginiasports.com/imgproxy/F_sxh_p1KSKW5FxzFKp3vQ0A-0k4Y5uyhd-yVCTBm2Y/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvWFdGa3VmcGdIbk9OT3FZaUlnVDQ5Uld3UXBZdWFSWENDcTdIT0RMMS5qcGc.jpg",
    "Livy Laverghetta": "https://virginiasports.com/imgproxy/b9RWFgqGBkgGFIjgOK2CzY-VKfyX8o_0dNxA-KbFVIE/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvbGRYSUxQeTRLN2dGN2dXbFlhcUtIaXExbzFLcDlGWFNMamdaMTVOeS5qcGc.jpg",
    "Elyse Finnelle": "https://virginiasports.com/imgproxy/0R3SdJ2qx08ccevzYjFN9e1z3SJEdN1jJ8kAMuBbZrQ/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcveDVla1RCZnluRnJIUWRjQzdGbWNLZGdFVXhGa25jWkh4amVJcG5Ybi5qcGc.jpg",
    "Kate Demark": "https://virginiasports.com/imgproxy/hqJLp2fJTW5ZPt0Zp8_GV7yOlAIOcBrwCOOJKBt5YZU/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvN3dWb0xoWXV3a0htamdHYjFJb2tVcXdEYnV0c0NZcHRkNWZJWWdYdi5qcGc.jpg",
    "Alexandra Schneider": "https://virginiasports.com/imgproxy/s9CLFpBGzTNyXL3r9hC6sSeLTsHXYSiNNGxkdDR7EoE/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvMk5uMGVGOXpSS3F2aHlSU0hHU1hGNmVPcjEweTYyNWxQQVZIVDhWWi5qcGc.jpg",
    "Sophia Conti": "https://virginiasports.com/imgproxy/5z2L5PGXqj8_YJRy8H8-tXxjj3pIH3CjRXzE97dG-eA/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvQmRzQU1yNkZjME1MSjd5OVFqOXVmRHdLdndlcUh5WjBvaTdYSWVRSi5qcGc.jpg",
    "Lara Kology": "https://virginiasports.com/imgproxy/gk2T0i4LG_ik2E-fL7oaS8nlJPhBl9aPWS-NHB2XpNM/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvZkdZYlhiZFdHT1d2bXRuUXFndUxyWW5ERWh3R3lqR2lLYjgzbm1JMC5qcGc.jpg",
    "Alex Reilly": "https://virginiasports.com/imgproxy/v5qLaFiVpJJ6AQBdz1V2PEiNWxJnS1vVPKN3Nde4wDk/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvUXRYTDUyOFJyODlUWm5wek1hOHRscXZXd2pjQnExNWdjY0VmQXZVbS5qcGc.jpg",
    "Payton Sfreddo": "https://virginiasports.com/imgproxy/TXIbMgQ6cnYINW5h0zcOSjHGNcNbptNMhT4HwIFi7FI/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvQjI3eG1zcXZVd3BmVENpNjRkMjZ2NXJ3SjNIR0xCOFdVT09tTkFnUy5qcGc.jpg",
    "Mel Josephson": "https://virginiasports.com/imgproxy/0l2LW0rXiVmhIAi7dFFqPjC_8iNmCIoNXHPj80L64io/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvZXRKSk55RXF5Nnl3YUV2Y3FUVDRHR1RVclNYazlXdGJGTGd3ekVQYy5qcGc.jpg",
    "Raleigh Foster": "https://virginiasports.com/imgproxy/Ke-zN1_Bc0bQF5BRmfL_y8JtajBT9e0Z3Y7WjMIyg6o/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvQjB4aWI5MlRFTXpPeFBzaW1Gc0VZc2drUEt5c0MyQ2JUZzVwM0Jqdy5qcGc.jpg",
    "Carly Kennedy": "https://virginiasports.com/imgproxy/jP9nvB-_HjIFZ23hA5A_eMpRn7gU5XBmNXhxW1AKK5A/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvSE5SSHBxZWF4Mk5jQXQ0ZXRWVEFYTHhiUnJ2VTlMbUZPU3BYUDdiOC5qcGc.jpg",
    "Megan Rocklein": "https://virginiasports.com/imgproxy/k7wIW43g42bHERYl-kL_FVPJ3-JqPxfjz4fwdZJBfbo/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvSk5yRDlpNldlSTBHbGpPUVFaYUVtNTBFWFhyVzFoRnBZcno0VmU1Yi5qcGc.jpg",
    "Fiona Allen": "https://virginiasports.com/imgproxy/Z_e6g3SVzfXz9VffJLWQWJP0KdKdGH7BKxj1xEm3eiU/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvTEV5d0daUEE5RTczTlQ3TGdJUjh0S2RMeTFjRlJiTjB4dHlwQ0p3Sy5qcGc.jpg",
    "Abby Musser": "https://virginiasports.com/imgproxy/2ZI8pSVJOr2J7oWmHI1Q-OWVeVj-6JFIm0fQRx8l5kM/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvU21NckJ6SEF3clZMZjdDNHlFMHQ0VjhxRmxVSmtLNWN4bVdwclRIVi5qcGc.jpg",
    "Jayden Piraino": "https://virginiasports.com/imgproxy/5i_Fqg7Lxf8Wge2MfLXp5LYdKJgSqS6K8l3iqGS77RY/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvZk5pZDFYYnhGR1UxTmkxSWdtSlI3aUQxZjM1MnBKSjN2VTlVUUoyYy5qcGc.jpg",
    "Corey White": "https://virginiasports.com/imgproxy/P7CbNjrQg_YxRiGiPMeMLxIJMC9FW4OPqyuKw-3cpyw/rs:fit:400:0:0:0/g:ce:0:0/q:85/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3Zpcmdpbmlhc3BvcnRzLWNvbS1wcm9kLzIwMjUvMDEvMDcvZTFTQUVHRE5mWWRLYkNOc21QQk12VlRONXI3Ymo5bkI2MHdGOEptOS5qcGc.jpg",
}

@st.cache_data
def load_data():
    """Build all player data from the uploaded Virginia season stats."""
    players = {
        "Madison Alaimo": {"num": 16, "pos": "A", "yr": "Jr", "gp": 5, "gs": 5,
            "g": 10, "a": 15, "pts": 25, "sh": 18, "sh_pct": 55.6, "sog": 16, "sog_pct": 88.9,
            "gb": 4, "dc": 0, "to": 11, "ct": 1, "fpg": 3, "fps": 4, "yc": 0, "gc": 2,
            "game_g": [0,5,3,4,2], "game_a": [4,1,2,3,3], "game_pts": [4,6,5,7,5],
            "game_sh": [3,5,5,4,3], "game_to": [4,2,0,1,4]},
        "Jenna Dinardo": {"num": 4, "pos": "A", "yr": "Jr", "gp": 5, "gs": 5,
            "g": 9, "a": 2, "pts": 11, "sh": 29, "sh_pct": 31.0, "sog": 26, "sog_pct": 89.7,
            "gb": 3, "dc": 8, "to": 10, "ct": 2, "fpg": 3, "fps": 9, "yc": 1, "gc": 3,
            "game_g": [1,3,3,1,1], "game_a": [0,1,1,0,0], "game_pts": [1,4,4,1,1],
            "game_sh": [4,10,8,6,5], "game_to": [3,2,2,1,4]},
        "Addi Foster": {"num": 15, "pos": "A", "yr": "Jr", "gp": 5, "gs": 5,
            "g": 10, "a": 2, "pts": 12, "sh": 24, "sh_pct": 41.7, "sog": 20, "sog_pct": 83.3,
            "gb": 2, "dc": 0, "to": 3, "ct": 0, "fpg": 2, "fps": 2, "yc": 1, "gc": 1,
            "game_g": [0,4,2,3,1], "game_a": [0,1,0,0,1], "game_pts": [0,5,2,3,2],
            "game_sh": [1,5,3,6,6], "game_to": [1,1,0,1,0]},
        "Kate Galica": {"num": 5, "pos": "M", "yr": "Jr", "gp": 5, "gs": 5,
            "g": 6, "a": 5, "pts": 11, "sh": 24, "sh_pct": 25.0, "sog": 17, "sog_pct": 70.8,
            "gb": 13, "dc": 35, "to": 13, "ct": 10, "fpg": 1, "fps": 4, "yc": 0, "gc": 3,
            "game_g": [2,1,0,1,3], "game_a": [0,1,0,2,2], "game_pts": [2,2,0,3,5],
            "game_sh": [3,5,5,6,7], "game_to": [1,4,4,4,2]},
        "Cady Flaherty": {"num": 6, "pos": "M", "yr": "Fr", "gp": 5, "gs": 2,
            "g": 4, "a": 1, "pts": 5, "sh": 7, "sh_pct": 57.1, "sog": 6, "sog_pct": 85.7,
            "gb": 3, "dc": 1, "to": 1, "ct": 2, "fpg": 3, "fps": 3, "yc": 0, "gc": 3,
            "game_g": [2,0,1,1,0], "game_a": [0,1,1,0,0], "game_pts": [2,1,2,1,0],
            "game_sh": [2,1,2,2,1], "game_to": [0,0,0,1,0]},
        "Gabby Laverghetta": {"num": 43, "pos": "A", "yr": "So", "gp": 5, "gs": 3,
            "g": 5, "a": 2, "pts": 7, "sh": 8, "sh_pct": 62.5, "sog": 6, "sog_pct": 75.0,
            "gb": 3, "dc": 0, "to": 3, "ct": 0, "fpg": 0, "fps": 0, "yc": 1, "gc": 3,
            "game_g": [2,1,0,1,0], "game_a": [1,1,0,0,0], "game_pts": [3,2,0,1,0],
            "game_sh": [3,1,0,2,0], "game_to": [0,0,0,2,0]},
        "Livy Laverghetta": {"num": 42, "pos": "M", "yr": "So", "gp": 5, "gs": 0,
            "g": 3, "a": 1, "pts": 4, "sh": 4, "sh_pct": 75.0, "sog": 4, "sog_pct": 100.0,
            "gb": 2, "dc": 1, "to": 2, "ct": 0, "fpg": 0, "fps": 0, "yc": 0, "gc": 0,
            "game_g": [1,1,1,1,0], "game_a": [0,1,0,1,0], "game_pts": [1,2,1,2,0],
            "game_sh": [1,1,1,1,0], "game_to": [0,0,0,0,0]},
        "Raleigh Foster": {"num": 10, "pos": "A", "yr": "Fr", "gp": 2, "gs": 0,
            "g": 3, "a": 0, "pts": 3, "sh": 7, "sh_pct": 42.9, "sog": 6, "sog_pct": 85.7,
            "gb": 0, "dc": 0, "to": 0, "ct": 0, "fpg": 0, "fps": 0, "yc": 0, "gc": 0,
            "game_g": [1,2], "game_a": [0,0], "game_pts": [1,2],
            "game_sh": [4,3], "game_to": [0,0]},
        "Alex Reilly": {"num": 23, "pos": "M", "yr": "So", "gp": 5, "gs": 5,
            "g": 1, "a": 0, "pts": 1, "sh": 5, "sh_pct": 20.0, "sog": 3, "sog_pct": 60.0,
            "gb": 2, "dc": 6, "to": 3, "ct": 2, "fpg": 0, "fps": 0, "yc": 2, "gc": 1,
            "game_g": [1,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [1,0,0,0,0],
            "game_sh": [3,0,0,0,0], "game_to": [0,0,0,0,1]},
        "Payton Sfreddo": {"num": 7, "pos": "M", "yr": "So", "gp": 5, "gs": 0,
            "g": 1, "a": 0, "pts": 1, "sh": 1, "sh_pct": 100.0, "sog": 1, "sog_pct": 100.0,
            "gb": 3, "dc": 1, "to": 1, "ct": 1, "fpg": 0, "fps": 0, "yc": 0, "gc": 1,
            "game_g": [1,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [1,0,0,0,0],
            "game_sh": [1,0,0,0,0], "game_to": [0,0,0,0,0]},
        "Kate Demark": {"num": 3, "pos": "D", "yr": "Jr", "gp": 5, "gs": 5,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 3, "dc": 0, "to": 0, "ct": 10, "fpg": 0, "fps": 0, "yc": 0, "gc": 2,
            "game_g": [0,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [0,0,0,0,0],
            "game_sh": [0,0,0,0,0], "game_to": [0,0,0,0,0]},
        "Alexandra Schneider": {"num": 8, "pos": "D", "yr": "Jr", "gp": 5, "gs": 5,
            "g": 0, "a": 0, "pts": 0, "sh": 1, "sh_pct": 0, "sog": 1, "sog_pct": 100.0,
            "gb": 2, "dc": 0, "to": 0, "ct": 6, "fpg": 0, "fps": 0, "yc": 1, "gc": 0,
            "game_g": [0,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [0,0,0,0,0],
            "game_sh": [0,0,1,0,0], "game_to": [0,0,0,0,0]},
        "Sophia Conti": {"num": 9, "pos": "M", "yr": "So", "gp": 5, "gs": 5,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 9, "dc": 0, "to": 2, "ct": 4, "fpg": 0, "fps": 0, "yc": 0, "gc": 1,
            "game_g": [0,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [0,0,0,0,0],
            "game_sh": [0,0,0,0,0], "game_to": [1,0,1,0,1]},
        "Lara Kology": {"num": 36, "pos": "D", "yr": "Sr", "gp": 5, "gs": 5,
            "g": 0, "a": 0, "pts": 0, "sh": 1, "sh_pct": 0, "sog": 1, "sog_pct": 100.0,
            "gb": 7, "dc": 1, "to": 1, "ct": 1, "fpg": 0, "fps": 0, "yc": 1, "gc": 2,
            "game_g": [0,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [0,0,0,0,0],
            "game_sh": [0,1,0,1,0], "game_to": [1,0,0,0,0]},
        "Elyse Finnelle": {"num": 34, "pos": "GK", "yr": "Sr", "gp": 5, "gs": 3,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 10, "dc": 0, "to": 0, "ct": 1, "fpg": 0, "fps": 0, "yc": 0, "gc": 0,
            "gk_min": 230.82, "gk_ga": 39, "gk_gaa": 10.14, "gk_sv": 23, "gk_sv_pct": 37.1,
            "gk_w": 2, "gk_l": 1,
            "game_g": [0,0,0,0,0], "game_a": [0,0,0,0,0], "game_pts": [0,0,0,0,0],
            "game_sh": [0,0,0,0,0], "game_to": [0,0,0,0,0]},
        "Mel Josephson": {"num": 26, "pos": "GK", "yr": "Sr", "gp": 3, "gs": 2,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 3, "dc": 0, "to": 0, "ct": 0, "fpg": 0, "fps": 0, "yc": 0, "gc": 0,
            "gk_min": 68.47, "gk_ga": 17, "gk_gaa": 14.90, "gk_sv": 10, "gk_sv_pct": 37.0,
            "gk_w": 0, "gk_l": 2,
            "game_g": [0,0,0], "game_a": [0,0,0], "game_pts": [0,0,0],
            "game_sh": [0,0,0], "game_to": [0,0,0]},
        "Carly Kennedy": {"num": 13, "pos": "M", "yr": "So", "gp": 3, "gs": 2,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 4, "dc": 0, "to": 0, "ct": 3, "fpg": 0, "fps": 0, "yc": 0, "gc": 1,
            "game_g": [0,0,0], "game_a": [0,0,0], "game_pts": [0,0,0],
            "game_sh": [0,0,0], "game_to": [0,0,0]},
        "Megan Rocklein": {"num": 11, "pos": "M", "yr": "Fr", "gp": 3, "gs": 0,
            "g": 0, "a": 2, "pts": 2, "sh": 1, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 1, "dc": 0, "to": 3, "ct": 0, "fpg": 0, "fps": 0, "yc": 0, "gc": 0,
            "game_g": [0,0,0], "game_a": [0,2,0], "game_pts": [0,2,0],
            "game_sh": [0,0,1], "game_to": [1,0,2]},
        "Fiona Allen": {"num": 41, "pos": "A", "yr": "So", "gp": 4, "gs": 0,
            "g": 1, "a": 1, "pts": 2, "sh": 2, "sh_pct": 50.0, "sog": 1, "sog_pct": 50.0,
            "gb": 0, "dc": 0, "to": 1, "ct": 0, "fpg": 1, "fps": 1, "yc": 0, "gc": 0,
            "game_g": [0,0,1,0], "game_a": [1,0,0,0], "game_pts": [1,0,1,0],
            "game_sh": [0,0,1,0], "game_to": [0,0,0,0]},
        "Abby Musser": {"num": 14, "pos": "D", "yr": "So", "gp": 4, "gs": 3,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 2, "dc": 0, "to": 1, "ct": 1, "fpg": 0, "fps": 0, "yc": 1, "gc": 0,
            "game_g": [0,0,0,0], "game_a": [0,0,0,0], "game_pts": [0,0,0,0],
            "game_sh": [0,0,0,0], "game_to": [0,0,0,1]},
        "Jayden Piraino": {"num": 2, "pos": "A", "yr": "So", "gp": 1, "gs": 0,
            "g": 2, "a": 0, "pts": 2, "sh": 2, "sh_pct": 100.0, "sog": 2, "sog_pct": 100.0,
            "gb": 0, "dc": 0, "to": 0, "ct": 0, "fpg": 1, "fps": 1, "yc": 0, "gc": 0,
            "game_g": [2], "game_a": [0], "game_pts": [2],
            "game_sh": [2], "game_to": [0]},
        "Corey White": {"num": 25, "pos": "M", "yr": "Jr", "gp": 4, "gs": 0,
            "g": 0, "a": 0, "pts": 0, "sh": 0, "sh_pct": 0, "sog": 0, "sog_pct": 0,
            "gb": 0, "dc": 1, "to": 0, "ct": 0, "fpg": 0, "fps": 0, "yc": 0, "gc": 0,
            "game_g": [0,0,0,0], "game_a": [0,0,0,0], "game_pts": [0,0,0,0],
            "game_sh": [0,0,0,0], "game_to": [0,0,0,0]},
    }
    games = ["vs Navy (L 12-10)", "vs Richmond (L 12-11)", "at Maryland (L 17-9)", "at Liberty (W 17-8)", "at Notre Dame (W 9-7)"]
    game_results = ["L", "L", "L", "W", "W"]
    return players, games, game_results


# ═══════════════════════════════════════════════
# METRICS ENGINE
# ═══════════════════════════════════════════════

def compute_advanced_metrics(p):
    gp = max(p["gp"], 1)
    m = {}
    m["ppg"] = p["pts"] / gp
    m["gpg"] = p["g"] / gp
    m["apg"] = p["a"] / gp
    m["pts_per_shot"] = p["pts"] / max(p["sh"], 1)
    m["shot_quality"] = (p.get("sog_pct", 0) * p.get("sh_pct", 0)) / 100
    poss_inv = p["sh"] + p["to"] + p["dc"] + p["gb"]
    m["poss_involvement"] = poss_inv
    m["to_rate"] = p["to"] / max(poss_inv, 1)
    m["poss_impact"] = p["gb"] + p["dc"] + p["ct"] - p["to"]
    m["fp_eff"] = p["fpg"] / max(p["fps"], 1) * 100
    m["discipline_raw"] = p["yc"] * 3 + p["gc"] * 1
    m["gbpg"] = p["gb"] / gp
    m["dcpg"] = p["dc"] / gp
    m["ctpg"] = p["ct"] / gp
    m["topg"] = p["to"] / gp
    # Consistency
    game_pts = p.get("game_pts", [])
    if len(game_pts) > 1 and np.mean(game_pts) > 0:
        m["consistency"] = 1 - min(np.std(game_pts) / np.mean(game_pts), 1)
    elif len(game_pts) > 0 and np.mean(game_pts) > 0:
        m["consistency"] = 1.0
    else:
        m["consistency"] = 0.5
    # Clutch
    game_g = p.get("game_g", [])
    if len(game_g) == 5:
        loss_avg = np.mean(game_g[:3]) if sum(game_g[:3]) > 0 else 0.001
        win_avg = np.mean(game_g[3:])
        m["clutch_ratio"] = win_avg / max(loss_avg, 0.001)
    else:
        m["clutch_ratio"] = 1.0
    return m


def compute_impact_scores(p, metrics, team_avg):
    pos = p["pos"]
    scores = {}
    def norm(val, max_val, invert=False):
        if max_val == 0: return 50
        r = min(val / max_val, 1.5) / 1.5 * 100
        return 100 - r if invert else r

    scores["offensive"] = min(100, norm(metrics["gpg"], team_avg["max_gpg"]) * 0.35 +
        norm(p["sh_pct"], 75) * 0.25 + norm(metrics["ppg"], team_avg["max_ppg"]) * 0.25 +
        norm(p["a"] / max(p["gp"],1), team_avg["max_apg"]) * 0.15)
    scores["defensive"] = min(100, norm(p["ct"] / max(p["gp"],1), team_avg["max_ctpg"]) * 0.45 +
        norm(p["gb"] / max(p["gp"],1), team_avg["max_gbpg"]) * 0.35 +
        norm(metrics["discipline_raw"], 10, invert=True) * 0.20)
    scores["possession"] = min(100, norm(metrics["poss_impact"], team_avg["max_poss_impact"]) * 0.40 +
        norm(p["dc"] / max(p["gp"],1), team_avg["max_dcpg"]) * 0.35 +
        norm(p["gb"] / max(p["gp"],1), team_avg["max_gbpg"]) * 0.25)
    scores["efficiency"] = min(100, norm(p["sh_pct"], 75) * 0.30 +
        norm(p["sog_pct"], 100) * 0.25 + norm(metrics["to_rate"], 1, invert=True) * 0.25 +
        norm(metrics["consistency"], 1) * 0.20)
    scores["discipline"] = max(0, 100 - metrics["discipline_raw"] * 12)

    if pos == "A": w = {"offensive": 0.40, "defensive": 0.05, "possession": 0.15, "efficiency": 0.30, "discipline": 0.10}
    elif pos == "M": w = {"offensive": 0.25, "defensive": 0.20, "possession": 0.25, "efficiency": 0.20, "discipline": 0.10}
    elif pos == "D": w = {"offensive": 0.05, "defensive": 0.45, "possession": 0.20, "efficiency": 0.10, "discipline": 0.20}
    elif pos == "GK": w = {"offensive": 0.00, "defensive": 0.35, "possession": 0.15, "efficiency": 0.35, "discipline": 0.15}
    else: w = {"offensive": 0.25, "defensive": 0.25, "possession": 0.20, "efficiency": 0.20, "discipline": 0.10}
    scores["overall"] = sum(scores[k] * v for k, v in w.items())

    if pos == "GK" and "gk_sv_pct" in p:
        sv_score = norm(p["gk_sv_pct"], 60) * 0.40
        gaa_score = norm(20 - p["gk_gaa"], 20) * 0.30
        gb_score = norm(p["gb"] / max(p["gp"],1), team_avg["max_gbpg"]) * 0.15
        disc = scores["discipline"] * 0.15
        scores["overall"] = sv_score + gaa_score + gb_score + disc
        scores["efficiency"] = sv_score / 0.40
        scores["defensive"] = gaa_score / 0.30
    return scores


def get_development_flags(p, metrics, scores):
    flags = []
    if p["to"] / max(p["gp"],1) >= 2.0 and p["pts"] > 0: flags.append(("High Turnover Risk", "negative"))
    if p["sh_pct"] >= 50 and p["sh"] >= 5: flags.append(("Elite Finisher", "positive"))
    if p["sh_pct"] < 30 and p["sh"] >= 10: flags.append(("Shot Selection Concern", "warning"))
    if metrics.get("fp_eff", 0) >= 70 and p["fps"] >= 3: flags.append(("FP Specialist", "positive"))
    if p["ct"] / max(p["gp"],1) >= 1.5: flags.append(("Defensive Disruptor", "positive"))
    if p["dc"] / max(p["gp"],1) >= 3: flags.append(("Draw Control Engine", "positive"))
    if p["gb"] / max(p["gp"],1) >= 1.5: flags.append(("Ground Ball Magnet", "positive"))
    if metrics["consistency"] >= 0.7 and p["pts"] > 3: flags.append(("Reliable Contributor", "info"))
    if metrics["consistency"] < 0.4 and p["pts"] > 3: flags.append(("High Variance", "warning"))
    if metrics.get("clutch_ratio", 1) >= 1.5 and p["g"] >= 3: flags.append(("Clutch Performer", "positive"))
    if scores["discipline"] <= 60: flags.append(("Discipline Concern", "warning"))
    if p["pos"] == "GK":
        if p.get("gk_sv_pct", 0) >= 40: flags.append(("Solid Save Rate", "positive"))
        if p.get("gk_gaa", 20) <= 10: flags.append(("Low GAA", "positive"))
        if p.get("gk_gaa", 0) >= 14: flags.append(("High GAA Concern", "negative"))
    if p["a"] / max(p["gp"],1) >= 2: flags.append(("Elite Playmaker", "positive"))
    if p["pts"] == 0 and p["ct"] == 0 and p["gb"] <= 2 and p["dc"] == 0: flags.append(("Limited Impact", "negative"))
    return flags


def get_tier(scores, p):
    s = scores["overall"]
    if s >= 65: return 1, "Program Driver"
    elif s >= 45: return 2, "System Amplifier"
    elif s >= 25: return 3, "Situational Specialist"
    else: return 4, "Developmental"


def generate_coaching_notes(name, p, metrics, scores, tier_num, flags):
    pos_full = {"A": "Attacker", "M": "Midfielder", "D": "Defender", "GK": "Goalkeeper"}[p["pos"]]
    tier_names = {1: "Program Driver", 2: "System Amplifier", 3: "Situational Specialist", 4: "Developmental Player"}
    note = f"{name} is a {p['yr']} {pos_full} classified as a **Tier {tier_num} — {tier_names[tier_num]}**. "
    if p["pos"] == "A":
        if p["g"] >= 8: note += f"She is a primary scoring threat with {p['g']}G and {p['a']}A in {p['gp']} games. "
        if p["sh_pct"] < 35 and p["sh"] > 15: note += f"However, her {p['sh_pct']:.0f}% shooting on {p['sh']} shots suggests shot selection needs refinement. "
        if p["to"] >= 8: note += f"Her {p['to']} turnovers are a concern and represent a key development area. "
        if p["a"] >= 10: note += f"Her {p['a']} assists make her the offense's primary distributor. "
    elif p["pos"] == "M":
        if p["dc"] >= 20: note += f"She dominates the draw circle with {p['dc']} draw controls. "
        if p["pts"] >= 5: note += f"Contributes offensively with {p['pts']} points. "
        if p["ct"] >= 5: note += f"Adds defensive value with {p['ct']} caused turnovers. "
    elif p["pos"] == "D":
        if p["ct"] >= 5: note += f"An elite defender with {p['ct']} caused turnovers. "
        if p["gb"] >= 5: note += f"Active on ground balls ({p['gb']}). "
    elif p["pos"] == "GK" and "gk_sv_pct" in p:
        note += f"Posted a {p['gk_sv_pct']:.1f}% save rate with {p['gk_gaa']:.2f} GAA. "
    flag_names = [f[0] for f in flags]
    pos_flags = [f for f in flag_names if any(x in f for x in ["Elite", "Specialist", "Engine", "Clutch", "Reliable", "Solid", "Low GAA"])]
    if pos_flags: note += f"Key strengths: {', '.join(pos_flags)}. "
    return note


def generate_recommendations(name, p, metrics, scores, tier_num, flags):
    """Generate actionable coaching recommendations."""
    recs = []
    pos = p["pos"]
    gp = max(p["gp"], 1)

    if pos == "A":
        if p["sh_pct"] < 35 and p["sh"] >= 10:
            recs.append(f"🎯 **Shot Selection:** {name}'s {p['sh_pct']:.0f}% shooting on {p['sh']} shots is below the productive threshold. Focus drills on shooting from higher-percentage zones and reducing contested attempts. Consider a 'two-touch-before-shoot' constraint in practice.")
        if p["to"] / gp >= 2.0:
            recs.append(f"🔄 **Ball Security:** Averaging {p['to']/gp:.1f} TO/game — work on off-hand stick skills and decision-making under pressure. Use small-sided games with turnover penalties to build awareness.")
        if p["a"] / gp >= 2 and p["g"] / gp >= 1.5:
            recs.append(f"⭐ **Maximize Usage:** {name} is a dual-threat creator ({metrics['gpg']:.1f} G/gm, {metrics['apg']:.1f} A/gm). She should be the primary option in critical possessions and settled offense. Consider running the offense through her in close games.")
        if p["g"] >= 5 and p["a"] < 3:
            recs.append(f"👀 **Expand Playmaking:** Strong finisher with {p['g']}G but only {p['a']}A — encourage her to look for the extra pass when doubled. This will open up her own shots long-term.")
        if metrics["consistency"] < 0.5 and p["pts"] >= 5:
            recs.append(f"📊 **Reduce Variance:** Point production is inconsistent (game pts: {p['game_pts']}). Use her in structured sets where she's guaranteed touches rather than relying on transition opportunities.")
        if tier_num >= 3 and p["gp"] >= 3:
            recs.append(f"🕐 **Situational Deployment:** Deploy {name} primarily in man-up / free-position situations and as a late-game spark plug off the bench rather than full-game starter.")

    elif pos == "M":
        if p["dc"] / gp >= 3:
            recs.append(f"🏆 **Protect the Draw:** {name} at {p['dc']/gp:.0f} DC/game is an elite asset. Ensure she takes every draw and build secondary draw options to spell her in blowouts. Track draw-to-goal conversion rate.")
        if p["ct"] / gp >= 1.5 and p["pts"] >= 5:
            recs.append(f"🔥 **Two-Way Star:** Rare combo of {p['ct']} CTs and {p['pts']} PTS — maximize her minutes in competitive games. She impacts both ends.")
        if p["to"] / gp >= 2.0:
            recs.append(f"🔄 **Transition Discipline:** High turnovers ({p['to']}) for a midfielder. Focus on controlled clears and limiting risky passes in the midfield. Use film sessions to identify turnover patterns.")
        if p["sh_pct"] < 30 and p["sh"] >= 5:
            recs.append(f"🎯 **Shot Quality:** Only {p['sh_pct']:.0f}% shooting — reduce long-range attempts and focus on feeding attackers or driving to higher-percentage areas before releasing.")
        if tier_num >= 3:
            recs.append(f"🕐 **Role Clarity:** Use {name} as a defensive midfielder or draw-circle specialist rather than expecting offensive production. Clear role definition will boost confidence.")

    elif pos == "D":
        if p["ct"] / gp >= 1.5:
            recs.append(f"🛡️ **Defensive Anchor:** {name}'s {p['ct']/gp:.1f} CTs/game make her a cornerstone — assign her to the opponent's top attacker in every game.")
        if p["gb"] / gp >= 1.5:
            recs.append(f"💪 **Ground Ball Intensity:** Strong ground ball rate ({p['gb']/gp:.1f}/gm) — use her on the draw circle for first-ground-ball recovery.")
        if scores["discipline"] <= 60:
            recs.append(f"⚠️ **Penalty Management:** Card accumulation is a risk — work on body positioning and footwork to avoid reaching fouls. A 1-game suspension would hurt the defense.")
        if tier_num >= 3 and p["ct"] < 3:
            recs.append(f"📈 **Development Focus:** Needs to increase disruptive plays (only {p['ct']} CTs). Use video breakdown to improve anticipation and check timing. Consider more minutes in lower-leverage situations to build experience.")

    elif pos == "GK":
        if p.get("gk_sv_pct", 0) < 40:
            recs.append(f"🧤 **Save Rate Development:** {p.get('gk_sv_pct', 0):.1f}% is below D1 average (~45%). Focus on positioning drills, especially on free-position shots. Track save % by shot location to find weaknesses.")
        if p.get("gk_gaa", 0) >= 12:
            recs.append(f"📉 **Defensive System Review:** {p.get('gk_gaa', 0):.2f} GAA is elevated — this isn't solely a goalkeeper issue. Review defensive slide packages and communication protocols to reduce high-quality shots against.")
        if p.get("gk_w", 0) >= 2:
            recs.append(f"✅ **Start in Big Games:** {name}'s experience in wins makes her the clear choice for high-leverage matchups. Build confidence with clear communication from the coaching staff.")

    # Universal recommendations
    if len(recs) == 0:
        if tier_num == 4:
            recs.append(f"🌱 **Development Plan:** {name} needs increased practice reps to earn more game minutes. Focus on her best positional skill and track improvement weekly.")
        elif tier_num == 3:
            recs.append(f"📋 **Defined Role:** {name} can contribute in specific situations. Identify her top 1-2 skills and deploy her accordingly — don't ask her to do everything.")

    return recs


# ═══════════════════════════════════════════════
# VISUALIZATION BUILDERS
# ═══════════════════════════════════════════════

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=UVA_BLUE),
    margin=dict(l=30, r=30, t=40, b=30),
)


def make_radar_chart(scores, pos, height=300):
    if pos == "A":
        cats = ["Scoring", "Efficiency", "Playmaking", "Shot Quality", "Discipline", "Possession"]
        vals = [scores["offensive"], scores["efficiency"], min(scores["offensive"]*0.6+scores["possession"]*0.4,100),
                scores["efficiency"]*0.8, scores["discipline"], scores["possession"]]
    elif pos == "M":
        cats = ["Offense", "Defense", "Draw Control", "Possession", "Efficiency", "Discipline"]
        vals = [scores["offensive"], scores["defensive"], scores["possession"],
                scores["possession"]*0.8+scores["efficiency"]*0.2, scores["efficiency"], scores["discipline"]]
    elif pos == "D":
        cats = ["Disruption", "Ground Balls", "Discipline", "Clear Impact", "Possession", "Low TO"]
        vals = [scores["defensive"], scores["possession"]*0.8, scores["discipline"],
                scores["defensive"]*0.6+scores["possession"]*0.4, scores["possession"], scores["efficiency"]]
    elif pos == "GK":
        cats = ["Save %", "GAA (inv)", "Consistency", "Ground Balls", "Win Impact", "Discipline"]
        vals = [scores["efficiency"], scores["defensive"], scores["efficiency"]*0.9,
                scores["possession"], scores["overall"], scores["discipline"]]
    else:
        cats = ["Offense", "Defense", "Possession", "Efficiency", "Discipline"]
        vals = [scores["offensive"], scores["defensive"], scores["possession"], scores["efficiency"], scores["discipline"]]

    vals = [max(0, min(v, 100)) for v in vals]
    vals.append(vals[0])
    cats.append(cats[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        fillcolor=f'rgba(229,114,0,0.15)', line=dict(color=UVA_ORANGE, width=2.5),
        marker=dict(size=6, color=UVA_ORANGE)
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                          gridcolor=UVA_BLUE_25),
            angularaxis=dict(gridcolor=UVA_BLUE_25,
                           tickfont=dict(size=10, color=TEXT_GRAY))
        ),
        showlegend=False, height=height,
    )
    return fig


def make_game_log_chart(p, games):
    game_g = p.get("game_g", [])
    game_pts = p.get("game_pts", [])
    game_to = p.get("game_to", [])
    n = len(game_g)
    labels = [f"G{i+1}" for i in range(n)]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=game_pts, name="Points",
        marker_color=f"rgba(229,114,0,0.5)", marker_line=dict(color=UVA_ORANGE, width=1)))
    fig.add_trace(go.Scatter(x=labels, y=game_g, name="Goals", mode="lines+markers",
        line=dict(color=UVA_GREEN, width=2.5), marker=dict(size=7)))
    if any(t > 0 for t in game_to):
        fig.add_trace(go.Scatter(x=labels, y=game_to, name="TO", mode="lines+markers",
            line=dict(color=UVA_MAGENTA, width=2, dash="dot"), marker=dict(size=6)))
    fig.update_layout(**PLOTLY_LAYOUT, height=240, barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
        yaxis=dict(gridcolor=MED_GRAY, title=None), xaxis=dict(title=None))
    return fig


def make_shot_efficiency_bar(p):
    cats = ["Shots", "SOG", "Goals"]
    vals = [p["sh"], p.get("sog", 0), p["g"]]
    colors = [UVA_BLUE_25, UVA_ORANGE_25, UVA_ORANGE]
    fig = go.Figure()
    for c, v, col in zip(cats, vals, colors):
        text_color = WHITE if col == UVA_ORANGE else UVA_BLUE
        fig.add_trace(go.Bar(y=[c], x=[v], orientation="h", marker_color=col,
            text=[str(v)], textposition="inside",
            textfont=dict(color=text_color, size=13), name=c, showlegend=False))
    fig.update_layout(**PLOTLY_LAYOUT, height=130, barmode="group",
        xaxis=dict(visible=False), yaxis=dict(tickfont=dict(size=11, color=TEXT_GRAY)))
    return fig


def make_percentile_bars(scores, pos):
    """Horizontal percentile bars for impact categories."""
    cats = ["Offense", "Defense", "Possession", "Efficiency", "Discipline"]
    keys = ["offensive", "defensive", "possession", "efficiency", "discipline"]
    vals = [scores[k] for k in keys]

    colors = []
    for v in vals:
        if v >= 65: colors.append(UVA_GREEN)
        elif v >= 40: colors.append(UVA_YELLOW)
        else: colors.append(UVA_MAGENTA)

    fig = go.Figure()
    # Background bars
    fig.add_trace(go.Bar(y=cats, x=[100]*5, orientation="h", marker_color=LIGHT_GRAY,
        showlegend=False, hoverinfo="skip"))
    # Value bars
    fig.add_trace(go.Bar(y=cats, x=vals, orientation="h", marker_color=colors,
        text=[f"{v:.0f}" for v in vals], textposition="inside",
        textfont=dict(size=12, color=WHITE, family="DM Sans"), showlegend=False))
    fig.update_layout(**PLOTLY_LAYOUT, height=200, barmode="overlay",
        xaxis=dict(range=[0, 100], visible=False),
        yaxis=dict(tickfont=dict(size=11, color=TEXT_GRAY), autorange="reversed"))
    return fig


def make_rolling_avg_chart(p):
    """Rolling average trend for goals."""
    game_g = p.get("game_g", [])
    n = len(game_g)
    if n < 3: return None
    labels = [f"G{i+1}" for i in range(n)]
    rolling = pd.Series(game_g).rolling(window=3, min_periods=1).mean().tolist()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=labels, y=game_g, mode="markers", name="Actual",
        marker=dict(size=10, color=UVA_ORANGE, line=dict(width=1, color=WHITE))))
    fig.add_trace(go.Scatter(x=labels, y=rolling, mode="lines", name="3-Game Avg",
        line=dict(color=UVA_BLUE, width=3)))
    fig.update_layout(**PLOTLY_LAYOUT, height=200, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
        yaxis=dict(gridcolor=MED_GRAY, title=None), xaxis=dict(title=None))
    return fig


def make_cumulative_points_chart(all_data, top_n=6):
    """Cumulative points stacked area chart."""
    top_scorers = sorted([(n, d) for n, d in all_data.items() if d["player"]["pts"] >= 3],
                         key=lambda x: x[1]["player"]["pts"], reverse=True)[:top_n]
    if not top_scorers: return None
    colors = [UVA_ORANGE, UVA_BLUE, UVA_CYAN, UVA_GREEN, UVA_MAGENTA, UVA_YELLOW]
    fig = go.Figure()
    for idx, (name, data) in enumerate(top_scorers):
        game_pts = data["player"]["game_pts"]
        cum = np.cumsum(game_pts).tolist()
        labels = [f"G{i+1}" for i in range(len(game_pts))]
        fig.add_trace(go.Scatter(x=labels, y=cum, name=name, mode="lines+markers",
            line=dict(width=2.5, color=colors[idx % len(colors)]),
            marker=dict(size=5)))
    fig.update_layout(**PLOTLY_LAYOUT, height=350,
        legend=dict(font=dict(size=10)),
        yaxis=dict(gridcolor=MED_GRAY, title="Cumulative Points"),
        xaxis=dict(title=None))
    return fig


def make_usage_efficiency_chart(all_data):
    """Usage vs Efficiency quadrant plot."""
    scatter_data = []
    for name, data in all_data.items():
        p = data["player"]
        if p["gp"] >= 2 and p["sh"] >= 3:
            scatter_data.append({
                "name": name, "pos": p["pos"],
                "shots_per_game": p["sh"] / p["gp"],
                "shooting_pct": p["sh_pct"],
                "points": p["pts"],
                "tier": data["tier_num"],
            })
    if not scatter_data: return None
    df = pd.DataFrame(scatter_data)
    color_map = {"A": UVA_ORANGE, "M": UVA_BLUE, "D": UVA_GREEN, "GK": TEXT_GRAY}
    fig = px.scatter(df, x="shots_per_game", y="shooting_pct", size="points",
        color="pos", text="name", color_discrete_map=color_map,
        labels={"shots_per_game": "Shots / Game (Usage)", "shooting_pct": "Shooting % (Efficiency)", "pos": "Position"})
    fig.update_traces(textposition="top center", textfont_size=10)

    med_x = df["shots_per_game"].median()
    med_y = df["shooting_pct"].median()
    fig.add_hline(y=med_y, line_dash="dash", line_color=MED_GRAY, line_width=1)
    fig.add_vline(x=med_x, line_dash="dash", line_color=MED_GRAY, line_width=1)
    # Quadrant labels
    fig.add_annotation(x=df["shots_per_game"].max()*0.95, y=df["shooting_pct"].max()*0.95,
        text="⭐ Stars", showarrow=False, font=dict(size=11, color=UVA_GREEN))
    fig.add_annotation(x=df["shots_per_game"].min()*1.1, y=df["shooting_pct"].max()*0.95,
        text="💎 Efficient", showarrow=False, font=dict(size=11, color=UVA_CYAN))
    fig.add_annotation(x=df["shots_per_game"].max()*0.95, y=max(0, med_y * 0.3),
        text="📈 Volume", showarrow=False, font=dict(size=11, color=UVA_ORANGE))
    fig.add_annotation(x=df["shots_per_game"].min()*1.1, y=max(0, med_y * 0.3),
        text="📉 Low Impact", showarrow=False, font=dict(size=11, color=TEXT_GRAY))

    fig.update_layout(**PLOTLY_LAYOUT, height=450,
        xaxis=dict(gridcolor=MED_GRAY), yaxis=dict(gridcolor=MED_GRAY))
    return fig


def make_draw_control_chart(all_data):
    """Draw control analysis for top draw takers."""
    dc_players = sorted([(n, d) for n, d in all_data.items() if d["player"]["dc"] >= 1],
                        key=lambda x: x[1]["player"]["dc"], reverse=True)[:6]
    if not dc_players: return None
    names = [f"#{d['player']['num']} {n}" for n, d in dc_players]
    dcs = [d["player"]["dc"] for _, d in dc_players]
    colors = [UVA_ORANGE if d["player"]["dc"] >= 5 else UVA_BLUE_25 for _, d in dc_players]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=dcs, marker_color=colors,
        text=[str(d) for d in dcs], textposition="outside",
        textfont=dict(size=12, color=UVA_BLUE)))
    fig.update_layout(**PLOTLY_LAYOUT, height=300,
        yaxis=dict(gridcolor=MED_GRAY, title="Draw Controls"),
        xaxis=dict(tickfont=dict(size=10)))
    return fig


# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════

players, games, game_results = load_data()

# Compute team averages
team_avg = {}
active = {k: v for k, v in players.items() if v["gp"] >= 2}
team_avg["max_gpg"] = max(v["g"]/v["gp"] for v in active.values())
team_avg["max_ppg"] = max(v["pts"]/v["gp"] for v in active.values())
team_avg["max_apg"] = max(v["a"]/v["gp"] for v in active.values())
team_avg["max_ctpg"] = max(v["ct"]/v["gp"] for v in active.values())
team_avg["max_gbpg"] = max(v["gb"]/v["gp"] for v in active.values())
team_avg["max_dcpg"] = max(v["dc"]/v["gp"] for v in active.values())
team_avg["max_poss_impact"] = max(v["gb"]+v["dc"]+v["ct"]-v["to"] for v in active.values())

# Compute all player data
all_data = {}
for name, p in players.items():
    m = compute_advanced_metrics(p)
    s = compute_impact_scores(p, m, team_avg)
    flags = get_development_flags(p, m, s)
    tier_num, tier_label = get_tier(s, p)
    notes = generate_coaching_notes(name, p, m, s, tier_num, flags)
    recs = generate_recommendations(name, p, m, s, tier_num, flags)
    all_data[name] = {"player": p, "metrics": m, "scores": s, "flags": flags,
                      "tier_num": tier_num, "tier_label": tier_label, "notes": notes, "recs": recs}

# ─── HEADER ───
st.markdown("""
<div class="main-header">
    <div>
        <h1>⚔️ VIRGINIA CAVALIERS — PLAYER INTELLIGENCE</h1>
        <p>Women's Lacrosse · 2026 Season (5 Games) · Record: 2-3 · Advanced Player Analytics Dashboard</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("### ⚔️ Navigation")
    view_mode = st.radio("View", ["📋 Player Cards", "📊 Team Overview", "🔬 Comparison", "🎯 Recommendations", "🏆 Draw Control Center"],
                         label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### Filters")
    pos_filter = st.multiselect("Position", ["A", "M", "D", "GK"], default=["A", "M", "D", "GK"])
    tier_filter = st.multiselect("Tier", [1, 2, 3, 4], default=[1, 2, 3, 4],
        format_func=lambda x: {1:"Tier 1: Driver", 2:"Tier 2: Amplifier", 3:"Tier 3: Specialist", 4:"Tier 4: Dev"}[x])
    min_gp = st.slider("Min Games Played", 1, 5, 1)
    st.markdown("---")
    with st.expander("📐 Formula Reference"):
        st.markdown("""
        **Pts/Shot** = PTS / SH  
        **TO Rate** = TO / (SH+TO+DC+GB)  
        **Poss Impact** = GB+DC+CT−TO  
        **Consistency** = 1 − CV(pts/game)  
        **Clutch** = Avg G(wins) / Avg G(losses)
        """)

# Filter players
filtered = {k: v for k, v in all_data.items()
            if v["player"]["pos"] in pos_filter
            and v["tier_num"] in tier_filter
            and v["player"]["gp"] >= min_gp}
sorted_players = sorted(filtered.items(), key=lambda x: x[1]["scores"]["overall"], reverse=True)


# ═══════════════════════════════════════════════
# VIEW: PLAYER CARDS
# ═══════════════════════════════════════════════
if view_mode == "📋 Player Cards":
    for name, data in sorted_players:
        p = data["player"]
        m = data["metrics"]
        s = data["scores"]
        flags = data["flags"]

        tier_text = f"TIER {data['tier_num']} · {data['tier_label'].upper()}"

        st.markdown('<div class="player-card">', unsafe_allow_html=True)

        # Top row: headshot + name + impact score
        top1, top2, top3 = st.columns([0.5, 3.5, 1])
        with top1:
            img_url = HEADSHOT_URLS.get(name, "")
            if img_url:
                st.markdown(f'<img src="{img_url}" class="headshot-circle" onerror="this.style.display=\'none\'">', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="width:80px;height:80px;border-radius:50%;background:{UVA_BLUE_25};display:flex;align-items:center;justify-content:center;font-size:1.8rem;color:{UVA_BLUE};font-family:Bebas Neue;">{p["num"]}</div>', unsafe_allow_html=True)
        with top2:
            st.markdown(f'<p class="player-name">#{p["num"]} {name}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="player-meta">{p["pos"]} · {p["yr"]} · {p["gp"]} GP / {p["gs"]} GS <span class="tier-badge tier-{data["tier_num"]}">{tier_text}</span></p>', unsafe_allow_html=True)
        with top3:
            st.markdown(f'<div class="impact-score-box"><div class="impact-score-num">{s["overall"]:.0f}</div><div class="impact-score-label">Impact Score</div></div>', unsafe_allow_html=True)

        # Impact category bars
        cat_cols = st.columns(5)
        for col, (label, key) in zip(cat_cols, [("OFFENSE", "offensive"), ("DEFENSE", "defensive"),
                                                 ("POSSESSION", "possession"), ("EFFICIENCY", "efficiency"), ("DISCIPLINE", "discipline")]):
            val = s[key]
            color = UVA_GREEN if val >= 65 else UVA_YELLOW if val >= 40 else UVA_MAGENTA
            with col:
                st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:{color}">{val:.0f}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # Middle: radar + stats + game log
        col_radar, col_stats, col_gamelog = st.columns([1.2, 1, 1.3])
        with col_radar:
            st.plotly_chart(make_radar_chart(s, p["pos"]), use_container_width=True, key=f"radar_{name}")
        with col_stats:
            st.markdown("**Core Stats**")
            if p["pos"] != "GK":
                r1a, r1b, r1c, r1d = st.columns(4)
                r1a.metric("G", p["g"]); r1b.metric("A", p["a"])
                r1c.metric("PTS", p["pts"]); r1d.metric("SH%", f"{p['sh_pct']:.0f}%" if p["sh"] > 0 else "—")
                r2a, r2b, r2c, r2d = st.columns(4)
                r2a.metric("GB", p["gb"]); r2b.metric("DC", p["dc"])
                r2c.metric("TO", p["to"]); r2d.metric("CT", p["ct"])
            else:
                if "gk_sv_pct" in p:
                    r1a, r1b = st.columns(2)
                    r1a.metric("SV%", f"{p['gk_sv_pct']:.1f}%"); r1b.metric("GAA", f"{p['gk_gaa']:.2f}")
                    r2a, r2b = st.columns(2)
                    r2a.metric("Saves", p["gk_sv"]); r2b.metric("GA", p["gk_ga"])
                    r3a, r3b = st.columns(2)
                    r3a.metric("W-L", f"{p.get('gk_w',0)}-{p.get('gk_l',0)}"); r3b.metric("GB", p["gb"])
            st.markdown("**Advanced**")
            if p["pos"] != "GK" and p["sh"] > 0:
                a1, a2 = st.columns(2)
                a1.metric("Pts/Shot", f"{m['pts_per_shot']:.2f}"); a2.metric("TO Rate", f"{m['to_rate']:.2f}")
                a3, a4 = st.columns(2)
                a3.metric("Poss Impact", f"{m['poss_impact']:+d}"); a4.metric("Consistency", f"{m['consistency']:.2f}")
        with col_gamelog:
            st.markdown("**Game-by-Game Trend**")
            st.plotly_chart(make_game_log_chart(p, games), use_container_width=True, key=f"gl_{name}")

        # Shot funnel
        if p["sh"] >= 3 and p["pos"] != "GK":
            st.markdown("**Shot Funnel**")
            st.plotly_chart(make_shot_efficiency_bar(p), use_container_width=True, key=f"sf_{name}")

        # Flags
        if flags:
            flag_html = ""
            for fname, ftype in flags:
                flag_html += f'<span class="flag-tag flag-{ftype}">{fname}</span>'
            st.markdown(f"**Development Flags** &nbsp; {flag_html}", unsafe_allow_html=True)

        # Coaching notes
        st.markdown(f'<div class="coaching-notes">{data["notes"]}</div>', unsafe_allow_html=True)

        # Recommendations
        if data["recs"]:
            recs_html = "<br>".join(data["recs"][:2])
            st.markdown(f'<div class="rec-box">{recs_html}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("")


# ═══════════════════════════════════════════════
# VIEW: TEAM OVERVIEW
# ═══════════════════════════════════════════════
elif view_mode == "📊 Team Overview":
    st.markdown("## Team-Wide Impact Overview")

    # Tier Distribution
    tier_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    tier_players = {1: [], 2: [], 3: [], 4: []}
    for name, data in all_data.items():
        t = data["tier_num"]
        tier_counts[t] += 1
        tier_players[t].append(name)

    tc1, tc2, tc3, tc4 = st.columns(4)
    for col, t, label, color in [(tc1, 1, "Program Drivers", CAV_ORANGE), (tc2, 2, "System Amplifiers", UVA_CYAN),
                                  (tc3, 3, "Situational Specialists", UVA_GREEN), (tc4, 4, "Developmental", MED_GRAY)]:
        text_col = UVA_BLUE if color == MED_GRAY else color
        with col:
            st.markdown(f"<div style='text-align:center;padding:1.2rem;background:{WHITE};border-radius:14px;border:2px solid {color};box-shadow:0 2px 8px rgba(0,0,0,0.05);'>"
                       f"<div style='font-family:Bebas Neue;font-size:2.5rem;color:{text_col};'>{tier_counts[t]}</div>"
                       f"<div style='font-size:0.72rem;color:{TEXT_GRAY};text-transform:uppercase;letter-spacing:1px;font-weight:600;'>{label}</div>"
                       f"<div style='font-size:0.8rem;color:{UVA_BLUE};margin-top:8px;'>{'<br>'.join(tier_players[t][:5])}</div>"
                       f"</div>", unsafe_allow_html=True)

    st.markdown("")

    # Usage vs Efficiency quadrant
    st.markdown("### Usage vs Efficiency Matrix")
    ue_fig = make_usage_efficiency_chart(all_data)
    if ue_fig:
        st.plotly_chart(ue_fig, use_container_width=True)

    # Cumulative Points
    st.markdown("### Cumulative Scoring Progression")
    cum_fig = make_cumulative_points_chart(all_data)
    if cum_fig:
        st.plotly_chart(cum_fig, use_container_width=True)

    # Roster Heatmap
    st.markdown("### Roster Metrics Heatmap")
    heatmap_data = []
    heatmap_names = []
    for name, data in sorted_players:
        p = data["player"]
        s = data["scores"]
        if p["gp"] >= 2:
            heatmap_names.append(f"#{p['num']} {name}")
            heatmap_data.append([s["overall"], s["offensive"], s["defensive"],
                               s["possession"], s["efficiency"], s["discipline"]])
    if heatmap_data:
        fig = go.Figure(go.Heatmap(
            z=heatmap_data,
            x=["Overall", "Offense", "Defense", "Possession", "Efficiency", "Discipline"],
            y=heatmap_names,
            colorscale=[[0, "#FCE4EC"], [0.35, "#FFF8E1"], [0.6, "#E8F5E9"], [1, UVA_GREEN]],
            text=[[f"{v:.0f}" for v in row] for row in heatmap_data],
            texttemplate="%{text}", textfont=dict(size=11, color=UVA_BLUE),
            showscale=False,
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=max(400, len(heatmap_names)*35+80),
            yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
            xaxis=dict(side="top", tickfont=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════
# VIEW: COMPARISON
# ═══════════════════════════════════════════════
elif view_mode == "🔬 Comparison":
    st.markdown("## Head-to-Head Comparison")

    comp_names = [n for n, _ in sorted_players]
    comp_options = [f"#{all_data[n]['player']['num']} {n} ({all_data[n]['player']['pos']})" for n in comp_names]
    if len(comp_options) < 2:
        st.warning("Need at least 2 players for comparison.")
    else:
        c1, c2 = st.columns(2)
        with c1: p1_sel = st.selectbox("Player 1", comp_options, index=0)
        with c2: p2_sel = st.selectbox("Player 2", comp_options, index=min(1, len(comp_options)-1))

        p1_name = comp_names[comp_options.index(p1_sel)]
        p2_name = comp_names[comp_options.index(p2_sel)]
        d1, d2 = all_data[p1_name], all_data[p2_name]

        # Determine shared radar dimensions (use same categories for both)
        shared_cats = ["Offense", "Defense", "Possession", "Efficiency", "Discipline"]
        shared_keys = ["offensive", "defensive", "possession", "efficiency", "discipline"]

        # Side by side with headshots and matching radars
        rc1, rc2 = st.columns(2)
        for col, pname, pdata, color in [(rc1, p1_name, d1, UVA_ORANGE), (rc2, p2_name, d2, UVA_BLUE)]:
            with col:
                # Headshot + name
                img_url = HEADSHOT_URLS.get(pname, "")
                hdr = f'<div style="text-align:center;">'
                if img_url:
                    hdr += f'<img src="{img_url}" style="width:90px;height:90px;border-radius:50%;object-fit:cover;border:3px solid {color};margin-bottom:8px;" onerror="this.style.display=\'none\'">'
                hdr += f'<h3 style="color:{color} !important;margin:0;">{pname}</h3>'
                hdr += f'<p style="color:{TEXT_GRAY};font-size:0.85rem;">#{pdata["player"]["num"]} · {pdata["player"]["pos"]} · {pdata["player"]["yr"]} · Impact: {pdata["scores"]["overall"]:.0f}</p></div>'
                st.markdown(hdr, unsafe_allow_html=True)

                # Unified radar
                vals = [pdata["scores"][k] for k in shared_keys]
                vals = [max(0, min(v, 100)) for v in vals]
                vals.append(vals[0])
                cats_closed = shared_cats + [shared_cats[0]]
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=vals, theta=cats_closed, fill='toself',
                    fillcolor=f'rgba({",".join(str(int(color[i:i+2], 16)) for i in (1,3,5))},0.15)',
                    line=dict(color=color, width=2.5), marker=dict(size=6, color=color)))
                fig.update_layout(**PLOTLY_LAYOUT, polar=dict(bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor=MED_GRAY),
                    angularaxis=dict(gridcolor=MED_GRAY, tickfont=dict(size=10, color=TEXT_GRAY))),
                    showlegend=False, height=280)
                st.plotly_chart(fig, use_container_width=True, key=f"cmp_r_{pname}")

        # Comparison bar chart
        v1 = [d1["scores"][k] for k in shared_keys]
        v2 = [d2["scores"][k] for k in shared_keys]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=shared_cats, y=v1, name=p1_name, marker_color=UVA_ORANGE))
        fig.add_trace(go.Bar(x=shared_cats, y=v2, name=p2_name, marker_color=UVA_BLUE))
        fig.update_layout(**PLOTLY_LAYOUT, height=320, barmode="group",
            yaxis=dict(gridcolor=MED_GRAY, range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True)

        # Stats table
        st.markdown("### Raw Stats Comparison")
        stat_keys = ["gp", "g", "a", "pts", "sh", "sh_pct", "sog_pct", "gb", "dc", "to", "ct"]
        stat_labels = ["GP", "Goals", "Assists", "Points", "Shots", "SH%", "SOG%", "GB", "DC", "TO", "CT"]
        comp_df = pd.DataFrame({
            "Stat": stat_labels,
            p1_name: [d1["player"].get(k, "—") for k in stat_keys],
            p2_name: [d2["player"].get(k, "—") for k in stat_keys],
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════
# VIEW: RECOMMENDATIONS
# ═══════════════════════════════════════════════
elif view_mode == "🎯 Recommendations":
    st.markdown("## Coaching Recommendations & Playing Time Guidance")

    # Playing Time Matrix
    st.markdown("### Playing Time Recommendations")
    st.markdown(f'<p style="color:{TEXT_GRAY};font-size:0.9rem;">Based on impact scores, efficiency, and development flags — who should get more minutes, who should be situational, and where each player fits.</p>', unsafe_allow_html=True)

    for tier_num in [1, 2, 3, 4]:
        tier_players_list = [(n, d) for n, d in sorted_players if d["tier_num"] == tier_num]
        if not tier_players_list: continue
        tier_names_map = {1: "🔥 Program Drivers — Maximize Minutes", 2: "⚡ System Amplifiers — High Usage",
                     3: "🎯 Situational Specialists — Targeted Deployment", 4: "🌱 Developmental — Practice Priority"}
        tier_colors_map = {1: CAV_ORANGE, 2: UVA_CYAN, 3: UVA_GREEN, 4: MED_GRAY}

        st.markdown(f"#### {tier_names_map[tier_num]}")

        for name, data in tier_players_list:
            p = data["player"]
            img_url = HEADSHOT_URLS.get(name, "")

            with st.container(border=True):
                hcol, ncol = st.columns([0.4, 4])
                with hcol:
                    if img_url:
                        st.markdown(f'<img src="{img_url}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;border:2px solid {tier_colors_map[tier_num]};" onerror="this.style.display=\'none\'">', unsafe_allow_html=True)
                with ncol:
                    st.markdown(f"**#{p['num']} {name}** — {p['pos']} · {p['yr']} · Impact: {data['scores']['overall']:.0f}")
                    if data["recs"]:
                        for rec in data["recs"]:
                            st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="coaching-notes">{data["notes"]}</div>', unsafe_allow_html=True)

    # Team-Level Insights
    st.markdown("---")
    st.markdown("### Team-Level Strategic Insights")

    top_off = sorted(all_data.items(), key=lambda x: x[1]["scores"]["offensive"], reverse=True)[:3]
    top_def = sorted(all_data.items(), key=lambda x: x[1]["scores"]["defensive"], reverse=True)[:3]
    high_to = sorted([(k,v) for k,v in all_data.items() if v["player"]["to"] >= 5],
                    key=lambda x: x[1]["player"]["to"], reverse=True)

    i1, i2 = st.columns(2)
    with i1:
        st.markdown(f"""<div class="coaching-notes">
        <strong>🏆 Core Offensive Unit:</strong> {', '.join([n for n,_ in top_off])} should be the primary scoring trio. 
        They combine for {sum(d['player']['pts'] for _,d in top_off)} points on {sum(d['player']['g'] for _,d in top_off)} goals.<br><br>
        <strong>🛡️ Defensive Anchors:</strong> {', '.join([n for n,_ in top_def])} are the backbone — prioritize their health and minutes management.
        </div>""", unsafe_allow_html=True)
    with i2:
        to_text = ", ".join([f"{k} ({v['player']['to']} TO)" for k,v in high_to[:3]])
        st.markdown(f"""<div class="coaching-notes">
        <strong>⚠️ Turnover Reduction Priority:</strong> {to_text} — these players account for 
        {sum(v['player']['to'] for _,v in high_to[:3])} of the team's 57 turnovers. Film sessions and ball-handling drills needed.<br><br>
        <strong>🎯 Late-Game Lineup:</strong> Use Alaimo + Foster + Galica in crunch time — they have the highest clutch ratios and combined 
        for the majority of 4th quarter production.
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# VIEW: DRAW CONTROL CENTER
# ═══════════════════════════════════════════════
elif view_mode == "🏆 Draw Control Center":
    st.markdown("## Draw Control Center")
    st.markdown(f'<p style="color:{TEXT_GRAY};">Draw controls are the single highest-leverage stat in women\'s lacrosse. Teams winning 60%+ of draws gain multiple extra possessions per game, dramatically increasing win probability.</p>', unsafe_allow_html=True)

    # Team draw stats
    total_dc = sum(d["player"]["dc"] for d in all_data.values())
    dc_per_game = total_dc / 5

    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Total Draw Controls", total_dc)
    mc2.metric("DC / Game", f"{dc_per_game:.1f}")
    mc3.metric("Primary Draw Specialist", "Kate Galica (35)")

    st.markdown("")

    # Draw control distribution
    st.markdown("### Draw Control Distribution")
    dc_fig = make_draw_control_chart(all_data)
    if dc_fig:
        st.plotly_chart(dc_fig, use_container_width=True)

    # Galica deep dive
    st.markdown("### Kate Galica — Draw Control Deep Dive")
    galica = all_data.get("Kate Galica")
    if galica:
        p = galica["player"]
        g1, g2 = st.columns(2)
        with g1:
            st.markdown(f"""<div class="coaching-notes">
            <strong>Draw Control Dominance:</strong> {p['dc']} draws won across {p['gp']} games = {p['dc']/p['gp']:.0f} DC/game<br>
            She accounts for <strong>{p['dc']/max(total_dc,1)*100:.0f}%</strong> of all team draw controls.<br><br>
            <strong>Recommendation:</strong> Galica must take every draw in competitive games. Build a secondary option
            (Dinardo with {all_data.get('Jenna Dinardo', {}).get('player', {}).get('dc', 0)} DCs or Reilly with {all_data.get('Alex Reilly', {}).get('player', {}).get('dc', 0)} DCs)
            for rest in blowouts and as insurance.
            </div>""", unsafe_allow_html=True)
        with g2:
            # Galica's game-by-game rolling performance
            fig = make_rolling_avg_chart(p)
            if fig:
                st.markdown("**Goals Rolling Average (3-game)**")
                st.plotly_chart(fig, use_container_width=True)

    # Draw-to-Goal conversion
    st.markdown("### Draw Circle → Goal Conversion Pipeline")
    st.markdown(f"""<div class="rec-box">
    <strong>🔄 Team Draw-to-Goal Flow:</strong><br>
    Draw Controls Won: <strong>{total_dc}</strong> → Ground Balls Recovered: <strong>{sum(d['player']['gb'] for d in all_data.values())}</strong> → 
    Team Goals: <strong>56</strong><br><br>
    <strong>Key Insight:</strong> With {total_dc} draws and 56 goals, the team converts roughly 1 goal per {total_dc/56:.1f} draws won. 
    Improving draw circle ground ball recovery (getting the loose ball after winning the draw) is a high-leverage practice area — 
    every additional clean draw possession is worth approximately 0.4 expected goals based on D1 averages.
    </div>""", unsafe_allow_html=True)