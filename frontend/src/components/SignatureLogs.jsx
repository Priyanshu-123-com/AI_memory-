import { motion, AnimatePresence } from "framer-motion";
import { Clock, Database, Layers } from "lucide-react";

export default function SignatureLogs({ activeMemories, metrics, currentSubgoal }) {
    return (
        <div className="w-96 h-full glass-panel rounded-2xl p-5 flex flex-col font-mono text-xs overflow-hidden shadow-[0_0_50px_rgba(0,240,255,0.2)]">
            {/* Header */}
            <div className="flex items-center gap-2 mb-4 text-neon-teal uppercase tracking-[0.25em] border-b border-white/10 pb-3">
                <Database size={16} className="animate-pulse" />
                <span className="text-[10px] neon-glow">MEMORY OS: ACTIVE SIGNATURES</span>
            </div>

            {/* Recursive State Indicator */}
            {currentSubgoal && (
                <div className="mb-4 p-3 rounded-lg bg-neon-purple/10 border border-neon-purple/30">
                    <div className="flex items-center gap-2 mb-2">
                        <Layers size={14} className="text-neon-purple" />
                        <span className="text-[9px] text-gray-500 tracking-wider">CURRENT_SUBGOAL</span>
                    </div>
                    <p className="text-[11px] text-neon-purple neon-glow">
                        {currentSubgoal}
                    </p>
                </div>
            )}

            {/* Latency Pulse */}
            <div className="mb-4 p-3 rounded-lg bg-black/60 border border-white/10">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-[9px] text-gray-500 tracking-widest">RETRIEVAL_LATENCY</span>
                    <div className="flex items-center gap-1.5 text-neon-green">
                        <Clock size={11} />
                        <span className="text-[12px] font-bold neon-glow">
                            {metrics?.latency_ms?.toFixed(2) || "0.00"}ms
                        </span>
                    </div>
                </div>
                <div className="w-full bg-gray-900 h-1 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-neon-green shadow-[0_0_10px_rgba(10,255,0,0.8)]"
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min((metrics?.latency_ms || 0) / 5, 100)}%` }}
                        transition={{ duration: 0.3 }}
                    />
                </div>
                <p className="text-[8px] text-gray-600 mt-1 tracking-wide">
                    O(1) CONSTANT → FLAT AT TURN 1,000
                </p>
            </div>

            {/* Signature Cards */}
            <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                <AnimatePresence>
                    {active Memories && activeMemories.length > 0 ? (
            activeMemories.map((mem, idx) => (
                    <motion.div
                        key={mem.id}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ delay: idx * 0.08 }}
                        className="bg-black/70 border border-neon-teal/20 rounded-lg p-3 hover:border-neon-teal/50 transition-all"
                    >
                        <pre className="text-[10px] leading-relaxed text-gray-300 overflow-x-auto">
                            {`{
  "sig_id": "${mem.id.substring(0, 12).toUpperCase()}",
  "origin": "Turn ${idx + 1}",
  "layer": "${mem.tier || 'L3'}_SEMANTIC",
  "retrieval": "O(1)_BINARY_SEARCH",
  "score": ${(mem.score * 100).toFixed(1)}%
}`}
                        </pre>
                    </motion.div>
                    ))
                    ) : (
                    <div className="text-center text-gray-700 mt-16">
                        <Database size={32} className="mx-auto mb-3 opacity-30" />
                        <p className="text-[10px] tracking-wider">NO_ACTIVE_SIGNATURES</p>
                    </div>
          )}
                </AnimatePresence>
            </div>
        </div>
    );
}
