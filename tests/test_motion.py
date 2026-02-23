"""Tests for motion_library.py"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
from motion_library import (
    linear, ease_in_quad, ease_out_quad, ease_in_out_quad,
    ease_in_cubic, ease_out_cubic, ease_in_out_cubic,
    ease_in_expo, ease_out_expo,
    ease_in_sine, ease_out_sine,
    ease_in_back, ease_out_back,
    ease_out_bounce, ease_in_bounce,
    ease_out_elastic, ease_in_elastic,
    spring, cubic_bezier, EASE, EASE_IN, EASE_OUT, EASE_IN_OUT,
    EASINGS, Keyframe, Timeline, PRESETS,
    serialize_to_css, serialize_to_js, serialize_to_framer_motion,
    sample_easing, easing_to_svg_path, get_preset, list_presets,
    _js_ident,
)


# ── Easing boundary conditions ────────────────────────────────────────────────
ALL_STANDARD_EASINGS = [
    linear, ease_in_quad, ease_out_quad, ease_in_out_quad,
    ease_in_cubic, ease_out_cubic, ease_in_out_cubic,
    ease_in_sine, ease_out_sine,
    ease_out_bounce, ease_in_bounce,
]

@pytest.mark.parametrize("fn", ALL_STANDARD_EASINGS)
def test_easing_at_zero(fn):
    assert abs(fn(0.0)) < 0.01

@pytest.mark.parametrize("fn", ALL_STANDARD_EASINGS)
def test_easing_at_one(fn):
    assert abs(fn(1.0) - 1.0) < 0.01

@pytest.mark.parametrize("fn", ALL_STANDARD_EASINGS)
def test_easing_midpoint_between_bounds(fn):
    v = fn(0.5)
    assert 0.0 <= v <= 1.0

def test_linear_midpoint():
    assert linear(0.5) == 0.5

def test_ease_in_quad_concave():
    # Should be slower than linear at start
    assert ease_in_quad(0.25) < 0.25

def test_ease_out_quad_convex():
    # Should be faster than linear at start
    assert ease_out_quad(0.25) > 0.25

def test_ease_in_out_quad_symmetry():
    a = ease_in_out_quad(0.25)
    b = ease_in_out_quad(0.75)
    assert abs(a + b - 1.0) < 0.001


# ── Back / elastic – allow overshoot ─────────────────────────────────────────
def test_ease_out_back_overshoots():
    peak = max(ease_out_back(t) for t in [i/100 for i in range(101)])
    assert peak > 1.0

def test_ease_in_back_undershoots():
    trough = min(ease_in_back(t) for t in [i/100 for i in range(101)])
    assert trough < 0.0

def test_ease_out_elastic_at_boundaries():
    assert abs(ease_out_elastic(0.0)) < 0.01
    assert abs(ease_out_elastic(1.0) - 1.0) < 0.01


# ── Spring ────────────────────────────────────────────────────────────────────
def test_spring_at_zero():
    assert abs(spring(0.0)) < 0.01

def test_spring_reaches_one():
    # By t=10 a typical spring should be near 1
    val = spring(10.0, mass=1, stiffness=100, damping=10)
    assert abs(val - 1.0) < 0.1

def test_spring_overdamped():
    val = spring(1.0, mass=1, stiffness=100, damping=100)
    assert 0.0 <= val <= 1.5


# ── Cubic bezier ──────────────────────────────────────────────────────────────
def test_cubic_bezier_boundaries():
    fn = cubic_bezier(0.25, 0.1, 0.25, 1.0)
    assert abs(fn(0)) < 0.01
    assert abs(fn(1) - 1.0) < 0.01

def test_cubic_bezier_css_ease():
    fn = EASE
    # CSS ease is roughly ease-in-out — midpoint ≠ 0.5 exactly
    v = fn(0.5)
    assert 0.4 < v < 0.9


# ── EASINGS registry ──────────────────────────────────────────────────────────
def test_easings_registry_has_keys():
    for name in ["linear","ease","ease-in","ease-out","ease-in-out","spring"]:
        assert name in EASINGS

def test_easings_all_callable():
    for name, fn in EASINGS.items():
        assert callable(fn), f"{name} not callable"


# ── Keyframe / Timeline ───────────────────────────────────────────────────────
def test_timeline_add_keyframe_sorted():
    tl = Timeline(id="t1", name="test", duration=300)
    tl.add_keyframe(1.0, {"opacity": 1})
    tl.add_keyframe(0.0, {"opacity": 0})
    assert tl.keyframes[0].offset == 0.0
    assert tl.keyframes[1].offset == 1.0

def test_timeline_sample_at_edges():
    tl = Timeline(id="t1", name="test", duration=300)
    tl.add_keyframe(0.0, {"opacity": 0})
    tl.add_keyframe(1.0, {"opacity": 1})
    assert tl.sample(0.0)["opacity"] == 0
    assert tl.sample(1.0)["opacity"] == 1

def test_timeline_sample_midpoint():
    tl = Timeline(id="t1", name="test", duration=300)
    tl.add_keyframe(0.0, {"opacity": 0.0}, "linear")
    tl.add_keyframe(1.0, {"opacity": 1.0}, "linear")
    mid = tl.sample(0.5)
    assert 0.49 < mid["opacity"] < 0.51

def test_timeline_sample_empty():
    tl = Timeline(id="t1", name="test", duration=300)
    assert tl.sample(0.5) == {}


# ── CSS serializer ────────────────────────────────────────────────────────────
def test_css_keyframes_contains_at_keyframes():
    tl = get_preset("fade-in")
    css = serialize_to_css(tl)
    assert "@keyframes" in css
    assert "0%" in css
    assert "100%" in css
    assert "opacity" in css

def test_css_animation_class():
    tl = get_preset("slide-up")
    css = serialize_to_css(tl)
    assert "animation:" in css
    assert "slide-up" in css

def test_css_duration_present():
    tl = get_preset("pop")
    css = serialize_to_css(tl)
    assert str(int(tl.duration)) in css


# ── JS serializer ─────────────────────────────────────────────────────────────
def test_js_output_valid():
    tl  = get_preset("bounce")
    js  = serialize_to_js(tl)
    assert "Keyframes" in js
    assert "Options"   in js
    assert "duration"  in js
    assert "animate("  in js

def test_js_ident_camel_case():
    assert _js_ident("slide-up")  == "slideUp"
    assert _js_ident("fade_in")   == "fadeIn"
    assert _js_ident("pop")       == "pop"


# ── Framer Motion serializer ──────────────────────────────────────────────────
def test_framer_motion_output():
    tl = get_preset("fade-in")
    fm = serialize_to_framer_motion(tl)
    assert "Variants" in fm
    assert "initial"  in fm
    assert "animate"  in fm
    assert "transition" in fm


# ── Presets ───────────────────────────────────────────────────────────────────
EXPECTED_PRESETS = [
    "fade-in","fade-out","slide-up","slide-down",
    "slide-in-left","slide-in-right","pop","shake",
    "bounce","pulse","spin","wiggle","flip","blur-in","typewriter",
]

@pytest.mark.parametrize("name", EXPECTED_PRESETS)
def test_preset_exists(name):
    tl = get_preset(name)
    assert tl is not None
    assert len(tl.keyframes) >= 2

@pytest.mark.parametrize("name", EXPECTED_PRESETS)
def test_preset_produces_valid_css(name):
    tl  = get_preset(name)
    css = serialize_to_css(tl)
    assert "@keyframes" in css
    assert "animation:" in css

def test_list_presets_returns_all():
    names = {p["name"] for p in list_presets()}
    for name in EXPECTED_PRESETS:
        assert name in names

def test_pulse_infinite_iterations():
    tl = get_preset("pulse")
    assert tl.iterations == float("inf")


# ── Easing sampler ────────────────────────────────────────────────────────────
def test_sample_easing_length():
    samples = sample_easing("ease-out-cubic", 10)
    assert len(samples) == 10

def test_sample_easing_boundaries():
    samples = sample_easing("linear", 10)
    assert samples[0]  == (0.0, 0.0)
    assert samples[-1] == (1.0, 1.0)

def test_svg_path_output():
    svg = easing_to_svg_path("ease-out-bounce")
    assert "<svg" in svg
    assert "<path" in svg
    assert 'fill="none"' in svg
