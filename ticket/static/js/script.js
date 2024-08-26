const settingDiv = document.getElementById("setting-div");
document.getElementById("setting-btn").addEventListener("click", () => {
  settingDiv.firstElementChild.classList.remove("closed");
  settingDiv.classList.remove("disappear");
});
document.getElementById("close-setting").addEventListener("click", () => {
  settingDiv.firstElementChild.classList.add("closed");
  setTimeout(() => settingDiv.classList.add("disappear"), 300);
})


document.getElementById("menu").firstElementChild.addEventListener("click", (e) => {
  document.querySelector(".sidenavbar").classList.remove("disappear-nav")
})

document.getElementById("close-nav").firstElementChild.addEventListener("click", (e) => {
  document.querySelector(".sidenavbar").classList.add("disappear-nav")
})
