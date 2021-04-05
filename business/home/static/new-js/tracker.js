// const news = document.getElementById("news");

// ===============================================
// var div = document.createElement("div");
// div.style.background = "rgba(0,0,0,0.9)";
// div.style.overflow = "hidden";
// div.style.zIndex = "10";
// div.style.position = "fixed";
// div.style.top = "10px";
// div.style.left = "50%";
// div.style.transform = "translateX(-50%)";
// div.style.padding = "10px";
// div.style.marginTop = "10px";
// div.style.color = "white";
// div.style.borderRadius = "10px";

// document.body.appendChild(div);
// ===============================================

// $("#news").on("mouseenter", function() {
//   console.log("mouse enter");
// });
// $("#news").on("mouseleave", function() {
//   console.log("mouse leave");
// });

const news = document.getElementById("news");
// console.log(news);
news.style.background = "orange";

window.addEventListener("scroll", function() {
  console.log("scrolled >>> windowHeight = " + this.window.innerHeight);
  console.log("logic Check >>> " + newsArticleIsInViewport());
  if (newsArticleIsInViewport()) {
    console.log(" || NEWS IS IN VIEWPORT ||\n");
    // div.innerHTML = "NEWS IS IN VIEWPORT";
  } else {
    console.log(" || NEWS IS NOT IN VIEWPORT ||\n");
    // div.innerHTML = "NEWS IS NOT IN VIEWPORT";
  }
});

function newsArticleIsInViewport() {
  elemTop = news.getBoundingClientRect().top;
  elemBottom = news.getBoundingClientRect().bottom;
  console.log("elemTop = " + elemTop + " elemBottom = " + elemBottom);
  if (elemTop > window.innerHeight || elemBottom < 0) {
    return false;
  } else {
    return true;
  }
}

// =================== single news tag fix =============
const singleNewsContent = document.getElementById("single-news-content");

var convert = function(convert) {
  return $("<span />", { html: convert }).text();
};

singleNewsContent.innerHTML = convert(singleNewsContent.innerHTML);

// =================== remove feature tag from single news ===================
var figureArray = singleNewsContent.getElementsByClassName("wp-block-image");
console.log(figureArray);

$.each(figureArray, function(i, el) {
  console.log(el);
  el.style.display = "none";
});
