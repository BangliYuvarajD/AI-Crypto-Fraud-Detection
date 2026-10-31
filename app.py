import streamlit as st
import requests
import pandas as pd
import joblib
import os
import time
import sys

# Allow Python to find live_ai.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from live_ai import LiveAIAnalyzer


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI Crypto Fraud Detection",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 AI-Based Cryptocurrency Fraud Detection")
st.write("Real-Time Bitcoin Transaction Monitoring & AI Risk Analysis")

st.divider()


# ============================================================
# LOAD RANDOM FOREST MODEL
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "crypto_fraud_model.pkl"
)

model = None

if os.path.exists(MODEL_PATH):

    try:
        model = joblib.load(MODEL_PATH)

        st.success(
            "🤖 Random Forest Model Loaded Successfully"
        )

    except Exception as e:

        st.error(
            f"❌ Model loading error: {e}"
        )

else:

    st.warning(
        "⚠️ Random Forest model not found."
    )


# ============================================================
# LIVE AI
# ============================================================

live_ai = LiveAIAnalyzer()


# ============================================================
# LIVE TRANSACTION RISK
# ============================================================

def calculate_risk(tx):

    risk = 0
    reasons = []

    fee = tx.get("fee", 0)

    size = tx.get(
        "vsize",
        tx.get("size", 0)
    )

    inputs = len(
        tx.get("vin", [])
    )

    outputs = len(
        tx.get("vout", [])
    )

    fee_rate = (
        fee / size
        if size > 0
        else 0
    )

    if fee_rate > 100:

        risk += 30
        reasons.append("Very high fee rate")

    elif fee_rate > 50:

        risk += 15
        reasons.append("High fee rate")

    if size > 100000:

        risk += 30
        reasons.append("Very large transaction")

    elif size > 50000:

        risk += 15
        reasons.append("Large transaction")

    if inputs > 50:

        risk += 20
        reasons.append("Very high number of inputs")

    elif inputs > 20:

        risk += 10
        reasons.append("High number of inputs")

    if outputs > 50:

        risk += 20
        reasons.append("Very high number of outputs")

    elif outputs > 20:

        risk += 10
        reasons.append("High number of outputs")

    risk = min(risk, 100)

    if risk >= 50:

        level = "🔴 HIGH RISK"

    elif risk >= 20:

        level = "🟠 MEDIUM RISK"

    else:

        level = "🟢 LOW RISK"

    if not reasons:

        reasons.append(
            "No unusual structural indicators detected"
        )

    return risk, level, ", ".join(reasons)


# ============================================================
# GET LIVE TRANSACTIONS
# ============================================================

def get_transactions():

    url = (
        "https://mempool.space/api/"
        "mempool/recent"
    )

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return response.json()[:10]


# ============================================================
# TXID ANALYZER
# ============================================================

st.subheader("🔎 Analyze Bitcoin Transaction")

txid_input = st.text_input(
    "Enter Bitcoin Transaction ID (TXID)",
    placeholder="Enter 64-character Bitcoin TXID"
)

if st.button("🔍 Analyze Transaction"):

    if not txid_input:

        st.warning(
            "Please enter a Bitcoin transaction ID."
        )

    else:

        try:

            url = (
                "https://mempool.space/api/tx/"
                + txid_input.strip()
            )

            response = requests.get(
                url,
                timeout=10
            )

            if response.status_code == 200:

                tx = response.json()

                st.success(
                    "✅ Bitcoin transaction found!"
                )

                # --------------------------------------------
                # TRANSACTION INFORMATION
                # --------------------------------------------

                st.subheader(
                    "📄 Transaction Information"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Fee",
                        f"{tx.get('fee', 0)} sats"
                    )

                with col2:

                    st.metric(
                        "Size",
                        f"{tx.get('vsize', tx.get('size', 0))} vbytes"
                    )

                with col3:

                    st.metric(
                        "Inputs",
                        len(tx.get("vin", []))
                    )

                with col4:

                    st.metric(
                        "Outputs",
                        len(tx.get("vout", []))
                    )

                # --------------------------------------------
                # RULE BASED RISK
                # --------------------------------------------

                risk, level, reason = calculate_risk(tx)

                st.divider()

                st.subheader(
                    "🛡️ Live Risk Analysis"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Risk Score",
                        f"{risk}%"
                    )

                with col2:

                    st.metric(
                        "Risk Level",
                        level
                    )

                st.info(
                    f"**Analysis:** {reason}"
                )

                # --------------------------------------------
                # AI ANOMALY ANALYSIS
                # --------------------------------------------

                st.divider()

                st.subheader(
                    "🤖 Live AI Anomaly Analysis"
                )

                # Use current transaction plus recent
                # transactions to establish a baseline.

                try:

                    recent_transactions = get_transactions()

                    training_data = recent_transactions + [tx]

                    if live_ai.train(training_data):

                        ai_risk, ai_level, ai_reason = (
                            live_ai.predict(tx)
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "AI Risk Score",
                                f"{ai_risk}%"
                            )

                        with col2:

                            st.metric(
                                "AI Result",
                                ai_level
                            )

                        st.info(
                            f"**AI Analysis:** {ai_reason}"
                        )

                    else:

                        st.warning(
                            "Not enough transactions for AI analysis."
                        )

                except Exception as e:

                    st.warning(
                        f"AI analysis unavailable: {e}"
                    )

                # --------------------------------------------
                # CONFIRMATION
                # --------------------------------------------

                status = tx.get(
                    "status",
                    {}
                )

                if status.get(
                    "confirmed",
                    False
                ):

                    st.success(
                        "✅ Confirmed transaction"
                    )

                else:

                    st.warning(
                        "⏳ Transaction is currently unconfirmed"
                    )

            else:

                st.error(
                    "❌ Transaction not found. "
                    "Check the TXID."
                )

        except requests.exceptions.RequestException as e:

            st.error(
                f"❌ Network error: {e}"
            )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )


