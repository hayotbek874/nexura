import { useState, useEffect, useRef } from 'react';
import './styles.css';
import { securityApi } from './api/securityApi';

const Graph = ({ count = 24, color = 'var(--cyan)' }) => {
  const [bars, setBars] = useState(Array.from({ length: count }, () => Math.random() * 100));

  useEffect(() => {
    const interval = setInterval(() => {
      setBars(prev => prev.map(() => Math.random() * 100));
    }, 400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="graph-container">
      {bars.map((height, i) => (
        <div
          key={i}
          className="graph-bar"
          style={{ height: `${height}%`, opacity: 0.3 + (height / 150), background: color }}
        />
      ))}
    </div>
  );
};

const FileIcon = ({ name, type = 'folder' }) => (
  <div className="file-item">
    <svg fill="currentColor" viewBox="0 0 20 20">
      {type === 'folder' ? (
        <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" />
      ) : (
        <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4zM18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clipRule="evenodd" />
      )}
    </svg>
    <div>{name}</div>
  </div>
);

const RiskIndicator = ({ name, risk = 'LOW' }) => (
  <div className="risk-item">
    <span>{name}</span>
    <span className={risk === 'CRITICAL' ? 'risk-critical' : risk === 'HIGH' ? 'text-orange-400' : 'text-teal-400'}>
      {risk}
    </span>
  </div>
);

export default function App() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());
  const [uptime, setUptime] = useState('0D 00:00:00');
  const [terminalLines, setTerminalLines] = useState([
    { text: "NEXURA NEURAL CORE v1.0.0 INITIALIZED", type: "info" },
    { text: "AI ENGINE: CONNECTING TO BACKEND SERVER...", type: "info" },
    { text: "[ OK ] AI BACKEND ONLINE: http://localhost:8000", type: "success" },
    { text: "Tizim tayyor. AI bilan muloqot qilish uchun matn kiriting...", type: "warning" },
    { text: "", type: "info" }
  ]);
  const [aiLogs, setAiLogs] = useState([
    "> AI: Analyzing API traffic for anomalies...",
    "> AI: Monitoring SWIFT zone connections...",
    "> AI: Scanning for SQL injection patterns..."
  ]);
  const [inputValue, setInputValue] = useState("");
  const [riskScore, setRiskScore] = useState(14);
  const [pressedKeys, setPressedKeys] = useState(new Set());

  const startTimeRef = useRef(Date.now());
  const scrollRef = useRef(null);
  const audioContextRef = useRef(null);

  // Keyboard Sound Engine (Web Audio API)
  const playClickSound = () => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    const ctx = audioContextRef.current;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine'; // Futuristik mayin ovoz
    osc.frequency.setValueAtTime(800, ctx.currentTime); // Yuqori chastotali "click"
    osc.frequency.exponentialRampToValueAtTime(100, ctx.currentTime + 0.05);

    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.05);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + 0.05);
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
      const diff = Date.now() - startTimeRef.current;
      const secs = Math.floor(diff / 1000) % 60;
      const mins = Math.floor(diff / 60000) % 60;
      const hrs = Math.floor(diff / 3600000);
      setUptime(`0D ${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`);
    }, 1000);

    const aiTimer = setInterval(() => {
      const logs = [
        "> AI: No DDoS patterns detected on Perimeter Layer.",
        "> AI: Checking Business Logic for IDOR vulnerabilities...",
        "> AI: Credential stuffing protection active.",
        "> AI: Encrypting PII data on Data Layer...",
        "> AI: Verifying call-center operator access tokens..."
      ];
      setAiLogs(prev => [logs[Math.floor(Math.random() * logs.length)], ...prev.slice(0, 5)]);
    }, 3000);

    const handleKeyDown = (e) => {
      let keyLabel = e.key.toUpperCase();
      if (keyLabel === 'ESCAPE') keyLabel = 'ESC';
      if (keyLabel === 'BACKSPACE') keyLabel = 'BACK';
      if (keyLabel === 'CAPSLOCK') keyLabel = 'CAPS';
      if (keyLabel === 'CONTROL') keyLabel = 'CTRL';
      if (keyLabel === ' ') keyLabel = 'SPACE';

      if (!pressedKeys.has(keyLabel)) {
        playClickSound(); // Ovoz chiqarish
      }
      setPressedKeys(prev => new Set(prev).add(keyLabel));
    };

    const handleKeyUp = (e) => {
      let keyLabel = e.key.toUpperCase();
      if (keyLabel === 'ESCAPE') keyLabel = 'ESC';
      if (keyLabel === 'BACKSPACE') keyLabel = 'BACK';
      if (keyLabel === 'CAPSLOCK') keyLabel = 'CAPS';
      if (keyLabel === 'CONTROL') keyLabel = 'CTRL';
      if (keyLabel === ' ') keyLabel = 'SPACE';

      setPressedKeys(prev => {
        const next = new Set(prev);
        next.delete(keyLabel);
        return next;
      });
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      clearInterval(timer);
      clearInterval(aiTimer);
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [pressedKeys]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [terminalLines]);

  const handleCommand = async (e) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      const userText = inputValue.trim();
      setTerminalLines(prev => [...prev, { text: `USER> ${userText}`, type: "user" }]);
      setInputValue("");

      try {
        const response = await securityApi.aiChat(userText);
        setTerminalLines(prev => [...prev, { text: `AI> ${response.response}`, type: "ai" }]);
        if (response.data?.risk) {
          setRiskScore(response.data.risk);
        }
      } catch (error) {
        setTerminalLines(prev => [...prev, { text: "AI> ERROR: Server bilan aloqa yo'q.", type: "error" }]);
      }
    }
  };

  const isPressed = (key) => pressedKeys.has(key) ? 'pressed' : '';

  return (
    <div className="app-container">
      <div className="scanline" />

      {/* Header */}
      <header className="panel">
        <div className="system-info">
          <div>
            <div className="opacity-50" style={{fontSize: '9px'}}>MANUFACTURER</div>
            <div className="font-bold">VICTUS HP</div>
          </div>
          <div className="ml-4">
            <div className="opacity-50" style={{fontSize: '9px'}}>THREAT ENGINE</div>
            <div className="font-bold text-teal-400">NEXURA AI</div>
          </div>
        </div>

        <div className="logo-center">
          NEXURA
          <div className="neural-pulse" />
        </div>

        <div className="system-info text-right flex items-center">
          <div>
            <div className="opacity-50" style={{fontSize: '9px'}}>UPTIME</div>
            <div className="font-bold">{uptime}</div>
          </div>
          <div className="clock-right">{time}</div>
        </div>
      </header>

      {/* Left Sidebar */}
      <aside className="panel flex flex-col gap-3">
        <div className="panel-header">AI NEURAL LOGIC <span className="ai-status-active">● ACTIVE</span></div>
        <div className="ai-logic-panel">
          {aiLogs.map((log, i) => <div key={i}>{log}</div>)}
        </div>

        <div className="panel-header mt-2">SECURITY LAYERS</div>
        <div className="layer-box">
          <div className="layer-title">PERIMETER (WAF/DDoS)</div>
          <div className="layer-status text-teal-400">SHIELDED</div>
          <Graph count={15} />
        </div>
        <div className="layer-box">
          <div className="layer-title">DATA LAYER (ENCRYPTION)</div>
          <div className="layer-status text-teal-400">PROTECTED</div>
          <Graph count={15} color="var(--cyan)" />
        </div>
        <div className="layer-box">
          <div className="layer-title">HUMAN FACTOR (MFA/PAM)</div>
          <div className="layer-status text-orange-400">MONITORING</div>
          <Graph count={15} color="#fbbf24" />
        </div>
      </aside>

      {/* Main Terminal */}
      <main>
        <div className="flex gap-1">
          <div className="px-3 py-1 border border-teal-500/30 border-b-0 bg-teal-500/20 text-[9px]">AI_CONVERSATION</div>
          <div className="px-3 py-1 border border-teal-500/30 border-b-0 opacity-40 text-[9px]">THREAT_MAP</div>
        </div>
        <div className="terminal-content" ref={scrollRef}>
          {terminalLines.map((line, i) => (
            <div
              key={i}
              className={`mb-1 ${
                line.type === 'success' ? 'text-teal-400' :
                line.type === 'warning' ? 'text-yellow-400' :
                line.type === 'user' ? 'text-blue-400 font-bold' :
                line.type === 'ai' ? 'text-teal-300 italic' :
                line.type === 'error' ? 'text-red-400' : 'text-white'
              }`}
            >
              {line.text}
            </div>
          ))}
          <div className="mt-2 flex items-center">
            <span className="text-teal-500 font-bold">USER&gt;</span>
            <input
              className="terminal-input"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleCommand}
              autoFocus
              spellCheck="false"
              autoComplete="off"
              placeholder="AI bilan gaplashing..."
            />
            <span className="cursor" />
          </div>
        </div>
      </main>

      {/* Right Sidebar */}
      <aside className="panel flex flex-col gap-3">
        <div className="panel-header">ENG XAVFLI 10 NUQTA</div>
        <div className="space-y-1">
          <RiskIndicator name="1. MOBIL BANKING API" risk="HIGH" />
          <RiskIndicator name="2. SMS OTP TIZIMI" risk="MEDIUM" />
          <RiskIndicator name="3. CALL-CENTER VERIF" risk="LOW" />
          <RiskIndicator name="4. INTERNAL ADMIN" risk="CRITICAL" />
          <RiskIndicator name="5. TEST SERVERLAR" risk="HIGH" />
          <RiskIndicator name="6. 3RD-PARTY INTEGR" risk="MEDIUM" />
          <RiskIndicator name="7. SWIFT GATEWAY" risk="LOW" />
          <RiskIndicator name="8. CARD PROCESSING" risk="LOW" />
          <RiskIndicator name="9. BACKUP SERVER" risk="LOW" />
          <RiskIndicator name="10. EMAIL SERVER" risk="MEDIUM" />
        </div>

        <div className="panel-header mt-2">AI THREAT ANALYSIS</div>
        <div className="h-24 bg-red-900/10 border border-red-500/20 p-2">
          <div className="text-[9px] text-red-400 font-bold mb-1">PROBABILITY OF ATTACK</div>
          <Graph count={20} color="var(--red)" />
          <div className="text-right text-[10px] text-red-400 mt-1">ESTIMATED RISK: {riskScore}%</div>
        </div>
        <div className="flex-1 mt-2">
           <div className="text-[9px] opacity-60">AI STRATEGY:</div>
           <div className="text-[10px] text-teal-400 mt-1">ZERO TRUST ARCHITECTURE ACTIVE. CONTINUOUS MONITORING ENABLED.</div>
        </div>
      </aside>

      {/* Bottom Filesystem */}
      <section className="panel filesystem-panel">
        <FileIcon name="AI_MODELS" />
        <FileIcon name="DATA_LOGS" />
        <FileIcon name="THREAT_DB" />
        <FileIcon name="SHIELDS" type="disk" />
        <FileIcon name="NET_MAP" />
        <FileIcon name="SYSTEM" />
      </section>

      {/* Bottom Keyboard */}
      <section className="panel keyboard-panel">
        <div className="key-row">
          {['ESC','1','2','3','4','5','6','7','8','9','0','BACK'].map(k => <div key={k} className={`key ${isPressed(k)}`}>{k}</div>)}
        </div>
        <div className="key-row">
          <div className={`key wide ${isPressed('TAB')}`}>TAB</div>
          {['Q','W','E','R','T','Y','U','I','O','P','[',']'].map(k => <div key={k} className={`key ${isPressed(k)}`}>{k}</div>)}
        </div>
        <div className="key-row">
          <div className={`key wide ${isPressed('CAPS')}`}>CAPS</div>
          {['A','S','D','F','G','H','J','K','L',';'].map(k => <div key={k} className={`key ${isPressed(k)}`}>{k}</div>)}
          <div className={`key wide ${isPressed('ENTER')}`}>ENTER</div>
        </div>
        <div className="key-row">
          <div className={`key wide ${isPressed('SHIFT')}`}>SHIFT</div>
          {['Z','X','C','V','B','N','M',',','.','/'].map(k => <div key={k} className={`key ${isPressed(k)}`}>{k}</div>)}
          <div className={`key wide ${isPressed('SHIFT')}`}>SHIFT</div>
        </div>
        <div className="key-row">
          <div className={`key ${isPressed('CTRL')}`}>CTRL</div>
          <div className="key">FN</div>
          <div className={`key ${isPressed('ALT')}`}>ALT</div>
          <div className={`key space ${isPressed('SPACE')}`}>SPACE</div>
          <div className={`key ${isPressed('ALT')}`}>ALT</div>
          <div className={`key ${isPressed('CTRL')}`}>CTRL</div>
        </div>
      </section>
    </div>
  );
}
