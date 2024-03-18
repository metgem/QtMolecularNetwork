import pytest

def test_init(mod):
    """Check SvgToPixmap."""

    if mod.__name__.endswith('._pure'):
        with pytest.raises(AttributeError):
            mod.IS_COMPILED
    else:
        assert mod.IS_COMPILED == True
