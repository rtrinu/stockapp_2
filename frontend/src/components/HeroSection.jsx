"use client";

import { useState, useEffect } from "react";

const stockData = [
  {
    symbol: "AAPL",
    price: 189.42,
    change: 2.34,
    changePercent: 1.25,
    prediction: "BUY",
    confidence: 87,
  },
  {
    symbol: "GOOGL",
    price: 141.8,
    change: -1.23,
    changePercent: -0.86,
    prediction: "HOLD",
    confidence: 72,
  },
  {
    symbol: "MSFT",
    price: 378.91,
    change: 5.67,
    changePercent: 1.52,
    prediction: "BUY",
    confidence: 91,
  },
  {
    symbol: "TSLA",
    price: 248.5,
    change: 8.92,
    changePercent: 3.72,
    prediction: "BUY",
    confidence: 78,
  },
  {
    symbol: "NVDA",
    price: 495.22,
    change: -3.45,
    changePercent: -0.69,
    prediction: "HOLD",
    confidence: 65,
  },
  {
    symbol: "AMZN",
    price: 178.35,
    change: 2.11,
    changePercent: 1.2,
    prediction: "BUY",
    confidence: 84,
  },
];

export default function HeroSection() {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % stockData.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="min-h-screen pt-20 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-base-100 to-base-100" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/5 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 pt-16 lg:pt-24 relative z-10">
        <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-16">
          {/* Left content */}
          <div className="flex-1 text-center lg:text-left">
            <div className="badge badge-primary badge-outline mb-6">
              AI-Powered Trading Intelligence
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6 text-balance">
              Predict the Market with{" "}
              <span className="text-primary">AI Precision</span>
            </h1>
            <p className="text-lg text-base-content/70 mb-8 max-w-xl mx-auto lg:mx-0 text-pretty">
              Harness the power of advanced machine learning algorithms to make
              smarter trading decisions. Get real-time predictions, risk
              analysis, and market insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button className="btn btn-primary btn-lg">
                Start Free Trial
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
              <button className="btn btn-outline btn-lg">Watch Demo</button>
            </div>
            <div className="mt-8 flex items-center gap-6 justify-center lg:justify-start text-sm text-base-content/60">
              <div className="flex items-center gap-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 text-success"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                No credit card required
              </div>
              <div className="flex items-center gap-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 text-success"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                14-day free trial
              </div>
            </div>
          </div>

          {/* Right content - Live predictions card */}
          <div className="flex-1 w-full max-w-lg">
            <div className="card bg-base-200 shadow-2xl border border-base-300">
              <div className="card-body">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="card-title text-lg">Live AI Predictions</h3>
                  <div className="badge badge-success gap-1">
                    <span className="w-2 h-2 bg-success rounded-full animate-pulse" />
                    Live
                  </div>
                </div>

                <div className="overflow-hidden">
                  {stockData.map((stock, index) => (
                    <div
                      key={stock.symbol}
                      className={`transition-all duration-500 ${
                        index === currentIndex
                          ? "opacity-100 max-h-32"
                          : "opacity-0 max-h-0 overflow-hidden"
                      }`}
                    >
                      <div className="flex items-center justify-between p-4 bg-base-300 rounded-lg mb-3">
                        <div>
                          <p className="font-bold text-xl">{stock.symbol}</p>
                          <p className="text-2xl font-mono">
                            ${stock.price.toFixed(2)}
                          </p>
                        </div>
                        <div className="text-right">
                          <p
                            className={`font-semibold ${stock.change >= 0 ? "text-success" : "text-error"}`}
                          >
                            {stock.change >= 0 ? "+" : ""}
                            {stock.change.toFixed(2)} (
                            {stock.changePercent.toFixed(2)}%)
                          </p>
                          <div
                            className={`badge ${
                              stock.prediction === "BUY"
                                ? "badge-success"
                                : stock.prediction === "SELL"
                                  ? "badge-error"
                                  : "badge-warning"
                            } mt-1`}
                          >
                            {stock.prediction}
                          </div>
                        </div>
                      </div>
                      <div className="px-1">
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-base-content/70">
                            AI Confidence
                          </span>
                          <span className="font-semibold">
                            {stock.confidence}%
                          </span>
                        </div>
                        <progress
                          className="progress progress-primary w-full"
                          value={stock.confidence}
                          max="100"
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex gap-2 mt-4 justify-center">
                  {stockData.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentIndex(index)}
                      className={`w-2 h-2 rounded-full transition-all ${
                        index === currentIndex
                          ? "bg-primary w-6"
                          : "bg-base-300"
                      }`}
                      aria-label={`View stock ${index + 1}`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
