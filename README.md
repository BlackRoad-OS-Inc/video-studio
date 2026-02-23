# 🎬 Video Studio — Motion & Animation Library

Part of **BlackRoad Studio** — production creative tools.

24 easing functions, a Timeline/keyframe engine, preset animations, and multi-format serializers (CSS, Web Animations API, Framer Motion).

## Features

- **24+ easing functions** — linear, quad, cubic, expo, sine, back, bounce, elastic, spring, cubic-bezier
- **Physics spring** — mass/stiffness/damping spring simulation
- **Custom cubic-bezier** — Newton-Raphson solver matching CSS `cubic-bezier()`
- **Timeline engine** — keyframe-based with per-keyframe easing and property interpolation
- **15 animation presets** — fade, slide, pop, shake, bounce, pulse, spin, wiggle, flip, blur-in, typewriter
- **CSS @keyframes** — valid `@keyframes` + animation class output
- **Web Animations API** — JS `element.animate()` format
- **Framer Motion** — React variants with transitions
- **SVG curve visualizer** — renders easing as SVG path

## Quick start

```bash
# List presets
python src/motion_library.py presets

# Get a preset as CSS
python src/motion_library.py preset slide-up --css

# Get as Web Animations API JS
python src/motion_library.py preset bounce --js

# Get as Framer Motion variants
python src/motion_library.py preset fade-in --framer

# Sample an easing curve
python src/motion_library.py easing ease-out-elastic --steps 10

# Export as SVG
python src/motion_library.py easing spring --svg
```

## Available presets

| Name | Duration | Description |
|---|---|---|
| `fade-in` | 300ms | Opacity fade in |
| `fade-out` | 300ms | Opacity fade out |
| `slide-up` | 400ms | Slide from below + fade |
| `slide-down` | 400ms | Slide from above + fade |
| `slide-in-left` | 350ms | Slide from left + fade |
| `slide-in-right` | 350ms | Slide from right + fade |
| `pop` | 300ms | Scale overshoot pop |
| `shake` | 500ms | Horizontal error shake |
| `bounce` | 800ms | Multi-bounce drop |
| `pulse` | 1000ms | Infinite attention pulse |
| `spin` | 1000ms | Continuous rotation |
| `wiggle` | 600ms | Playful rotation |
| `flip` | 600ms | 3D Y-axis flip |
| `blur-in` | 400ms | Blur-to-focus entrance |
| `typewriter` | 2000ms | Text width reveal |

## Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src
```
