export default function CtaSection() {
  return (
    <section className="py-20 lg:py-28 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-base-100 to-accent/10" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 relative z-10">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-3xl lg:text-5xl font-bold mb-6">
            Ready to Trade Smarter?
          </h2>
          <p className="text-lg text-base-content/70 mb-8 max-w-xl mx-auto">
            Join thousands of traders already using AI to make better investment
            decisions. Start your free trial today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
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
            <button className="btn btn-outline btn-lg">Contact Sales</button>
          </div>
          <p className="text-sm text-base-content/50 mt-6">
            No credit card required. 14-day free trial. Cancel anytime.
          </p>
        </div>
      </div>
    </section>
  );
}
