document.addEventListener("DOMContentLoaded", () => {
  // Mobile menu toggle
  const menuButton = document.querySelector(".menu-button");
  const nav = document.querySelector("header nav");
  if (menuButton && nav) {
    menuButton.addEventListener("click", () => {
      nav.classList.toggle("active");
    });
  }

  // Pricing toggle
  const pricingToggleButtons = document.querySelectorAll(".pricing-toggle button");
  const prices = document.querySelectorAll(".plan .price");
  if (pricingToggleButtons.length > 0 && prices.length > 0) {
    const monthlyPrices = ["$800", "$1700", "$4700"];
    const yearlyPrices = ["$560", "$1190", "$3290"];

    pricingToggleButtons.forEach((button) => {
      button.addEventListener("click", () => {
        pricingToggleButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");

        if (button.textContent.includes("Yearly")) {
          prices.forEach((price, index) => {
            price.innerHTML = `${yearlyPrices[index]}<span>/month</span>`;
          });
        } else {
          prices.forEach((price, index) => {
            price.innerHTML = `${monthlyPrices[index]}<span>/month</span>`;
          });
        }
      });
    });
  }

  // FAQ Accordion
  const faqItems = document.querySelectorAll(".faq-item h3");
  if (faqItems.length > 0) {
    faqItems.forEach((item) => {
      item.addEventListener("click", () => {
        const p = item.nextElementSibling;
        p.style.display = p.style.display === "block" ? "none" : "block";
      });
    });
  }

  // Team Slider
  const teamSlider = document.querySelector(".team-slider");
  if (teamSlider) {
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    const memberWidth = teamSlider.querySelector(".team-member").offsetWidth;

    nextBtn.addEventListener("click", () => {
      teamSlider.scrollBy({ left: memberWidth, behavior: "smooth" });
    });

    prevBtn.addEventListener("click", () => {
      teamSlider.scrollBy({ left: -memberWidth, behavior: "smooth" });
    });
  }

  // Scroll-to-top button
  const scrollToTopBtn = document.querySelector(".scroll-to-top-btn");
  if (scrollToTopBtn) {
    window.addEventListener("scroll", () => {
      if (
        document.body.scrollTop > 20 ||
        document.documentElement.scrollTop > 20
      ) {
        scrollToTopBtn.style.display = "block";
      } else {
        scrollToTopBtn.style.display = "none";
      }
    });

    scrollToTopBtn.addEventListener("click", () => {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    });
  }
});
