// Multi-item carousel properties
$("#slick, #carousel-body").slick({
    infinite: true,
    speed: 300,
    arrows: true,
    slidesToShow: 8,
    slidesToScroll: 8,
    adaptiveHeight: true,
    responsive: [{
        breakpoint: 992,
        settings: {
            slidesToShow: 7,
            slidesToScroll: 7
        }
    }, {
        breakpoint: 768,
        settings: {
            slidesToShow: 7,
            slidesToScroll: 7
        }
    }, {
        breakpoint: 576,
        settings: {
            slidesToShow: 7,
            slidesToScroll: 7
        }
    }]
});


// The javascript code for the featured carousel was retrieved from:
// iamJoey, infinite carousel [Source code]. https://codepen.io/YousifW/pen/LKBxZX
// And has been modified and implemented in this web application

const slider = document.querySelector(".items");
const slides = document.querySelectorAll(".item");
const button = document.querySelectorAll(".button");

const dot = document.querySelectorAll(".dot");

let current = 0;
let prev = 4;
let next = 1;

for (let i = 0; i < button.length; i++) {
    button[i].addEventListener("click", () => i == 0 ? gotoPrev() : gotoNext());
}

for (let i = 0; i < dot.length; i++) {
    dot[i].addEventListener("click", () => i == 0 ? gotoPrev() : gotoNext());
}

const gotoPrev = () => current > 0 ? gotoNum(current - 1) : gotoNum(slides.length - 1);
const gotoNext = () => current < 4 ? gotoNum(current + 1) : gotoNum(0);

const gotoNum = number => {

    current = number;
    prev = current - 1;
    next = current + 1;

    for (let i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
        slides[i].classList.remove("prev");
        slides[i].classList.remove("next");
    }

    if (next == 5) {
        next = 0;
    }

    if (prev == -1) {
        prev = 4;
    }

    slides[current].classList.add("active");
    slides[prev].classList.add("prev");
    slides[next].classList.add("next");
}
