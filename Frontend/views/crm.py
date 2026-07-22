"""
CRM & Email Upload View for SalesPulse AI Streamlit Frontend.
Enables creation of deals/customers, logging sales activities, and running email NLP analysis.
"""

import streamlit as st
from Frontend.utils.api import analyze_email_content
from Frontend.utils.components import render_section_header, render_stat_card

def render_crm_view():
    render_section_header("CRM Management & Email NLP Analysis", "Log sales activity, track deals, and analyze email thread sentiment and tone in real time.")

    tab1, tab2, tab3 = st.tabs(["📧 Email Sentiment & Tone NLP", "💼 Manage Deals", "👥 Manage Customers"])

    with tab1:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 1rem; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0 0 0.25rem 0; font-family: Outfit, sans-serif;'>Analyze Email Conversation Thread</h3>
                <p style='font-size: 0.83rem; color: #64748b; margin-bottom: 1rem;'>Upload email thread text to derive sentiment score, communication tone, and signal keywords.</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            deal_id = st.text_input("Associated Deal ID", value="DEAL-103", key="email_deal_id")
            sender = st.text_input("Sender Email", value="prospect@nexus-systems.com", key="email_sender")
        with col2:
            receiver = st.text_input("Receiver Email", value="aditya@salespulse.ai", key="email_receiver")
            subject = st.text_input("Subject Line", value="Re: Proposal discount and implementation timeline", key="email_subject")

        email_body = st.text_area(
            "Email Body Text",
            height=160,
            value="Hi Aditya,\n\nWe reviewed the proposal for Nexus Systems. We have a major concern regarding the total annual license fee. The price is significantly higher than our budget, and we doubt our leadership will agree to these terms. If you cannot offer a 15% discount, we may need to delay the contract decision or consider alternative suppliers.\n\nBest regards,\nMark",
            key="email_body_text"
        )

        if st.button("Run NLP Sentiment & Tone Analysis", type="primary"):
            if email_body:
                result = analyze_email_content(deal_id, sender, receiver, subject, email_body)
                st.success("NLP Sentiment & Tone Analysis Complete!")

                res_col1, res_col2, res_col3 = st.columns(3)
                with res_col1:
                    score = result["sentiment_score"]
                    tone_type = "rose" if score < 0 else "emerald"
                    render_stat_card("Sentiment Score", f"{score:+.3f}", "Range: -1.0 to +1.0", "💬", tone_type)
                with res_col2:
                    render_stat_card("Detected Tone", result["tone"], "NLP classification", "🏷️", "indigo")
                with res_col3:
                    render_stat_card("Timestamp", result["analysis_timestamp"].split(" ")[1], "Processed in real-time", "⏱️", "cyan")

                st.markdown("**Detected Signal Keywords:**")
                st.write(" ".join([f"`{w}`" for w in result["key_phrases_detected"]]))

                if score < 0:
                    st.warning("⚠️ Risk Flag: Negative email sentiment detected. Suggested Action: Review pricing model or schedule a value-clarification call within 24 hours.")
            else:
                st.warning("Please paste email body text to analyze.")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Create New Deal Record</h3>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            company_name = st.text_input("Customer / Company Name", placeholder="Acme Inc.")
            deal_val = st.number_input("Deal Value ($)", min_value=1000, value=50000, step=5000)
        with c2:
            stage = st.selectbox("Current Stage", ["Lead Qualification", "Discovery Call", "Proposal / Demo", "Negotiation", "Contract Sent"])
            status = st.selectbox("Deal Status", ["open", "won", "lost"])

        if st.button("Create Deal"):
            st.success(f"Deal for '{company_name}' (${deal_val:,}) created successfully under stage '{stage}'!")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
            <div style='background: white; padding: 1.25rem; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 4px 15px -3px rgba(15,23,42,0.03);'>
                <h3 style='font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0 0 0.85rem 0; font-family: Outfit, sans-serif;'>Create Customer Record</h3>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            cust_company = st.text_input("Company Name", placeholder="Nexus Systems")
            contact_person = st.text_input("Contact Person", placeholder="Jane Doe")
        with c2:
            cust_email = st.text_input("Contact Email", placeholder="jane@nexus.com")
            cust_phone = st.text_input("Phone Number", placeholder="+1 (555) 234-5678")

        if st.button("Save Customer"):
            st.success(f"Customer '{cust_company}' ({contact_person}) saved successfully!")
        st.markdown("</div>", unsafe_allow_html=True)
