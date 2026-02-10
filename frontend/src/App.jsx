import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import GlassChat from "./components/GlassChat";
import ServerVoid from "./components/ServerVoid";
import InternalEngine from "./components/InternalEngine";

export default function App() {
    const [activeMemories, setActiveMemories] = useState([]);
    const [metrics, setMetrics] = useState({ latency_ms: 0, cache_hit: false });
    const [activeTier, setActiveTier] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [particles, setParticles] = useState([]);

    // Shatter Animation Logic
    const handleShatter = (text) => {
        // Generate particles
        const newParticles = Array.from({ length: 8 }).map((_, i) => ({
            id: Math.random(),
            xStart: 50, // Center (vw)
            yStart: 80, // Bottom (vh)
            xEnd: 50 + (Math.random() * 40 - 20), // Target specific nodes ideally, random for now
            yEnd: 30 + (Math.random() * 20 - 10),
            delay: i * 0.05
        }));
        setParticles(newParticles);

        setTimeout(() => setParticles([]), 2000);
    };

    const handleMessageSent = (data) => {
        if (typeof data === "string") {
            setIsProcessing(true);
            setActiveTier("L1_Redis_Cache"); // Pulse L1 on input
            return;
        }

        setIsProcessing(false);
        setActiveMemories(data.active_memories || []);
        setMetrics({
            latency_ms: data.latency_ms || 0,
            cache_hit: data.cache_hit
        });

        // Tier Activation Visualization
        if (data.cache_hit) {
            setActiveTier("L1_Redis_Cache");
        } else if (data.active_memories?.length > 0) {
            const primary = data.active_memories[0].tier;
            if (primary === "L1") setActiveTier("L1_Redis_Cache");
            else if (primary === "L2") setActiveTier("L2_Episodic_Log");
            else if (primary === "L3") setActiveTier("L3_Vector_Store");
            else setActiveTier("L4_Graph");
        } else {
            setActiveTier("L2_Episodic_Log");
        }

        setTimeout(() => setActiveTier(null), 2500);
    };

    return (
        <div className="relative w-screen h-screen overflow-hidden flex items-center justify-center bg-[#050505] text-white">
            {/* Background Layer */}
            <ServerVoid activeTier={activeTier} />

            {/* Shatter Particles Layer */}
            <AnimatePresence>
                {particles.map((p) => (
                    <motion.div
                        key={p.id}
                        initial={{ x: `${p.xStart}vw`, y: `${p.yStart}vh`, opacity: 1, scale: 1 }}
                        animate={{ x: `${p.xEnd}vw`, y: `${p.yEnd}vh`, opacity: 0, scale: 0 }}
                        transition={{ duration: 1.2, ease: "anticipate", delay: p.delay }}
                        className="fixed z-10 w-2 h-2 bg-neon-cyan rounded-full shadow-[0_0_10px_#00F2FF]"
                    />
                ))}
            </AnimatePresence>

            {/* Interface Layer */}
            <div className="flex items-center justify-center w-full max-w-[1400px] gap-8 pointer-events-none">
                {/* Chat - Pointer Events enabled internally */}
                <div className="pointer-events-auto flex-1 flex justify-center">
                    <GlassChat
                        onMessageSent={handleMessageSent}
                        isProcessing={isProcessing}
                        onShatter={handleShatter}
                    />
                </div>

                {/* Sidebar - Pointer Events enabled internally */}
                <div className="pointer-events-auto">
                    <InternalEngine activeMemories={activeMemories} metrics={metrics} />
                </div>
            </div>
        </div>
    );
}
