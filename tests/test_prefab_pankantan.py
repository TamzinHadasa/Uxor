from uxor.prefabs import LineBreak, ReportInvalid, PankantanUxor


def test_default():
    u = PankantanUxor()
    assert u("toki li pona") == "󱥬󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁2󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁03󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁04󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "[SITELEN IKE: this] [SITELEN IKE: isn't] 󱥬󱥔"
    assert u("󱥬󱤧󱥔") == "󱥬󱤧​󱥔"


def test_unspaced():
    u = PankantanUxor(allow_unspaced=True)
    assert u("toki li pona") == "󱥬󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁2󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁03󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁04󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "[SITELEN IKE: this] [SITELEN IKE: isn't] 󱥬󱥔"
    assert u("󱥬󱤧󱥔") == "󱥬󱤧​󱥔"
    assert u("tokipona") == "󱥬󱥔"
    assert u("kalama") == "󱤕"
    assert u("thisisnttokipona") == "[SITELEN IKE: thisisnttokipona]"


def test_ignore_variants():
    u = PankantanUxor(ignore_variants=True)
    assert u("toki li pona") == "󱥬󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "[SITELEN IKE: this] [SITELEN IKE: isn't] 󱥬󱥔"
    assert u("󱥬󱤧󱥔") == "󱥬󱤧​󱥔"


def test_report_invalid0():
    u = PankantanUxor(report_invalid=ReportInvalid.NEVER)
    assert u("toki li pona") == "󱥬󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁2󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁03󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁04󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "this isn't 󱥬󱥔"
    assert u("󱥬󱤧󱥔") == "󱥬󱤧​󱥔"


def test_report_invalid2():
    u = PankantanUxor(report_invalid=ReportInvalid.ALWAYS)
    assert u("toki li pona") == "󱥬󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁2󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁03󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁04󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "[SITELEN IKE: this] [SITELEN IKE: isn't] 󱥬󱥔"
    assert u("󱥬󱤧󱥔") == "[SITELEN IKE: 󱥬󱤧​󱥔]"


def test_line_break0():
    u = PankantanUxor(line_break=LineBreak.AFTER_SENTENCE)
    assert u("toki li pona") == "󱥬󱤧󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁2󱤧󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁03󱤧󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁04󱤧󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "[SITELEN IKE: this] [SITELEN IKE: isn't] 󱥬󱥔"
    assert u("󱥬󱤧󱥔") == "󱥬󱤧󱥔"


def test_line_break2():
    u = PankantanUxor(line_break=LineBreak.AFTER_WORD_GROUP)
    assert u("toki li pona") == "󱥬​󱤧​󱥔​"
    assert u("ni li toki+pona") == "󱥁​󱤧​󱥬󱦖󱥔​"
    assert u("ni2 li toki+pona") == "󱥁2​󱤧​󱥬󱦖󱥔​"
    assert u("ni03 li toki+pona") == "󱥁03​󱤧​󱥬󱦖󱥔​"
    assert u("ni< li toki+pona") == "󱥁04​󱤧​󱥬󱦖󱥔​"
    assert u("this isn't toki pona") == "[SITELEN IKE: this] [SITELEN IKE: isn't] 󱥬​󱥔​"
    assert u("󱥬󱤧󱥔") == "󱥬​󱤧​󱥔​"
