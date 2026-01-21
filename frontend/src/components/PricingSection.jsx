const plans = [
  {
    name: "Starter",
    price: 29,
    description: "Perfect for beginners exploring AI trading",
    features: [
      "10 stock predictions/day",
      "Basic market analysis",
      "Email alerts",
      "Community access",
      "24/7 email support",
    ],
    popular: false,
  },
  {
    name: "Professional",
    price: 99,
    description: "For serious traders who demand more",
    features: [
      "Unlimited predictions",
      "Advanced AI analytics",
      "Real-time alerts",
      "API access",
      "Portfolio optimization",
      "Priority support",
      "Custom watchlists",
    ],
    popular: true,
  },
  {
    name: "Enterprise",
    price: 299,
    description: "Custom solutions for institutions",
    features: [
      "Everything in Professional",
      "Dedicated account manager",
      "Custom AI models",
      "White-label options",
      "SLA guarantee",
      "On-premise deployment",
    ],
    popular: false,
  },
];

export default function PricingSection() {
  return (
    <section id="pricing" className="py-20 lg:py-28 bg-base-200/50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <div className="badge badge-primary badge-outline mb-4">Pricing</div>
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-base-content/70 max-w-2xl mx-auto">
            Choose the plan that fits your trading needs. All plans include a
            14-day free trial.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`card bg-base-100 border ${
                plan.popular
                  ? "border-primary shadow-lg shadow-primary/10"
                  : "border-base-300"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <div className="badge badge-primary">Most Popular</div>
                </div>
              )}
              <div className="card-body pt-8">
                <h3 className="text-xl font-bold">{plan.name}</h3>
                <p className="text-base-content/60 text-sm">
                  {plan.description}
                </p>
                <div className="my-4">
                  <span className="text-4xl font-bold">${plan.price}</span>
                  <span className="text-base-content/60">/month</span>
                </div>
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5 text-success flex-shrink-0"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                          clipRule="evenodd"
                        />
                      </svg>
                      {feature}
                    </li>
                  ))}
                </ul>
                <button
                  className={`btn w-full ${plan.popular ? "btn-primary" : "btn-outline"}`}
                >
                  Get Started
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
