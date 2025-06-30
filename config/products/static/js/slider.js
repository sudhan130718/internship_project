document.addEventListener('DOMContentLoaded', function () {
  const sliders = document.querySelectorAll('.slider-container');

  sliders.forEach(sliderContainer => {
    const sliderTrack = sliderContainer.querySelector('.slider-track');
    const nextBtn = sliderContainer.querySelector('.next');
    const prevBtn = sliderContainer.querySelector('.prev');
    const productCard = sliderTrack.querySelector('.product-card');

    let scrollPosition = 0;
    let slideWidth;
    let visibleCards;
    let maxClicks;
    let clickCount = 0;

    function updateSliderSettings() {
      // Calculate slide width (including margin)
      slideWidth = productCard.offsetWidth + 20;

      // Determine visible cards based on screen width
      const screenWidth = window.innerWidth;
      if (screenWidth >= 1024) {
        visibleCards = 3;
      } else if (screenWidth >= 768) {
        visibleCards = 2;
      } else {
        visibleCards = 1;
      }

      // Calculate maximum clicks possible
      maxClicks = sliderTrack.children.length - visibleCards;

      // Ensure clickCount is within bounds for the new screen size
      if (clickCount > maxClicks) {
        clickCount = maxClicks < 0 ? 0 : maxClicks;
      }

      // Update slider position
      scrollPosition = -slideWidth * clickCount;
      sliderTrack.style.transform = `translateX(${scrollPosition}px)`;
    }

    // Initial setup
    updateSliderSettings();

    // Update slider settings on window resize
    window.addEventListener('resize', updateSliderSettings);

    // Next button click
    nextBtn.addEventListener('click', () => {
      if (clickCount < maxClicks) {
        clickCount++;
        scrollPosition = -slideWidth * clickCount;
        sliderTrack.style.transform = `translateX(${scrollPosition}px)`;
      }
    });

    // Previous button click
    prevBtn.addEventListener('click', () => {
      if (clickCount > 0) {
        clickCount--;
        scrollPosition = -slideWidth * clickCount;
        sliderTrack.style.transform = `translateX(${scrollPosition}px)`;
      }
    });
  });
});
