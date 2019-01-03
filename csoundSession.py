'''
    ctcsoundSession.py:
    
    Copyright (C) 2016 Francois Pinot
    
    This code is free software; you can redistribute it
    and/or modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    
    Csound is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with Csound; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
    02111-1307 USA
'''

import os
import ctypes
import ctcsound

class CsoundSession(ctcsound.Csound):
    """A class for running a csound session"""
    
    def __init__(self, csdFileName=None):
        """Start a csound session, eventually loading a csd file"""
        ctcsound.Csound.__init__(self)
        self.pt = None
        if csdFileName and os.path.exists(csdFileName):
            self.csd = csdFileName
            self.startThread()
        else:
            self.csd = None
    
    def startThread(self):
        if self.compile_("csoundSession", self.csd) == 0 :
            self.pt = ctcsound.CsoundPerformanceThread(self.cs)
            self.pt.play()
            
    def resetSession(self, csdFileName=None):
        """Reset the current session, eventually loading a new csd file"""
        if csdFileName and os.path.exists(csdFileName):
            self.csd = csdFileName
        if self.csd:
            self.stopPerformance()
            self.startThread()
    
    def stopPerformance(self):
        """Stop the current score performance if any"""
        if self.pt:
            if self.pt.status() == 0:
                self.pt.stop()
            self.pt.join()
            self.pt = None
        self.cleanup()

    def csdFileName(self):
        """Return the loaded csd filename or None"""
        return self.csd
        
    def note(self, pfields, absp2mode = 0):
        """Send a score note to a csound instrument"""
        return self.pt.scoreEvent(absp2mode, 'i', pfields)
        
    def scoreEvent(self, eventType, pfields, absp2mode = False):
        """Send a score event to csound"""
        self.pt.scoreEvent(absp2mode, eventType, pfields)
    
    def flushMessages(self):
        """Wait until all pending messages are actually received by the performance thread"""
        if self.pt:
            self.pt.flushMessageQueue()

cs = ctcsound.Csound() 
# session = CsoundSession(); 

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
  f 0 14400    ; a 4 hours session should be enough

  e
  </CsScore>
</CsoundSynthesizer>
'''

# cs.compileCsdText(csd)
# cs.start()

# pt = ctcsound.CsoundPerformanceThread(cs.csound())


ret = cs.compileCsd(csd)
if ret == ctcsound.CSOUND_SUCCESS:
    while not cs.performBuffer():
        print('.', end='')
        # pt.play()

        # pt.scoreEvent(False, 'i', (1, 0, 1, 0.5, 8.06, 0.05, 0.3, 0.5))
        # pt.scoreEvent(False, 'i', (1, 0.5, 1, 0.5, 9.06, 0.05, 0.3, 0.5))
    print()
    cs.reset()

 

