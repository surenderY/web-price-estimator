MAPPINGS = 'mappings.xlsx'
PRICING_INPUT_DIR = 'sources'
MASTER_PRICING_FILE = "Master 1- WWT Pricing and SKUs  v1.1.xlsx"
ESTIMATOR_TEMPLATE = 'estimator.xlsm'
ESTIMATOR_WORK_SHEET = 'CSOW Pricing & WWT Cost (2)'

keyword_map = {
    "integration": {
        "service": "Assembly and Integration",
        "sum_all": "yes"
    },
    "title": {
        "service": "Logistics",
        "sum_all": "no",
        "type": "Trade Compliance",
        "descriptions": ["Title Registration, Asset Holding"]
    },
    "install": {
        "service": "On-Site Installation",
        "sum_all": "yes"
    },
    "pmo": {
        "service": "Logistics",
        "sum_all": "no",
        "type": "Trade Compliance",
        "descriptions": [
            "PMO - That also includes generation of  Compliance reports: SCRM, COO, Platform Security Certificates"
        ]
    },
    "break/fix": {
        "service": "Support",
        "sum_all": "no",
        "type": "Break Fix Support Security Clearances (when required)",
        "descriptions": []
    },
    "call center": {
        "service": "Support",
        "sum_all": "no",
        "type": "First line of support",
        "descriptions": []
    },
    "delivery": {
        "service": "Logistics",
        "sum_all": "no",
        "type": "Shipping (inlcude only one type based on customer)"
    },
    "partner cost-call center": {
        "external_lookup": True
    },
    "partner cost-break fix": {
        "external_lookup": True
    },
    "partner cost-install": {
        "external_lookup": True
    },
    "wwt internal - integration cost": {
        "external_lookup": True
    },
    "rfp": { "special": "service_price_monthly" },
}

partner_cost_breakfix_file_map = {
    "4hr os": "Master 3 -Park Place cost for BreakFix 4 Hour SLA.xlsx",
    "nbd os": "Master 3 -Park Place cost for BreakFix NBD SLA.xlsx"
}

partner_cost_install_file_map = {
    "public sector": "Master 4 - Park Place - Deployment - Per Install - Public Sector.xlsx",
    "commercial": "Master 4 - Park Place - Deployment - Per Install -  Commercial.xlsx"
}