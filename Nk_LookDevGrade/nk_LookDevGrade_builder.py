import nuke
import nukescripts
import os

# ══════════════════════════════════════════════════════════════════
#  Nk_LookDevGrade — nk_LookDevGrade_builder.py
#  Author  : Nitin Kashyap
#  Version : 1.0
#  Updated : 31 March 2026
#  Place in: ~/.nuke/ Nk_LookDevGrade/
#  Builds the gizmo entirely in Python at Nuke startup.
#  No external .nk file required.
# ══════════════════════════════════════════════════════════════════

def _create_nk_LookDevGrade():
    """
    Builds and returns a fully wired Nk_LookDevGrade Group node.
    Called every time the user places the node.
    """

    # ── helpers ──────────────────────────────────────────────────
    def dbl(name, label, lo, hi, val):
        k = nuke.Double_Knob(name, label)
        k.setRange(lo, hi)
        k.setValue(val)
        return k

    def col(name, label, val):
        k = nuke.AColor_Knob(name, label)
        k.setValue(val)
        return k

    def div(name):
        return nuke.Text_Knob(name, "", " ")

    # ── Group ─────────────────────────────────────────────────────
    g = nuke.createNode("Group", inpanel=False)
    g.setName("Nk_LookDevGrade")
    g["label"].setValue("")
    g["tile_color"].setValue(0x473eff)

    g.begin()

    # inputs
    inp = nuke.createNode("Input", inpanel=False)
    inp.setName("Input")
    inp["number"].setValue(0)
    inp["xpos"].setValue(0);   inp["ypos"].setValue(-500)

    msk = nuke.createNode("Input", inpanel=False)
    msk.setName("mask")
    msk["number"].setValue(1)
    msk["xpos"].setValue(160); msk["ypos"].setValue(-500)

    # blackpoint / whitepoint
    bw = nuke.createNode("Grade", inpanel=False)
    bw.setName("BWPoint")
    bw.setInput(0, inp)
    for i, ch in enumerate("rgb"):
        bw["blackpoint"].setExpression("parent.blackpoint.%s" % ch, i)
        bw["whitepoint"].setExpression("parent.whitepoint.%s" % ch, i)
    bw["xpos"].setValue(0);  bw["ypos"].setValue(-420)

    # temperature / tint
    tt = nuke.createNode("Expression", inpanel=False)
    tt.setName("TempTint")
    tt.setInput(0, bw)
    tt["expr0"].setValue("r + parent.temperature * 0.1")
    tt["expr1"].setValue("g + parent.tint * 0.05")
    tt["expr2"].setValue("b - parent.temperature * 0.1")
    tt["xpos"].setValue(0);  tt["ypos"].setValue(-360)

    # exposure
    eg = nuke.createNode("Grade", inpanel=False)
    eg.setName("ExpGrade")
    eg.setInput(0, tt)
    for i in range(3):
        eg["multiply"].setExpression("pow(2, parent.exposure)", i)
    eg["xpos"].setValue(0);  eg["ypos"].setValue(-300)

    # contrast / grey point
    cg = nuke.createNode("Expression", inpanel=False)
    cg.setName("ContrGrey")
    cg.setInput(0, eg)
    for i, ch in enumerate("rgb"):
        cg["expr%d" % i].setValue(
            "(%s - parent.grey_point) * parent.contrast + parent.grey_point" % ch)
    cg["xpos"].setValue(0);  cg["ypos"].setValue(-240)

    # clarity — blur branch
    cb = nuke.createNode("Blur", inpanel=False)
    cb.setName("ClarBlur")
    cb.setInput(0, cg)
    cb["size"].setExpression("parent.clarity_amount * 30")
    cb["xpos"].setValue(160); cb["ypos"].setValue(-240)

    # clarity — merge (B=sharp, A=blurred)
    cm = nuke.createNode("Merge2", inpanel=False)
    cm.setName("ClarMerge")
    cm.setInput(0, cg)   # B pipe  (input 0 = bottom/B)
    cm.setInput(1, cb)   # A pipe  (input 1 = top/A)
    cm["operation"].setValue("soft-light")
    cm["mix"].setExpression(
        "clamp(parent.clarity_amount * 10, 0, 1) * (parent.clarity_op != 2)")
    cm["xpos"].setValue(0);  cm["ypos"].setValue(-180)

    # vibrance
    vib = nuke.createNode("Saturation", inpanel=False)
    vib.setName("VibNode")
    vib.setInput(0, cm)
    vib["saturation"].setExpression("parent.vibrance")
    vib["xpos"].setValue(0); vib["ypos"].setValue(-120)

    # saturation
    sat = nuke.createNode("Saturation", inpanel=False)
    sat.setName("SatNode")
    sat.setInput(0, vib)
    sat["saturation"].setExpression("parent.saturation")
    sat["xpos"].setValue(0); sat["ypos"].setValue(-60)

    # lift / gamma / gain
    lgg = nuke.createNode("Grade", inpanel=False)
    lgg.setName("LGG")
    lgg.setInput(0, sat)
    for i, ch in enumerate("rgb"):
        lgg["blackpoint"].setExpression(
            "parent.lift.%s * parent.lift_intensity" % ch, i)
        lgg["white"].setExpression(
            "parent.gain_col.%s * parent.gain_intensity" % ch, i)
        lgg["gamma"].setExpression(
            "parent.gamma_col.%s * parent.gamma_intensity" % ch, i)
    lgg["xpos"].setValue(0); lgg["ypos"].setValue(0)

    # mix dissolve  (input 0 = original, input 1 = graded)
    mx = nuke.createNode("Dissolve", inpanel=False)
    mx.setName("MixOut")
    mx.setInput(0, inp)
    mx.setInput(1, lgg)
    mx["which"].setExpression("parent.mix")
    mx["xpos"].setValue(0);  mx["ypos"].setValue(60)

    # output
    out = nuke.createNode("Output", inpanel=False)
    out.setName("Output")
    out.setInput(0, mx)
    out["xpos"].setValue(0); out["ypos"].setValue(120)

    g.end()

    # ── user knobs ────────────────────────────────────────────────
    g.addKnob(nuke.Tab_Knob("LookDevGrade_tab", "Nk_LookDevGrade"))

    t = nuke.Text_Knob("title_label", "")
    t.setValue(
        "<b><font size=12>"
        "<font color=#dddddd>LookDev</font>"
        "<font color=#5b9bd5>\xb7Grade</font>"
        "</font></b><br>"
        "<font color=#5b9bd5><small>by Nitin Kashyap &nbsp;|&nbsp; v1.0 &nbsp;|&nbsp; 31 Mar 2026</small></font>")
    g.addKnob(t)

    g.addKnob(div("div_wb"))
    g.addKnob(dbl("temperature",    "Temperature",    -1,   1,    0.0))
    g.addKnob(dbl("tint",           "Tint",           -1,   1,   -0.02))

    g.addKnob(div("div_bw"))
    g.addKnob(col("blackpoint",     "Blackpoint",     [0, 0, 0, 0]))
    g.addKnob(col("whitepoint",     "Whitepoint",     [1, 1, 1, 1]))

    g.addKnob(div("div_exp"))
    g.addKnob(dbl("exposure",       "Exposure",       -2,   2,   -0.16))
    g.addKnob(dbl("contrast",       "Contrast",        0,   2,    1.18))
    g.addKnob(dbl("grey_point",     "Grey Point",      0,   1,    0.18))
    g.addKnob(dbl("soft_contrast",  "Soft Contrast",   0,   1,    0.94))

    g.addKnob(div("div_clar"))
    k = nuke.Enumeration_Knob("clarity_op", "Clarity Operation",
                               ["High Pass", "Unsharp Mask", "Off"])
    k.setValue(0)
    g.addKnob(k)
    g.addKnob(dbl("clarity_amount", "Clarity Amount",  0,   0.1,  0.035))
    g.addKnob(dbl("vibrance",       "Vibrance",        0,   2,    0.9))
    g.addKnob(dbl("saturation",     "Saturation",      0,   2,    1.0))

    g.addKnob(div("div_lift"))
    g.addKnob(col("lift",           "Lift",           [0, 0, 0, 0]))
    g.addKnob(dbl("lift_intensity", "Lift Intensity", -1,   1,    0.0))

    g.addKnob(div("div_gamma"))
    g.addKnob(col("gamma_col",      "Gamma",          [1, 1, 1, 1]))
    g.addKnob(dbl("gamma_intensity","Gamma Intensity",  0,   2,    1.0))

    g.addKnob(div("div_gain"))
    g.addKnob(col("gain_col",       "Gain",           [1, 1, 1, 1]))
    g.addKnob(dbl("gain_intensity", "Gain Intensity",   0,   2,    1.0))

    g.addKnob(div("div_mix"))
    g.addKnob(dbl("mix",            "mix",              0,   1,    1.0))

    # open the properties panel
    g.showControlPanel()
    return g
