
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // ============================================================
  // EXACT TIMING
  // ============================================================

  const IMPACT = Math.round(2.15 * fps);
  const IMPACT_END = Math.round(2.35 * fps);

  const EARTH_GROW = Math.round(3.0 * fps);

  // EARTH BURSTS AT 4.30s
  const EXPLOSION = Math.round(4.3 * fps);

  // PARTICLES POP AT 4.40s
  const PARTICLE_POP = Math.round(4.4 * fps);

  // ============================================================
  // EARTH INITIAL POSITION
  //
  // Earth is half visible from the TOP from frame 0.
  // ============================================================

  const EARTH_INITIAL_Y = 0;

  // ============================================================
  // BACKGROUND
  // ============================================================

  const backgroundGlow = interpolate(
    frame,
    [
      0,
      IMPACT,
      EARTH_GROW,
      EXPLOSION,
    ],
    [0.22, 0.30, 0.42, 0.62],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // EARTH OPACITY
  //
  // Earth remains visible from frame 0 until 4.30s.
  // ============================================================

  const earthOpacity = interpolate(
    frame,
    [
      0,
      EXPLOSION - 3,
      EXPLOSION,
      PARTICLE_POP + 6,
    ],
    [
      1,
      1,
      0,
      0,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // EARTH POSITION
  //
  // 0 → 3s:
  // Earth stays at the top.
  //
  // 3s onward:
  // Earth moves toward center.
  // ============================================================

  const earthY = interpolate(
    frame,
    [
      0,
      IMPACT,
      IMPACT_END,
      EARTH_GROW,
      Math.round(3.35 * fps),
      Math.round(3.7 * fps),
      Math.round(4.0 * fps),
      EXPLOSION,
    ],
    [
      EARTH_INITIAL_Y,
      EARTH_INITIAL_Y,
      EARTH_INITIAL_Y,
      height * 0.08,
      height * 0.24,
      height * 0.35,
      height * 0.44,
      height * 0.50,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // EARTH SCALE
  //
  // Earth remains stable until 3 seconds.
  // Then it enlarges.
  // ============================================================

  const earthScale = interpolate(
    frame,
    [
      0,
      IMPACT,
      IMPACT_END,
      EARTH_GROW,
      Math.round(3.3 * fps),
      Math.round(3.65 * fps),
      Math.round(4.0 * fps),
      EXPLOSION,
    ],
    [
      0.58,
      0.58,
      0.58,
      0.62,
      0.78,
      1.02,
      1.32,
      1.58,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // EARTH ROTATION
  // ============================================================

  const earthRotation = interpolate(
    frame,
    [
      0,
      IMPACT,
      EARTH_GROW,
      EXPLOSION,
    ],
    [0, 1, 5, 15],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // IMPACT SHAKE
  // ============================================================

  const shakeAmount = interpolate(
    frame,
    [
      IMPACT,
      IMPACT + Math.round(0.035 * fps),
      IMPACT + Math.round(0.09 * fps),
      IMPACT_END,
    ],
    [0, 13, 5, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const shakeX =
    Math.sin(frame * 4.5) * shakeAmount;

  const shakeY =
    Math.cos(frame * 5.1) *
    shakeAmount *
    0.5;

  // ============================================================
  // GUARDIAN
  //
  // STRAIGHT UPWARD MOVEMENT
  // ============================================================

  const guardianStartY =
    height + 180;

  const guardianImpactY =
    EARTH_INITIAL_Y +
    300 * 0.58 +
    65;

  const guardianY = interpolate(
    frame,
    [
      0,
      Math.round(0.35 * fps),
      Math.round(0.8 * fps),
      Math.round(1.2 * fps),
      Math.round(1.55 * fps),
      Math.round(1.85 * fps),
      IMPACT,
      IMPACT_END,
      Math.round(2.55 * fps),
      Math.round(2.9 * fps),
    ],
    [
      guardianStartY,
      height * 0.88,
      height * 0.70,
      height * 0.51,
      height * 0.34,
      height * 0.17,
      guardianImpactY,
      guardianImpactY,
      guardianImpactY,
      guardianImpactY,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // GUARDIAN SCALE
  // ============================================================

  const guardianScale = interpolate(
    frame,
    [
      0,
      Math.round(0.8 * fps),
      Math.round(1.5 * fps),
      IMPACT,
      IMPACT_END,
    ],
    [
      0.68,
      0.72,
      0.82,
      0.94,
      0.94,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // GUARDIAN OPACITY
  //
  // Guardian pauses for 0.2s after impact.
  // ============================================================

  const guardianOpacity = interpolate(
    frame,
    [
      0,
      Math.round(0.12 * fps),
      IMPACT,
      IMPACT_END,
      Math.round(2.55 * fps),
      Math.round(2.9 * fps),
    ],
    [
      0,
      1,
      1,
      1,
      0.45,
      0,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // GUARDIAN ENERGY TRAIL
  // ============================================================

  const trailOpacity = interpolate(
    frame,
    [
      0,
      Math.round(0.3 * fps),
      IMPACT,
      IMPACT_END,
      Math.round(2.55 * fps),
    ],
    [
      0,
      0.65,
      0.85,
      0.35,
      0,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // COLLISION PROGRESS
  // ============================================================

  const collisionProgress = interpolate(
    frame,
    [
      IMPACT,
      IMPACT + 1,
      IMPACT + 4,
      IMPACT + 10,
      IMPACT + 20,
    ],
    [
      0,
      0.15,
      0.5,
      0.85,
      1,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // COLLISION OPACITY
  // ============================================================

  const collisionOpacity = interpolate(
    frame,
    [
      IMPACT,
      IMPACT + 3,
      IMPACT + 10,
      IMPACT + 22,
    ],
    [
      0,
      1,
      0.5,
      0,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // COLLISION RING
  // ============================================================

  const collisionRingScale = interpolate(
    frame,
    [
      IMPACT,
      IMPACT + 4,
      IMPACT + 12,
      IMPACT + 24,
    ],
    [
      0.08,
      0.45,
      1.0,
      1.75,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // COLLISION FLASH
  // ============================================================

  const collisionFlash = interpolate(
    frame,
    [
      IMPACT,
      IMPACT + 2,
      IMPACT + 6,
      IMPACT + 18,
    ],
    [
      0,
      1,
      0.35,
      0,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // COLLISION PARTICLES
  // ============================================================

  const collisionParticles = Array.from(
    { length: 70 },
    (_, i) => {
      const angle =
        (i / 70) * Math.PI * 2 +
        ((i * 17) % 30) * 0.01;

      const distance =
        50 + ((i * 31) % 250);

      const delay =
        (i % 7) * 0.7;

      const progress = interpolate(
        frame,
        [
          IMPACT + delay,
          IMPACT + 14 + delay,
        ],
        [
          0,
          1,
        ],
        {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }
      );

      return {
        x:
          Math.cos(angle) *
          distance *
          progress,

        y:
          Math.sin(angle) *
          distance *
          progress,

        size:
          i % 7 === 0
            ? 4
            : i % 3 === 0
            ? 2.5
            : 1.5,

        opacity: interpolate(
          progress,
          [
            0,
            0.1,
            0.7,
            1,
          ],
          [
            0,
            1,
            0.6,
            0,
          ],
          {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }
        ),
      };
    }
  );

  // ============================================================
  // EARTH EXPLOSION FLASH
  //
  // EARTH DISAPPEARS AT 4.30s.
  // ============================================================

  const explosionFlash = interpolate(
    frame,
    [
      EXPLOSION - 2,
      EXPLOSION,
      EXPLOSION + 2,
      PARTICLE_POP + 5,
    ],
    [
      0,
      0.95,
      0.45,
      0,
    ],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // EARTH SHATTER PARTICLES
  //
  // IMPORTANT:
  // They remain hidden until EXACTLY 4.40s.
  //
  // 4.40s = particle pop.
  // ============================================================

  const earthParticles = Array.from(
    { length: 280 },
    (_, i) => {
      const angle =
        (i / 280) * Math.PI * 2 +
        ((i * 17) % 30) * 0.01;

      const distance =
        80 + ((i * 43) % 560);

      const particleDelay =
        (i % 12) * 0.65;

      const particleProgress = interpolate(
        frame,
        [
          PARTICLE_POP + particleDelay,
          PARTICLE_POP + 2 + particleDelay,
          PARTICLE_POP + 10 + particleDelay,
          PARTICLE_POP + 22 + particleDelay,
        ],
        [
          0,
          0.18,
          0.65,
          1,
        ],
        {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }
      );

      return {
        x:
          Math.cos(angle) *
          distance *
          particleProgress,

        y:
          Math.sin(angle) *
          distance *
          particleProgress,

        size:
          i % 15 === 0
            ? 4
            : i % 5 === 0
            ? 2.5
            : 1.4,

        opacity: interpolate(
          particleProgress,
          [
            0,
            0.08,
            0.55,
            1,
          ],
          [
            0,
            1,
            0.8,
            0,
          ],
          {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }
        ),
      };
    }
  );

  // ============================================================
  // PARTICLE ORIGIN
  // ============================================================

  const particleOriginX =
    width / 2 + shakeX;

  const particleOriginY =
    earthY + shakeY;

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 50% 42%, #09243d 0%, #061522 38%, #020a13 70%, #000207 100%)",
        overflow: "hidden",
      }}
    >

      {/* ========================================================
          BACKGROUND ATMOSPHERE
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "42%",
          width: 1200,
          height: 850,
          transform:
            "translate(-50%, -50%)",
          borderRadius: "50%",
          background:
            "radial-gradient(ellipse, rgba(20,130,255,0.16), rgba(10,80,180,0.06) 45%, transparent 72%)",
          filter: "blur(80px)",
          opacity: backgroundGlow,
          zIndex: 1,
        }}
      />

      {/* ========================================================
          STARS
      ======================================================== */}

      {Array.from(
        { length: 100 },
        (_, i) => (
          <div
            key={`star-${i}`}
            style={{
              position: "absolute",
              left: `${(i * 73) % 100}%`,
              top: `${(i * 47) % 100}%`,
              width:
                i % 8 === 0 ? 2 : 1,
              height:
                i % 8 === 0 ? 2 : 1,
              borderRadius: "50%",
              background: "#c9f4ff",
              opacity:
                0.15 +
                ((i * 11) % 35) / 100,
            }}
          />
        )
      )}

      {/* ========================================================
          EARTH OUTER GLOW
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left:
            width / 2 + shakeX,
          top:
            earthY + shakeY,
          width: 670,
          height: 670,
          transform:
            `translate(-50%, -50%) scale(${earthScale})`,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, transparent 55%, rgba(60,205,255,0.14) 70%, transparent 76%)",
          filter: "blur(15px)",
          opacity: earthOpacity,
          zIndex: 7,
          pointerEvents: "none",
        }}
      />

      {/* ========================================================
          EARTH
          HALF VISIBLE FROM TOP FROM FRAME 0
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left:
            width / 2 + shakeX,
          top:
            earthY + shakeY,
          width: 600,
          height: 600,
          transform:
            `translate(-50%, -50%) scale(${earthScale}) rotate(${earthRotation}deg)`,
          opacity: earthOpacity,
          zIndex: 10,
          borderRadius: "50%",
          overflow: "hidden",
          background:
            "radial-gradient(circle at 30% 25%, #668d96 0%, #3b6876 32%, #19495a 62%, #06131e 100%)",
          boxShadow:
            "inset -130px -100px 170px rgba(0,0,0,0.82), inset 35px 20px 70px rgba(130,220,235,0.10), 0 0 25px rgba(70,210,255,0.25)",
        }}
      >

        {/* CONTINENT 1 */}

        <div
          style={{
            position: "absolute",
            left: 55,
            top: 80,
            width: 245,
            height: 155,
            borderRadius: "50%",
            background:
              "radial-gradient(ellipse, #536d4c, #334b38 55%, transparent 80%)",
            filter: "blur(7px)",
            transform:
              "rotate(-15deg)",
          }}
        />

        {/* CONTINENT 2 */}

        <div
          style={{
            position: "absolute",
            left: 275,
            top: 235,
            width: 150,
            height: 230,
            borderRadius: "50%",
            background:
              "radial-gradient(ellipse, #4e6848, #304934 55%, transparent 80%)",
            filter: "blur(7px)",
          }}
        />

        {/* CONTINENT 3 */}

        <div
          style={{
            position: "absolute",
            left: 350,
            top: 90,
            width: 170,
            height: 135,
            borderRadius: "50%",
            background:
              "radial-gradient(ellipse, #536c49, #40583d 55%, transparent 80%)",
            filter: "blur(7px)",
          }}
        />

        {/* CLOUDS */}

        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: "50%",
            background: `
              radial-gradient(
                ellipse at 20% 35%,
                rgba(255,255,255,0.14),
                transparent 20%
              ),
              radial-gradient(
                ellipse at 52% 20%,
                rgba(255,255,255,0.10),
                transparent 22%
              ),
              radial-gradient(
                ellipse at 73% 40%,
                rgba(255,255,255,0.12),
                transparent 20%
              )
            `,
            filter: "blur(10px)",
          }}
        />

        {/* NIGHT SIDE */}

        <div
          style={{
            position: "absolute",
            inset: 0,
            borderRadius: "50%",
            background:
              "linear-gradient(110deg, transparent 10%, transparent 42%, rgba(0,0,0,0.12) 52%, rgba(0,0,0,0.55) 78%, rgba(0,0,0,0.92) 100%)",
          }}
        />

        {/* ATMOSPHERIC RIM */}

        <div
          style={{
            position: "absolute",
            inset: 1,
            borderRadius: "50%",
            border:
              "2px solid rgba(110,225,255,0.30)",
          }}
        />

      </div>

      {/* ========================================================
          GUARDIAN ENERGY TRAIL
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left:
            width / 2,
          top:
            guardianY + 140,
          width: 90,
          height: 850,
          transform:
            "translateX(-50%)",
          background:
            "linear-gradient(to bottom, transparent, rgba(70,210,255,0.46), rgba(20,120,255,0.08), transparent)",
          filter:
            "blur(22px)",
          opacity:
            trailOpacity,
          zIndex: 20,
          pointerEvents: "none",
        }}
      />

      {/* ========================================================
          GUARDIAN
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left:
            width / 2,
          top:
            guardianY,
          width: 150,
          height: 370,
          transform:
            `translate(-50%, -50%) scale(${guardianScale})`,
          opacity:
            guardianOpacity,
          zIndex: 30,
          filter:
            "drop-shadow(0 0 8px rgba(110,235,255,1)) drop-shadow(0 0 25px rgba(30,150,255,0.9))",
        }}
      >

        {/* HEAD */}

        <div
          style={{
            position: "absolute",
            left: 53,
            top: 0,
            width: 44,
            height: 48,
            borderRadius: "50%",
            background:
              "radial-gradient(circle at 35% 25%, #d0f8ff, #4bc9ed 48%, #07527a 80%)",
          }}
        />

        {/* BODY */}

        <div
          style={{
            position: "absolute",
            left: 38,
            top: 60,
            width: 74,
            height: 135,
            borderRadius:
              "30px 30px 22px 22px",
            background:
              "linear-gradient(105deg, #06466b, #60d9f7 40%, #086b98 65%, #032d4a)",
          }}
        />

        {/* LEFT ARM */}

        <div
          style={{
            position: "absolute",
            left: 17,
            top: 68,
            width: 25,
            height: 125,
            borderRadius: 18,
            background:
              "linear-gradient(90deg, #043653, #55cff1, #07527a)",
          }}
        />

        {/* RIGHT ARM */}

        <div
          style={{
            position: "absolute",
            right: 17,
            top: 68,
            width: 25,
            height: 125,
            borderRadius: 18,
            background:
              "linear-gradient(90deg, #07527a, #55cff1, #043653)",
          }}
        />

        {/* LEFT LEG */}

        <div
          style={{
            position: "absolute",
            left: 40,
            top: 188,
            width: 30,
            height: 155,
            borderRadius:
              "16px 16px 10px 10px",
            background:
              "linear-gradient(90deg, #043653, #43c3e9 42%, #06466a)",
          }}
        />

        {/* RIGHT LEG */}

        <div
          style={{
            position: "absolute",
            right: 40,
            top: 188,
            width: 30,
            height: 155,
            borderRadius:
              "16px 16px 10px 10px",
            background:
              "linear-gradient(90deg, #06466a, #43c3e9 58%, #043653)",
          }}
        />

      </div>

      {/* ========================================================
          COLLISION FLASH
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left:
            width / 2,
          top:
            EARTH_INITIAL_Y +
            300 * 0.58,
          width: 550,
          height: 550,
          transform:
            "translate(-50%, -50%)",
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(220,250,255,0.95) 0%, rgba(80,215,255,0.45) 22%, rgba(30,150,255,0.12) 48%, transparent 70%)",
          filter:
            "blur(10px)",
          opacity:
            collisionFlash,
          zIndex: 40,
          pointerEvents: "none",
        }}
      />

      {/* ========================================================
          COLLISION RING
      ======================================================== */}

      <div
        style={{
          position: "absolute",
          left:
            width / 2,
          top:
            EARTH_INITIAL_Y +
            300 * 0.58,
          width: 280,
          height: 280,
          transform:
            `translate(-50%, -50%) scale(${collisionRingScale})`,
          borderRadius: "50%",
          border:
            "4px solid rgba(120,230,255,0.95)",
          boxShadow:
            "0 0 30px rgba(60,210,255,0.95), 0 0 70px rgba(30,150,255,0.7)",
          opacity:
            collisionOpacity,
          zIndex: 42,
          pointerEvents: "none",
        }}
      />

      {/* ========================================================
          COLLISION RAYS
      ======================================================== */}

      {Array.from(
        { length: 24 },
        (_, i) => {
          const angle =
            (i / 24) * 360;

          const rayLength =
            260 + (i % 6) * 45;

          return (
            <div
              key={`collision-ray-${i}`}
              style={{
                position: "absolute",
                left:
                  width / 2,
                top:
                  EARTH_INITIAL_Y +
                  300 * 0.58,
                width: 3,
                height:
                  rayLength,
                transform:
                  `translate(-50%, -50%) rotate(${angle}deg) scaleY(${collisionProgress})`,
                background:
                  "linear-gradient(to bottom, transparent, rgba(90,225,255,0.95), transparent)",
                filter:
                  "blur(2px)",
                opacity:
                  collisionOpacity,
                zIndex: 41,
                pointerEvents: "none",
              }}
            />
          );
        }
      )}

      {/* ========================================================
          COLLISION PARTICLES
      ======================================================== */}

      {collisionParticles.map(
        (particle, i) => (
          <div
            key={`collision-particle-${i}`}
            style={{
              position: "absolute",
              left:
                width / 2,
              top:
                EARTH_INITIAL_Y +
                300 * 0.58,
              width:
                particle.size,
              height:
                particle.size,
              borderRadius:
                "50%",
              background:
                i % 5 === 0
                  ? "#ffffff"
                  : "#65dcff",
              transform:
                `translate(${particle.x}px, ${particle.y}px)`,
              opacity:
                particle.opacity,
              boxShadow:
                "0 0 8px rgba(70,215,255,0.95)",
              zIndex: 45,
              pointerEvents: "none",
            }}
          />
        )
      )}

      {/* ========================================================
          EARTH SHATTER PARTICLES
          POP STARTS AT 4.40s
      ======================================================== */}

      {earthParticles.map(
        (particle, i) => (
          <div
            key={`earth-particle-${i}`}
            style={{
              position: "absolute",

              left:
                particleOriginX,

              top:
                particleOriginY,

              width:
                particle.size,

              height:
                particle.size,

              borderRadius:
                "50%",

              background:
                i % 10 === 0
                  ? "#ffffff"
                  : "#65dcff",

              transform:
                `translate(${particle.x}px, ${particle.y}px)`,

              opacity:
                frame >= PARTICLE_POP
                  ? particle.opacity
                  : 0,

              boxShadow:
                "0 0 8px rgba(70,215,255,0.95)",

              zIndex: 60,

              pointerEvents: "none",
            }}
          />
        )
      )}

      {/* ========================================================
          EXPLOSION FLASH
      ======================================================== */}

      <div
        style={{
          position: "absolute",

          inset: 0,

          background:
            "radial-gradient(circle at 50% 50%, rgba(180,245,255,0.8) 0%, rgba(70,200,255,0.3) 18%, transparent 58%)",

          opacity:
            explosionFlash,

          zIndex: 70,

          pointerEvents: "none",
        }}
      />

      {/* ========================================================
          VIGNETTE
      ======================================================== */}

      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 42%, rgba(0,0,0,0.72) 100%)",

          pointerEvents: "none",

          zIndex: 80,
        }}
      />

    </AbsoluteFill>
  );
};
