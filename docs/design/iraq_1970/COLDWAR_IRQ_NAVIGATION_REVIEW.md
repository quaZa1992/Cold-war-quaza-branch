# COLDWAR_IRQ — mouse navigation correction

18 October 2026. Preview change only; no HOI4 GUI or loaded mod file changed.

The old pointer-down handler rejected every focus button, so most occupied tree areas could not start a pan. Its wheel handler always zoomed. Width changes also repeatedly refitted the selected branch, which could discard a manually positioned viewport.

The current preview arms a drag on background or focus, with a5pixel movement threshold. A drag captures the pointer, pans the shared entire world and suppresses only its resulting click. A new click immediately clears suppression and still opens the focus inspector. Left, middle and right mouse buttons work. Plain wheel input pans vertically, deltaX or Shift+wheel pans horizontally, and Ctrl/Command+wheel zooms at the pointer. Manual camera position and zoom survive responsive width changes and host state echoes. Fit/overview remain explicit actions; the fit calculation reserves space for the navigation hint at the bottom.

`tools/iraq_1970_concept/verify_navigation.cjs` exercises actual Chromium mouse buttons, mouse motion, wheel and modifier keys. Twelve checks pass with zero browser errors, including dragging from an unselected focus without opening it, the next normal click, all three background drag buttons, vertical/horizontal wheel motion, Ctrl zoom, travel from the far-right Iran sector to the far-left Iraqi State and a physical click there, a simulated host state echo, resize preservation, and physical inspection of An Iraqi Province. Results and the inspected core screenshot are `NAVIGATION_VALIDATION.json` and `PREVIEW_navigation_core.png`.

The existing browser suite also passes69branch views across320/736/1024pixel widths,426focus inspectors and13government views. The inline preview remains below1MB. These are browser-level results; the actual Codex host and HOI4 runtime were not launched for this check.
