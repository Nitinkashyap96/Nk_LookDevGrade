# Nk_LookDevGrade
Nk_LookDevGrade — Tool Description Author: Nitin Kashyap | Version: 1.0 |  Nuke 12+ A self-contained LookDev Grading Group node for Nuke, built entirely in Python. It combines a comprehensive set of grading controls into a single, clean interface — no external .nk gizmo file needed.




Nk_LookDevGrade

A LookDev Grading Tool for Nuke

Author: Nitin Kashyap

Version: 1.0

Nuke (12+)

Install: ~/.nuke/ (no external .nk file required)

Overview

Nk_LookDevGrade is a self-contained Nuke Group node built entirely in
Python. It provides a comprehensive grading toolkit for look-development
work, combining white balance, exposure, contrast, clarity, and colour
correction controls in a single, clean interface.

Because the node is constructed programmatically at startup from
aa_LookDevGrade_builder.py, no external .nk gizmo file is needed. All
internal wiring, expressions, and knob definitions live in one Python
module.

# Installation

File Layout

Place both files inside your Nuke user directory:

  ~/.nuke/

  Nk_LookDevGrade_builder.py <- node builder module

  menu.py <- Nuke startup script

menu.py Contents

Your menu.py should contain the following (no other code from the
builder is needed):

      import nuke
    
      import Nk_LookDevGrade_builder
    
      toolbar = nuke.toolbar("Nodes")
    
      m = toolbar.addMenu("Nk_Tools", icon="icon_256.png")
    
      m.addCommand(
    
      "LookDev Grade",
    
      nk_LookDevGrade_builder._create_nk_LookDevGrade,
    
      icon="icon_256.png",
    
      tooltip="Nk_LookDevGrade — LookDev Grade by Nitin Kashyap | v1.0 | 31
      Mar 2026"
    
      )
    
      print("[Nk_LookDevGrade] Registered — Nodes > Nk_Tools > LookDev
      Grade")

Important: Pass the function reference _create_aa_LookDevGrade without
parentheses. Nuke's addCommand expects a callable, not the result of
calling it.

Verification

After restarting Nuke, the node is accessible from:

  Nodes toolbar > Nk_Tools > LookDev Grade

The Nuke Script Editor should also print:

  [Nk_LookDevGrade] Registered — Nodes > Nk_Tools > LookDev Grade

Node Internals

The Group node contains the following internal nodes, wired
top-to-bottom:

  ------------------------------------------------------------------------
  Internal Node   Type           Purpose
  --------------- -------------- -----------------------------------------
  BWPoint         Grade          Applies blackpoint and whitepoint
                                 per-channel

  TempTint        Expression     Shifts temperature (R/B) and tint (G) via
                                 additive offset

  ExpGrade        Grade          Exposure control — multiplies by pow(2,
                                 exposure)

  ContrGrey       Expression     Contrast pivoted around a user-defined
                                 grey point

  ClarBlur        Blur           Blurred copy of the image used for the
                                 clarity effect

  ClarMerge       Merge2         Soft-light blend of sharp vs blurred for
                                 clarity

  VibNode         Saturation     Vibrance (overall saturation boost/cut)

  SatNode         Saturation     Independent saturation control

  LGG             Grade          Lift / Gamma / Gain with per-colour and
                                 intensity knobs

  MixOut          Dissolve       Final mix dissolve between original and
                                 graded signal
  ------------------------------------------------------------------------

Controls Reference

White Balance

  -------------------------------------------------------------------------
  Knob            Range       Default     Description
  --------------- ----------- ----------- ---------------------------------
  temperature     -1 to 1     0.0         Shifts red/blue channels to warm
                                          or cool the image

  tint            -1 to 1     -0.02       Shifts green channel for
                                          magenta/green tint correction
  -------------------------------------------------------------------------

Black & White Point

  -------------------------------------------------------------------------
  Knob            Range       Default     Description
  --------------- ----------- ----------- ---------------------------------
  blackpoint      RGB colour  [0,0,0,0]   Per-channel black point remapping

  whitepoint      RGB colour  [1,1,1,1]   Per-channel white point remapping
  -------------------------------------------------------------------------

Exposure & Contrast

  -------------------------------------------------------------------------
  Knob            Range       Default     Description
  --------------- ----------- ----------- ---------------------------------
  exposure        -2 to 2     -0.16       EV-based exposure in stops —
                                          multiplies by pow(2, value)

  contrast        0 to 2      1.18        Contrast multiplier pivoted
                                          around grey_point

  grey_point      0 to 1      0.18        Pivot value used for contrast
                                          calculation

  soft_contrast   0 to 1      0.94        Reserved for soft/sigmoidal
                                          contrast (future use)
  -------------------------------------------------------------------------

Clarity

  --------------------------------------------------------------------------
  Knob             Range       Default     Description
  ---------------- ----------- ----------- ---------------------------------
  clarity_op       enum        High Pass   High Pass, Unsharp Mask, or Off

  clarity_amount   0 to 0.1    0.035       Strength of the clarity / local
                                           contrast effect
  --------------------------------------------------------------------------

Saturation & Vibrance

  -------------------------------------------------------------------------
  Knob            Range       Default     Description
  --------------- ----------- ----------- ---------------------------------
  vibrance        0 to 2      0.9         Global saturation level via
                                          Saturation node (VibNode)

  saturation      0 to 2      1.0         Independent saturation control
                                          (SatNode)
  -------------------------------------------------------------------------

Lift / Gamma / Gain

  ---------------------------------------------------------------------------
  Knob              Range       Default     Description
  ----------------- ----------- ----------- ---------------------------------
  lift              RGB colour  [0,0,0,0]   Per-channel lift colour

  lift_intensity    -1 to 1     0.0         Scalar multiplier for lift colour

  gamma_col         RGB colour  [1,1,1,1]   Per-channel gamma colour

  gamma_intensity   0 to 2      1.0         Scalar multiplier for gamma
                                            colour

  gain_col          RGB colour  [1,1,1,1]   Per-channel gain colour

  gain_intensity    0 to 2      1.0         Scalar multiplier for gain colour
  ---------------------------------------------------------------------------

Output Mix

  -------------------------------------------------------------------------
  Knob            Range       Default     Description
  --------------- ----------- ----------- ---------------------------------
  mix             0 to 1      1.0         Dissolve between the ungraded
                                          input and the fully graded output

  -------------------------------------------------------------------------

Inputs & Outputs

-   Input: Input (pipe 0) — the image to be graded.

-   mask: mask (pipe 1) — optional mask input (wired but not yet
    connected internally; reserved for future masking support).

-   Output: Output — the graded result, optionally blended with the
    original via the mix knob.

Usage Tips

-   Start with exposure and contrast before touching colour knobs —
    getting tonality right first makes colour work easier.

-   Use mix at the end for a subtle blending of the grade, great for
    applying looks non-destructively.

-   Set clarity_op to Off when you don't need it to save a Blur + Merge2
    evaluation.

-   The lift_intensity, gamma_intensity, and gain_intensity knobs let
    you scale the colour wheels without resetting them — useful for
    fading a colour decision in or out.

-   Temperature and tint adjustments are additive (not multiplied), so
    extreme values will clip. Keep them subtle.

Known Limitations

-   The soft_contrast knob is exposed but not yet wired to any internal
    node. It is reserved for a future sigmoidal contrast implementation.

-   The mask input (pipe 1) is created but not connected to any internal
    node's mask channel. Masking support is planned.

-   clarity_op mode switching (High Pass vs Unsharp Mask) currently uses
    only the soft-light Merge2 approach for both modes.

-   Temperature and tint are linear additive offsets, not a proper
    Kelvin-based colour temperature model.

Licence

Free to use and modify for personal and commercial production work.
Please retain the author credit in the title label when redistributing.
