"""Comprova si l'àudio RTVA conserva canals separats per a diarització."""
from pathlib import Path
import wave, numpy as np
ROOT=Path(__file__).parents[1]; CAND=ROOT/'proveniencia'/'candidats'/'lead-rtva-001'

def main():
 p=CAND/'audio-stereo.wav'
 with wave.open(str(p),'rb') as w:
  rate=w.getframerate(); channels=w.getnchannels(); data=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,channels).astype(float)
 corr=float(np.corrcoef(data[:,0],data[:,1])[0,1]); rms=np.sqrt(np.mean(data**2,axis=0)); diff=float(np.sqrt(np.mean((data[:,0]-data[:,1])**2)))
 lines=['# Comprovació dels canals estèreo — Joan Verdú','',f'- Fitxer: `audio-stereo.wav`; {channels} canals, {rate} Hz.',f'- Correlació global L/R: **{corr:.6f}**.',f'- RMS L/R: **{rms[0]:.2f} / {rms[1]:.2f}**; RMS de diferència: **{diff:.2f}**.', '', 'Els canals són pràcticament una mescla comuna (correlació molt alta); no hi ha una pista esquerra/dreta que permeti separar entrevistador i entrevistat. La diarització continua pendent i el fitxer estèreo només es conserva com a comprovació de la font.']
 (CAND/'stereo-canals.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(f'correlació {corr:.6f} · rms diferència {diff:.2f}')
if __name__=='__main__':main()
