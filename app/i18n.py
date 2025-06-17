LANGUAGES = {
    "en": "English",
    "ja": "日本語",
    "es": "Español",
    "zh": "中文"
}

TRANSLATIONS = {
    "title": {
        "en": "🔐 HavenAI - AI-Powered Log Analyzer",
        "ja": "🔐 HavenAI - AI搭載のログ分析ツール",
        "es": "🔐 HavenAI - Analizador de Logs con IA",
        "zh": "🔐 HavenAI - AI日志分析器"
    },
    "upload_prompt": {
        "en": "📤 Upload your log file (CSV format)",
        "ja": "📤 ログファイルをアップロードしてください (CSV形式)",
        "es": "📤 Sube tu archivo de logs (formato CSV)",
        "zh": "📤 上传日志文件（CSV格式）"
    },
    "ai_summary_btn": {
        "en": "Generate AI Summary",
        "ja": "AI要約を生成",
        "es": "Generar resumen con IA",
        "zh": "生成AI摘要"
    },
    "threat_score_btn": {
        "en": "Run Threat Scoring",
        "ja": "脅威スコアリングを実行",
        "es": "Ejecutar puntuación de amenazas",
        "zh": "运行威胁评分"
    },
    "download_csv": {
        "en": "Download Cleaned CSV",
        "ja": "クリーンなCSVをダウンロード",
        "es": "Descargar CSV limpio",
        "zh": "下载清理后的CSV"
    },
    "generate_report": {
        "en": "Generate & Download Report",
        "ja": "レポートを生成・ダウンロード",
        "es": "Generar y descargar informe",
        "zh": "生成并下载报告"
    }
}

def t(key, lang):
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS[key]["en"])
