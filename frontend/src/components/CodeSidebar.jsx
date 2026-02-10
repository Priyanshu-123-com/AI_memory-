import { motion, AnimatePresence } from "framer-motion";
import { Activity, Database, GitBranch, Zap, Cpu } from "lucide-react";

export default function CodeSidebar({ activeMemories, metrics }) {
    const cacheHit = metrics?.cache_hit || false;

    return (
        <div className="w-96 h-[75vh] glass-panel rounded-2xl p-5 flex flex-col font-mono text-xs overflow-hidden shadow-[0_0_50px_rgba(255,255,255,0.1)]">
            {/* Header */}
            <div className="flex items-center gap-2 mb-4 text-gray-400 uppercase tracking-[0.2em] border-b border-white/10 pb-3">
                <GitBranch size={16} />
                <span className="text-[11px]">Live Memory Stack</span>
            </div>

            {/* Neural State Indicator */}
            <div className={`mb-4 p-3 rounded-lg border transition-all ${cacheHit
                    ? "bg-neon-green/10 border-neon-green/40 shadow-[0_0_20px_rgba(10,255,0,0.3)]"
                    : "bg-white/5 border-white/10"
                }`}>
                <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] text-gray-500 tracking-wider">NEURAL STATE</span>
                    {cacheHit && <Zap size={14} className="text-neon-green animate-pulse" />}
                </div>
                <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${cacheHit ? "bg-neon-green animate-ping" : "bg-gray-700"}`} />
                    <span className={`text-[11px] tracking-wide ${cacheHit ? "text-neon-green neon-text" : "text-gray-600"}`}>
                        {cacheHit ? "L1_CACHE_HIT_ACTIVE" : "SEMANTIC_SEARCH"}
                    </span>
                </div>
            </div>

            {/* Memory Cards */}
            <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                <AnimatePresence>
                    {activeMemories && activeMemories.length > 0 ? (
                        activeMemories.map((mem, idx) => (
                            <motion.div
                                key={mem.id}
                                initial={{ opacity: 0, x: 20, scale: 0.95 }}
                                animate={{ opacity: 1, x: 0, scale: 1 }}
                                exit={{ opacity: 0, x: -20, scale: 0.95 }}
                                transition={{ delay: idx * 0.1 }}
                                className="bg-black/50 border border-white/10 p-3 rounded-lg hover:border-electric-teal/50 transition-all group cursor-pointer hover:shadow-[0_0_15px_rgba(0,240,255,0.2)]"
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-electric-teal font-bold tracking-wider text-[11px]">
                                        {mem.id.substring(0, 10).toUpperCase()}
                                    </span>
                                    <span className={`text-[9px] px-2 py-0.5 rounded border ${getTierStyle(mem.tier)}`}>
                                        {mem.tier}
                                    </span>
                                </div>
                                <p className="text-gray-400 text-[11px] leading-relaxed line-clamp-2 group-hover:text-gray-200 transition-colors mb-2">
                                    {mem.content}
                                </p>
                                <div className="flex justify-between items-center pt-2 border-t border-white/5">
                                    <span className="text-[9px] text-neon-green tracking-wide">
                                        CONF: {(mem.score * 100).toFixed(0)}%
                                    </span>
                                    <div className="w-16 bg-gray-800 h-1 rounded-full overflow-hidden">
                                        <motion.div
                                            className="h-full bg-neon-green shadow-[0_0_8px_rgba(10,255,0,0.8)]"
                                            initial={{ width: 0 }}
                                            animate={{ width: `${mem.score * 100}%` }}
                                            transition={{ duration: 0.5, delay: idx * 0.1 }}
                                        />
                                    </div>
                                </div>
                            </motion.div>
                        ))
                    ) : (
                        <div className="text-center text-gray-600 mt-16">
                            <Database size={32} className="mx-auto mb-3 opacity-30" />
                            <p className="text-[11px] tracking-wider">NO_DETECTED_CONTEXT</p>
                            <p className="text-[9px] text-gray-700 mt-1">Awaiting neural input...</p>
                        </div>
                    )}
                </AnimatePresence>
            </div>

            {/* Dashboard Stats */}
            <div className="mt-4 pt-4 border-t border-white/10 space-y-3">
                {/* Latency */}
                <div>
                    <div className="flex justify-between items-center mb-1.5">
                        <span className="text-gray-500 text-[9px] tracking-widest">LATENCY</span>
                        <div className="flex items-center gap-1.5 text-electric-teal">
                            <Activity size={11} />
                            <span className="text-[11px] font-bold">{metrics?.latency_ms?.toFixed(1) || 0}ms</span>
                        </div>
                    </div>
                    <div className="w-full bg-gray-900 h-1.5 rounded-full overflow-hidden">
                        <motion.div
                            className="h-full bg-gradient-to-r from-neon-green via-electric-teal to-amber-decay shadow-[0_0_10px_currentColor]"
                            initial={{ width: 0 }}
                            animate={{ width: `${Math.min((metrics?.latency_ms || 0) / 10, 100)}%` }}
                            transition={{ duration: 0.5 }}
                        />
                    </div>
                </div>

                {/* Token Efficiency (Mock) */}
                <div>
                    <div className="flex justify-between items-center mb-1.5">
                        <span className="text-gray-500 text-[9px] tracking-widest">TOKEN_EFFICIENCY</span>
                        <div className="flex items-center gap-1.5 text-neon-green">
                            <Cpu size={11} />
                            <span className="text-[11px] font-bold">87%</span>
                        </div>
                    </div>
                    <div className="w-full bg-gray-900 h-1.5 rounded-full overflow-hidden">
                        <div className="h-full w-[87%] bg-neon-green shadow-[0_0_10px_rgba(10,255,0,0.8)]" />
                    </div>
                </div>
            </div>
        </div>
    );
}

function getTierStyle(tier) {
    switch (tier) {
        case "L1": return "bg-neon-green/20 border-neon-green/50 text-neon-green";
        case "L2": return "bg-electric-teal/20 border-electric-teal/50 text-electric-teal";
        case "L3": return "bg-purple-500/20 border-purple-500/50 text-purple-400";
        case "L4": return "bg-amber-decay/20 border-amber-decay/50 text-amber-decay";
        default: return "bg-white/10 border-white/20 text-gray-400";
    }
}
