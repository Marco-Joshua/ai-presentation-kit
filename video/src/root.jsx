import React from 'react';
import {Composition} from 'remotion';
import {WeeklyReport} from './weekly-report.jsx';

const fallback = {
  fps: 30,
  totalFrames: 900,
  meta: {brand: 'WEEKLY REPORT', period: '', accent: '#245BFF'},
  scenes: [{type: 'hero', frames: 900, title: '주간보고', subtitle: '자료를 먼저 생성해 주세요.'}],
};

export const Root = () => (
  <Composition
    id="WeeklyReport"
    component={WeeklyReport}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={fallback.totalFrames}
    defaultProps={fallback}
    calculateMetadata={({props}) => ({
      durationInFrames: Math.max(1, props.totalFrames || fallback.totalFrames),
      fps: props.fps || 30,
    })}
  />
);
