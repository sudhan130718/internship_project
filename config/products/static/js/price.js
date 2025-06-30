document.addEventListener("DOMContentLoaded", function() {
  const minSlider = document.getElementById("priceMinSlider");
  const maxSlider = document.getElementById("priceMaxSlider");
  const minOutput = document.getElementById("priceMinOutput");
  const maxOutput = document.getElementById("priceMaxOutput");
  const minGap = 0;

  minSlider.addEventListener("input", function() {
    let minVal = parseInt(minSlider.value);
    let maxVal = parseInt(maxSlider.value);

    if (minVal > maxVal - minGap) {
      minVal = maxVal - minGap;
      minSlider.value = minVal;
    }
    minOutput.value = minVal;
    minSlider.style.zIndex = 3;  // Bring minSlider on top while moving
    maxSlider.style.zIndex = 2;
  });

  maxSlider.addEventListener("input", function() {
    let minVal = parseInt(minSlider.value);
    let maxVal = parseInt(maxSlider.value);

    if (maxVal < minVal + minGap) {
      maxVal = minVal + minGap;
      maxSlider.value = maxVal;
    }
    maxOutput.value = maxVal;
    maxSlider.style.zIndex = 3;  // Bring maxSlider on top while moving
    minSlider.style.zIndex = 2;
  });

  minOutput.value = minSlider.value;
  maxOutput.value = maxSlider.value;
});