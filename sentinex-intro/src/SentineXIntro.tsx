import React from "react";
import {
  AbsoluteFill,
  Sequence,
} from "remotion";

import { HelloWorld } from "./HelloWorld";
import { DashboardScene } from "./DashboardScene";

export const SentineXIntro: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        background: "#000207",
        overflow: "hidden",
      }}
    >
      {/* =========================================
          0–3 SECONDS
          YOUR EXISTING PERFECT INTRO
          ========================================= */}

      <Sequence
        from={0}
        durationInFrames={90}
      >
        <HelloWorld />
      </Sequence>

      {/* =========================================
          3–4.5 SECONDS
          EARTH + IMPACT
          ========================================= */}

      <Sequence
        from={90}
        durationInFrames={45}
      >
        <DashboardScene />
      </Sequence>

      {/* =========================================
          TEMPORARY
          4.5–7 SECONDS
          
          We will add:
          EnergyBurstScene
          LogoRevealScene
          
          after DashboardScene is confirmed.
          ========================================= */}
    </AbsoluteFill>
  );
};