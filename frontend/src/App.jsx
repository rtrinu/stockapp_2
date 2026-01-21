import Navbar from "./components/Navbar.jsx";
import HeroSection from "./components/HeroSection.jsx";
import StatsSection from "./components/StatsSection.jsx";
import FeaturesSection from "./components/FeaturesSection.jsx";
import PricingSection from "./components/PricingSection.jsx";
import TestimonialsSection from "./components/TestimonialsSection.jsx";
import CtaSection from "./components/CtaSection.jsx";
import Footer from "./components/Footer.jsx";

function App() {
  return (
    <div data-theme="dark" className="min-h-screen bg-base-100">
      <Navbar />
      <main>
        <HeroSection />
        <StatsSection />
        <FeaturesSection />
        <PricingSection />
        <TestimonialsSection />
        <CtaSection />
      </main>
      <Footer />
    </div>
  );
}

export default App;
