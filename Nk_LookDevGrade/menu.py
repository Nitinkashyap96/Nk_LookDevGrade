# ══════════════════════════════════════════════════════════════════
#  Nk_LookDevGrade — menu.py
#  Author  : Nitin Kashyap
#  Version : 1.0
#  Updated : 31 March 2026
# ══════════════════════════════════════════════════════════════════
import nuke
import nk_LookDevGrade_builder

toolbar = nuke.toolbar("Nodes")
m = toolbar.addMenu("Nk_Tools", icon="icon_256.png")
m.addCommand(
    "LookDev Grade",
    nk_LookDevGrade_builder._create_nk_LookDevGrade,
    icon="icon_256.png",
    tooltip="Nk_LookDevGrade — LookDev Grade by Nitin Kashyap | v1.0 | 31 Mar 2026"
)
print("[Nk_LookDevGrade] Registered — Nodes > Nk_Tools > LookDev Grade")
