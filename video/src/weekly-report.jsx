import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Series,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const BLACK = '#0A0A0A';
const GRAY = '#6D6D72';
const LIGHT = '#E7E7EA';
const WHITE = '#FFFFFF';

const FONT_CSS = `
@font-face { font-family: Pretendard; src: url('${staticFile('Pretendard-Regular.otf')}'); font-weight: 400; }
@font-face { font-family: Pretendard; src: url('${staticFile('Pretendard-SemiBold.otf')}'); font-weight: 600; }
@font-face { font-family: Pretendard; src: url('${staticFile('Pretendard-Bold.otf')}'); font-weight: 800; }
`;

const reveal = (frame, fps, delay = 0, distance = 42) => {
  const v = spring({frame: frame - delay, fps, config: {damping: 18, stiffness: 115, mass: 0.8}});
  return {opacity: v, transform: `translateY(${interpolate(v, [0, 1], [distance, 0])}px)`};
};

const pushIn = (frame, fps, delay = 0) => {
  const v = spring({frame: frame - delay, fps, config: {damping: 20, stiffness: 92}});
  return {opacity: v, transform: `translateX(${interpolate(v, [0, 1], [80, 0])}px) scale(${interpolate(v, [0, 1], [1.04, 1])})`};
};

const Header = ({meta, section}) => (
  <>
    <div style={{position: 'absolute', top: 46, left: 72, right: 72, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
      <div style={{fontSize: 20, fontWeight: 800, letterSpacing: '0.16em'}}>{meta.brand || 'WEEKLY REPORT'}</div>
      <div style={{fontSize: 18, fontWeight: 600, color: GRAY}}>{meta.period || ''}</div>
    </div>
    <div style={{position: 'absolute', top: 91, left: 72, right: 72, height: 2, background: BLACK}} />
    <div style={{position: 'absolute', top: 112, left: 72, fontSize: 17, fontWeight: 800, color: meta.accent, letterSpacing: '0.13em'}}>{section}</div>
  </>
);

const Footer = ({meta, scene, index}) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, scene.frames], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <div style={{position: 'absolute', left: 72, right: 72, bottom: 68, height: 2, background: '#ECECEE'}}>
        <div style={{height: '100%', width: `${progress}%`, background: meta.accent}} />
      </div>
      <div style={{position: 'absolute', left: 72, right: 72, bottom: 22, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{fontSize: 25, fontWeight: 600}}>{scene.caption || ''}</div>
        <div style={{fontSize: 19, fontWeight: 800, color: GRAY}}>{String(index + 1).padStart(2, '0')} / {String(meta.sceneCount).padStart(2, '0')}</div>
      </div>
    </>
  );
};

const Subtitle = ({text}) => text ? (
  <div style={{
    position: 'absolute',
    zIndex: 20,
    left: '50%',
    bottom: 96,
    maxWidth: 1420,
    transform: 'translateX(-50%)',
    padding: '14px 24px 15px',
    background: 'rgba(10, 10, 10, 0.94)',
    color: WHITE,
    fontSize: 34,
    lineHeight: 1.28,
    fontWeight: 800,
    letterSpacing: '-0.025em',
    textAlign: 'center',
    whiteSpace: 'pre-line',
  }}>{text}</div>
) : null;

