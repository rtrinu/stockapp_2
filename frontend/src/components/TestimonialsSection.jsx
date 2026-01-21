const testimonials = [
  {
    content:
      "StockAI has completely transformed my trading strategy. The AI predictions are incredibly accurate, and I've seen a 40% improvement in my returns.",
    author: "Sarah Chen",
    role: "Day Trader",
    avatar: "SC",
    rating: 5,
  },
  {
    content:
      "The real-time analytics and risk management tools are game-changers. I feel much more confident making trades now.",
    author: "Michael Rodriguez",
    role: "Portfolio Manager",
    avatar: "MR",
    rating: 5,
  },
  {
    content:
      "Best investment I've made for my trading career. The pattern recognition feature has helped me spot opportunities I would have missed.",
    author: "Emily Thompson",
    role: "Swing Trader",
    avatar: "ET",
    rating: 5,
  },
];

export default function TestimonialsSection() {
  return (
    <section id="testimonials" className="py-20 lg:py-28">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <div className="badge badge-primary badge-outline mb-4">
            Testimonials
          </div>
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">
            Trusted by Traders Worldwide
          </h2>
          <p className="text-base-content/70 max-w-2xl mx-auto">
            See what our community has to say about their experience with
            StockAI.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="card bg-base-200 border border-base-300"
            >
              <div className="card-body">
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <svg
                      key={i}
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 text-primary"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <p className="text-base-content/80 mb-6 leading-relaxed">
                  "{testimonial.content}"
                </p>
                <div className="flex items-center gap-3 mt-auto">
                  <div className="avatar placeholder">
                    <div className="bg-primary text-primary-content rounded-full w-10">
                      <span className="text-sm">{testimonial.avatar}</span>
                    </div>
                  </div>
                  <div>
                    <p className="font-semibold text-sm">
                      {testimonial.author}
                    </p>
                    <p className="text-xs text-base-content/60">
                      {testimonial.role}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
