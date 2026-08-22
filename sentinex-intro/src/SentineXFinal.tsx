import React from "react";
import {
  AbsoluteFill,
  Sequence,
} from "remotion";

import { HelloWorld } from "./HelloWorld";
import { DashboardScene } from "./DashboardScene";
import { EnergyBurst } from "./EnergyBurst";
import { LogoReveal } from "./LogoReveal";

export const SentineXFinal: React.FC = () => {
  return (
    <AbsoluteFill>

      {/* =========================================
          0–3.0 SEC
          GUARDIAN + EARTH
          DON'T TOUCH HELLOWORLD
      ========================================= */}

      <Sequence
        from={0}
        durationInFrames={90}
      >
        <HelloWorld />
      </Sequence>


      {/* =========================================
          3.0–4.5 SEC
          EARTH CONTINUES / GROWS
          DON'T TOUCH DASHBOARDSCENE
      ========================================= */}

      <Sequence
        from={90}
        durationInFrames={45}
      >
        <DashboardScene />
      </Sequence>


      {/* =========================================
          4.5–5.7 SEC
          ENERGY BURST
      ========================================= */}

      <Sequence
        from={135}
        durationInFrames={36}
      >
        <EnergyBurst />
      </Sequence>


      {/* =========================================
          4.5–7.0 SEC
          LOGO FADES IN DURING THE BURST
          AND REMAINS UNTIL THE END
      ========================================= */}

      <Sequence
        from={135}
        durationInFrames={75}
      >
        <LogoReveal />
      </Sequence>

    </AbsoluteFill>
  );
};