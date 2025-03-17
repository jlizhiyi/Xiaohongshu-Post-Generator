"use client";
import Image from "next/image";
import ReactMarkdown from "react-markdown";
import { useState } from "react";

type AIResponse = {
  type?: string;
  content?: string;
  reasoning?: string;
  error?: string;
};

<ReactMarkdown
  components={{
    h1: ({node, ...props}) => <h1 className="text-xl font-bold my-4" {...props} />,
    h2: ({node, ...props}) => <h2 className="text-lg font-bold my-3" {...props} />,
    h3: ({node, ...props}) => <h3 className="text-md font-bold my-2" {...props} />
  }}
></ReactMarkdown>

export default function Home() {
  const [formData, setFormData] = useState({
    api_key: "",
    topic: "",
    username: "",
    lang: "zh",
    geotag: "北京",
    further_context: "",
  });

  const [response, setResponse] = useState<AIResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [showReasoning, setShowReasoning] = useState(false);
  const [actualKey, setActualKey] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
  
    try {
      const res = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const reader = res.body?.getReader();
      if (!reader) throw new Error("Failed to get reader from response");  
  
      let accumulatedReasoning = "";
      let accumulatedResponse = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunkText = new TextDecoder("utf-8").decode(value);
        chunkText.split("\n\n").forEach((chunk) => {
          if (chunk.startsWith("data: ")) {
            try {
              const parsedChunk = JSON.parse(chunk.slice(6)); // Remove "data: "
              if (parsedChunk.type === "reasoning") {
                accumulatedReasoning += parsedChunk.reasoning;
              } else if (parsedChunk.type === "response") {
                accumulatedResponse += parsedChunk.content;
              }
  
              // ✅ Update state in real-time
              setResponse((prev) => ({
                ...prev,
                reasoning: accumulatedReasoning.trim(),
                content: accumulatedResponse.trim(),
              }));
            } catch (error) {
              console.error("Error parsing chunk:", error);
            }
          }
        });
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setResponse({ error: "Failed to get AI response." });
    } finally {
      setLoading(false);
    }
  };

  const LoadingSpinner = () => (
    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  );

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center w-full justify-center">
        <Image
          className="dark:invert"
          src="/xhs.svg"
          alt="REDnote logo"
          width={120}
          height={24}
          priority
        />

        <div className="text-4xl font-medium font-sans mb-6">
          Xiaohongshu Post Generator
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
            <label className="block mb-2">
              API key:
              <div className="relative">
                <input 
                  type="password"
                  name="api_key" 
                  value={actualKey}
                  onChange={(e) => {
                    const key = e.target.value;
                    setActualKey(key);
                    setFormData({...formData, api_key: key});
                  }}
                  className="w-full p-2 border rounded-md"
                  required 
                />
              </div>
            </label>
            </div>
            <div>
              <label className="block mb-2">
                Username:
                <input type="text" name="username" value={formData.username} onChange={handleChange}
                  className="w-full p-2 border rounded-md" />
              </label>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block mb-2">
                Language:
                <input type="text" name="lang" value={formData.lang} onChange={handleChange}
                  className="w-full p-2 border rounded-md" />
              </label>
            </div>
            <div>
              <label className="block mb-2">
                Geotag:
                <input type="text" name="geotag" value={formData.geotag} onChange={handleChange}
                  className="w-full p-2 border rounded-md" />
              </label>
            </div>
          </div>
          
          <label className="block mb-2">
            Topic:
            <textarea name="topic" value={formData.topic} onChange={handleChange}
              className="w-full p-2 border rounded-md" rows={4} />
          </label>

          <label className="block mb-2">
            Further Context:
            <textarea name="further_context" value={formData.further_context} onChange={handleChange}
              className="w-full p-2 border rounded-md" rows={4} />
          </label>

          <button
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
            type="submit"
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              {loading ? (<><LoadingSpinner /><span>Generating...</span></>) : ("Generate")}
            </span>
          </button>
        </form>

          {response && (
            <div className="flex items-center flex-col w-full justify-center">
              {response.reasoning && (
                <div className="mt-6 w-full max-w-lg bg-white p-6 rounded-lg shadow-lg">
                  <button 
                  onClick={() => setShowReasoning(!showReasoning)}
                  className="w-full flex justify-between items-center focus:outline-none"
                  >
                    <h2 className="text-xl font-bold">AI Reasoning:</h2>
                    <span className="text-sm text-gray-500">{showReasoning ? "Hide" : "Show"}</span>
                  </button>
                  <div className="bg-gray-100 p-4 rounded whitespace-pre-wrap max-h-80 overflow-y-auto text-gray-500 italic">
                    {showReasoning ? (
                      <ReactMarkdown>
                        {response.reasoning}
                      </ReactMarkdown>
                    ) : (
                      <span className="text-gray-500">Click to show reasoning</span>
                    )}
                  </div>
                </div>
              )}
              
              {response.content && (
                <div className="mt-6 w-full max-w-lg bg-white p-6 rounded-lg shadow-lg">
                  <h2 className="text-xl font-bold">AI Response:</h2>
                  <div className="bg-gray-100 p-4 rounded whitespace-pre-wrap">
                    <ReactMarkdown>
                      {response.content}
                    </ReactMarkdown>
                  </div>
                </div>
              )}

              {response.error && (
                <div className="mt-6 w-full max-w-lg bg-red-200 p-6 rounded-lg shadow-lg">
                  <h2 className="text-xl font-bold text-red-600">Error:</h2>
                  <div className="bg-red-100 p-4 rounded whitespace-pre-wrap text-red-700">
                    <ReactMarkdown>
                      {`Error: ${response.error}`}
                    </ReactMarkdown>
                  </div>
                </div>
              )}
            </div>
          )}
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="text-gray-400">© Joshua Li, 2025</div>
          <div className="text-gray-400">Powered by <a href="https://www.deepseek.com/">DeepSeek</a></div>
        </div>
      </footer>
    </div>
  );
}
