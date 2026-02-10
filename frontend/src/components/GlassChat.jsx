import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Zap, Activity, Brain, Network, Hexagon } from "lucide-react";
import axios from "axios";

// Signature Generation Hook
function useSignatureGen(text) {
    const [signature, setSignature] = useState("");

    useEffect(() => {
        if (!text) {
            setSignature("");
            return;
        }
        // Generate pseudorandom hex signature based on text length
        const hex = Math.floor(text.length * 1337).toString(16).toUpperCase().padStart(6, '0');
        setSignature(`0x${hex}`);
    }, [text]);

    return signature;
}

export default function GlassChat({ onMessageSent, isProcessing, onShatter }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const scrollRef = useRef(null);
    const signature = useSignatureGen(input);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isProcessing) return;

        const userMsg = { role: "user", content: input, timestamp: Date.now() };
        setMessages((prev) => [...prev, userMsg]);

        // Trigger Shatter Animation
        if (onShatter) {
            onShatter(input);
        }

        const messageContent = input;
        setInput("");
        onMessageSent(messageContent);

        try {
            const res = await axios.post("http://localhost:8000/chat", { message: messageContent });

            // Retrieval Flash (Visualized by delay/animation in parent or here)
            const botMsg = { role: "assistant", content: res.data.response, timestamp: Date.now() };
            setMessages((prev) => [...prev, botMsg]);

            onMessageSent(res.data);
        } catch (e) {
            console.error(e);
            setMessages((prev) => [...prev, {
                role: "assistant",
                content: "⚠️ SYSTEM_ERROR: UPLINK_FAILED",
                timestamp: Date.now()
            }]);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "circOut" }}
            className="glass-substrate w-full max-w-3xl h-[80vh] flex flex-col rounded-[20px] relative z-20 overflow-hidden"
        >
            {/* Header: System State */}
            <div className="h-12 border-b border-white/10 flex items-center px-6 justify-between bg-white/[0.02]">
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-neon-cyan animate-pulse shadow-[0_0_8px_#00F2FF]" />
                        <span className="font-mono text-[10px] tracking-[0.2em] text-neon-cyan/80">SYSTEM_OPTIMIZED</span>
                    </div>
                    <div className="h-3 w-[1px] bg-white/10" />
                    <span className="font-mono text-[10px] tracking-widest text-gray-500">MEM_OS_v2.0</span>
                </div>
                <div className="flex gap-4 font-mono text-[10px] text-gray-500">
                    <span>CACHE: <span className="text-neon-cyan">WARM</span></span>
                    <span>UPLINK: <span className="text-neon-cyan">STABLE</span></span>
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-8 space-y-8 font-mono text-sm custom-scrollbar relative">
                <AnimatePresence>
                    {messages.map((msg, i) => (
                        <MessageBubble key={`${msg.timestamp}-${i}`} msg={msg} />
                    ))}
                    {isProcessing && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex justify-start"
                        >
                            <div className="flex items-center gap-3 px-4 py-2 rounded-full border border-neon-cyan/20 bg-neon-cyan/5">
                                <Hexagon size={14} className="text-neon-cyan animate-spin" />
                                <span className="text-[10px] tracking-widest text-neon-cyan">RETRIEVING_SIGNATURES...</span>
                            </div>
                        </motion.div>
                    )}
                    <div ref={scrollRef} />
                </AnimatePresence>
            </div>

            {/* Input Area: Glass Sheet Interaction */}
            <div className="p-6 relative">
                {/* Live Signature Projection */}
                <AnimatePresence>
                    {input && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="absolute -top-4 left-8 text-[10px] font-mono text-neon-cyan/60 tracking-widest flex items-center gap-2"
                        >
                            <Activity size={10} />
                            SIG_GEN: {signature}
                        </motion.div>
                    )}
                </AnimatePresence>

                <div className="relative flex items-center group">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        placeholder="Initialize sequence..."
                        className="w-full bg-black/40 text-gray-200 font-mono text-sm p-4 pl-6 pr-14 rounded-xl border border-white/10 focus:outline-none focus:border-neon-cyan/50 focus:shadow-[0_0_30px_rgba(0,242,255,0.1)] placeholder-white/20 transition-all backdrop-blur-md"
                        disabled={isProcessing}
                    />
                    <button
                        onClick={handleSend}
                        disabled={isProcessing}
                        className="absolute right-2 p-2.5 rounded-lg text-gray-400 hover:text-neon-cyan hover:bg-white/5 transition-all disabled:opacity-30"
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </motion.div>
    );
}

function MessageBubble({ msg }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20, filter: "blur(10px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.5 }}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
            <div className={`max-w-[80%] p-5 rounded-md backdrop-blur-md border ${msg.role === "user"
                    ? "bg-neon-cyan/5 border-neon-cyan/20 text-neon-cyan/90 shadow-[0_0_20px_rgba(0,242,255,0.05)]"
                    : "bg-white/[0.02] border-white/5 text-gray-300 shadow-[0_4px_20px_rgba(0,0,0,0.2)]"
                }`}>
                <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                {/* Metadata Footer */}
                <div className="mt-3 pt-3 border-t border-white/5 flex gap-3 text-[9px] text-gray-600 tracking-wider">
                    <span>TS: {msg.timestamp}</span>
                    <span>SIG: {msg.role === "user" ? "INPUT" : "GENERATED"}</span>
                </div>
            </div>
        </motion.div>
    );
}
