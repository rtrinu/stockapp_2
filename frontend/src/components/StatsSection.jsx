const stats = [
  {
    value: "94.7%",
    label: "Prediction Accuracy",
    description: "Verified over 10,000+ trades",
  },
  {
    value: "50K+",
    label: "Active Traders",
    description: "Growing community worldwide",
  },
  {
    value: "<100ms",
    label: "Analysis Speed",
    description: "Real-time market processing",
  },
  {
    value: "$2.4B",
    label: "Assets Analyzed",
    description: "Daily trading volume tracked",
  },
];

export default function StatsSection() {
  return (
    <section className="py-16 bg-base-200/50">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center p-6">
              <p className="text-3xl lg:text-4xl font-bold text-primary mb-2">
                {stat.value}
              </p>
              <p className="font-semibold text-base-content mb-1">
                {stat.label}
              </p>
              <p className="text-sm text-base-content/60">{stat.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
