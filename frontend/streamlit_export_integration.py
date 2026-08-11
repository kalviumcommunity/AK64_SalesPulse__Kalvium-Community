"""
Streamlit Export Integration Module
------------------------------------
Assignment 2.50 - Task 3: Streamlit Interactive Dashboard Export Download Hub

Allows stakeholders to trigger multi-format export generation directly from the
Streamlit UI and download CSV data or interactive HTML reports with one click.
"""

import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

try:
    import streamlit as st
except ImportError:
    st = None

# Import core export engine
from export_functions import export_analysis, generate_sample_analysis_payload, verify_exports


def render_streamlit_export_app():
    """Task 3: Streamlit Dashboard with integrated Sidebar Export & One-Click Download Buttons."""
    if st is None:
        print("Streamlit not installed — running CLI export demo.")
        return

    st.set_page_config(
        page_title="SalesPulse Executive Export Hub",
        page_icon="📥",
        layout="wide"
    )

    st.title("SalesPulse Executive Dashboard & Export Hub")
    st.caption("Assignment 2.50 — Multi-Format Portable Insight Delivery (CSV, PDF, HTML)")

    # Generate sample dataset & charts
    df, summary_text, charts_dict = generate_sample_analysis_payload()

    # Layout Level 1: Key Summary
    st.markdown(summary_text)
    st.divider()

    # Layout Level 2: Interactive Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts_dict['Response Time Distribution'], use_container_width=True)
    with col2:
        st.plotly_chart(charts_dict['Revenue vs Delay Scatter'], use_container_width=True)

    st.divider()

    # Task 3: Sidebar Export Controls
    st.sidebar.header("📥 Report Export Hub")
    st.sidebar.markdown("Generate and download multi-format reports on demand.")

    output_folder = st.sidebar.text_input("Output Directory", value="output")

    if st.sidebar.button("⚙️ Trigger Full Multi-Format Export"):
        with st.spinner("Generating CSV, PDF, and HTML interactive reports..."):
            report_dir = export_analysis(df, summary_text, charts_dict, output_dir=output_folder)
            st.sidebar.success(f"✓ Export generated in:\n`{report_dir}`")
            st.session_state['last_report_dir'] = report_dir

    st.sidebar.divider()
    st.sidebar.subheader("One-Click Downloads")

    # CSV Direct Download
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📊 Download Cleaned Dataset (CSV)",
        data=csv_bytes,
        file_name=f"salespulse_cleaned_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # HTML Interactive Report Download
    if 'last_report_dir' in st.session_state and os.path.exists(st.session_state['last_report_dir']):
        html_file = os.path.join(st.session_state['last_report_dir'], 'interactive_report.html')
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                html_bytes = f.read()
            st.sidebar.download_button(
                label="🌐 Download Interactive Report (HTML)",
                data=html_bytes,
                file_name=f"salespulse_interactive_report_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
        
        pdf_file = os.path.join(st.session_state['last_report_dir'], 'summary_report.pdf')
        if os.path.exists(pdf_file):
            with open(pdf_file, 'rb') as f:
                pdf_bytes = f.read()
            st.sidebar.download_button(
                label="📄 Download Summary Report (PDF)",
                data=pdf_bytes,
                file_name=f"salespulse_summary_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

    st.subheader("Data Preview")
    st.dataframe(df.head(10), use_container_width=True)


if __name__ == '__main__':
    render_streamlit_export_app()