const Shell = ({children, runtime, scene, index, section}) => (
  <AbsoluteFill style={{background: WHITE, color: BLACK, fontFamily: 'Pretendard, sans-serif', overflow: 'hidden'}}>
    <style>{FONT_CSS}</style>
    <Header meta={runtime.meta} section={section} />
    {children}
    <Subtitle text={scene.closedCaption} />
    <Footer meta={runtime.meta} scene={scene} index={index} />
    {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
  </AbsoluteFill>
);

const Hero = ({runtime, scene, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Shell runtime={runtime} scene={scene} index={index} section={scene.section || 'THIS WEEK'}>
      <div style={{position: 'absolute', left: 72, top: 205, width: scene.contentWidth || (scene.image ? 820 : 1500), zIndex: 2, ...reveal(frame, fps, 2)}}>
        <div style={{fontSize: 26, fontWeight: 800, color: runtime.meta.accent, letterSpacing: '0.09em', marginBottom: 23}}>{scene.eyebrow || 'WEEKLY REPORT'}</div>
        <div style={{fontSize: scene.titleSize || 102, lineHeight: 1.02, fontWeight: 800, letterSpacing: '-0.06em', whiteSpace: 'pre-line'}}>{scene.title}</div>
        {scene.subtitle ? <div style={{marginTop: 30, fontSize: 31, lineHeight: 1.45, color: GRAY, fontWeight: 600, whiteSpace: 'pre-line'}}>{scene.subtitle}</div> : null}
      </div>
      {scene.image ? <Img src={staticFile(scene.image)} style={{position: 'absolute', right: -45, top: 145, width: 1040, height: 760, objectFit: 'contain', ...pushIn(frame, fps, 5)}} /> : null}
      <div style={{position: 'absolute', left: 72, top: 810, width: 330, height: 11, background: runtime.meta.accent, transformOrigin: 'left', transform: `scaleX(${interpolate(frame, [10, 50], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})})`}} />
    </Shell>
  );
};

const Sources = ({runtime, scene, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Shell runtime={runtime} scene={scene} index={index} section={scene.section || '01 · SOURCES'}>
      <div style={{position: 'absolute', left: 72, top: 192, width: 720, ...reveal(frame, fps)}}>
        <div style={{fontSize: 54, lineHeight: 1.15, fontWeight: 800, letterSpacing: '-0.04em', whiteSpace: 'pre-line'}}>{scene.title}</div>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px 36px', marginTop: 52}}>
          {(scene.items || []).map((item, i) => (
            <div key={item} style={{height: 104, borderTop: `3px solid ${i === 0 ? runtime.meta.accent : BLACK}`, display: 'flex', alignItems: 'center', gap: 20, ...reveal(frame, fps, 9 + i * 6, 24)}}>
              <span style={{fontSize: 18, fontWeight: 800, color: runtime.meta.accent}}>{String(i + 1).padStart(2, '0')}</span>
              <span style={{fontSize: 37, fontWeight: 800}}>{item}</span>
            </div>
          ))}
        </div>
      </div>
      {scene.image ? <Img src={staticFile(scene.image)} style={{position: 'absolute', right: 50, top: 180, width: 990, height: 700, objectFit: 'contain', objectPosition: 'center', ...pushIn(frame, fps, 10)}} /> : null}
    </Shell>
  );
};

const List = ({runtime, scene, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Shell runtime={runtime} scene={scene} index={index} section={scene.section || '02 · DELIVERED'}>
      <div style={{position: 'absolute', left: 72, top: 190, ...reveal(frame, fps)}}>
        <div style={{fontSize: 54, fontWeight: 800, letterSpacing: '-0.04em'}}>{scene.title}</div>
      </div>
      <div style={{position: 'absolute', left: 72, right: 72, top: 320}}>
        {(scene.items || []).map((item, i) => (
          <div key={item.title || item} style={{minHeight: 152, borderTop: `${i === 0 ? 3 : 2}px solid ${i === 0 ? BLACK : LIGHT}`, display: 'grid', gridTemplateColumns: '110px 1fr 640px', gap: 24, alignItems: 'center', ...reveal(frame, fps, 9 + i * 8, 28)}}>
            <div style={{fontSize: 19, color: runtime.meta.accent, fontWeight: 800}}>{String(i + 1).padStart(2, '0')}</div>
            <div style={{fontSize: 43, fontWeight: 800}}>{item.title || item}</div>
            <div style={{fontSize: 27, color: GRAY, lineHeight: 1.45}}>{item.detail || ''}</div>
          </div>
        ))}
      </div>
    </Shell>
  );
};

const numeric = (value) => {
  if (value === null || value === undefined || String(value).trim() === '') return null;
  if (typeof value === 'number') return value;
  const parsed = Number(String(value ?? '').replace(/[^0-9.-]/g, ''));
  return Number.isFinite(parsed) ? parsed : null;
};

const Metrics = ({runtime, scene, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items = (scene.items || []).slice(0, 4);
  return (
    <Shell runtime={runtime} scene={scene} index={index} section={scene.section || '02 · METRICS'}>
      <div style={{position: 'absolute', left: 72, top: 185, right: 72, ...reveal(frame, fps)}}>
        <div style={{fontSize: 58, fontWeight: 800, letterSpacing: '-0.045em'}}>{scene.title}</div>
        {scene.subtitleLine ? <div style={{fontSize: 28, color: GRAY, marginTop: 16}}>{scene.subtitleLine}</div> : null}
      </div>
      <div style={{position: 'absolute', left: 72, right: 72, top: 360, display: 'grid', gridTemplateColumns: `repeat(${Math.max(1, items.length)}, 1fr)`, gap: 34}}>
        {items.map((item, i) => {
          const before = numeric(item.before);
          const after = numeric(item.after);
          const progress = interpolate(frame, [14 + i * 7, 52 + i * 7], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          const display = after === null ? String(item.after ?? item.value ?? '') : String(Math.round((before ?? 0) + (after - (before ?? 0)) * progress));
          return (
            <div key={`${item.label}-${i}`} style={{minHeight: 360, borderTop: `${i === 0 ? 7 : 3}px solid ${i === 0 ? runtime.meta.accent : BLACK}`, paddingTop: 24, ...reveal(frame, fps, 8 + i * 7, 26)}}>
              <div style={{fontSize: 20, color: i === 0 ? runtime.meta.accent : GRAY, fontWeight: 800, letterSpacing: '0.08em'}}>{item.label}</div>
              <div style={{display: 'flex', alignItems: 'baseline', gap: 8, marginTop: 52}}>
                <span style={{fontSize: 108, lineHeight: 0.95, fontWeight: 800, letterSpacing: '-0.07em'}}>{display}</span>
                <span style={{fontSize: 31, fontWeight: 800}}>{item.unit || ''}</span>
              </div>
              {before !== null && after !== null ? <div style={{fontSize: 24, color: GRAY, marginTop: 28}}>{item.before}{item.unit || ''} → {item.after}{item.unit || ''}</div> : null}
              {item.detail ? <div style={{fontSize: 24, lineHeight: 1.4, color: GRAY, marginTop: 20, whiteSpace: 'pre-line'}}>{item.detail}</div> : null}
            </div>
          );
        })}
      </div>
    </Shell>
  );
};

const Compare = ({runtime, scene, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const line = interpolate(frame, [18, 65], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <Shell runtime={runtime} scene={scene} index={index} section={scene.section || '03 · CHECK'}>
      <div style={{position: 'absolute', left: 72, top: 188, ...reveal(frame, fps)}}>
        <div style={{fontSize: 54, fontWeight: 800, letterSpacing: '-0.04em'}}>{scene.title}</div>
        {scene.subtitle ? <div style={{fontSize: 29, color: GRAY, marginTop: 16}}>{scene.subtitle}</div> : null}
      </div>
      <div style={{position: 'absolute', left: 72, right: 72, top: 380, display: 'grid', gridTemplateColumns: '1fr 180px 1fr', alignItems: 'center'}}>
        {[scene.left, scene.right].map((side, i) => (
          <React.Fragment key={i}>
            {i === 1 ? <div style={{height: 4, background: LIGHT, position: 'relative'}}><div style={{position: 'absolute', left: 0, top: 0, height: 4, width: `${line * 100}%`, background: runtime.meta.accent}} /><div style={{position: 'absolute', right: -3, top: -9, width: 22, height: 22, borderRadius: 20, background: runtime.meta.accent, transform: `scale(${line})`}} /></div> : null}
            <div style={{height: 310, borderTop: `6px solid ${i === 0 ? BLACK : runtime.meta.accent}`, paddingTop: 32, ...reveal(frame, fps, 8 + i * 16)}}>
              <div style={{fontSize: 21, color: i === 0 ? GRAY : runtime.meta.accent, fontWeight: 800, letterSpacing: '0.12em'}}>{side?.label || ''}</div>
              <div style={{fontSize: 49, fontWeight: 800, lineHeight: 1.2, marginTop: 25, whiteSpace: 'pre-line'}}>{side?.title || ''}</div>
              <div style={{fontSize: 26, color: GRAY, lineHeight: 1.45, marginTop: 22, whiteSpace: 'pre-line'}}>{side?.detail || ''}</div>
            </div>
          </React.Fragment>
        ))}
      </div>
      {scene.callout ? <div style={{position: 'absolute', right: 72, bottom: 112, fontSize: 27, fontWeight: 800, color: runtime.meta.accent, ...reveal(frame, fps, 50)}}>{scene.callout}</div> : null}
    </Shell>
  );
};

const Closing = ({runtime, scene, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <Shell runtime={runtime} scene={scene} index={index} section={scene.section || 'NEXT WEEK'}>
      {scene.image ? <Img src={staticFile(scene.image)} style={{position: 'absolute', right: -30, top: 145, width: 1050, height: 740, objectFit: 'contain', ...pushIn(frame, fps, 4)}} /> : null}
      <div style={{position: 'absolute', left: 72, top: 210, width: 930, ...reveal(frame, fps, 2)}}>
        <div style={{fontSize: 26, fontWeight: 800, color: runtime.meta.accent, letterSpacing: '0.1em'}}>{scene.eyebrow || 'NEXT'}</div>
        <div style={{fontSize: scene.titleSize || 82, lineHeight: 1.08, fontWeight: 800, letterSpacing: '-0.055em', marginTop: 24, whiteSpace: 'pre-line'}}>{scene.title}</div>
        <div style={{marginTop: 42}}>
          {(scene.items || []).map((item, i) => <div key={item} style={{fontSize: 32, fontWeight: 700, marginBottom: 17, ...reveal(frame, fps, 14 + i * 7, 20)}}><span style={{color: runtime.meta.accent, marginRight: 18}}>{String(i + 1).padStart(2, '0')}</span>{item}</div>)}
        </div>
      </div>
    </Shell>
  );
};

const TYPES = {hero: Hero, sources: Sources, metrics: Metrics, list: List, compare: Compare, closing: Closing};

export const WeeklyReport = (runtime) => {
  const meta = {...runtime.meta, sceneCount: runtime.scenes.length};
  const normalized = {...runtime, meta};
  return (
    <AbsoluteFill style={{background: WHITE}}>
      {runtime.bgm ? <Audio src={staticFile(runtime.bgm)} volume={runtime.bgmVolume || 0.08} loop /> : null}
      <Series>
        {runtime.scenes.map((scene, index) => {
          const Scene = TYPES[scene.type] || List;
          return <Series.Sequence key={`${scene.type}-${index}`} durationInFrames={scene.frames}><Scene runtime={normalized} scene={scene} index={index} /></Series.Sequence>;
        })}
      </Series>
    </AbsoluteFill>
  );
};
