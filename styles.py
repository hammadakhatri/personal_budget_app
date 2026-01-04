
def get_custom_css():
    return """
    <style>
        /* Import a nice font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #333333; /* Default text dark grey */
        }

        /* Sidebar Styling - Dark and Modern */
        [data-testid="stSidebar"] {
            background-color: #1E293B; /* Dark Blue-Grey */
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #FFFFFF !important; /* White text in sidebar */
        }
        [data-testid="stSidebar"] .stRadio label {
             color: #E2E8F0 !important;
        }

        /* Cards for Metrics */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            color: #1e293b;
        }
        
        /* Metric Labels */
        div[data-testid="stMetricLabel"] {
            color: #64748b !important; /* Muted slate */
        }
        div[data-testid="stMetricValue"] {
            color: #0f172a !important; /* Dark slate */
        }

        /* Buttons */
        div[data-testid="stButton"] > button {
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.2s;
            border: none;
            background-color: #3b82f6; /* Blue 500 */
            color: white !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
            background-color: #2563eb; /* Blue 600 */
        }
        
        /* Secondary/Form Buttons */
        div[data-testid="stForm"] div[data-testid="stButton"] > button {
            background-color: #10b981; /* Emerald 500 */
        }

        /* Custom Wallet Card */
        .wallet-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            transition: transform 0.2s;
        }
        .wallet-card:hover {
            transform: translateY(-2px);
        }
        .wallet-card.pkr {
            background: linear-gradient(135deg, #059669 0%, #34d399 100%); /* Emerald Gradient */
        }
        .wallet-card.usd {
            background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%); /* Blue Gradient */
        }
        .wallet-currency {
            font-size: 0.85rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .wallet-balance {
            font-size: 2rem;
            font-weight: 800;
            margin-top: 8px;
            letter-spacing: -0.5px;
        }
        .wallet-name {
            font-size: 1.1rem;
            font-weight: 500;
            opacity: 0.95;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #1e293b;
            font-weight: 700;
        }
    </style>
    """

