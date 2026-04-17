from uxor.main import LineBreak, ReportInvalid, Uxor


def test_default():
    u = Uxor()
    assert u("toki li pona") == "󱥬󱤧󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁‍2󱤧󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁‍03󱤧󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁‍04󱤧󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "this isn't toki pona"


def test_unspaced():
    u = Uxor(allow_unspaced=True)
    assert u("toki li pona") == "󱥬󱤧󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁‍2󱤧󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁‍03󱤧󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁‍04󱤧󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "this isn't toki pona"
    assert u("tokipona") == "󱥬󱥔"
    assert u("kalama") == "󱤕"
    assert u("thisisnttokipona") == "thisisnttokipona"


def test_ignore_variants():
    u = Uxor(ignore_variants=True)
    assert u("toki li pona") == "󱥬󱤧󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "this isn't toki pona"


def test_report_invalid1():
    u = Uxor(report_invalid=ReportInvalid.UNLESS_VALID_REPLACEMENT)
    assert u("toki li pona") == "󱥬󱤧󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁‍2󱤧󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁‍03󱤧󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁‍04󱤧󱥬󱦖󱥔"
    assert u("this isn't toki pona") == u._INVALID_SEQ_MESSAGE.format("this")
    assert u("󱥬󱤧󱥔") == "󱥬󱤧󱥔"


def test_report_invalid2():
    u = Uxor(report_invalid=ReportInvalid.ALWAYS)
    assert u("toki li pona") == "󱥬󱤧󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁‍2󱤧󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁‍03󱤧󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁‍04󱤧󱥬󱦖󱥔"
    assert u("this isn't toki pona") == u._INVALID_SEQ_MESSAGE.format("this")
    assert u("󱥬󱤧󱥔") == u._INVALID_SEQ_MESSAGE.format("󱥬󱤧󱥔")


def test_line_break1():
    u = Uxor(line_break=LineBreak.WHEN_UNAMBIGUOUS)
    assert u("toki li pona") == "󱥬󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁‍2󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁‍03󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁‍04󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "this isn't toki pona"


def test_line_break2():
    u = Uxor(line_break=LineBreak.AFTER_ANY_GLYPH)
    assert u("toki li pona") == "󱥬​󱤧​󱥔"
    assert u("ni li toki+pona") == "󱥁​󱤧​󱥬󱦖󱥔"
    assert u("ni2 li toki+pona") == "󱥁‍2​󱤧​󱥬󱦖󱥔"
    assert u("ni03 li toki+pona") == "󱥁‍03​󱤧​󱥬󱦖󱥔"
    assert u("ni< li toki+pona") == "󱥁‍04​󱤧​󱥬󱦖󱥔"
    assert u("this isn't toki pona") == "this isn't toki pona"