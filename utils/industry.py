def get_industry(movie_obj):
    lang = movie_obj.get('original_language', '')
    countries = [c['iso_3166_1'] for c in movie_obj.get('production_countries', [])]
    industry_map = {
        ('hi', 'IN'): "Bollywood",        # Hindi - India
        ('en', 'US'): "Hollywood",        # English - USA
        ('ko', 'KR'): "Korean",           # Korean - South Korea
        ('ta', 'IN'): "Kollywood",        # Tamil - India
        ('te', 'IN'): "Tollywood",        # Telugu - India
        ('ml', 'IN'): "Mollywood",        # Malayalam - India
        ('bn', 'IN'): "Tollywood",        # Bengali - India (often overlaps with Tollywood)
        ('fr', 'FR'): "French Cinema",   # French - France
        ('de', 'DE'): "German Cinema",   # German - Germany
        ('ja', 'JP'): "Japanese Cinema", # Japanese - Japan
        ('zh', 'CN'): "Chinese Cinema",  # Chinese - China
        ('es', 'ES'): "Spanish Cinema",  # Spanish - Spain
        ('it', 'IT'): "Italian Cinema",  # Italian - Italy
        ('ru', 'RU'): "Russian Cinema",  # Russian - Russia
        ('pt', 'BR'): "Brazilian Cinema",# Portuguese - Brazil
        ('ar', 'EG'): "Egyptian Cinema", # Arabic - Egypt
        ('pl', 'PL'): "Polish Cinema",   # Polish - Poland
        ('tr', 'TR'): "Turkish Cinema",  # Turkish - Turkey
        ('en', 'GB'): "British Cinema",  # English - UK
    }
    for c in countries:
        key = (lang, c)
        if key in industry_map:
            return industry_map[key]
    # Fallback to industry based only on language if country not matched
    lang_only_map = {
        'hi': "Bollywood",
        'en': "Hollywood",
        'ko': "Korean",
        'ta': "Kollywood",
        'te': "Tollywood",
        'ml': "Mollywood",
        'bn': "Tollywood",
        'fr': "French Cinema",
        'de': "German Cinema",
        'ja': "Japanese Cinema",
        'zh': "Chinese Cinema",
        'es': "Spanish Cinema",
        'it': "Italian Cinema",
        'ru': "Russian Cinema",
        'pt': "Brazilian Cinema",
        'ar': "Egyptian Cinema",
        'pl': "Polish Cinema",
        'tr': "Turkish Cinema",
    }
    if lang in lang_only_map:
        return lang_only_map[lang]
    return "Other"
