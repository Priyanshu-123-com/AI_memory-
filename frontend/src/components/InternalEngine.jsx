import { motion, AnimatePresence } from "framer-motion";
import { Activity, Clock, Database, Layers, Zap } from "lucide-react";

export default function InternalEngine({ activeMemories, metrics }) {
    return (
        <div className="w-[400px] h-[80vh] glass-substrate rounded-[20px] p-6 flex flex-col font-mono relative z-20 ml-8">
            {/* Header */}
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/10">
                <h2 className="text-[11px] tracking-[0.2em] text-neon-teal flex items-center gap-2">
                    <Zap size={12} className="fill-current" />
                    INTERNAL ENGINE
                </h2>
                <span className="text-[9px] text-gray-500">OBSERVABILITY: 100%</span>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 gap-4 mb-8">
                <MetricCard
                    label="E2E LATENCY"
                    value={`${metrics?.latency_ms?.toFixed(1) || 0}ms`}
                    color="text-neon-cyan"
                    icon={Clock}
                />
                <MetricCard
                    label="CONTEXT RATIO"
                    value="1:1000"
                    color="text-neon-amber"
                    icon={Layers}
                />
            </div>

            {/* Active Signatures */}
            <div className="flex-1 overflow-hidden flex flex-col">
                <h3 className="text-[9px] text-gray-500 tracking-widest mb-4 flex items-center gap-2">
                    <Database size={10} />
                    ACTIVE MEMORY SIGNATURES
                </h3>

                <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                    <AnimatePresence>
                        {activeMemories && activeMemories.length > 0 ? (
                            activeMemories.map((mem, idx) => (
                                <motion.div
                                    key={mem.id}
                                    initial={{ x: 50, opacity: 0 }}
                                    animate={{ x: 0, opacity: 1 }}
                                    exit={{ x: -20, opacity: 0 }}
                                    transition={{ delay: idx * 0.05 }}
                                    className="bg-white/[0.02] border border-white/10 rounded-lg p-4 hover:border-gray-600 transition-colors group relative overflow-hidden"
                                >
                                    {/* Tier Indicator Line */}
                                    <div className={`absolute top-0 left-0 bottom-0 w-[2px] ${getTierColor(mem.tier)}`} />

                                    <div className="flex justify-between items-start mb-2 pl-3">
                                        <span className={`text-[10px] font-bold ${getTierTextColor(mem.tier)}`}>
                                            {mem.tier}_NODE
                                        </span>
                                        <span className="text-[9px] text-gray-600">TURN {idx + 1}</span>
                                    </div>

                                    <div className="pl-3 mb-3">
                                        <div className="text-[10px] text-gray-500 mb-1">VAR_SIGNATURE</div>
                                        <code className="text-xs text-gray-300 block truncate">
                                            {mem.id.substring(0, 16).toUpperCase()}...
                                        </code>
                                    </div>

                                    <div className="pl-3 flex justify-between items-center text-[9px] text-gray-500">
                                        <span>CONFIDENCE: {(mem.score * 100).toFixed(1)}%</span>
                                        <Activity size={10} className={getTierTextColor(mem.tier)} />
                                    </div>
                                </motion.div>
                            ))
                        ) : (
                            <div className="text-center mt-20 opacity-30">
                                <div className="w-16 h-16 border-2 border-dashed border-gray-600 rounded-full mx-auto mb-4 animate-spin-slow" />
                                <span className="text-xs tracking-widest">AWAITING_INPUT...</span>
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}

function MetricCard({ label, value, color, icon: Icon }) {
    return (
        <div className="bg-white/5 border border-white/5 rounded-xl p-3">
            <div className="flex items-center gap-2 mb-2 text-gray-500">
                <Icon size={10} />
                <span className="text-[9px] tracking-widest">{label}</span>
            </div>
            <div className={`text-xl font-mono ${color} neon-glow`}>
                {value}
            </div>
        </div>
    )
}

function getTierColor(tier) {
    switch (tier) {
        case "L1": return "bg-neon-cyan";
        case "L2": return "bg-neon-blue";
        case "L3": return "bg-neon-teal";
        default: return "bg-neon-amber";
    }
}

function getTierTextColor(tier) {
    switch (tier) {
        case "L1": return "text-neon-cyan";
        case "L2": return "text-neon-blue";
        case "L3": return "text-neon-teal";
        default: return "text-neon-amber";
    }
}
