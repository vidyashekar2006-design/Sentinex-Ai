
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  staticFile,
} from "remotion";

export const BurstLogoScene: React.FC = () => {
  const frame = useCurrentFrame();

  /*
   * GLOBAL:
   * 4.5s = frame 0
   * 5.7s = frame 36
   * 7.0s = frame 75
   *
   * 4.5–5.7 → ENERGY BURST
   * 5.7–7.0 → LOGO FADES IN + GROWS
   */

  // ============================================================
  // BURST
  // ============================================================

  const burstProgress = interpolate(
    frame,
    [0, 8, 18, 28, 36, 55, 75],
    [0, 0.08, 0.3, 0.58, 0.78, 0.92, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // ENERGY CORE
  // ============================================================

  const coreScale = interpolate(
    frame,
    [0, 8, 18, 28, 36, 55, 75],
    [0.15, 0.35, 0.65, 0.9, 1.05, 1.25, 1.4],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const coreOpacity = interpolate(
    frame,
    [0, 5, 12, 22, 36, 50, 75],
    [0, 0.35, 0.7, 0.85, 0.7, 0.4, 0.18],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // BLUE FLASH
  // ============================================================

  const flashOpacity = interpolate(
    frame,
    [0, 6, 12, 20, 30, 36, 50, 75],
    [0, 0.05, 0.12, 0.18, 0.14, 0.09, 0.04, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // MAIN RING
  // ============================================================

  const ringScale = interpolate(
    frame,
    [0, 7, 15, 25, 36, 50, 75],
    [0.1, 0.3, 0.65, 1.25, 1.8, 2.5, 3.4],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const ringOpacity = interpolate(
    frame,
    [0, 6, 13, 22, 32, 45, 65, 75],
    [0, 0.45, 0.9, 0.8, 0.6, 0.35, 0.1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // SECONDARY RING
  // ============================================================

  const secondRingScale = interpolate(
    frame,
    [0, 10, 22, 38, 55, 75],
    [0.1, 0.3, 0.65, 1.15, 2, 2.8],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const secondRingOpacity = interpolate(
    frame,
    [0, 10, 20, 35, 50, 70, 75],
    [0, 0.35, 0.6, 0.5, 0.25, 0.06, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // LOGO
  //
  // 5.7s → 7.0s
  // Local frames 36 → 75
  // ============================================================

  const logoOpacity = interpolate(
    frame,
    [0, 34, 36, 42, 50, 58, 66, 75],
    [0, 0, 0.02, 0.10, 0.28, 0.50, 0.75, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const logoScale = interpolate(
    frame,
    [0, 36, 46, 56, 66, 75],
    [0.65, 0.68, 0.76, 0.86, 0.94, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const logoY = interpolate(
    frame,
    [36, 50, 65, 75],
    [18, 12, 5, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const logoGlow = interpolate(
    frame,
    [0, 36, 45, 55, 65, 75],
    [0, 0, 0.15, 0.35, 0.7, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ============================================================
  // PARTICLES
  // ============================================================

  const particles = Array.from({ length: 100 }, (_, i) => {
    const angle =
      (i / 100) * Math.PI * 2 +
      ((i * 17) % 30) * 0.01;

    const distance = 80 + ((i * 43) % 420);

    const delay = i % 8;

    const progress = interpolate(
      frame,
      [5 + delay, 40 + delay],
      [0, 1],
      {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      }
    );

    return {
      x: Math.cos(angle) * distance * progress,
      y: Math.sin(angle) * distance * progress,

      size:
        i % 12 === 0
          ? 3
          : i % 4 === 0
            ? 2
            : 1.2,

      opacity: interpolate(
        progress,
        [0, 0.08, 0.55, 1],
        [0, 1, 0.7, 0],
        {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }
      ),
    };
  });

  // ============================================================
  // ENERGY RAYS
  // ============================================================

  const rayOpacity = interpolate(
    frame,
    [0, 10, 22, 36, 55, 75],
    [0, 0.25, 0.6, 0.7, 0.35, 0.12],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const rayScale = interpolate(
    frame,
    [0, 10, 25, 40, 75],
    [0.2, 0.5, 0.85, 1, 1.15],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 50% 42%, #09243d 0%, #061522 38%, #020a13 70%, #000207 100%)",
        overflow: "hidden",
      }}
    >
      {/* ======================================================
          ATMOSPHERIC GLOW
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "42%",
          width: 1200,
          height: 800,
          transform: "translate(-50%, -50%)",
          borderRadius: "50%",
          background:
            "radial-gradient(ellipse, rgba(20,130,255,0.16), rgba(10,80,180,0.07) 45%, transparent 72%)",
          filter: "blur(80px)",
          opacity: 0.5 + burstProgress * 0.4,
          zIndex: 1,
        }}
      />

      {/* ======================================================
          ENERGY CORE
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: 520,
          height: 520,
          transform:
            `translate(-50%, -50%) scale(${coreScale})`,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(130,235,255,0.42) 0%, rgba(50,190,255,0.28) 20%, rgba(20,125,255,0.14) 45%, transparent 72%)",
          filter: "blur(20px)",
          opacity: coreOpacity,
          zIndex: 4,
        }}
      />

      {/* ======================================================
          BLUE FLASH
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 50%, rgba(150,240,255,0.35) 0%, rgba(70,200,255,0.16) 15%, rgba(30,140,255,0.06) 35%, transparent 65%)",
          opacity: flashOpacity,
          pointerEvents: "none",
          zIndex: 6,
        }}
      />

      {/* ======================================================
          MAIN ENERGY RING
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: 260,
          height: 260,
          transform:
            `translate(-50%, -50%) scale(${ringScale})`,
          borderRadius: "50%",
          border:
            "3px solid rgba(105,225,255,0.95)",
          boxShadow:
            "0 0 25px rgba(60,200,255,0.9), 0 0 60px rgba(30,150,255,0.65), inset 0 0 25px rgba(80,210,255,0.35)",
          opacity: ringOpacity,
          zIndex: 8,
        }}
      />

      {/* ======================================================
          SECOND ENERGY RING
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: 430,
          height: 430,
          transform:
            `translate(-50%, -50%) scale(${secondRingScale})`,
          borderRadius: "50%",
          border:
            "2px solid rgba(70,195,255,0.6)",
          boxShadow:
            "0 0 35px rgba(40,170,255,0.4)",
          opacity: secondRingOpacity,
          zIndex: 7,
        }}
      />

      {/* ======================================================
          ENERGY RAYS
      ====================================================== */}

      {Array.from({ length: 20 }, (_, i) => {
        const angle = (i / 20) * 360;
        const rayHeight = 400 + (i % 5) * 90;

        return (
          <div
            key={`ray-${i}`}
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: 3,
              height: rayHeight,
              transform: `
                translate(-50%, -50%)
                rotate(${angle}deg)
                scaleY(${rayScale})
              `,
              background:
                "linear-gradient(to bottom, transparent, rgba(75,210,255,0.7), transparent)",
              filter: "blur(3px)",
              opacity: rayOpacity,
              zIndex: 5,
            }}
          />
        );
      })}

      {/* ======================================================
          PARTICLES
      ====================================================== */}

      {particles.map((particle, i) => (
        <div
          key={`particle-${i}`}
          style={{
            position: "absolute",
            left: "50%",
            top: "50%",
            width: particle.size,
            height: particle.size,
            borderRadius: "50%",
            background:
              i % 10 === 0
                ? "#ffffff"
                : "#65dcff",
            transform:
              `translate(${particle.x}px, ${particle.y}px)`,
            opacity: particle.opacity,
            boxShadow:
              "0 0 8px rgba(70,210,255,0.95)",
            zIndex: 12,
          }}
        />
      ))}

      {/* ======================================================
          VIGNETTE
      ====================================================== */}

      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, transparent 42%, rgba(0,0,0,0.72) 100%)",
          pointerEvents: "none",
          zIndex: 15,
        }}
      />

      {/* ======================================================
          LOGO GLOW
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: 900,
          height: 500,
          transform:
            `translate(-50%, calc(-50% + ${logoY}px))
             scale(${logoScale})`,
          borderRadius: "50%",
          background:
            "radial-gradient(ellipse, rgba(50,195,255,0.3), rgba(20,110,255,0.12) 45%, transparent 72%)",
          filter: "blur(55px)",
          opacity: logoGlow,
          zIndex: 50,
          pointerEvents: "none",
        }}
      />

      {/* ======================================================
          ACTUAL SENTINEX AI LOGO
          
          IMPORTANT:
          Using Remotion staticFile()
      ====================================================== */}

<div
  style={{
    position: "absolute",
    left: "50%",
    top: "50%",
    width: 700,
    height: 450,

    transform:
      `translate(-50%, calc(-50% + ${logoY}px))
       scale(${logoScale})`,

    opacity: logoOpacity,

    display: "flex",
    alignItems: "center",
    justifyContent: "center",

    zIndex: 1000,

    pointerEvents: "none",
  }}
>
  <div
    style={{
      width: 560,
      maxWidth: "90%",
      maxHeight: "90%",
      borderRadius: 40,
      overflow: "hidden",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}
  >
    <img
      src={staticFile("sentinex-ai.jpeg")}
      alt="SentineX AI"
      draggable={false}
      style={{
        width: "100%",
        height: "auto",
        objectFit: "contain",
        display: "block",

        filter: `
          drop-shadow(0 0 10px rgba(120,235,255,1))
          drop-shadow(0 0 25px rgba(30,170,255,0.95))
          drop-shadow(0 0 55px rgba(15,110,255,0.8))
        `,
      }}
    />
  </div>
</div>
      {/* ======================================================
          FINAL LOGO ATMOSPHERE
      ====================================================== */}

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: 850,
          height: 450,
          transform: "translate(-50%, -50%)",
          borderRadius: "50%",
          background:
            "radial-gradient(ellipse, rgba(60,190,255,0.1), transparent 70%)",
          filter: "blur(40px)",
          opacity: logoOpacity * 0.7,
          zIndex: 900,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};

