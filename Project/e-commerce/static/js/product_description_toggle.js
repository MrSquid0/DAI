document.addEventListener("DOMContentLoaded", function () {
    var descriptionButtons = document.querySelectorAll(".toggle-description-btn");

    descriptionButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var description = this.nextElementSibling; // Obtén el elemento siguiente (p.product-description)
        toggleDescription(description);
      });
    });

    function toggleDescription(description) {
      if (description.style.display === "none" || description.style.display === "") {
        description.style.display = "block";
      } else {
        description.style.display = "none";
      }
    }
});