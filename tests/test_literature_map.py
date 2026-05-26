from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LITERATURE_MAP = ROOT / "docs" / "00a_literature_map.md"


def test_literature_map_exists_and_blocks_equation_registry():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "gate_status: source_skeleton_created" in text
    assert "equation_registry_allowed: false" in text
    assert "dynare_allowed: false" in text
    assert "Gate 2b is not passed." in text


def test_literature_map_has_verified_bcb_primary_sources():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "BCB_WP239" in text
    assert "https://www.bcb.gov.br/pec/wps/ingl/wps239.pdf" in text
    assert "BCB_WP578" in text
    assert "https://www.bcb.gov.br/content/publicacoes/WorkingPaperSeries/WP578.pdf" in text
    assert "verified_official_bcb" in text


def test_literature_map_keeps_precise_locators_pending():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "TBD-after-primary-source-reading-WBS-033A" in text
    assert "Current status: source skeleton created; precise locators pending." in text

