import ctcsound

cs = ctcsound.Csound() 
csd = '''
<CsoundSynthesizer>
<CsOptions>
  -odac
</CsOptions>
<CsInstruments>
  sr = 44100 ; sample rate
  kr = 4410 ; control rate (allows slower moving singal less compute time)
  ksmps = 10  ; control period (sr / kr)
  nchnls = 1 ; number of channels
    instr 1; 
a1  oscil   1000, 440, 1
    out     a1
    endin
</CsInstruments>
<CsScore>
  f1  0   4096    10 1  ;  this line defines function number 1, a sine wave
  i1   0    1    100      880  ; 
  e
  </CsScore>
</CsoundSynthesizer>
'''

ret = cs.compileCsdText(csd)
if ret == ctcsound.CSOUND_SUCCESS:
  cs.start()
  cs.perform()
  cs.reset()