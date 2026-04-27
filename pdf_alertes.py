from io import BytesIO
from pathlib import Path
import tempfile

import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet

from config import SEUIL_ALERTE_MM, SEUIL_VIGILANCE_MM


def _prepare_alert_df(df: pd.DataFrame, include_vigilance: bool = True) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    df = df.copy()
    if include_vigilance:
        return df[df["Pluie_mm"] >= SEUIL_VIGILANCE_MM].copy()
    return df[df["Pluie_mm"] >= SEUIL_ALERTE_MM].copy()


def _build_bar_chart(df: pd.DataFrame) -> str | None:
    if df.empty:
        return None
    agg = df.groupby("Ville", as_index=False)["Pluie_mm"].sum().sort_values("Pluie_mm", ascending=False)
    if agg.empty:
        return None
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.figure(figsize=(9, 4))
    plt.bar(agg["Ville"], agg["Pluie_mm"], color="#d32f2f")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Pluie (mm)")
    plt.title("Cumuls par ville")
    plt.tight_layout()
    plt.savefig(tmp.name, dpi=150)
    plt.close()
    return tmp.name


def _build_line_chart(df: pd.DataFrame) -> str | None:
    if df.empty or "Date_Heure" not in df.columns:
        return None
    dfx = df.dropna(subset=["Date_Heure"]).copy()
    if dfx.empty:
        return None
    daily = dfx.groupby(dfx["Date_Heure"].dt.date, as_index=False)["Pluie_mm"].sum()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.figure(figsize=(9, 4))
    plt.plot(daily["Date_Heure"], daily["Pluie_mm"], marker="o", color="#1976d2")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Pluie (mm)")
    plt.title("Evolution journalière")
    plt.tight_layout()
    plt.savefig(tmp.name, dpi=150)
    plt.close()
    return tmp.name


def generer_rapport_alertes_pdf(
    df: pd.DataFrame,
    titre: str = "Rapport des alertes pluviométriques",
    include_vigilance: bool = True,
    logo_path: str | Path | None = None
) -> bytes:
    styles = getSampleStyleSheet()
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm
    )

    story = []
    story.append(Paragraph(f"<b>{titre}</b>", styles["Title"]))
    story.append(Spacer(1, 0.3 * cm))

    df_alert = _prepare_alert_df(df, include_vigilance=include_vigilance)

    if logo_path and Path(logo_path).exists():
        story.append(Image(str(logo_path), width=3.5 * cm, height=3.5 * cm))
        story.append(Spacer(1, 0.2 * cm))

    nb_releves = len(df_alert)
    nb_villes = df_alert["Ville"].nunique() if not df_alert.empty else 0
    cumul = float(df_alert["Pluie_mm"].sum()) if not df_alert.empty else 0.0

    intro = (
        f"Nombre de relevés critiques : <b>{nb_releves}</b><br/>"
        f"Nombre de villes concernées : <b>{nb_villes}</b><br/>"
        f"Cumul total observé : <b>{cumul:.1f} mm</b>"
    )
    story.append(Paragraph(intro, styles["BodyText"]))
    story.append(Spacer(1, 0.3 * cm))

    if df_alert.empty:
        story.append(Paragraph("Aucune alerte sur la période sélectionnée.", styles["BodyText"]))
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    table_df = df_alert[["Ville", "Date", "Heure", "Pluie_mm", "Phenomene", "Agent"]].copy()
    table_df["Pluie_mm"] = table_df["Pluie_mm"].map(lambda x: f"{float(x):.1f}")

    data = [table_df.columns.tolist()] + table_df.astype(str).values.tolist()
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d47a1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    story.append(Paragraph("<b>Tableau des alertes</b>", styles["Heading2"]))
    story.append(table)
    story.append(Spacer(1, 0.4 * cm))

    bar_chart = _build_bar_chart(df_alert)
    if bar_chart:
        story.append(Paragraph("<b>Graphique 1 : Cumuls par ville</b>", styles["Heading2"]))
        story.append(Image(bar_chart, width=17 * cm, height=7 * cm))
        story.append(Spacer(1, 0.3 * cm))

    line_chart = _build_line_chart(df_alert)
    if line_chart:
        story.append(Paragraph("<b>Graphique 2 : Evolution journalière</b>", styles["Heading2"]))
        story.append(Image(line_chart, width=17 * cm, height=7 * cm))
        story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        "Seuils utilisés : vigilance ≥ 20 mm ; alerte ≥ 50 mm.",
        styles["Italic"]
    ))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
