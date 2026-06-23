# theWayItIs.py
# Plays main chord progression from Bruce Hornsby's
# &amp;quot;The Way It Is&amp;quot; (1986).

from music import *

mPhrase = Phrase()
mPhrase.setTempo(105)

mPhrase.addNote(A4, SN)
mPhrase.addNote(B4, SN)
mPhrase.addChord([A3,E4,G4,C5], DEN)
mPhrase.addChord([A3,E4,G4,C5], DEN)
mPhrase.addChord([E3,D4,G4,B4], HN)
mPhrase.addChord([D4,A4], SN)
mPhrase.addNote(G4, SN)
mPhrase.addChord([D3,D4, FS4, A4], DEN)
mPhrase.addChord([D3, D4, G4, B4], DEN)
mPhrase.addChord([C3, C4, D4, G4], DQN)
mPhrase.addChord([C3, E4], EN)
mPhrase.addNote(D4, SN)
mPhrase.addNote(C4, SN)
mPhrase.addChord([G2, B4, D4], DQN)
mPhrase.addChord([G2, D4, G4, B4], EN)
mPhrase.addChord([D3, E4, A4, C5], DEN)
mPhrase.addChord([D3, D4, G4, B4], EN)
mPhrase.addNote(A4, SN)
mPhrase.addNote(G4, EN)
mPhrase.addChord([C3,C4,D4,G4], DEN)
mPhrase.addChord([C3,C4,D4,G4], DEN)
mPhrase.addChord([G3,B3,D4,G4], HN)

Play.midi(mPhrase)