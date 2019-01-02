#OPCODES
#opcodes: interconnecting 'modules' that are represented by symbols, labels or variable names
#opcodes can be 'patched' from one another
OUTPUT  OPCODE ARGUMENTS                         (OPTIONAL COMMENT)
output  oscil  amplitude  frequency  function ;  COMMENT
a1      oscil  1000,      440,       1

#VARIABLES
#i-rate: setting paramter values and note durartions
#'evaluated' at initialization time and remain constant 
#k-rate: setting paramater values and note durations
#recomputed at the control-rate
#a-rate: variables are array or vectors

#HEADER SECTION
#def sample & control rates 
sr = 44100 #sample rate 
kr = 4410  #control rate
ksmps = 10 #ksmps = sr/kr
nchnls = 1 #num channels

#INSTRUMENTS
#are giving a unique instrument number
#delimited by the (instr) and (endin) statments


#instrument 101
#fixed frequency and amplitude table-lookup oscillator
#amplitude: 10000
#frequency 440
#function 1

    instr   101    ;SIMPLE SINE WAVE
a1  oscil   10000,  440,  1
    out     a1
    endin

    instr   102    ;SIMPLE FM
a1  foscil  10000,  440,  1,  2,  3,  1
    out     a1
    endin

    instr   103    ;SIMPPLE BUZZ
a1  buzz    10000,  440,  1
    out     a1
    endin

    instr   104    ;SIMPLE WAVEGUIDE
a1  pluck   10000,  440,  440, 2, 1
    out     a1
    endin

    instr   105    ;SIMPLE GRANULAR
a1  grain   10000,  440,  55,  10, 0.5, 1, 3, 1
    out     a1
    endin

#GEN STATEMENTS
#function generator

f   number load-time  table-size  GEN  Routine  parameter1  parameter...  ; COMMENT
f   111    0          16          10   1                                  ; A SINEWAVE

#P-FIELDS
;   P1              P2          P3
1   INSTRUMENT num  START-TIME  DURATION


#Paramater Fields in the Orchestra

    instr   107
a1  oscil   p4, p5, p6
    out     a1
    endin

; P1     P2     P3     P4       P5       P6
; INS    STRT   DUR    AMP      FREQ     WAVESHAPE
 
i 107    0      1      10000    440      1
i 107    1.5    1      20000    220      2
i 107    3      3      10000    110      2
i 107    3.5    2.5    10000    138.6    2
i 107    4      2      5000     329.6    2
i 107    4.5    1.5    6000     440      2