st.divider()


# ============================================================
# LIVE MONITORING
# ============================================================

st.subheader(
    "🔴 Live Bitcoin Monitoring"
)

auto_refresh = st.checkbox(
    "🔄 Automatic monitoring",
    value=False
)

refresh_seconds = 30

if auto_refresh:

    st.info(
        "🔄 Checking the Bitcoin mempool "
        "every 30 seconds."
    )


try:

    transactions = get_transactions()

    results = []

    # Train live AI with recent transactions

    live_ai.train(transactions)

    for tx in transactions:

        risk, level, reason = calculate_risk(tx)

        try:

            ai_risk, ai_level, ai_reason = (
                live_ai.predict(tx)
            )

        except Exception:

            ai_risk = 0
            ai_level = "N/A"
            ai_reason = "AI unavailable"

        results.append({

            "TXID": tx.get(
                "txid",
                "N/A"
            ),

            "Fee (sats)": tx.get(
                "fee",
                0
            ),

            "Size (vbytes)": tx.get(
                "vsize",
                tx.get("size", 0)
            ),

            "Inputs": len(
                tx.get("vin", [])
            ),

            "Outputs": len(
                tx.get("vout", [])
            ),

            "Rule Risk": f"{risk}%",

            "Rule Result": level,

            "AI Risk": f"{ai_risk}%",

            "AI Result": ai_level,

            "Reason": reason
        })


    df = pd.DataFrame(
        results
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.success(
        f"✅ {len(df)} live Bitcoin transactions analyzed!"
    )

    low_count = sum(
        "LOW RISK" in x
        for x in df["Rule Result"]
    )

    medium_count = sum(
        "MEDIUM RISK" in x
        for x in df["Rule Result"]
    )

    high_count = sum(
        "HIGH RISK" in x
        for x in df["Rule Result"]
    )

    st.subheader(
        "📊 Risk Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total",
            len(df)
        )

    with col2:

        st.metric(
            "🟢 Low Risk",
            low_count
        )

    with col3:

        st.metric(
            "🟠 Medium Risk",
            medium_count
        )

    with col4:

        st.metric(
            "🔴 High Risk",
            high_count
        )


    st.divider()


    # ========================================================
    # TABLE
    # ========================================================

    st.subheader(
        "📋 Latest 10 Bitcoin Transactions"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DETAILS
    # ========================================================

    st.divider()

    st.subheader(
        "🔎 Transaction Details"
    )

    for _, row in df.iterrows():

        with st.expander(
            f"{row['AI Result']} — "
            f"{row['TXID'][:16]}..."
        ):

            st.write(
                "**Transaction ID:**",
                row["TXID"]
            )

            st.write(
                "**Rule Risk:**",
                row["Rule Risk"]
            )

            st.write(
                "**AI Risk:**",
                row["AI Risk"]
            )

            st.write(
                "**AI Result:**",
                row["AI Result"]
            )

            st.write(
                "**Reason:**",
                row["Reason"]
            )


    st.caption(
        "Last checked: "
        + time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


except requests.exceptions.RequestException as e:

    st.error(
        f"❌ Connection error: {e}"
    )

except Exception as e:

    st.error(
        f"❌ Application error: {e}"
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

st.divider()

st.subheader(
    "🤖 AI Model Information"
)

if model is not None:

    st.success(
        "Random Forest model is available."
    )

    st.write(
        "The Random Forest model was trained "
        "using the Elliptic Bitcoin transaction dataset."
    )

    st.info(
        "Test accuracy: approximately 98.96%"
    )

else:

    st.warning(
        "Random Forest model is unavailable."
    )


st.divider()

st.caption(
    "⚠️ Live AI analysis is anomaly detection based "
    "on recent transaction patterns. It is not proof "
    "of fraudulent activity."
)


# ============================================================
# AUTO REFRESH
# ============================================================

if auto_refresh:

    time.sleep(
        refresh_seconds
    )

    st.rerun()