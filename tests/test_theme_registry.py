from themes.styles import get_all_themes


def test_music_theme_is_registered():
    themes = get_all_themes()
    assert "Music" in themes


def test_music_theme_has_tags_for_sidebar_filters():
    themes = get_all_themes()
    music_theme = themes["Music"]
    tags = music_theme.get("tags", [])
    assert "music" in [tag.lower() for tag in tags]


def test_aurora_gradient_theme_is_registered_with_tags():
    themes = get_all_themes()
    assert "Aurora Gradient" in themes

    aurora_theme = themes["Aurora Gradient"]
    tags = aurora_theme.get("tags", [])
    assert "aurora" in [tag.lower() for tag in tags]


def test_midnight_theme_has_required_schema():
    themes = get_all_themes()
    assert "Midnight" in themes

    midnight_theme = themes["Midnight"]
    assert "font_family" in midnight_theme
    assert isinstance(midnight_theme["font_family"], str)
    assert midnight_theme["font_family"].strip() != ""


def test_forest_theme_is_registered_with_tags():
    themes = get_all_themes()
    assert "Forest" in themes

    forest_theme = themes["Forest"]
    tags = forest_theme.get("tags", [])
    assert "forest" in [tag.lower() for tag in tags]


def test_new_aesthetic_calm_minimal_themes_have_required_schema():
    themes = get_all_themes()
    new_theme_names = [
        "Aesthetic Glass",
        "Aesthetic Neon",
        "Aesthetic Sunset",
        "Calm Lavender",
        "Calm Ocean",
        "Calm Sand",
        "Minimal Dark",
        "Minimal Light",
        "Minimal Mono",
    ]

    for theme_name in new_theme_names:
        assert theme_name in themes
        theme = themes[theme_name]
        assert "font_family" in theme
        assert isinstance(theme["font_family"], str)
        assert theme["font_family"].strip() != ""


def test_spider_man_theme_is_registered():
    themes = get_all_themes()
    assert "Spider-Man" in themes
