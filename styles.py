
def get_custom_css():
    return """
    <style>
        /* Import a nice font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global Font */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #020617; /* Very Dark Slate */
            border-right: 1px solid #1e293b;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #F8FAFC !important;
        }
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #1e293b; /* Dark card background */
            border: 1px solid #334155;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s;
        }
        div[data-testid="stMetric"]:hover {
             transform: translateY(-2px);
             border-color: #475569;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #94a3b8 !important; /* Muted text */
            font-size: 0.9rem !important;
            font-weight: 500;
        }
        div[data-testid="stMetricValue"] {
            color: #f8fafc !important; /* White text */
            font-weight: 700;
        }

        /* Input Fields & Select Boxes */
        /* Target the input container to ensure background is dark and text is light */
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            background-color: #1e293b !important;
            border-color: #334155 !important;
            border-radius: 8px !important;
            color: white !important;
        }
        
        /* The actual input text element */
        input[type="text"], input[type="number"], input[type="date"] {
            color: white !important;
        }
        
        /* Dropdown text color */
        div[data-baseweb="select"] span {
            color: white !important;
        }
        
        /* Helper text/Label */
        label[data-testid="stWidgetLabel"] p {
            font-size: 0.9rem;
            color: #cbd5e1 !important; /* Light text for labels */
        }

        /* Buttons */
        div[data-testid="stButton"] > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.25rem;
            border: none;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }
        
        /* Primary Button */
        div[data-testid="stButton"] > button:first-child {
             background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
             color: white !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        }

        /* Secondary Button */
        button[kind="secondary"] {
            background-color: transparent !important;
            border: 1px solid #ef4444 !important;
            color: #ef4444 !important;
        }
        button[kind="secondary"]:hover {
             background-color: rgba(239, 68, 68, 0.1) !important;
        }

        /* Wallet Cards */
        .wallet-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); /* Dark gradient base */
            border: 1px solid #334155;
            color: white !important;
            padding: 24px;
            border-radius: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .wallet-card.pkr {
            border-top: 4px solid #10b981; /* Green Top for PKR */
        }
        .wallet-card.usd {
             border-top: 4px solid #3b82f6; /* Blue Top for USD */
        }

        .wallet-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            border-color: #475569;
        }

        .wallet-currency {
            font-size: 0.75rem;
            background: rgba(255,255,255,0.1);
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .wallet-balance {
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -1px;
            color: #f8fafc;
        }
        .wallet-name {
            font-size: 1.1rem;
            font-weight: 500;
            color: #cbd5e1;
            margin-top: 4px;
        }
        
        /* Header Colors */
        h1, h2, h3 {
            color: #f8fafc !important;
        }
        
        /* Expander */
        div[data-testid="stExpander"] {
            background-color: #1e293b;
            border-color: #334155;
            color: white;
        }
        
        /* Toast style */
        div[data-testid="stToast"] {
            background-color: #1e293b;
            color: white;
            border: 1px solid #334155;
        }
    </style>
    """ 
    + """
    <style>
        /* Transaction Row Styling */
        .transaction-row {
            display: flex;
            align_items: center;
            justify_content: space-between;
            padding: 12px 16px;
            background-color: #1e293b; /* Dark Slate */
            border: 1px solid #334155;
            border-radius: 12px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }
        
        .transaction-row:hover {
            transform: translateX(4px);
            border-color: #475569;
            background-color: #263345;
        }
        
        .t-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify_content: center;
            font-size: 1.2rem;
            margin-right: 16px;
            flex-shrink: 0;
        }
        
        .t-icon.income { background-color: rgba(16, 185, 129, 0.2); color: #10b981; }
        .t-icon.expense { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; }
        .t-icon.transfer { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6; }
        
        .t-details {
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            margin-right: 16px;
        }
        
        .t-description {
            font-weight: 600;
            color: #f8fafc;
            font-size: 1rem;
            margin-bottom: 2px;
        }
        
        .t-category {
            font-size: 0.8rem;
            color: #94a3b8;
        }
        
        .t-date {
            font-size: 0.8rem;
            color: #64748b;
            margin-right: 16px;
            white-space: nowrap;
        }
        
        .t-amount {
            font-weight: 700;
            font-size: 1rem;
            white-space: nowrap;
        }
        .t-amount.income { color: #10b981; }
        .t-amount.expense { color: #ef4444; }
        .t-amount.transfer { color: #3b82f6; }
    </style>
    """
