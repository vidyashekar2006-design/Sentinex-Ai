
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Sequence,
} from "remotion";

import { IntroScene } from "./IntroScene";
import { BurstLogoScene } from "./BurstLogoScene";

const SentineXFinal: React.FC = () => {
  return (
    <AbsoluteFill>

      {/* =====================================================
          0 – 4.5 SECONDS
          GUARDIAN → COLLISION → EARTH GROWTH → EXPLOSION
      ===================================================== */}

      <Sequence
        from={0}
        durationInFrames={135}
      >
        <IntroScene />
      </Sequence>


      {/* =====================================================
          4.5 – 7 SECONDS
          EXISTING BURST + LOGO
          
          DO NOT CHANGE THIS SCENE
      ===================================================== */}

      <Sequence
        from={135}
        durationInFrames={75}
      >
        <BurstLogoScene />
      </Sequence>

    </AbsoluteFill>
  );
};


export const RemotionRoot: React.FC = () => {
  return (
    <>

      <Composition
        id="SentineXFinal"
        component={SentineXFinal}
        durationInFrames={210}
        fps={30}
        width={1920}
        height={1080}
      />

    </>
  );
};

