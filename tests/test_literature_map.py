from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LITERATURE_MAP = ROOT / "docs" / "00a_literature_map.md"


def test_literature_map_exists_and_blocks_dynare_until_gate2b():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "gate_status: source_locator_pass_complete" in text
    assert "equation_registry_allowed: true" in text
    assert "dynare_allowed: false" in text
    assert "Gate 2a is passed for equation-registry anchoring" in text


def test_literature_map_has_verified_bcb_primary_sources():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "BCB_WP239" in text
    assert "https://www.bcb.gov.br/pec/wps/ingl/wps239.pdf" in text
    assert "BCB_WP578" in text
    assert "https://www.bcb.gov.br/content/publicacoes/WorkingPaperSeries/WP578.pdf" in text
    assert "verified_official_bcb" in text


def test_literature_map_has_verified_wp239_equation_locators():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "wp239_equation_table_locators_verified: true" in text
    assert "pending_equation_locator" not in text
    assert "Main equations (61)-(62)" in text
    assert "Log-linear shock equations (C.48)-(C.61)" in text


def test_literature_map_has_verified_wp578_section_locators():
    text = LITERATURE_MAP.read_text(encoding="utf-8")

    assert "WP578 The model, PDF page 8" in text
    assert "WP578 Priors, posteriors and SMC estimation, PDF page 42" in text
    assert "Computational details, PDF page 91" in text
