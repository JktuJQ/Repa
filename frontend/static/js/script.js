profile_container = document.querySelector(".profile-container");
profile_small = document.querySelector(".profile-container").querySelector(".profile");
profile_small.addEventListener("click", function() {
    profile_container.querySelector(".profile-retractable").classList.toggle("active");
    profile_small.classList.toggle("border");
});