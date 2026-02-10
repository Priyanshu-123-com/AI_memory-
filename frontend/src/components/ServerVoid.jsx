import { motion } from "framer-motion";
import { Zap, Activity, Brain, Network } from "lucide-react";

export default function ServerVoid({ activeTier }) {
    const modules = [
        {
            id: "L1_Redis_Cache",
            label: "L1 // NEURAL CACHE",
            icon: Zap,
            color: "text-neon-cyan",
            glow: "shadow-[0_0_60px_rgba(0,242,255,0.4)]",
            description: "HOT ACTIVATION CORE",
            position: "top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2"
        },
        {
            id: "L2_Episodic_Log",
            label: "L2 // EPISODIC GRID",
            icon: Activity,
            color: "text-neon-blue",
            glow: "shadow-[0_0_60px_rgba(46,124,255,0.4)]",
            description: "TEMPORAL MATRIX",
            position: "top-1/4 right-1/4 translate-x-1/2 -translate-y-1/2"
        },
        {
            id: "L3_Vector_Store",
            label: "L3 // SEMANTIC MONOLITH",
            icon: Brain,
            color: "text-neon-teal",
            glow: "shadow-[0_0_60px_rgba(0,194,203,0.4)]",
            description: "DEEP STORAGE FACILITY",
            position: "bottom-1/4 left-1/4 -translate-x-1/2 translate-y-1/2"
        },
        {
            id: "L4_Graph",
            label: "L4 // KNOWLEDGE GRAPH",
            icon: Network,
            color: "text-neon-amber",
            glow: "shadow-[0_0_60px_rgba(255,184,0,0.4)]",
            description: "RELATIONSHIP CONSTELLATION",
            position: "bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2"
        },
    ];

    return (
        <div className="absolute inset-0 -z-10 pointer-events-none overflow-hidden bg-obsidian">
            {/* Ambient Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:100px_100px]" />

            {modules.map((module) => {
                const isActive = activeTier === module.id;
                return (
                    <motion.div
                        key={module.id}
                        initial={{ scale: 1, opacity: 0.2 }}
                        animate={{
                            scale: isActive ? 1.1 : 1,
                            opacity: isActive ? 1 : 0.2,
                            filter: isActive ? "brightness(1.5)" : "brightness(0.8)"
                        }}
                        transition={{ duration: 0.6, ease: "easeInOut" }}
                        className={`absolute ${module.position} w-64 h-64 flex flex-col items-center justify-center`}
                    >
                        {/* 3D Module Container */}
                        <div className={`relative w-full h-full border border-white/5 rounded-3xl bg-black/40 backdrop-blur-sm flex flex-col items-center justify-center ${module.color} ${isActive ? module.glow : ''}`}>
                            {/* Inner Graphic */}
                            <module.icon
                                size={64}
                                strokeWidth={1}
                                className={`mb-4 opacity-80 ${isActive ? 'animate-pulse-fast' : ''}`}
                            />

                            {/* HUD Overlay */}
                            <div className="text-center space-y-1">
                                <h3 className="font-mono text-xs tracking-widest">{module.label}</h3>
                                <p className="font-mono text-[9px] text-gray-500 tracking-[0.2em]">{module.description}</p>
                            </div>

                            {/* Status Ring */}
                            {isActive && (
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    animate={{ opacity: 1, scale: 1.2 }}
                                    transition={{ repeat: Infinity, duration: 2 }}
                                    className="absolute inset-0 border border-current rounded-3xl opacity-20"
                                />
                            )}
                        </div>

                        {/* Connection Node */}
                        <div className="absolute -bottom-12 w-[1px] h-12 bg-gradient-to-b from-current to-transparent opacity-30" />
                    </motion.div>
                );
            })}

            {/* Central Hub Connection (Visual only) */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full border border-white/5 opacity-20" />
        </div>
    );
}
